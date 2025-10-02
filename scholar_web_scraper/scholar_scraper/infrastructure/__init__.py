"""
Módulo de infraestrutura do Scholar Web Scraper.

Contém implementações para web scraping, processamento de PDF,
integração com IA, geração de Excel e processamento assíncrono.
"""

from .web_driver import GoogleScholarDriver
from .pdf_processor import PDFProcessor
from .gemini_client import GeminiClient
from .excel_generator import ExcelGenerator
from .celery_worker import celery_app, process_articles

__all__ = [
    'GoogleScholarDriver',
    'PDFProcessor', 
    'GeminiClient',
    'ExcelGenerator',
    'celery_app',
    'process_articles'
]