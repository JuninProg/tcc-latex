"""
Entidade ProcessingJob - Representa um job de processamento de busca no Scholar.

Esta entidade gerencia o estado e progresso de um job completo,
desde a busca inicial até a geração da planilha final.
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import uuid

from .search_query import SearchQuery
from .article import Article


class JobStatus(Enum):
    """Status possíveis de um job de processamento."""
    PENDING = "pending"
    SEARCHING = "searching"
    EXTRACTING = "extracting"
    ANALYZING = "analyzing"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class ProcessingJob:
    """
    Entidade que representa um job de processamento completo.
    
    Attributes:
        id: Identificador único do job
        search_query: Consulta de busca que originou o job
        status: Status atual do processamento
        articles: Lista de artigos sendo processados
        total_articles: Número total de artigos encontrados
        processed_articles: Número de artigos já processados
        result_file_path: Caminho do arquivo de resultado (quando pronto)
        created_at: Timestamp de criação do job
        started_at: Timestamp de início do processamento
        completed_at: Timestamp de conclusão
        error_message: Mensagem de erro detalhada (se houver)
        progress_details: Detalhes adicionais sobre o progresso
        celery_task_id: ID da task Celery (para tracking)
    """
    
    search_query: SearchQuery
    id: str = ""
    status: JobStatus = JobStatus.PENDING
    articles: List[Article] = None
    total_articles: int = 0
    processed_articles: int = 0
    result_file_path: Optional[str] = None
    created_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    progress_details: Dict[str, Any] = None
    celery_task_id: Optional[str] = None
    
    def __post_init__(self) -> None:
        """Inicializa valores padrão se não fornecidos."""
        if not self.id:
            self.id = str(uuid.uuid4())
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.articles is None:
            self.articles = []
        if self.progress_details is None:
            self.progress_details = {}
    
    def start_processing(self, celery_task_id: str) -> None:
        """
        Marca o início do processamento.
        
        Args:
            celery_task_id: ID da task Celery responsável pelo processamento
        """
        self.status = JobStatus.SEARCHING
        self.started_at = datetime.now()
        self.celery_task_id = celery_task_id
        self.error_message = None
    
    def update_status(self, new_status: JobStatus, details: Optional[str] = None) -> None:
        """
        Atualiza o status do job.
        
        Args:
            new_status: Novo status do job
            details: Detalhes adicionais sobre o status
        """
        self.status = new_status
        
        if details:
            self.progress_details["last_update"] = details
            self.progress_details["updated_at"] = datetime.now().isoformat()
    
    def complete_successfully(self, result_file_path: str) -> None:
        """
        Marca o job como concluído com sucesso.
        
        Args:
            result_file_path: Caminho do arquivo de resultado gerado
        """
        self.status = JobStatus.COMPLETED
        self.completed_at = datetime.now()
        self.result_file_path = result_file_path
        self.processed_articles = len(self.articles)
    
    def fail(self, error_message: str) -> None:
        """
        Marca o job como falhado.
        
        Args:
            error_message: Mensagem de erro detalhada
        """
        self.status = JobStatus.FAILED
        self.completed_at = datetime.now()
        self.error_message = error_message
    
    def cancel(self) -> None:
        """Cancela o job."""
        self.status = JobStatus.CANCELLED
        self.completed_at = datetime.now()
    
    def add_article(self, article: Article) -> None:
        """
        Adiciona um artigo à lista de processamento.
        
        Args:
            article: Artigo a ser adicionado
        """
        self.articles.append(article)
        self.total_articles = len(self.articles)
    
    def update_article_progress(self) -> None:
        """Atualiza contadores de progresso baseado nos artigos."""
        completed_articles = [
            article for article in self.articles 
            if article.is_completed() or article.has_failed()
        ]
        self.processed_articles = len(completed_articles)
    
    def get_progress_percentage(self) -> float:
        """
        Calcula porcentagem de progresso.
        
        Returns:
            Porcentagem de progresso (0.0 a 100.0)
        """
        if self.total_articles == 0:
            return 0.0
        
        return (self.processed_articles / self.total_articles) * 100.0
    
    def get_successful_articles(self) -> List[Article]:
        """Retorna apenas artigos processados com sucesso."""
        return [article for article in self.articles if article.is_completed()]
    
    def get_failed_articles(self) -> List[Article]:
        """Retorna apenas artigos que falharam no processamento."""
        return [article for article in self.articles if article.has_failed()]
    
    def is_in_progress(self) -> bool:
        """Verifica se o job está em andamento."""
        active_statuses = {
            JobStatus.PENDING, JobStatus.SEARCHING, 
            JobStatus.EXTRACTING, JobStatus.ANALYZING, JobStatus.GENERATING
        }
        return self.status in active_statuses
    
    def is_finished(self) -> bool:
        """Verifica se o job foi finalizado (sucesso, falha ou cancelamento)."""
        finished_statuses = {JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.CANCELLED}
        return self.status in finished_statuses
    
    def get_duration(self) -> Optional[float]:
        """
        Calcula duração do processamento em segundos.
        
        Returns:
            Duração em segundos ou None se não iniciado/finalizado
        """
        if not self.started_at:
            return None
        
        end_time = self.completed_at or datetime.now()
        return (end_time - self.started_at).total_seconds()
    
    def get_status_display(self) -> str:
        """Retorna status formatado para exibição."""
        status_map = {
            JobStatus.PENDING: "Aguardando",
            JobStatus.SEARCHING: "Buscando artigos",
            JobStatus.EXTRACTING: "Extraindo conteúdo",
            JobStatus.ANALYZING: "Analisando com IA",
            JobStatus.GENERATING: "Gerando planilha",
            JobStatus.COMPLETED: "Concluído",
            JobStatus.FAILED: "Falhou",
            JobStatus.CANCELLED: "Cancelado"
        }
        return status_map.get(self.status, self.status.value)
    
    def to_dict(self) -> dict:
        """
        Converte o job para dicionário para serialização.
        
        Returns:
            Dicionário com dados do job
        """
        return {
            "id": self.id,
            "search_query": self.search_query.to_dict(),
            "status": self.status.value,
            "status_display": self.get_status_display(),
            "total_articles": self.total_articles,
            "processed_articles": self.processed_articles,
            "progress_percentage": self.get_progress_percentage(),
            "result_file_path": self.result_file_path,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "duration_seconds": self.get_duration(),
            "error_message": self.error_message,
            "progress_details": self.progress_details,
            "celery_task_id": self.celery_task_id,
            "successful_articles": len(self.get_successful_articles()),
            "failed_articles": len(self.get_failed_articles())
        }