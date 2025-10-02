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
        Constrói prompt dinâmico para análise.
        
        Args:
            article: Artigo a analisar
            pdf_content: Conteúdo do PDF
            columns: Configurações de colunas
            filter_criteria: Critérios de filtro
            
        Returns:
            Prompt formatado para o Gemini
        """
        # Cabeçalho do sistema
        prompt = """Você é um assistente especializado em análise de artigos científicos. 
Sua tarefa é analisar o artigo fornecido e extrair informações específicas baseadas nos critérios definidos.

IMPORTANTE: Responda SEMPRE em formato JSON válido, seguindo exatamente a estrutura especificada.

"""
        
        # Informações do artigo
        title = getattr(article.metadata, 'title', article.id) if hasattr(article, 'metadata') else article.id
        summary = getattr(article.metadata, 'summary', None) if hasattr(article, 'metadata') else None
        authors = getattr(article.metadata, 'authors', []) if hasattr(article, 'metadata') else []
        
        prompt += f"""## ARTIGO PARA ANÁLISE

**Título:** {title}

**Resumo/Abstract:** {summary or "Não disponível"}

**Metadados:**
- Autores: {', '.join(authors) or "Não especificado"}
- Ano: {getattr(article.metadata, 'year', 'Não especificado') if hasattr(article, 'metadata') and article.metadata else 'Não especificado'}
- Venue: {getattr(article.metadata, 'venue', 'Não especificado') if hasattr(article, 'metadata') and article.metadata else 'Não especificado'}
- Citações: {getattr(article.metadata, 'citations', 0) if hasattr(article, 'metadata') and article.metadata else 0}

"""

        # Conteúdo do PDF se disponível
        if pdf_content and pdf_content.text:
            # Limita o texto para não exceder limites do modelo
            text_preview = pdf_content.text[:8000]
            if len(pdf_content.text) > 8000:
                text_preview += "\n\n[... texto truncado ...]"
                
            prompt += f"""**Conteúdo do PDF (primeiras páginas):**
{text_preview}

"""

        # Critérios de filtro
        prompt += f"""## CRITÉRIOS DE FILTRO

{filter_criteria}

"""

        # Configurações de colunas
        prompt += """## COLUNAS PARA EXTRAÇÃO

Analise o artigo e forneça os valores para as seguintes colunas:

"""

        for i, col in enumerate(columns, 1):
            prompt += f"""{i}. **{col.name}**
   - Tipo: {col.column_type}
   - Descrição: {col.description or "Extrair conforme nome da coluna"}

"""

        # Formato de resposta
        prompt += """## FORMATO DE RESPOSTA

Responda EXCLUSIVAMENTE em formato JSON válido com a seguinte estrutura:

```json
{
    "meets_criteria": true/false,
    "confidence_score": 0.85,
    "reasoning": "Explicação detalhada da análise e decisão",
    "column_values": {
"""

        # Adiciona exemplos de valores para cada coluna
        for i, col in enumerate(columns):
            comma = "," if i < len(columns) - 1 else ""
            
            if col.column_type == "boolean":
                example = "true/false"
            elif col.column_type == "number":
                example = "42"
            elif col.column_type == "date":
                example = "\"2023-12-15\""
            else:  # text
                example = "\"texto extraído ou analisado\""
                
            prompt += f"""        "{col.name}": {example}{comma}
"""

        prompt += """    }
}
```

## INSTRUÇÕES ESPECÍFICAS

1. **meets_criteria**: Determine se o artigo atende aos critérios de filtro (true/false)
2. **confidence_score**: Nível de confiança na análise (0.0 a 1.0)
3. **reasoning**: Explique sua análise, destacando pontos-chave que levaram à decisão
4. **column_values**: Para cada coluna:
   - **text**: Extraia ou analise o texto relevante
   - **number**: Extraia números específicos ou conte elementos
   - **boolean**: Determine true/false baseado na análise
   - **date**: Extraia datas no formato YYYY-MM-DD
   - Se não encontrar informação, use valores apropriados (ex: "Não especificado", 0, false, null)

Seja preciso, objetivo e baseie suas respostas no conteúdo real do artigo.
"""

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
            
            # Valida estrutura básica
            required_keys = ['meets_criteria', 'confidence_score', 'column_values', 'reasoning']
            for key in required_keys:
                if key not in data:
                    raise ValueError(f"Chave obrigatória '{key}' não encontrada")
                    
            # Valida tipos
            if not isinstance(data['meets_criteria'], bool):
                data['meets_criteria'] = str(data['meets_criteria']).lower() == 'true'
                
            if not isinstance(data['confidence_score'], (int, float)):
                try:
                    data['confidence_score'] = float(data['confidence_score'])
                except (ValueError, TypeError):
                    data['confidence_score'] = 0.5
                    
            # Garante que confidence_score está entre 0 e 1
            data['confidence_score'] = max(0.0, min(1.0, float(data['confidence_score'])))
            
            if not isinstance(data['column_values'], dict):
                data['column_values'] = {}
                
            if not isinstance(data['reasoning'], str):
                data['reasoning'] = str(data['reasoning'])
                
            return data
            
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao decodificar JSON: {e}")
            logger.debug(f"Resposta original: {response_text}")
            raise ValueError(f"Resposta não é JSON válido: {e}")
            
        except Exception as e:
            logger.error(f"Erro ao processar resposta: {e}")
            raise
            
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