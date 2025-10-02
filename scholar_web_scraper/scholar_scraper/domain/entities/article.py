"""
Entidade Article - Representa um artigo científico do Google Scholar.

Esta entidade encapsula todas as informações de um artigo científico,
incluindo metadados básicos, conteúdo extraído e resultados de análise.
"""

from typing import Optional, List
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

from ..value_objects.article_metadata import ArticleMetadata
from ..value_objects.pdf_content import PDFContent
from ..value_objects.analysis_result import AnalysisResult


class ArticleStatus(Enum):
    """Status do processamento do artigo."""
    PENDING = "pending"
    EXTRACTING_METADATA = "extracting_metadata"
    DOWNLOADING_PDF = "downloading_pdf"
    EXTRACTING_TEXT = "extracting_text"
    ANALYZING = "analyzing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Article:
    """
    Entidade principal que representa um artigo científico.
    
    Attributes:
        id: Identificador único do artigo
        metadata: Metadados básicos do artigo
        pdf_content: Conteúdo extraído do PDF (opcional)
        analysis_result: Resultado da análise via IA (opcional)
        status: Status atual do processamento
        scholar_url: URL original no Google Scholar
        created_at: Timestamp de criação
        updated_at: Timestamp da última atualização
        error_message: Mensagem de erro (se houver falha)
    """
    
    id: str
    metadata: ArticleMetadata
    scholar_url: str
    status: ArticleStatus = ArticleStatus.PENDING
    pdf_content: Optional[PDFContent] = None
    analysis_result: Optional[AnalysisResult] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    error_message: Optional[str] = None
    
    def __post_init__(self) -> None:
        """Inicializa timestamps se não fornecidos."""
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
    
    def update_status(self, new_status: ArticleStatus, error_message: Optional[str] = None) -> None:
        """
        Atualiza o status do artigo.
        
        Args:
            new_status: Novo status do processamento
            error_message: Mensagem de erro (opcional)
        """
        self.status = new_status
        self.updated_at = datetime.now()
        if error_message:
            self.error_message = error_message
    
    def set_pdf_content(self, pdf_content: PDFContent) -> None:
        """
        Define o conteúdo extraído do PDF.
        
        Args:
            pdf_content: Conteúdo do PDF extraído
        """
        self.pdf_content = pdf_content
        self.updated_at = datetime.now()
    
    def set_analysis_result(self, analysis_result: AnalysisResult) -> None:
        """
        Define o resultado da análise via IA.
        
        Args:
            analysis_result: Resultado da análise
        """
        self.analysis_result = analysis_result
        self.updated_at = datetime.now()
    
    def is_completed(self) -> bool:
        """Verifica se o processamento foi concluído com sucesso."""
        return self.status == ArticleStatus.COMPLETED
    
    def has_failed(self) -> bool:
        """Verifica se o processamento falhou."""
        return self.status == ArticleStatus.FAILED
    
    def get_content_for_analysis(self) -> str:
        """
        Retorna o melhor conteúdo disponível para análise.
        
        Prioridade: PDF completo > Abstract > Snippet
        
        Returns:
            Texto para ser analisado pela IA
        """
        if self.pdf_content and self.pdf_content.full_text:
            return self.pdf_content.full_text
        
        if self.metadata.abstract:
            return self.metadata.abstract
        
        return self.metadata.snippet or ""
    
    def get_display_title(self) -> str:
        """Retorna título formatado para exibição."""
        return self.metadata.title or "Título não disponível"
    
    def get_authors_display(self) -> str:
        """Retorna autores formatados para exibição."""
        if not self.metadata.authors:
            return "Autores não disponíveis"
        return ", ".join(self.metadata.authors)
    
    def to_dict(self) -> dict:
        """
        Converte o artigo para dicionário para serialização.
        
        Returns:
            Dicionário com dados do artigo
        """
        return {
            "id": self.id,
            "title": self.metadata.title,
            "authors": self.metadata.authors,
            "year": self.metadata.year,
            "abstract": self.metadata.abstract,
            "snippet": self.metadata.snippet,
            "pdf_url": self.metadata.pdf_url,
            "scholar_url": self.scholar_url,
            "status": self.status.value,
            "has_pdf_content": bool(self.pdf_content),
            "has_analysis": bool(self.analysis_result),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "error_message": self.error_message
        }