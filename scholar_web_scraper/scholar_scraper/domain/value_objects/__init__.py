"""
Value Objects do Scholar Web Scraper.

Exporta todos os value objects do sistema.
"""

from .article_metadata import ArticleMetadata
from .pdf_content import PDFContent
from .analysis_result import AnalysisResult

__all__ = [
    'ArticleMetadata',
    'PDFContent',
    'AnalysisResult'
]