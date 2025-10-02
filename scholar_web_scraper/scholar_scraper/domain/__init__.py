"""
Domínio do Scholar Web Scraper.

Contém toda a lógica de negócio, entidades e value objects.
"""

from .entities import Article, SearchQuery, ColumnConfig, ProcessingJob
from .value_objects import ArticleMetadata, PDFContent, AnalysisResult

__all__ = [
    # Entidades
    'Article',
    'SearchQuery',
    'ColumnConfig', 
    'ProcessingJob',
    # Value Objects
    'ArticleMetadata',
    'PDFContent',
    'AnalysisResult'
]