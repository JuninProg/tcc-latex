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

import requests
import PyPDF2
import pdfplumber
from dataclasses import asdict

from scholar_scraper.domain.value_objects import PDFContent
from scholar_scraper.domain.entities import Article


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
                 timeout: int = 30,
                 max_pages: int = 50,
                 ssl_verify: bool = True):
        """
        Inicializa o processador.
        
        Args:
            timeout: Timeout para downloads em segundos
            max_pages: Número máximo de páginas a processar
            ssl_verify: Se deve verificar certificados SSL
        """
        self.timeout = timeout
        self.max_pages = max_pages
        self.ssl_verify = ssl_verify
        
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
        Gera lista de URLs candidatas para PDF.
        
        Args:
            article: Artigo fonte
            
        Returns:
            Lista de URLs para tentar
        """
        urls = []
        
        if not article.scholar_url:
            return urls
            
        # URL original
        urls.append(article.scholar_url)
        
        # Se for link do Google Scholar, tenta encontrar PDF direto
        if 'scholar.google.com' in article.scholar_url:
            # Não podemos acessar diretamente, mas vamos tentar
            pass
        else:
            # Para URLs diretas, adiciona variações comuns
            base_url = article.scholar_url.rstrip('/')
            
            # Variações com .pdf
            if not base_url.endswith('.pdf'):
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
            
            response = requests.get(
                url,
                headers=headers,
                timeout=self.timeout,
                stream=True,
                allow_redirects=True,
                verify=self.ssl_verify
            )
            
            response.raise_for_status()
            
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
                        text=full_text,
                        page_count=len(pdf.pages),
                        extraction_method="pdfplumber",
                        metadata={
                            'processed_pages': processed_pages,
                            'total_pages': len(pdf.pages),
                            'char_count': len(full_text)
                        }
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
                    text=full_text,
                    page_count=len(reader.pages),
                    extraction_method="pypdf2",
                    metadata={
                        'processed_pages': processed_pages,
                        'total_pages': len(reader.pages),
                        'char_count': len(full_text),
                        'encrypted': reader.is_encrypted
                    }
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