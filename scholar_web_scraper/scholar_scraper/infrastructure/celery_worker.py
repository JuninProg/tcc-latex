"""
Worker Celery para processamento assíncrono de artigos.

Implementa pipeline completo de busca, análise e geração
de relatórios em background com acompanhamento de progresso.
"""

import logging
from typing import List, Dict, Any, Optional
import os
from dataclasses import asdict

from celery import Celery
from celery.utils.log import get_task_logger

from scholar_scraper.domain.entities import Article, SearchQuery, ColumnConfig
from scholar_scraper.domain.value_objects import AnalysisResult, PDFContent
from scholar_scraper.infrastructure.web_driver import GoogleScholarDriver
from scholar_scraper.infrastructure.pdf_processor import PDFProcessor
from scholar_scraper.infrastructure.gemini_client import GeminiClient
from scholar_scraper.infrastructure.excel_generator import ExcelGenerator


# Configuração do Celery
celery_app = Celery('scholar_scraper')
celery_app.conf.update(
    broker_url=os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0'),
    result_backend=os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0'),
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='America/Sao_Paulo',
    enable_utc=True,
    task_track_started=True,
    task_routes={
        'scholar_scraper.infrastructure.celery_worker.process_articles': {'queue': 'main'},
    }
)

# Logger específico para tarefas
task_logger = get_task_logger(__name__)


@celery_app.task(bind=True, name='process_articles')
def process_articles(self,
                    search_query_dict: Dict[str, Any],
                    filter_criteria: str,
                    gemini_api_key: str) -> Dict[str, Any]:
    """
    Tarefa principal de processamento de artigos.
    
    Args:
        search_query_dict: Dicionário com dados da query (incluindo colunas)
        filter_criteria: Critérios de filtro
        gemini_api_key: Chave da API do Gemini
        
    Returns:
        Resultado do processamento com caminho do arquivo
    """
    try:
        # Reconstrói objetos ColumnConfig das colunas
        columns = [ColumnConfig(**col_dict) for col_dict in search_query_dict['columns']]
        
        # Reconstrói SearchQuery com objetos ColumnConfig reais
        search_query_data = search_query_dict.copy()
        search_query_data['columns'] = columns
        search_query = SearchQuery(**search_query_data)
        
        task_logger.info(f"Iniciando processamento: '{search_query.query_text}'")
        
        # Atualiza progresso inicial
        self.update_state(
            state='PROGRESS',
            meta={
                'current': 0,
                'total': 5,
                'status': 'Inicializando busca...',
                'stage': 'init'
            }
        )
        
        # Pipeline de processamento
        pipeline = ArticleProcessingPipeline(
            task=self,
            gemini_api_key=gemini_api_key
        )
        
        result = pipeline.execute(
            search_query=search_query,
            columns=columns,
            filter_criteria=filter_criteria
        )
        
        task_logger.info("Processamento concluído com sucesso")
        return result
        
    except Exception as e:
        task_logger.error(f"Erro no processamento: {e}")
        self.update_state(
            state='FAILURE',
            meta={
                'error': str(e),
                'status': f'Erro: {str(e)}',
                'stage': 'error'
            }
        )
        raise


