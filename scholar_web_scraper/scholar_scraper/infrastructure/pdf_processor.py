"""
Processador de PDFs para extração de texto.

Implementa múltiplas estratégias de extração com fallbacks
para garantir máxima compatibilidade com diferentes tipos de PDF.
"""

import io
import logging
from typing import Optional, List, Dict, Any
import tempfile
import os
from urllib.parse import urlparse

import requests
import PyPDF2
import pdfplumber
from dataclasses import asdict

from scholar_scraper.domain.value_objects import PDFContent
from scholar_scraper.domain.value_objects.pdf_content import ExtractionMethod
from scholar_scraper.domain.entities import Article
from scholar_scraper.infrastructure.html_page_processor import HTMLPageProcessor


logger = logging.getLogger(__name__)

# Desabilita warning de SSL para desenvolvimento
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class PDFProcessor:
    """
    Processador de PDFs com múltiplas estratégias de extração.
    
    Implementa fallbacks automáticos para maximizar a taxa
    de sucesso na extração de texto.
    """
    
    def __init__(self, 
                 timeout: int = 10,  # Reduzido de 30 para 10
                 max_pages: int = 3,
                 max_content_length: int = 15000,
                 ssl_verify: bool = False):  # Mudado de True para False
        """
        Inicializa o processador.
        
        Args:
            timeout: Timeout para downloads em segundos
            max_pages: Número máximo de páginas a processar
            max_content_length: Tamanho máximo do conteúdo
            ssl_verify: Se deve verificar certificados SSL
        """
        self.timeout = timeout
        self.max_pages = max_pages
        self.max_content_length = max_content_length
        self.ssl_verify = ssl_verify
        
        # Inicializa HTMLPageProcessor para análise das páginas
        self.html_processor = HTMLPageProcessor(timeout=timeout)
        
        # IA para detecção de PDF como fallback (opcional - precisa de API key)
        self.gemini_client = None
        try:
            import os
            api_key = os.getenv('GOOGLE_API_KEY')
            if api_key:
                from scholar_scraper.infrastructure.gemini_client import GeminiClient
                self.gemini_client = GeminiClient(api_key=api_key)
                logger.debug("GeminiClient inicializado para detecção de PDF")
        except Exception as e:
            logger.debug(f"GeminiClient não disponível para detecção de PDF: {e}")
        
        # Obtém configuração SSL do ambiente
        import os
        env_ssl_verify = os.getenv('SCHOLAR_SSL_VERIFY', 'true').lower()
        if env_ssl_verify in ('false', '0', 'no', 'off'):
            self.ssl_verify = False
            logger.info("Verificação SSL desabilitada via variável de ambiente")
        
    def process_article_pdf(self, article: Article) -> Optional[PDFContent]:
        """
        Processa PDF de um artigo e extrai conteúdo de texto.
        
        Args:
            article: Artigo com URL do PDF
            
        Returns:
            Objeto PDFContent ou None se falhar
        """
        if not article.scholar_url:
            logger.warning(f"Artigo '{article.metadata.title or article.id}' sem URL")
            return None
            
        try:
            # Tenta diferentes estratégias de obtenção do PDF
            pdf_urls = self._get_pdf_urls(article)
            
            for pdf_url in pdf_urls:
                try:
                    content = self._download_and_extract(pdf_url)
                    if content and content.text.strip():
                        article_title = article.metadata.title if article.metadata else article.id
                        logger.info(f"PDF extraído com sucesso: {article_title}")
                        return content
                except Exception as e:
                    logger.warning(f"Falha na URL {pdf_url}: {e}")
                    continue
                    
            article_title = article.metadata.title if article.metadata else article.id
            logger.warning(f"Não foi possível extrair PDF para: {article_title}")
            return None
            
        except Exception as e:
            article_title = article.metadata.title if article.metadata else article.id
            logger.error(f"Erro ao processar PDF do artigo '{article_title}': {e}")
            return None
            
    def _get_pdf_urls(self, article: Article) -> List[str]:
        """
        Estratégia inteligente para encontrar URLs de PDF seguindo o fluxo correto:
        
        1. Extrai HTML da página do artigo
        2. Busca tags <a href="*.pdf"> 
        3. Se não encontrar → IA analisa HTML
        4. Se IA não encontrar → Heurísticas por base_url
        
        Args:
            article: Artigo fonte
            
        Returns:
            Lista priorizada de URLs para tentar
        """
        if not article.scholar_url:
            return []
            
        logger.info(f"Detectando PDF para: {article.scholar_url}")
        
        # ETAPA 1: Extrai HTML da página do artigo
        try:
            page_content = self.html_processor.extract_page_content(article.scholar_url)
            if not page_content:
                logger.warning(f"Não foi possível extrair HTML da página: {article.scholar_url}")
                return self._fallback_heuristic_urls(article.scholar_url)
                
        except Exception as e:
            logger.error(f"Erro ao extrair HTML: {e}")
            return self._fallback_heuristic_urls(article.scholar_url)
        
        # ETAPA 2: Busca URLs de PDF detectadas pelo HTMLPageProcessor
        detected_urls = page_content.detected_pdf_links
        if detected_urls:
            logger.info(f"PDFs detectados via HTML tags: {detected_urls}")
            return detected_urls
        
        # ETAPA 3: IA analisa HTML para encontrar PDF
        ai_detected_urls = self._detect_pdf_with_ai(page_content.raw_html, article.scholar_url)
        if ai_detected_urls:
            logger.info(f"PDFs detectados via IA: {ai_detected_urls}")
            return ai_detected_urls
        
        # ETAPA 4: Fallback para heurísticas por base_url
        logger.info("Nenhum PDF detectado via HTML, usando heurísticas...")
        return self._fallback_heuristic_urls(article.scholar_url)
    
    def _fallback_heuristic_urls(self, base_url: str) -> List[str]:
        """
        URLs de fallback baseadas em heurísticas quando HTML não funciona.
        
        Args:
            base_url: URL base do artigo
            
        Returns:
            Lista de URLs para tentar
        """
        urls = []
        base_url = base_url.rstrip('/')
        domain = urlparse(base_url).netloc.lower()
        
        # Estratégias específicas por site (simplificadas)
        if 'scielo.br' in domain:
            urls.extend([
                f"{base_url}/?format=pdf&lang=pt",
                f"{base_url}/?format=pdf&lang=en", 
                f"{base_url}/?format=pdf"
            ])
        elif 'arxiv.org' in domain and '/abs/' in base_url:
            pdf_url = base_url.replace('/abs/', '/pdf/') + '.pdf'
            urls.append(pdf_url)
        else:
            # Heurísticas genéricas
            urls.extend([
                f"{base_url}.pdf",
                f"{base_url}/download",
                f"{base_url}/pdf",
                f"{base_url}/fulltext.pdf"
            ])
        
        return urls
        
    def _download_and_extract(self, url: str) -> Optional[PDFContent]:
        """
        Baixa PDF e extrai texto usando múltiplas estratégias.
        
        Args:
            url: URL do PDF
            
        Returns:
            Conteúdo extraído ou None
        """
        try:
            # Download do PDF
            pdf_data = self._download_pdf(url)
            if not pdf_data:
                return None
                
            # Tenta múltiplas estratégias de extração
            strategies = [
                self._extract_with_pdfplumber,
                self._extract_with_pypdf2,
            ]
            
            for strategy in strategies:
                try:
                    content = strategy(pdf_data)
                    if content and content.text.strip():
                        logger.debug(f"Extração bem-sucedida com {strategy.__name__}")
                        return content
                except Exception as e:
                    logger.debug(f"Falha em {strategy.__name__}: {e}")
                    continue
                    
            return None
            
        except Exception as e:
            logger.error(f"Erro no download/extração de {url}: {e}")
            return None
            
    def _download_pdf(self, url: str) -> Optional[bytes]:
        """
        Baixa PDF da URL especificada.
        
        Args:
            url: URL do PDF
            
        Returns:
            Dados do PDF em bytes ou None
        """
        try:
            headers = {
                'User-Agent': (
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/120.0.0.0 Safari/537.36'
                ),
                'Accept': 'application/pdf,application/octet-stream,*/*',
                'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            }
            
            # Primeira tentativa SEM SSL verificação (mais rápido)
            try:
                response = requests.get(
                    url,
                    headers=headers,
                    timeout=self.timeout,
                    stream=True,
                    allow_redirects=True,
                    verify=False  # Começa sem SSL
                )
                response.raise_for_status()
            except requests.exceptions.RequestException as error:
                logger.debug(f"Erro sem verificação SSL: {error}")
                # Segunda tentativa COM verificação SSL se a primeira falhar
                try:
                    response = requests.get(
                        url,
                        headers=headers,
                        timeout=self.timeout,
                        stream=True,
                        allow_redirects=True,
                        verify=True
                    )
                    response.raise_for_status()
                except requests.exceptions.RequestException as ssl_error:
                    logger.warning(f"Falha ao baixar PDF de {url}: {ssl_error}")
                    return None
            
            # Verifica se é realmente um PDF
            content_type = response.headers.get('content-type', '').lower()
            if 'pdf' not in content_type:
                # Verifica pelos primeiros bytes
                first_bytes = response.content[:4]
                if not first_bytes.startswith(b'%PDF'):
                    logger.warning(f"URL não retornou PDF válido: {url}")
                    return None
                    
            logger.debug(f"PDF baixado: {len(response.content)} bytes")
            return response.content
            
        except requests.RequestException as e:
            logger.warning(f"Erro no download de {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Erro inesperado no download de {url}: {e}")
            return None
            
    def _extract_with_pdfplumber(self, pdf_data: bytes) -> Optional[PDFContent]:
        """
        Extrai texto usando pdfplumber (mais robusto).
        
        Args:
            pdf_data: Dados do PDF
            
        Returns:
            Conteúdo extraído
        """
        try:
            with io.BytesIO(pdf_data) as pdf_stream:
                with pdfplumber.open(pdf_stream) as pdf:
                    text_parts = []
                    processed_pages = 0
                    
                    for page in pdf.pages:
                        if processed_pages >= self.max_pages:
                            break
                            
                        page_text = page.extract_text()
                        if page_text:
                            text_parts.append(page_text)
                            
                        processed_pages += 1
                        
                    full_text = '\n\n'.join(text_parts)
                    
                    if not full_text.strip():
                        return None
                        
                    return PDFContent(
                        full_text=full_text,
                        page_count=len(pdf.pages),
                        extraction_method=ExtractionMethod.PDFPLUMBER,
                        extraction_confidence=0.9,
                        file_size_bytes=None,
                        has_images=False
                    )
                    
        except Exception as e:
            logger.debug(f"Erro com pdfplumber: {e}")
            return None
            
    def _extract_with_pypdf2(self, pdf_data: bytes) -> Optional[PDFContent]:
        """
        Extrai texto usando PyPDF2 (fallback).
        
        Args:
            pdf_data: Dados do PDF
            
        Returns:
            Conteúdo extraído
        """
        try:
            with io.BytesIO(pdf_data) as pdf_stream:
                reader = PyPDF2.PdfReader(pdf_stream)
                
                if reader.is_encrypted:
                    logger.warning("PDF criptografado, tentando sem senha")
                    try:
                        reader.decrypt("")
                    except Exception:
                        return None
                        
                text_parts = []
                processed_pages = 0
                
                for page_num, page in enumerate(reader.pages):
                    if processed_pages >= self.max_pages:
                        break
                        
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text_parts.append(page_text)
                    except Exception as e:
                        logger.debug(f"Erro na página {page_num}: {e}")
                        continue
                        
                    processed_pages += 1
                    
                full_text = '\n\n'.join(text_parts)
                
                if not full_text.strip():
                    return None
                    
                return PDFContent(
                    full_text=full_text,
                    page_count=len(reader.pages),
                    extraction_method=ExtractionMethod.PYPDF2,
                    extraction_confidence=0.8,
                    file_size_bytes=None,
                    has_images=False
                )
                
        except Exception as e:
            logger.debug(f"Erro com PyPDF2: {e}")
            return None
            
    def extract_from_file(self, file_path: str) -> Optional[PDFContent]:
        """
        Extrai texto de arquivo PDF local.
        
        Args:
            file_path: Caminho para o arquivo PDF
            
        Returns:
            Conteúdo extraído ou None
        """
        try:
            with open(file_path, 'rb') as file:
                pdf_data = file.read()
                
            return self._extract_with_pdfplumber(pdf_data) or \
                   self._extract_with_pypdf2(pdf_data)
                   
        except Exception as e:
            logger.error(f"Erro ao extrair arquivo {file_path}: {e}")
            return None
    
    def _detect_pdf_with_ai(self, html_content: str, base_url: str) -> List[str]:
        """
        Usa IA para detectar URLs de PDF no HTML quando busca por tags falha.
        
        Args:
            html_content: Conteúdo HTML da página
            base_url: URL base para resolver links relativos
            
        Returns:
            Lista de URLs de PDF detectadas pela IA
        """
        if not self.gemini_client:
            logger.debug("GeminiClient não disponível para detecção de PDF")
            return []
            
        try:
            # Limita o HTML para evitar exceder limites da API
            html_sample = html_content[:8000] if len(html_content) > 8000 else html_content
            
            prompt = f"""Analise o HTML fornecido e encontre APENAS URLs diretas para PDF do artigo.

URL da página: {base_url}

HTML da página:
{html_sample}

TAREFA: Encontre links para o PDF do artigo científico.

PROCURE POR:
- Links com extensão .pdf
- Links com "format=pdf", "download", "/pdf/"
- Botões/links com texto "PDF", "Download", "Baixar", "Full Text"
- Atributos href que levam a PDFs

REGRAS:
1. Retorne APENAS URLs completas (com http/https)
2. Se encontrar links relativos, combine com a URL base
3. Se não encontrar nenhum PDF, retorne "NAO_ENCONTRADO"
4. NÃO invente URLs
5. Máximo 3 URLs

FORMATO DE RESPOSTA:
- URL1
- URL2
- URL3

OU:

NAO_ENCONTRADO"""

            # Configura geração para respostas curtas
            import google.generativeai as genai
            response = self.gemini_client.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.1,
                    max_output_tokens=200,
                )
            )
            
            if not response or not response.text:
                return []
                
            response_text = response.text.strip()
            
            if "NAO_ENCONTRADO" in response_text.upper():
                logger.debug("IA não encontrou URLs de PDF")
                return []
            
            # Extrai URLs da resposta
            urls = []
            for line in response_text.split('\n'):
                line = line.strip()
                if line.startswith('-'):
                    line = line[1:].strip()
                if line.startswith('http'):
                    urls.append(line)
                elif line and not line.startswith('http'):
                    # Tenta resolver como URL relativa
                    from urllib.parse import urljoin
                    full_url = urljoin(base_url, line)
                    if full_url.startswith('http'):
                        urls.append(full_url)
                        
            return urls[:3]  # Máximo 3 URLs
            
        except Exception as e:
            logger.error(f"Erro na detecção de PDF via IA: {e}")
            return []