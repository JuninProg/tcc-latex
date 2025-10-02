"""
Entidades de domínio do Scholar Web Scraper.

Exporta todas as entidades principais do sistema.
"""

from .article import Article
from .search_query import SearchQuery
from .column_config import ColumnConfig
from .processing_job import ProcessingJob

__all__ = [
    'Article',
    'SearchQuery', 
    'ColumnConfig',
    'ProcessingJob'
]