"""
DownloadState - Estado de gerenciamento de downloads de resultados.

Este estado gerencia o processo de download de arquivos de resultado,
incluindo validação, preparação e entrega de arquivos Excel.
"""

import reflex as rx
import os
from typing import Optional
from datetime import datetime


class DownloadState(rx.State):
    """Estado de gerenciamento de downloads."""
    
    # Estados de download
    download_ready: bool = False
    download_url: str = ""
    download_filename: str = ""
    file_size_bytes: int = 0
    
    # Informações do arquivo
    file_path: str = ""
    generated_at: str = ""
    expires_at: str = ""
    
    # Estados de erro
    download_error: str = ""
    has_download_error: bool = False
    
    def prepare_download(self, file_path: str, filename: str = "") -> bool:
        """
        Prepara arquivo para download.
        
        Args:
            file_path: Caminho do arquivo no servidor
            filename: Nome para download (opcional)
            
        Returns:
            True se preparação foi bem-sucedida
        """
        try:
            # Verifica se arquivo existe
            if not os.path.exists(file_path):
                self._set_download_error("Arquivo de resultado não encontrado")
                return False
            
            # Obtém informações do arquivo
            file_stats = os.stat(file_path)
            self.file_size_bytes = file_stats.st_size
            self.file_path = file_path
            
            # Define nome do arquivo
            if not filename:
                filename = os.path.basename(file_path)
            self.download_filename = filename
            
            # Define URL de download (será implementada no Reflex)
            self.download_url = f"/download/{os.path.basename(file_path)}"
            
            # Timestamps
            self.generated_at = datetime.fromtimestamp(
                file_stats.st_mtime
            ).strftime("%d/%m/%Y às %H:%M")
            
            # Define expiração (24 horas)
            expire_time = datetime.fromtimestamp(file_stats.st_mtime)
            expire_time = expire_time.replace(
                hour=expire_time.hour + 24
            )
            self.expires_at = expire_time.strftime("%d/%m/%Y às %H:%M")
            
            # Marca como pronto
            self.download_ready = True
            self.has_download_error = False
            self.download_error = ""
            
            return True
            
        except Exception as e:
            self._set_download_error(f"Erro ao preparar download: {str(e)}")
            return False
    
    def _set_download_error(self, error_message: str) -> None:
        """Define erro de download."""
        self.has_download_error = True
        self.download_error = error_message
        self.download_ready = False
    
    def clear_download(self) -> None:
        """Limpa estado de download."""
        self.download_ready = False
        self.download_url = ""
        self.download_filename = ""
        self.file_size_bytes = 0
        self.file_path = ""
        self.generated_at = ""
        self.expires_at = ""
        self.download_error = ""
        self.has_download_error = False
    
    def get_file_size_display(self) -> str:
        """Retorna tamanho do arquivo formatado."""
        if self.file_size_bytes == 0:
            return "Tamanho desconhecido"
        
        # Converte bytes para unidades legíveis
        if self.file_size_bytes < 1024:
            return f"{self.file_size_bytes} bytes"
        elif self.file_size_bytes < 1024 * 1024:
            kb = self.file_size_bytes / 1024
            return f"{kb:.1f} KB"
        else:
            mb = self.file_size_bytes / (1024 * 1024)
            return f"{mb:.1f} MB"
    
    def is_file_expired(self) -> bool:
        """Verifica se arquivo está expirado."""
        if not self.file_path or not os.path.exists(self.file_path):
            return True
        
        try:
            file_stats = os.stat(self.file_path)
            file_age_hours = (
                datetime.now().timestamp() - file_stats.st_mtime
            ) / 3600
            
            return file_age_hours > 24  # Expira em 24 horas
            
        except Exception:
            return True
    
    def validate_download(self) -> bool:
        """
        Valida se download está disponível e válido.
        
        Returns:
            True se download é válido
        """
        if not self.download_ready:
            return False
        
        if self.has_download_error:
            return False
        
        if self.is_file_expired():
            self._set_download_error("Arquivo expirado. Gere novamente os resultados.")
            return False
        
        return True
    
    async def initiate_download(self) -> str:
        """
        Inicia processo de download.
        
        Returns:
            URL de download ou string vazia se erro
        """
        if not self.validate_download():
            return ""
        
        # TODO: Implementar logging de download
        # log_download_attempt(self.file_path, self.download_filename)
        
        return self.download_url
    
    def get_download_info(self) -> dict:
        """Retorna informações completas do download."""
        return {
            "ready": self.download_ready,
            "filename": self.download_filename,
            "file_size": self.get_file_size_display(),
            "generated_at": self.generated_at,
            "expires_at": self.expires_at,
            "download_url": self.download_url,
            "has_error": self.has_download_error,
            "error_message": self.download_error,
            "is_expired": self.is_file_expired(),
            "is_valid": self.validate_download()
        }