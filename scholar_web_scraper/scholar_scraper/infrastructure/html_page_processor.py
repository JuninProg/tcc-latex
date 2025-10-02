"""
HTMLPageProcessor - Processa páginas HTML de artigos para extrair conteúdo e metadados.

Este módulo é responsável por:
1. Acessar páginas de artigos científicos
2. Extrair conteúdo HTML sanitizado 
3. Detectar links de PDF específicos por site
4. Extrair metadados enriquecidos (resumo, autores completos, etc.)
"""

import re
import logging
import requests
from typing import Optional, List, Dict, Any, Tuple
from dataclasses import dataclass
from bs4 import BeautifulSoup, Tag
from urllib.parse import urljoin, urlparse

logger = logging.getLogger(__name__)


@dataclass
class PageContent:
    """
    Representa o conteúdo extraído de uma página HTML.
    """
    raw_html: str
    clean_text: str
    detected_pdf_links: List[str]
    title: Optional[str] = None
    abstract: Optional[str] = None
    authors: List[str] = None
    keywords: List[str] = None
    publication_info: Optional[str] = None
    
    def __post_init__(self):
        if self.authors is None:
            self.authors = []
        if self.keywords is None:
            self.keywords = []


class HTMLPageProcessor:
    """
    Processa páginas HTML de artigos científicos.
    """
    
    def __init__(self, timeout: int = 10, max_content_length: int = 50000):
        """
        Inicializa processador de páginas HTML.
        
        Args:
            timeout: Timeout para requisições HTTP
            max_content_length: Tamanho máximo do conteúdo a ser processado
        """
        self.timeout = timeout
        self.max_content_length = max_content_length
        
        # Headers para parecer um navegador real
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        # Patterns específicos por site
        self.site_patterns = {
            'scielo.br': {
                'pdf_patterns': [
                    r'href="([^"]*\?format=pdf[^"]*)"',
                    r'href="([^"]*\.pdf)"',
                    r'href="([^"]*format=pdf[^"]*)"'
                ],
                'abstract_selectors': ['div.abstract', 'div[id*="abstract"]', 'section[id*="abstract"]'],
                'content_selectors': ['div.article-content', 'main', 'article', 'div[id*="content"]']
            },
            'pubmed.ncbi.nlm.nih.gov': {
                'pdf_patterns': [
                    r'href="([^"]*\.pdf)"',
                    r'href="([^"]*pmc/articles/[^"]*\.pdf)"'
                ],
                'abstract_selectors': ['div#abstract', 'div.abstract-content'],
                'content_selectors': ['div.article-details', 'main', 'div[id*="content"]']
            },
            'default': {
                'pdf_patterns': [
                    r'href="([^"]*\.pdf)"',
                    r'href="([^"]*download[^"]*\.pdf)"',
                    r'href="([^"]*format=pdf[^"]*)"'
                ],
                'abstract_selectors': ['div.abstract', 'section.abstract', '[id*="abstract"]'],
                'content_selectors': ['main', 'article', 'div[id*="content"]', 'div.content']
            }
        }
    
    def extract_page_content(self, url: str) -> Optional[PageContent]:
        """
        Extrai conteúdo completo de uma página de artigo.
        
        Args:
            url: URL da página do artigo
            
        Returns:
            PageContent com dados extraídos ou None se erro
        """
        try:
            logger.info(f"Extraindo conteúdo da página: {url}")
            
            # Primeira tentativa sem SSL verificação (mais rápida)
            try:
                response = requests.get(url, headers=self.headers, timeout=self.timeout, verify=False)
                response.raise_for_status()
            except requests.exceptions.RequestException as ssl_error:
                logger.warning(f"Erro sem SSL: {ssl_error}")
                logger.info("Tentando novamente com SSL habilitado...")
                # Segunda tentativa com verificação SSL
                response = requests.get(url, headers=self.headers, timeout=self.timeout, verify=True)
                response.raise_for_status()
            
            # Verifica tamanho do conteúdo
            if len(response.content) > self.max_content_length:
                logger.warning(f"Conteúdo muito grande ({len(response.content)} bytes), truncando...")
                html_content = response.text[:self.max_content_length]
            else:
                html_content = response.text
            
            # Processa HTML
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Detecta tipo de site
            site_type = self._detect_site_type(url)
            patterns = self.site_patterns.get(site_type, self.site_patterns['default'])
            
            # Extrai dados específicos
            pdf_links = self._detect_pdf_links(soup, url, patterns['pdf_patterns'])
            clean_text = self._extract_clean_text(soup, patterns['content_selectors'])
            title = self._extract_title(soup)
            abstract = self._extract_abstract(soup, patterns['abstract_selectors'])
            authors = self._extract_authors(soup)
            keywords = self._extract_keywords(soup)
            pub_info = self._extract_publication_info(soup)
            
            return PageContent(
                raw_html=html_content,
                clean_text=clean_text,
                detected_pdf_links=pdf_links,
                title=title,
                abstract=abstract,
                authors=authors,
                keywords=keywords,
                publication_info=pub_info
            )
            
        except requests.RequestException as e:
            logger.error(f"Erro ao acessar página {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Erro ao processar conteúdo da página {url}: {e}")
            return None
    
    def _detect_site_type(self, url: str) -> str:
        """
        Detecta o tipo de site baseado na URL.
        
        Args:
            url: URL da página
            
        Returns:
            Tipo do site ou 'default'
        """
        domain = urlparse(url).netloc.lower()
        
        for site_pattern in self.site_patterns.keys():
            if site_pattern != 'default' and site_pattern in domain:
                return site_pattern
                
        return 'default'
    
    def _detect_pdf_links(self, soup: BeautifulSoup, base_url: str, patterns: List[str]) -> List[str]:
        """
        Detecta links de PDF na página usando patterns específicos.
        
        Args:
            soup: BeautifulSoup da página
            base_url: URL base para links relativos
            patterns: Lista de patterns regex para detectar PDFs
            
        Returns:
            Lista de URLs de PDF encontradas
        """
        pdf_links = []
        html_str = str(soup)
        
        for pattern in patterns:
            matches = re.findall(pattern, html_str, re.IGNORECASE)
            for match in matches:
                # Converte URL relativa para absoluta
                full_url = urljoin(base_url, match)
                if full_url not in pdf_links:
                    pdf_links.append(full_url)
        
        # Log dos links encontrados
        if pdf_links:
            logger.info(f"PDFs detectados: {pdf_links}")
        else:
            logger.warning(f"Nenhum PDF detectado na página: {base_url}")
            
        return pdf_links
    
    def _extract_clean_text(self, soup: BeautifulSoup, content_selectors: List[str]) -> str:
        """
        Extrai texto limpo da página, focando no conteúdo principal.
        
        Args:
            soup: BeautifulSoup da página
            content_selectors: Seletores CSS para encontrar conteúdo principal
            
        Returns:
            Texto limpo da página
        """
        # Remove elementos desnecessários
        for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'noscript']):
            element.decompose()
        
        # Tenta encontrar conteúdo principal
        main_content = None
        for selector in content_selectors:
            try:
                main_content = soup.select_one(selector)
                if main_content:
                    break
            except:
                continue
        
        # Se não encontrar, usa o body inteiro
        if not main_content:
            main_content = soup.find('body') or soup
        
        # Extrai texto limpo
        text = main_content.get_text(separator=' ', strip=True)
        
        # Limpa texto
        text = re.sub(r'\s+', ' ', text)  # Remove espaços múltiplos
        text = re.sub(r'\n+', '\n', text)  # Remove quebras múltiplas
        
        # Limita tamanho
        if len(text) > self.max_content_length:
            text = text[:self.max_content_length] + "..."
        
        return text.strip()
    
    def _extract_title(self, soup: BeautifulSoup) -> Optional[str]:
        """
        Extrai título da página.
        
        Args:
            soup: BeautifulSoup da página
            
        Returns:
            Título extraído ou None
        """
        # Tenta vários seletores
        selectors = [
            'h1.article-title',
            'h1[id*="title"]',
            'title',
            'h1',
            'h2.article-title'
        ]
        
        for selector in selectors:
            try:
                element = soup.select_one(selector)
                if element:
                    title = element.get_text(strip=True)
                    if title and len(title) > 10:  # Título deve ter pelo menos 10 chars
                        return title
            except:
                continue
                
        return None
    
    def _extract_abstract(self, soup: BeautifulSoup, abstract_selectors: List[str]) -> Optional[str]:
        """
        Extrai resumo/abstract da página.
        
        Args:
            soup: BeautifulSoup da página
            abstract_selectors: Seletores para encontrar resumo
            
        Returns:
            Resumo extraído ou None
        """
        for selector in abstract_selectors:
            try:
                element = soup.select_one(selector)
                if element:
                    abstract = element.get_text(strip=True)
                    if abstract and len(abstract) > 50:  # Abstract deve ter pelo menos 50 chars
                        return abstract
            except:
                continue
                
        return None
    
    def _extract_authors(self, soup: BeautifulSoup) -> List[str]:
        """
        Extrai lista de autores da página.
        
        Args:
            soup: BeautifulSoup da página
            
        Returns:
            Lista de autores
        """
        authors = []
        
        # Seletores comuns para autores
        selectors = [
            '.author', '.authors', '[class*="author"]',
            '.contributor', '[class*="contributor"]',
            '.byline', '[class*="byline"]'
        ]
        
        for selector in selectors:
            try:
                elements = soup.select(selector)
                for element in elements:
                    author_text = element.get_text(strip=True)
                    if author_text and len(author_text) < 100:  # Evita textos muito longos
                        authors.append(author_text)
                        
                if authors:  # Se encontrou autores, para de procurar
                    break
                    
            except:
                continue
        
        return authors[:10]  # Máximo 10 autores
    
    def _extract_keywords(self, soup: BeautifulSoup) -> List[str]:
        """
        Extrai palavras-chave da página.
        
        Args:
            soup: BeautifulSoup da página
            
        Returns:
            Lista de palavras-chave
        """
        keywords = []
        
        # Procura meta keywords
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        if meta_keywords and meta_keywords.get('content'):
            keywords.extend([k.strip() for k in meta_keywords['content'].split(',')])
        
        # Procura seção de keywords
        selectors = ['.keywords', '[class*="keyword"]', '[id*="keyword"]']
        for selector in selectors:
            try:
                element = soup.select_one(selector)
                if element:
                    text = element.get_text(strip=True)
                    if text:
                        keywords.extend([k.strip() for k in text.split(',') if k.strip()])
                        break
            except:
                continue
        
        return keywords[:10]  # Máximo 10 keywords
    
    def _extract_publication_info(self, soup: BeautifulSoup) -> Optional[str]:
        """
        Extrai informações de publicação (revista, volume, etc.).
        
        Args:
            soup: BeautifulSoup da página
            
        Returns:
            Informações de publicação ou None
        """
        selectors = [
            '.journal-info', '.publication-info', 
            '[class*="journal"]', '[class*="publication"]',
            '.citation', '[class*="citation"]'
        ]
        
        for selector in selectors:
            try:
                element = soup.select_one(selector)
                if element:
                    pub_info = element.get_text(strip=True)
                    if pub_info and len(pub_info) < 200:
                        return pub_info
            except:
                continue
                
        return None