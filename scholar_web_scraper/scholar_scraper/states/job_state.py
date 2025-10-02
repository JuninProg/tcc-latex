"""
JobState - Estado de gerenciamento de jobs de processamento.

Este estado gerencia o ciclo de vida dos jobs de processamento,
incluindo criação, monitoramento de progresso e recuperação de resultados.
"""

import reflex as rx
import asyncio
from typing import Optional, Dict, Any
from datetime import datetime

from ..domain.entities.processing_job import ProcessingJob, JobStatus
from ..domain.entities.search_query import SearchQuery


class JobState(rx.State):
    """Estado de gerenciamento de jobs."""
    
    # Job atual
    current_job: Optional[Dict[str, Any]] = None
    job_id: str = ""
    
    # Estados de processamento
    is_processing: bool = False
    processing_status: str = "idle"
    progress_percentage: float = 0.0
    
    # Progresso detalhado
    total_articles: int = 0
    processed_articles: int = 0
    current_step: str = ""
    estimated_time_remaining: Optional[int] = None
    
    # Resultado
    result_ready: bool = False
    result_file_path: str = ""
    download_filename: str = ""
    
    # Erro
    has_error: bool = False
    error_message: str = ""
    
    # Polling
    polling_active: bool = False
    last_update: str = ""
    
    async def start_job(self, search_query: SearchQuery) -> bool:
        """
        Inicia novo job de processamento.
        
        Args:
            search_query: Consulta de busca para processar
            
        Returns:
            True se job iniciado com sucesso
        """
        try:
            # Reset estado anterior
            self._reset_job_state()
            
            # TODO: Integrar com Celery para iniciar job real
            # Por enquanto, simula início do job
            
            job = ProcessingJob(search_query=search_query)
            job.start_processing(celery_task_id="simulated-task-id")
            
            # Atualiza estado
            self.current_job = job.to_dict()
            self.job_id = job.id
            self.is_processing = True
            self.processing_status = "Buscando artigos..."
            self.current_step = "Iniciando busca no Google Scholar"
            self.last_update = datetime.now().strftime("%H:%M:%S")
            
            # Inicia polling de status
            await self._start_polling()
            
            return True
            
        except Exception as e:
            self.has_error = True
            self.error_message = f"Erro ao iniciar processamento: {str(e)}"
            return False
    
    async def _start_polling(self) -> None:
        """Inicia polling de status do job."""
        self.polling_active = True
        
        # TODO: Implementar polling real com Celery
        # Por enquanto, simula progresso
        asyncio.create_task(self._simulate_progress())
    
    async def _simulate_progress(self) -> None:
        """Simula progresso do job para demonstração."""
        steps = [
            ("Buscando artigos no Google Scholar", 0),
            ("Extraindo metadados dos artigos", 20),
            ("Baixando e processando PDFs", 40),
            ("Analisando conteúdo com IA", 70),
            ("Gerando planilha Excel", 90),
            ("Processamento concluído", 100)
        ]
        
        for step_name, progress in steps:
            if not self.polling_active:
                break
                
            self.current_step = step_name
            self.progress_percentage = progress
            self.processing_status = step_name
            self.last_update = datetime.now().strftime("%H:%M:%S")
            
            # Simula artigos sendo processados
            if progress > 0:
                self.total_articles = 15  # Simulado
                self.processed_articles = int((progress / 100) * self.total_articles)
            
            yield  # Permite que o Reflex atualize a UI
            await asyncio.sleep(2)  # Simula tempo de processamento
        
        # Finaliza job
        if self.polling_active:
            await self._complete_job()
    
    async def _complete_job(self) -> None:
        """Finaliza job com sucesso."""
        self.is_processing = False
        self.polling_active = False
        self.result_ready = True
        self.progress_percentage = 100.0
        self.current_step = "Concluído"
        self.processing_status = "Processamento concluído com sucesso"
        
        # Simula arquivo de resultado
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.result_file_path = f"results/scholar_results_{timestamp}.xlsx"
        self.download_filename = f"artigos_scholar_{timestamp}.xlsx"
        
        self.last_update = datetime.now().strftime("%H:%M:%S")
    
    def stop_polling(self) -> None:
        """Para o polling de status."""
        self.polling_active = False
    
    def cancel_job(self) -> None:
        """Cancela o job atual."""
        if self.is_processing:
            # TODO: Cancelar job no Celery
            pass
        
        self.is_processing = False
        self.polling_active = False
        self.processing_status = "Cancelado pelo usuário"
        self.current_step = "Cancelado"
        self.last_update = datetime.now().strftime("%H:%M:%S")
    
    async def check_job_status(self) -> None:
        """Verifica status atual do job."""
        if not self.job_id or not self.polling_active:
            return
        
        # TODO: Implementar verificação real com Celery
        # self._update_from_celery_task()
        
        self.last_update = datetime.now().strftime("%H:%M:%S")
    
    def handle_job_error(self, error_message: str) -> None:
        """Trata erro no processamento do job."""
        self.is_processing = False
        self.polling_active = False
        self.has_error = True
        self.error_message = error_message
        self.processing_status = "Erro no processamento"
        self.current_step = "Falhou"
        self.last_update = datetime.now().strftime("%H:%M:%S")
    
    def clear_error(self) -> None:
        """Limpa estado de erro."""
        self.has_error = False
        self.error_message = ""
    
    def _reset_job_state(self) -> None:
        """Reseta estado do job para novo processamento."""
        self.current_job = None
        self.job_id = ""
        self.is_processing = False
        self.processing_status = "idle"
        self.progress_percentage = 0.0
        self.total_articles = 0
        self.processed_articles = 0
        self.current_step = ""
        self.estimated_time_remaining = None
        self.result_ready = False
        self.result_file_path = ""
        self.download_filename = ""
        self.has_error = False
        self.error_message = ""
        self.polling_active = False
        self.last_update = ""
    
    def get_progress_display(self) -> str:
        """Retorna progresso formatado para exibição."""
        if self.total_articles > 0:
            return f"{self.processed_articles}/{self.total_articles} artigos processados"
        else:
            return f"{self.progress_percentage:.0f}% concluído"
    
    def get_status_color(self) -> str:
        """Retorna cor do status para UI."""
        if self.has_error:
            return "red"
        elif self.result_ready:
            return "green"
        elif self.is_processing:
            return "blue"
        else:
            return "gray"
    
    def can_start_new_job(self) -> bool:
        """Verifica se pode iniciar novo job."""
        return not self.is_processing and not self.polling_active
    
    def get_job_summary(self) -> Dict[str, Any]:
        """Retorna resumo do job atual."""
        return {
            "job_id": self.job_id,
            "is_processing": self.is_processing,
            "status": self.processing_status,
            "progress": self.progress_percentage,
            "current_step": self.current_step,
            "total_articles": self.total_articles,
            "processed_articles": self.processed_articles,
            "result_ready": self.result_ready,
            "has_error": self.has_error,
            "error_message": self.error_message,
            "last_update": self.last_update,
            "can_start_new": self.can_start_new_job(),
            "download_filename": self.download_filename
        }