class ArticleProcessingPipeline:
    """
    Pipeline de processamento completo de artigos.
    
    Implementa todas as etapas do processo:
    1. Busca no Google Scholar
    2. Extração de PDFs
    3. Análise com IA
    4. Geração de Excel
    """
    
    def __init__(self, task, gemini_api_key: str):
        """
        Inicializa pipeline.
        
        Args:
            task: Instância da tarefa Celery
            gemini_api_key: Chave da API do Gemini
        """
        self.task = task
        self.gemini_api_key = gemini_api_key
        
        # Inicializa componentes com configurações do ambiente
        import os
        pdf_timeout = int(os.getenv('SCHOLAR_PDF_TIMEOUT', '30'))
        max_pages = int(os.getenv('SCHOLAR_MAX_PDF_PAGES', '50'))
        
        self.pdf_processor = PDFProcessor(
            timeout=pdf_timeout,
            max_pages=max_pages
        )
        self.gemini_client = GeminiClient(api_key=gemini_api_key)
        self.excel_generator = ExcelGenerator()
        
    def execute(self,
               search_query: SearchQuery,
               columns: List[ColumnConfig],
               filter_criteria: str) -> Dict[str, Any]:
        """
        Executa pipeline completo.
        
        Args:
            search_query: Query de busca
            columns: Configurações de colunas
            filter_criteria: Critérios de filtro
            
        Returns:
            Resultado com caminho do arquivo gerado
        """
        try:
            # Etapa 1: Busca de artigos
            articles = self._search_articles(search_query)
            
            # Etapa 2: Processamento de PDFs
            pdf_contents = self._process_pdfs(articles)
            
            # Etapa 3: Análise com IA
            analysis_results = self._analyze_articles(
                articles, pdf_contents, columns, filter_criteria
            )
            
            # Etapa 4: Filtragem de resultados
            filtered_data = self._filter_results(articles, analysis_results)
            
            # Etapa 5: Geração de CSV (mais fácil para visualizar)
            excel_path = self._generate_excel(
                filtered_data['articles'],
                filtered_data['analysis_results'],
                columns,
                search_query.query_text,
                filter_criteria,
                format_type='csv'
            )
            
            # Resultado final
            return {
                'status': 'SUCCESS',
                'excel_path': excel_path,
                'total_articles': len(articles),
                'filtered_articles': len(filtered_data['articles']),
                'meets_criteria': filtered_data['meets_criteria_count'],
                'stage': 'completed'
            }
            
        except Exception as e:
            task_logger.error(f"Erro na execução do pipeline: {e}")
            raise
            
    def _search_articles(self, search_query: SearchQuery) -> List[Article]:
        """
        Executa busca de artigos no Google Scholar.
        
        Args:
            search_query: Query de busca
            
        Returns:
            Lista de artigos encontrados
        """
        self.task.update_state(
            state='PROGRESS',
            meta={
                'current': 1,
                'total': 5,
                'status': 'Buscando artigos no Google Scholar...',
                'stage': 'search'
            }
        )
        
        with GoogleScholarDriver(headless=True) as driver:
            articles = driver.search_articles(search_query)
            
        task_logger.info(f"Encontrados {len(articles)} artigos")
        return articles
        
    def _process_pdfs(self, articles: List[Article]) -> List[Optional[PDFContent]]:
        """
        Processa PDFs dos artigos.
        
        Args:
            articles: Lista de artigos
            
        Returns:
            Lista de conteúdos de PDF (pode conter None)
        """
        self.task.update_state(
            state='PROGRESS',
            meta={
                'current': 2,
                'total': 5,
                'status': 'Extraindo texto dos PDFs...',
                'stage': 'pdf_processing'
            }
        )
        
        pdf_contents = []
        processed = 0
        
        for article in articles:
            try:
                pdf_content = self.pdf_processor.process_article_pdf(article)
                pdf_contents.append(pdf_content)
                processed += 1
                
                # Atualiza progresso dentro da etapa
                if processed % 5 == 0 or processed == len(articles):
                    self.task.update_state(
                        state='PROGRESS',
                        meta={
                            'current': 2,
                            'total': 5,
                            'status': f'Processando PDFs... ({processed}/{len(articles)})',
                            'stage': 'pdf_processing',
                            'sub_progress': processed / len(articles) * 100
                        }
                    )
                    
            except Exception as e:
                article_title = article.metadata.title if article.metadata else article.id
                task_logger.warning(f"Erro ao processar PDF de '{article_title}': {e}")
                pdf_contents.append(None)
                processed += 1
                
        task_logger.info(f"PDFs processados: {processed}/{len(articles)}")
        return pdf_contents
        
    def _analyze_articles(self,
                         articles: List[Article],
                         pdf_contents: List[Optional[PDFContent]],
                         columns: List[ColumnConfig],
                         filter_criteria: str) -> List[AnalysisResult]:
        """
        Analisa artigos com IA.
        
        Args:
            articles: Lista de artigos
            pdf_contents: Conteúdos dos PDFs
            columns: Configurações de colunas
            filter_criteria: Critérios de filtro
            
        Returns:
            Lista de resultados de análise
        """
        self.task.update_state(
            state='PROGRESS',
            meta={
                'current': 3,
                'total': 5,
                'status': 'Analisando artigos com IA...',
                'stage': 'ai_analysis'
            }
        )
        
        analysis_results = []
        analyzed = 0
        
        for i, article in enumerate(articles):
            try:
                pdf_content = pdf_contents[i] if i < len(pdf_contents) else None
                
                result = self.gemini_client.analyze_article(
                    article=article,
                    pdf_content=pdf_content,
                    columns=columns,
                    filter_criteria=filter_criteria
                )
                
                analysis_results.append(result)
                analyzed += 1
                
                # Atualiza progresso
                if analyzed % 3 == 0 or analyzed == len(articles):
                    self.task.update_state(
                        state='PROGRESS',
                        meta={
                            'current': 3,
                            'total': 5,
                            'status': f'Analisando com IA... ({analyzed}/{len(articles)})',
                            'stage': 'ai_analysis',
                            'sub_progress': analyzed / len(articles) * 100
                        }
                    )
                    
            except Exception as e:
                title = getattr(article.metadata, 'title', article.id) if hasattr(article, 'metadata') else article.id
                task_logger.warning(f"Erro na análise de '{title}': {e}")
                # Cria resultado de fallback
                fallback_result = AnalysisResult(
                    column_data={col.name: "Erro na análise" for col in columns},
                    meets_filter=False,
                    confidence_score=0.0,
                    error_message=f"Erro durante análise: {str(e)}"
                )
                analysis_results.append(fallback_result)
                analyzed += 1
                
        task_logger.info(f"Artigos analisados: {analyzed}/{len(articles)}")
        return analysis_results
        
    def _filter_results(self,
                       articles: List[Article],
                       analysis_results: List[AnalysisResult]) -> Dict[str, Any]:
        """
        Filtra e organiza resultados.
        
        Args:
            articles: Lista de artigos
            analysis_results: Resultados das análises
            
        Returns:
            Dados filtrados e estatísticas
        """
        self.task.update_state(
            state='PROGRESS',
            meta={
                'current': 4,
                'total': 5,
                'status': 'Organizando resultados...',
                'stage': 'filtering'
            }
        )
        
        # Para esta implementação, incluímos todos os artigos
        # mas marcamos quais atendem aos critérios
        meets_criteria_count = sum(
            1 for result in analysis_results 
            if result.meets_filter
        )
        
        task_logger.info(f"Artigos que atendem critérios: {meets_criteria_count}/{len(articles)}")
        
        return {
            'articles': articles,
            'analysis_results': analysis_results,
            'meets_criteria_count': meets_criteria_count
        }
        
    def _generate_excel(self,
                       articles: List[Article],
                       analysis_results: List[AnalysisResult],
                       columns: List[ColumnConfig],
                       search_query: str,
                       filter_criteria: str,
                       format_type: str = 'xlsx') -> str:
        """
        Gera planilha Excel.
        
        Args:
            articles: Lista de artigos
            analysis_results: Resultados das análises
            columns: Configurações de colunas
            search_query: Query de busca
            filter_criteria: Critérios de filtro
            
        Returns:
            Caminho do arquivo Excel gerado
        """
        self.task.update_state(
            state='PROGRESS',
            meta={
                'current': 5,
                'total': 5,
                'status': 'Gerando planilha Excel...',
                'stage': 'excel_generation'
            }
        )
        
        excel_path = self.excel_generator.generate_excel(
            articles=articles,
            analysis_results=analysis_results,
            columns=columns,
            search_query=search_query,
            filter_criteria=filter_criteria,
            format_type=format_type
        )
        
        task_logger.info(f"Arquivo gerado: {excel_path}")
        return excel_path


# Worker startup
if __name__ == '__main__':
    celery_app.start()