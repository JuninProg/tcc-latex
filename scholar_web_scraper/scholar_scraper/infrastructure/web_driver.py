"""
Driver para web scraping do Google Scholar.

Implementa busca automatizada de artigos científicos
com rate limiting e tratamento de erros robusto.
"""

import time
import logging
import re
from typing import List, Optional, Dict, Any
from urllib.parse import urlencode
from dataclasses import asdict

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    WebDriverException
)
from bs4 import BeautifulSoup

from scholar_scraper.domain.entities import Article, SearchQuery
from scholar_scraper.domain.value_objects import ArticleMetadata


logger = logging.getLogger(__name__)


class GoogleScholarDriver:
    """
    Driver para scraping do Google Scholar com Selenium e BeautifulSoup.
    
    Implementa busca robusta com rate limiting, retry logic
    e parsing inteligente de resultados.
    """
    
    BASE_URL = "https://scholar.google.com/scholar"
    RESULTS_PER_PAGE = 10
    
    def __init__(self, 
                 headless: bool = True,
                 timeout: int = 30,
                 rate_limit_delay: float = 2.0):
        """
        Inicializa o driver com configurações padrão.
        
        Args:
            headless: Executar browser em modo headless
            timeout: Timeout para operações em segundos
            rate_limit_delay: Delay entre requests em segundos
        """
        self.headless = headless
        self.timeout = timeout
        self.rate_limit_delay = rate_limit_delay
        self._driver: Optional[webdriver.Chrome] = None
        
    def __enter__(self):
        """Context manager entry."""
        self._setup_driver()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self._cleanup_driver()
        
    def _setup_driver(self) -> None:
        """Configura e inicializa o WebDriver Chrome."""
        try:
            options = Options()
            
            if self.headless:
                options.add_argument("--headless")
                
            # Configurações para evitar detecção
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # User agent realista
            options.add_argument(
                "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
            
            self._driver = webdriver.Chrome(options=options)
            self._driver.execute_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            )
            
            logger.info("WebDriver Chrome inicializado com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao inicializar WebDriver: {e}")
            raise
            
    def _cleanup_driver(self) -> None:
        """Limpa recursos do WebDriver."""
        if self._driver:
            try:
                self._driver.quit()
                logger.info("WebDriver finalizado")
            except Exception as e:
                logger.warning(f"Erro ao finalizar WebDriver: {e}")
            finally:
                self._driver = None
                
    def search_articles(self, query: SearchQuery) -> List[Article]:
        """
        Executa busca de artigos no Google Scholar.
        
        Args:
            query: Objeto com parâmetros de busca
            
        Returns:
            Lista de artigos encontrados
        """
        if not self._driver:
            raise RuntimeError("Driver não inicializado. Use context manager.")
            
        logger.info(f"Iniciando busca: '{query.query_text}'")
        logger.info(f"Máximo de resultados: {query.max_results}")
        if query.year_min or query.year_max:
            logger.info(f"Filtro de ano: {query.year_min or 'sem limite'} - {query.year_max or 'sem limite'}")
            
        try:
            articles = []
            pages_needed = (query.max_results + self.RESULTS_PER_PAGE - 1) // self.RESULTS_PER_PAGE
            
            for page in range(pages_needed):
                start_index = page * self.RESULTS_PER_PAGE
                
                logger.info(f"Buscando página {page + 1}/{pages_needed}")
                
                page_articles = self._search_page(
                    query.query_text, 
                    start_index,
                    year_min=query.year_min,
                    year_max=query.year_max
                )
                articles.extend(page_articles)
                
                # Respeitamos o limite máximo
                if len(articles) >= query.max_results:
                    articles = articles[:query.max_results]
                    break
                    
                # Rate limiting entre páginas
                if page < pages_needed - 1:
                    time.sleep(self.rate_limit_delay)
                    
            logger.info(f"Busca concluída: {len(articles)} artigos encontrados")
            return articles
            
        except Exception as e:
            logger.error(f"Erro na busca de artigos: {e}")
            raise
            
    def _search_page(self, search_text: str, start: int = 0, 
                     year_min: Optional[int] = None, year_max: Optional[int] = None) -> List[Article]:
        """
        Busca uma página específica de resultados.
        
        Args:
            search_text: Texto da busca
            start: Índice de início dos resultados
            year_min: Ano mínimo para filtro (opcional)
            year_max: Ano máximo para filtro (opcional)
            
        Returns:
            Lista de artigos da página
        """
        # Monta URL da busca
        params = {
            'q': search_text,
            'start': start,
            'hl': 'pt'
        }
        
        # Adiciona filtros de ano se especificados
        if year_min is not None:
            params['as_ylo'] = str(year_min)
        if year_max is not None:
            params['as_yhi'] = str(year_max)
            
        search_url = f"{self.BASE_URL}?{urlencode(params)}"
        
        logger.debug(f"Navegando para: {search_url}")
        
        try:
            # Navega para a página
            self._driver.get(search_url)
            
            # Aguarda carregamento dos resultados
            WebDriverWait(self._driver, self.timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-rp]"))
            )
            
            # Extrai HTML e processa com BeautifulSoup
            html = self._driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            return self._parse_search_results(soup)
            
        except TimeoutException:
            logger.warning("Timeout aguardando resultados da busca")
            return []
        except Exception as e:
            logger.error(f"Erro ao buscar página: {e}")
            return []
            
    def _parse_search_results(self, soup: BeautifulSoup) -> List[Article]:
        """
        Processa HTML da página e extrai dados dos artigos.
        
        Args:
            soup: Objeto BeautifulSoup com HTML da página
            
        Returns:
            Lista de artigos extraídos
        """
        articles = []
        
        # Encontra elementos de resultado
        result_elements = soup.find_all('div', {'data-rp': True})
        
        for element in result_elements:
            try:
                article = self._parse_article_element(element)
                if article:
                    articles.append(article)
            except Exception as e:
                logger.warning(f"Erro ao processar artigo: {e}")
                continue
                
        return articles
        
    def _parse_article_element(self, element) -> Optional[Article]:
        """
        Extrai dados de um elemento de artigo.
        
        Args:
            element: Elemento HTML do artigo
            
        Returns:
            Objeto Article ou None se inválido
        """
        try:
            # Título (obrigatório)
            title_elem = element.find('h3', class_='gs_rt')
            if not title_elem:
                return None
                
            # Limpa título removendo marcadores HTML
            title = title_elem.get_text().strip()
            # Remove prefixos como [HTML], [PDF], etc.
            title = re.sub(r'^\[.*?\]\s*', '', title)
            title = title.replace('\n', ' ').replace('\r', ' ')
            # Remove espaços duplos
            while '  ' in title:
                title = title.replace('  ', ' ')
            
            if not title:
                return None
            
            # Link (opcional mas importante)
            link_elem = title_elem.find('a')
            url = ""
            if link_elem and link_elem.get('href'):
                url = link_elem['href'].strip()
                # Valida se é uma URL válida
                if not (url.startswith('http://') or url.startswith('https://')):
                    url = ""
            
            # Autores e publicação
            authors_elem = element.find('div', class_='gs_a')
            authors_text = authors_elem.get_text().strip() if authors_elem else ""
            
            # Extrai autores e ano
            authors, year = self._parse_authors_and_year(authors_text)
            
            # Resumo/snippet
            snippet_elem = element.find('span', class_='gs_rs')
            summary = ""
            if snippet_elem:
                summary = snippet_elem.get_text().strip()
                summary = summary.replace('\n', ' ').replace('\r', ' ')
                # Remove espaços duplos
                while '  ' in summary:
                    summary = summary.replace('  ', ' ')
            
            # Citações
            citations_count = self._extract_citations(element)
            
            # Cria metadados
            metadata = ArticleMetadata(
                title=title,
                authors=authors if isinstance(authors, list) else [],
                year=year,
                citations_count=citations_count,
                snippet=summary
            )
            
            # Cria artigo
            article = Article(
                id=f"scholar_{hash(url + title)}",  # ID único baseado na URL + título
                metadata=metadata,
                scholar_url=url
            )
            
            # Log detalhado do artigo extraído
            logger.debug(f"Artigo extraído: '{title[:50]}...' | URL: {url[:50]}... | Autores: {len(authors)} | Ano: {year}")
            
            return article
            
        except Exception as e:
            logger.warning(f"Erro ao extrair dados do artigo: {e}")
            return None
            
    def _parse_authors_and_year(self, authors_text: str) -> tuple[List[str], Optional[int]]:
        """
        Extrai autores e ano de publicação do texto.
        
        Args:
            authors_text: Texto completo de autores/publicação
            
        Returns:
            Tupla (lista_autores, ano)
        """
        authors = []
        year = None
        
        if not authors_text:
            return authors, year
            
        # Remove caracteres problemáticos
        clean_text = authors_text.replace('\n', ' ').replace('\r', ' ').strip()
        
        # Pattern comum: "Autor1, Autor2 - Revista, 2023"
        parts = clean_text.split(' - ')
        
        if parts:
            # Primeira parte são os autores
            authors_part = parts[0].strip()
            if authors_part:
                # Remove elementos extras e divide por vírgula
                author_candidates = [
                    author.strip() 
                    for author in authors_part.split(',')
                    if author.strip() and not author.strip().startswith('…')
                ]
                
                # Filtra autores válidos (evita pegar partes do título da revista)
                for author in author_candidates[:5]:  # Máximo 5 autores
                    if len(author) > 2 and not author.isdigit():
                        # Remove caracteres especiais do final
                        clean_author = author.rstrip('.,;:-')
                        if clean_author:
                            authors.append(clean_author)
                
        # Procura ano (4 dígitos) - prioriza anos mais recentes
        import re
        year_matches = re.findall(r'\b(19|20)\d{2}\b', clean_text)
        if year_matches:
            # Pega o ano mais recente encontrado
            years = [int(y) for y in year_matches]
            year = max(years)
                
        return authors, year
                
        return authors, year
        
    def _extract_venue(self, authors_text: str) -> str:
        """
        Extrai venue/conferência do texto de autores.
        
        Args:
            authors_text: Texto completo de autores/publicação
            
        Returns:
            Nome da venue ou string vazia
        """
        if not authors_text or ' - ' not in authors_text:
            return ""
            
        parts = authors_text.split(' - ')
        if len(parts) > 1:
            venue_part = parts[1].strip()
            # Remove ano e outros elementos
            import re
            venue_clean = re.sub(r'\b(19|20)\d{2}\b', '', venue_part)
            venue_clean = re.sub(r'\s+', ' ', venue_clean).strip()
            return venue_clean
            
        return ""
        
    def _extract_citations(self, element) -> int:
        """
        Extrai número de citações do elemento.
        
        Args:
            element: Elemento HTML do artigo
            
        Returns:
            Número de citações
        """
        try:
            # Procura link "Citado por X"
            cite_links = element.find_all('a')
            for link in cite_links:
                link_text = link.get_text().strip().lower()
                if 'citado por' in link_text:
                    # Extrai número
                    import re
                    numbers = re.findall(r'\d+', link_text)
                    if numbers:
                        return int(numbers[0])
                        
        except Exception:
            pass
            
        return 0