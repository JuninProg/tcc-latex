"""
Cliente para integração com Google Gemini AI.

Implementa análise inteligente de artigos científicos
com prompts dinâmicos baseados em configurações de usuário.
"""

import logging
from typing import Dict, Any, Optional, List
import json
import time
from dataclasses import asdict

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

from scholar_scraper.domain.entities import Article, ColumnConfig
from scholar_scraper.domain.value_objects import AnalysisResult, PDFContent


logger = logging.getLogger(__name__)


class GeminiClient:
    """
    Cliente para análise de artigos usando Google Gemini AI.
    
    Fornece análise inteligente com prompts dinâmicos
    baseados nas configurações de colunas do usuário.
    """
    
    def __init__(self, 
                 api_key: str,
                 model_name: str = "gemini-2.5-flash",
                 max_retries: int = 3,
                 retry_delay: float = 1.0):
        """
        Inicializa cliente Gemini.
        
        Args:
            api_key: Chave da API do Google
            model_name: Nome do modelo Gemini
            max_retries: Número máximo de tentativas
            retry_delay: Delay entre tentativas em segundos
        """
        self.api_key = api_key
        self.model_name = model_name
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
        # Configura cliente
        genai.configure(api_key=api_key)
        
        # Configurações de segurança permissivas para conteúdo acadêmico
        self.safety_settings = {
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }
        
        # Inicializa modelo
        self.model = genai.GenerativeModel(
            model_name=model_name,
            safety_settings=self.safety_settings
        )
        
        logger.info(f"Cliente Gemini inicializado com modelo {model_name}")
        
    def analyze_article(self, 
                       article: Article,
                       pdf_content: Optional[PDFContent],
                       columns: List[ColumnConfig],
                       filter_criteria: str) -> AnalysisResult:
        """
        Analisa artigo usando IA com configurações dinâmicas.
        
        Args:
            article: Artigo a ser analisado
            pdf_content: Conteúdo do PDF (opcional)
            columns: Configurações de colunas para análise
            filter_criteria: Critérios de filtro do usuário
            
        Returns:
            Resultado da análise com dados estruturados
        """
        try:
            # Gera prompt dinâmico
            prompt = self._build_analysis_prompt(
                article, pdf_content, columns, filter_criteria
            )
            
            # Executa análise com retry
            for attempt in range(self.max_retries):
                try:
                    response = self.model.generate_content(
                        prompt,
                        generation_config=genai.types.GenerationConfig(
                            temperature=0.1,  # Baixa para consistência
                            top_p=0.8,
                            top_k=40,
                            max_output_tokens=4000,
                        )
                    )
                    
                    # Processa resposta
                    analysis_data = self._parse_response(response.text)
                    
                    return AnalysisResult(
                        column_data=analysis_data.get('column_data', {}),
                        meets_filter=analysis_data.get('meets_filter', False),
                        confidence_score=analysis_data.get('confidence_score', 0.0),
                        justification=analysis_data.get('justification', ''),
                        analysis_model=self.model_name
                    )
                    
                except Exception as e:
                    logger.warning(f"Tentativa {attempt + 1} falhou: {e}")
                    if attempt < self.max_retries - 1:
                        time.sleep(self.retry_delay * (attempt + 1))
                    else:
                        raise
                        
        except Exception as e:
            title = getattr(article.metadata, 'title', article.id) if hasattr(article, 'metadata') else article.id
            logger.error(f"Erro na análise do artigo '{title}': {e}")
            
            # Retorna resultado de fallback
            return AnalysisResult(
                column_data={col.name: "Erro na análise" for col in columns},
                meets_filter=False,
                confidence_score=0.0,
                error_message=f"Erro durante análise: {str(e)}"
            )
            
    def _build_analysis_prompt(self, 
                             article: Article,
                             pdf_content: Optional[PDFContent],
                             columns: List[ColumnConfig],
                             filter_criteria: str) -> str:
        """
        Constrói prompt dinâmico para análise estruturada.
        
        Args:
            article: Artigo a analisar
            pdf_content: Conteúdo do PDF
            columns: Configurações de colunas
            filter_criteria: Critérios de filtro
            
        Returns:
            Prompt formatado para o Gemini
        """
        # Obter dados do artigo
        title = getattr(article.metadata, 'title', article.id) if hasattr(article, 'metadata') else article.id
        summary = getattr(article.metadata, 'snippet', '') if hasattr(article, 'metadata') else ''
        authors = getattr(article.metadata, 'authors', []) if hasattr(article, 'metadata') else []
        year = getattr(article.metadata, 'year', None) if hasattr(article, 'metadata') else None
        
        # Conteúdo disponível para análise
        content_for_analysis = ""
        if pdf_content and pdf_content.text:
            # Usa o PDF completo se disponível
            content_for_analysis = pdf_content.text[:15000]  # Limita para evitar exceder tokens
            if len(pdf_content.text) > 15000:
                content_for_analysis += "\n\n[... conteúdo adicional truncado ...]"
        elif summary:
            # Fallback para o resumo do Google Scholar
            content_for_analysis = summary
        else:
            content_for_analysis = "Apenas título disponível para análise"
        
        prompt = f"""Você é um especialista em análise de artigos científicos na área de tecnologia e aplicativos móveis. 

Analise o artigo científico fornecido e extraia as informações solicitadas. Retorne APENAS um JSON válido com a estrutura especificada.

## ARTIGO PARA ANÁLISE

**Título:** {title}

**Autores:** {', '.join(authors) if authors else 'Não especificado'}

**Ano:** {year if year else 'Não especificado'}

**Conteúdo para análise:**
{content_for_analysis}

## CRITÉRIOS DE FILTRO

{filter_criteria}

## INSTRUÇÕES

Analise o conteúdo e responda APENAS com um JSON no formato exato abaixo:

```json
{{
    "descricao": "Breve descrição em 1-2 frases do que o artigo apresenta",
    "tecnologias_usadas": "Principais tecnologias, linguagens ou frameworks mencionados",
    "tem_aplicativo_movel": true/false,
    "tem_painel_gestao": true/false,
    "atende_filtro": true/false,
    "confianca": 0.85,
    "justificativa": "Explicação breve de por que atende ou não aos critérios"
}}
```

## REGRAS ESPECÍFICAS:

1. **descricao**: Máximo 200 caracteres, focando no objetivo/contribuição principal
2. **tecnologias_usadas**: Liste as principais tecnologias mencionadas (ex: "React Native, Node.js, PostgreSQL")
3. **tem_aplicativo_movel**: true se menciona desenvolvimento de app móvel, false caso contrário
4. **tem_painel_gestao**: true se menciona sistema web para gestão/administração, false caso contrário
5. **atende_filtro**: true se o artigo atende aos critérios especificados
6. **confianca**: Número entre 0.0 e 1.0 indicando sua confiança na análise
7. **justificativa**: Máximo 100 caracteres explicando a decisão sobre atender o filtro

Retorne APENAS o JSON, sem texto adicional."""

        return prompt
        
    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        """
        Processa resposta do Gemini e extrai dados estruturados.
        
        Args:
            response_text: Texto da resposta
            
        Returns:
            Dicionário com dados estruturados
        """
        try:
            # Remove markdown code blocks se presentes
            clean_text = response_text.strip()
            if clean_text.startswith('```json'):
                clean_text = clean_text[7:]
            if clean_text.startswith('```'):
                clean_text = clean_text[3:]
            if clean_text.endswith('```'):
                clean_text = clean_text[:-3]
                
            clean_text = clean_text.strip()
            
            # Tenta parsear JSON
            data = json.loads(clean_text)
            
            # Converte para o formato esperado pelo AnalysisResult
            result = {
                'meets_filter': bool(data.get('atende_filtro', False)),
                'confidence_score': float(data.get('confianca', 0.5)),
                'justification': str(data.get('justificativa', '')),
                'column_data': {
                    'Descrição': str(data.get('descricao', '')),
                    'Tecnologias Usadas': str(data.get('tecnologias_usadas', '')),
                    'Tem Aplicativo Móvel?': bool(data.get('tem_aplicativo_movel', False)),
                    'Tem Painel de Gestão?': bool(data.get('tem_painel_gestao', False))
                }
            }
            
            # Valida e ajusta valores
            result['confidence_score'] = max(0.0, min(1.0, result['confidence_score']))
            
            logger.debug(f"Dados extraídos: {result}")
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao decodificar JSON: {e}")
            logger.debug(f"Resposta original: {response_text}")
            
            # Retorna valores padrão em caso de erro
            return {
                'meets_filter': False,
                'confidence_score': 0.0,
                'justification': f'Erro ao processar resposta da IA: {e}',
                'column_data': {
                    'Descrição': 'Erro na análise',
                    'Tecnologias Usadas': 'Erro na análise',
                    'Tem Aplicativo Móvel?': False,
                    'Tem Painel de Gestão?': False
                }
            }
            
        except Exception as e:
            logger.error(f"Erro ao processar resposta: {e}")
            
            # Retorna valores padrão em caso de erro
            return {
                'meets_filter': False,
                'confidence_score': 0.0,
                'justification': f'Erro inesperado: {e}',
                'column_data': {
                    'Descrição': 'Erro na análise',
                    'Tecnologias Usadas': 'Erro na análise',
                    'Tem Aplicativo Móvel?': False,
                    'Tem Painel de Gestão?': False
                }
            }
            
    def test_connection(self) -> bool:
        """
        Testa conexão com a API do Gemini.
        
        Returns:
            True se conectado com sucesso
        """
        try:
            test_response = self.model.generate_content(
                "Responda apenas 'OK' para testar a conexão.",
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=10
                )
            )
            
            return "OK" in test_response.text.upper()
            
        except Exception as e:
            logger.error(f"Erro no teste de conexão: {e}")
            return False