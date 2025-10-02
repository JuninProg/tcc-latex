"""
Estado principal da aplicação Reflex.

Gerencia estado global, eventos de UI e coordena
outras funcionalidades da aplicação.
"""

import reflex as rx
import os
import asyncio
import tempfile
from datetime import datetime
from typing import Optional, Dict, Any
from dataclasses import asdict
from dotenv import load_dotenv

from scholar_scraper.domain.entities import SearchQuery, ColumnConfig
from scholar_scraper.infrastructure.celery_worker import celery_app, process_articles

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()


class AppState(rx.State):
    """
    Estado principal da aplicação.
    
    Gerencia formulário, validação, processamento assíncrono
    e download de resultados.
    """
    
    # Versão da aplicação
    app_version: str = "1.0.0"
    
    # Campos do formulário
    query_text: str = "aleitamento materno aplicativo"
    filter_criteria: str = "não apenas protótipo"
    max_results: int = 20
    
    # Erros de validação
    query_text_error: str = ""
    filter_criteria_error: str = ""
    
    # Estado do processamento
    is_processing: bool = False
    progress_percentage: int = 0
    progress_message: str = ""
    current_task_id: Optional[str] = None
    
    # Estado do resultado
    result_ready: bool = False
    download_ready: bool = False
    excel_file_path: Optional[str] = None
    result_summary: str = ""
    
    def update_query_text(self, value: str) -> None:
        """Atualiza texto da query e limpa erro."""
        print(f"DEBUG: update_query_text called with: '{value}'")
        self.query_text = value
        if self.query_text_error:
            self.query_text_error = ""
            
    def update_filter_criteria(self, value: str) -> None:
        """Atualiza critérios de filtro e limpa erro."""
        print(f"DEBUG: update_filter_criteria called with: '{value}'")
        self.filter_criteria = value
        if self.filter_criteria_error:
            self.filter_criteria_error = ""
            
    def update_max_results(self, value: str) -> None:
        """Atualiza número máximo de resultados."""
        try:
            self.max_results = max(1, min(100, int(value)))
        except (ValueError, TypeError):
            self.max_results = 20
            
    def can_submit_form(self) -> bool:
        """Verifica se o formulário pode ser submetido."""
        return (
            bool(self.query_text.strip()) and
            bool(self.filter_criteria.strip()) and
            not self.is_processing
        )
        
    def debug_print_values(self) -> None:
        """Debug: Imprime valores atuais."""
        print(f"DEBUG: Current values:")
        print(f"  query_text = '{self.query_text}'")
        print(f"  filter_criteria = '{self.filter_criteria}'")
        print(f"  max_results = {self.max_results}")
        
    def _validate_form(self) -> bool:
        """
        Valida formulário antes do submit.
        
        Returns:
            True se válido, False caso contrário
        """
        print("DEBUG: _validate_form called!")
        is_valid = True
        
        # Validação do texto de pesquisa
        if not self.query_text.strip():
            print("DEBUG: query_text is empty")
            self.query_text_error = "Campo obrigatório"
            is_valid = False
        elif len(self.query_text.strip()) < 3:
            print("DEBUG: query_text too short")
            self.query_text_error = "Mínimo de 3 caracteres"
            is_valid = False
        else:
            self.query_text_error = ""
            
        # Validação dos critérios de filtro
        if not self.filter_criteria.strip():
            print("DEBUG: filter_criteria is empty")
            self.filter_criteria_error = "Campo obrigatório"
            is_valid = False
        elif len(self.filter_criteria.strip()) < 10:
            print("DEBUG: filter_criteria too short")
            self.filter_criteria_error = "Mínimo de 10 caracteres para critérios específicos"
            is_valid = False
        else:
            self.filter_criteria_error = ""
            
        print(f"DEBUG: validation result = {is_valid}")
        return is_valid
        
    async def submit_search(self) -> None:
        """
        Submete formulário e inicia processamento assíncrono.
        """
        print("DEBUG: submit_search called!")
        print(f"DEBUG: query_text = '{self.query_text}'")
        print(f"DEBUG: filter_criteria = '{self.filter_criteria}'")
        print(f"DEBUG: is_processing = {self.is_processing}")
        
        # Valida formulário
        if not self._validate_form():
            print("DEBUG: Form validation failed!")
            return
            
        print("DEBUG: Form validation passed!")
            
        # Verifica se já está processando
        if self.is_processing:
            print("DEBUG: Already processing, returning")
            return
            
        print("DEBUG: Starting processing...")
        
        try:
            print("DEBUG: Entering try block...")
            
            # Inicializa estado de processamento
            self.is_processing = True
            self.result_ready = False
            self.download_ready = False
            self.progress_percentage = 0
            self.progress_message = "Iniciando processamento..."
            self.result_summary = ""
            self.excel_file_path = None
            
            print("DEBUG: State initialized...")
            
            # Verifica chave da API
            gemini_api_key = os.getenv('GEMINI_API_KEY')
            print(f"DEBUG: Gemini API key exists: {bool(gemini_api_key)}")
            if not gemini_api_key:
                self.progress_message = "Erro: Chave da API do Gemini não configurada"
                self.is_processing = False
                return
                
            print("DEBUG: Verifying API key...")
                
            # Colunas padrão (podem ser configuráveis no futuro)
            columns = [
                ColumnConfig(
                    name="Tecnologia Principal",
                    column_type="text",
                    description="Principal tecnologia ou framework utilizado no artigo"
                ),
                ColumnConfig(
                    name="Tem Implementação Prática",
                    column_type="boolean",
                    description="Se o artigo apresenta implementação real, não apenas teoria"
                ),
                ColumnConfig(
                    name="Ano de Publicação",
                    column_type="text",
                    description="Ano em que o artigo foi publicado"
                ),
                ColumnConfig(
                    name="Relevância do Estudo",
                    column_type="text",
                    description="Breve avaliação da relevância e contribuição do estudo"
                )
            ]
            
            # Cria objetos de domínio
            search_query = SearchQuery(
                query_text=self.query_text.strip(),
                filter_criteria=self.filter_criteria.strip(),
                max_results=self.max_results,
                columns=columns
            )
            
            print("DEBUG: Created columns configuration...")
            
            # Converte para dicionários para serialização
            search_query_dict = asdict(search_query)
            
            print("DEBUG: Converted to dicts for serialization...")
            print(f"DEBUG: search_query_dict = {search_query_dict}")
            
            # Envia tarefa para Celery
            print("DEBUG: About to send task to Celery...")
            task = process_articles.delay(
                search_query_dict=search_query_dict,
                filter_criteria=self.filter_criteria.strip(),
                gemini_api_key=gemini_api_key
            )
            
            print(f"DEBUG: Task created with ID: {task.id}")
            
            self.current_task_id = task.id
            self.progress_message = "Tarefa criada, aguardando processamento..."
            
            print("DEBUG: About to start monitoring...")
            # Inicia monitoramento do progresso
            await self._monitor_task_progress()
            
        except Exception as e:
            print(f"DEBUG: Exception in submit_search: {e}")
            self.progress_message = f"Erro ao iniciar processamento: {str(e)}"
            self.is_processing = False
            
    async def _monitor_task_progress(self) -> None:
        """
        Monitora progresso da tarefa Celery.
        """
        if not self.current_task_id:
            return
            
        try:
            # Loop de monitoramento
            while self.is_processing:
                # Verifica status da tarefa
                result = celery_app.AsyncResult(self.current_task_id)
                
                if result.state == 'PENDING':
                    self.progress_message = "Aguardando início do processamento..."
                    self.progress_percentage = 0
                    
                elif result.state == 'PROGRESS':
                    # Atualiza progresso
                    info = result.info
                    if isinstance(info, dict):
                        self.progress_percentage = int(
                            (info.get('current', 0) / info.get('total', 5)) * 100
                        )
                        self.progress_message = info.get('status', 'Processando...')
                        
                elif result.state == 'SUCCESS':
                    # Processamento concluído
                    self.progress_percentage = 100
                    self.progress_message = "Processamento concluído!"
                    
                    # Obtém resultado
                    task_result = result.result
                    if isinstance(task_result, dict):
                        self.excel_file_path = task_result.get('excel_path')
                        total_articles = task_result.get('total_articles', 0)
                        meets_criteria = task_result.get('meets_criteria', 0)
                        
                        self.result_summary = (
                            f"Processados {total_articles} artigos. "
                            f"{meets_criteria} atendem aos critérios especificados."
                        )
                        
                        self.result_ready = True
                        self.download_ready = True
                    elif isinstance(task_result, str):
                        # Worker retorna apenas o caminho do arquivo
                        self.excel_file_path = task_result
                        self.result_summary = "Processamento concluído! Arquivo CSV gerado."
                        self.result_ready = True
                        self.download_ready = True
                    
                    self.is_processing = False
                    break
                    
                elif result.state == 'FAILURE':
                    # Erro no processamento
                    self.progress_message = f"Erro no processamento: {str(result.info)}"
                    self.is_processing = False
                    break
                    
                # Aguarda antes da próxima verificação
                await asyncio.sleep(2)
                
        except Exception as e:
            self.progress_message = f"Erro no monitoramento: {str(e)}"
            self.is_processing = False
            
    def download_excel(self) -> rx.event.EventSpec:
        """Faz o download do arquivo CSV."""
        if not self.excel_file_path:
            print("DEBUG: No file path available for download")
            return rx.toast.error("Arquivo não encontrado")
        
        file_path = self.excel_file_path
        
        try:
            # Ler o conteúdo do arquivo CSV
            with open(file_path, 'r', encoding='utf-8') as f:
                csv_content = f.read()
            
            # Escapar o conteúdo CSV para JavaScript
            escaped_content = csv_content.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r')
            filename = f"resultados_pesquisa_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            # Usar JavaScript para fazer o download
            js_code = f"""
            const content = "{escaped_content}";
            const blob = new Blob([content], {{ type: 'text/csv;charset=utf-8;' }});
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = '{filename}';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            """
            
            return rx.call_script(js_code)
            
        except Exception as e:
            print(f"Erro no download: {e}")
            return rx.toast.error(f"Erro ao baixar arquivo: {e}")
    
    async def initiate_download(self) -> rx.event.EventSpec:
        """
        Inicia processo de download usando JavaScript.
        """
        if not self.excel_file_path or not self.download_ready:
            return rx.toast.error("Arquivo não está pronto para download")
        
        try:
            # Lê o conteúdo do arquivo CSV
            with open(self.excel_file_path, 'r', encoding='utf-8') as f:
                csv_content = f.read()
            
            # Escapar o conteúdo CSV para JavaScript
            escaped_content = csv_content.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r')
            filename = f"resultados_pesquisa_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            # Usar JavaScript para fazer o download
            js_code = f"""
            const content = "{escaped_content}";
            const blob = new Blob([content], {{ type: 'text/csv;charset=utf-8;' }});
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = '{filename}';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            """
            
            return rx.call_script(js_code)
            
        except Exception as e:
            print(f"Erro no initiate_download: {e}")
            return rx.toast.error(f"Erro ao baixar arquivo: {e}")