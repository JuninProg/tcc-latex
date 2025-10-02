"""
Estado principal da aplicação Reflex.

Gerencia estado global, eventos de UI e coordena
outras funcionalidades da aplicação.
"""

import reflex as rx
import os
import asyncio
import tempfile
import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List
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
    
    # Campos do formulário (copiados do FormState)
    query_text: str = "aleitamento materno aplicativo"
    filter_criteria: str = "não apenas protótipo"
    max_results: int = 50
    
    # Gerenciamento de colunas
    columns: List[Dict[str, Any]] = []
    
    # Estados de validação
    query_text_error: str = ""
    filter_criteria_error: str = ""
    columns_error: str = ""
    form_is_valid: bool = False
    
    # Campos específicos do Scholar Scraper
    year_min: int = 2022
    year_max: int = 2025
    
    # Estado do processamento
    is_processing: bool = False
    progress_percentage: int = 0
    progress_message: str = ""
    processing_status: str = "idle"
    current_step: str = ""
    total_articles: int = 0
    processed_articles: int = 0
    last_update: str = ""
    current_task_id: Optional[str] = None
    
    # Estado da interface
    show_help: bool = False
    download_filename: str = ""
    generated_at: str = ""
    
    # Estado do resultado
    result_ready: bool = False
    download_ready: bool = False
    excel_file_path: Optional[str] = None
    result_summary: str = ""
    error_message: str = ""
    
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
            
    def add_column(self) -> None:
        """Adiciona uma nova coluna."""
        new_column = {
            "id": str(uuid.uuid4()),
            "name": "",
            "type": "text",
            "description": "",
            "is_required": False,
            "order": len(self.columns) + 1
        }
        self.columns.append(new_column)
        
    def update_column_name(self, column_id: str, name: str) -> None:
        """Atualiza o nome de uma coluna."""
        for column in self.columns:
            if column["id"] == column_id:
                column["name"] = name
                break
                
    def update_column_type(self, column_id: str, column_type: str) -> None:
        """Atualiza o tipo de uma coluna."""
        for column in self.columns:
            if column["id"] == column_id:
                column["type"] = column_type
                break
                
    def update_column_description(self, column_id: str, description: str) -> None:
        """Atualiza a descrição de uma coluna."""
        for column in self.columns:
            if column["id"] == column_id:
                column["description"] = description
                break
                
    def remove_column(self, column_id: str) -> None:
        """Remove uma coluna."""
        self.columns = [col for col in self.columns if col["id"] != column_id]
        
    def update_max_results(self, value: str) -> None:
        """Atualiza número máximo de resultados."""
        try:
            self.max_results = max(1, min(5000, int(value)))  # Permite até 5000
        except (ValueError, TypeError):
            self.max_results = 20
            
    def update_year_min(self, value: str) -> None:
        """Atualiza ano mínimo para filtro."""
        try:
            year = int(value)
            if 1900 <= year <= 2030:  # Validação básica
                self.year_min = year
                # Garante que year_min <= year_max
                if self.year_min > self.year_max:
                    self.year_max = self.year_min
        except (ValueError, TypeError):
            self.year_min = 2022
            
    def update_year_max(self, value: str) -> None:
        """Atualiza ano máximo para filtro."""
        try:
            year = int(value)
            if 1900 <= year <= 2030:  # Validação básica
                self.year_max = year
                # Garante que year_min <= year_max
                if self.year_max < self.year_min:
                    self.year_min = self.year_max
        except (ValueError, TypeError):
            self.year_max = 2025
            
    def can_submit_form(self) -> bool:
        """Verifica se o formulário pode ser submetido."""
        return (
            bool(self.query_text.strip()) and
            bool(self.filter_criteria.strip()) and
            not self.is_processing
        )
        
    def toggle_help(self) -> None:
        """Alterna exibição da ajuda."""
        self.show_help = not self.show_help
        
    def cancel_job(self) -> None:
        """Cancela o job atual."""
        if self.current_task_id:
            # Revoga a task do Celery
            celery_app.control.revoke(self.current_task_id, terminate=True)
            self.current_task_id = None
        
        # Reset do estado
        self.is_processing = False
        self.progress_percentage = 0
        self.progress_message = ""
        
    def reset_application(self) -> None:
        """Reseta a aplicação para o estado inicial."""
        # Cancela job se estiver rodando
        self.cancel_job()
        
        # Reset formulário (se herdado do FormState)
        if hasattr(self, 'reset_form'):
            self.reset_form()
        
        # Reset específico do AppState
        self.show_help = False
        
    def clear_error(self) -> None:
        """Limpa mensagens de erro."""
        self.error_message = ""
        self.query_text_error = ""
        self.filter_criteria_error = ""
        
    def add_column(self) -> None:
        """Adiciona uma nova coluna (compatibilidade com FormState)."""
        # Implementação simples para compatibilidade
        pass
        
    @rx.var
    def get_main_action_text(self) -> str:
        """Retorna texto do botão principal baseado no estado."""
        if self.is_processing:
            return "Processando..."
        return "Buscar Artigos"
        
    @rx.var
    def has_error(self) -> bool:
        """Indica se há erros de validação."""
        return bool(self.query_text_error or self.filter_criteria_error)
        
    @rx.var
    def get_file_size_display(self) -> str:
        """Retorna o tamanho do arquivo de download formatado."""
        if self.download_filename:
            return "Arquivo disponível"
        return "Nenhum arquivo"
        
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
                year_min=self.year_min if self.year_min else None,
                year_max=self.year_max if self.year_max else None,
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
                    print(f"DEBUG: task_result type: {type(task_result)}")
                    print(f"DEBUG: task_result: {task_result}")
                    
                    if isinstance(task_result, dict):
                        self.excel_file_path = task_result.get('excel_path')
                        print(f"DEBUG: excel_file_path set to: {self.excel_file_path}")
                        total_articles = task_result.get('total_articles', 0)
                        meets_criteria = task_result.get('meets_criteria', 0)
                        
                        self.result_summary = (
                            f"Processados {total_articles} artigos. "
                            f"{meets_criteria} atendem aos critérios especificados."
                        )
                        
                        self.result_ready = True
                        self.download_ready = True
                        print(f"DEBUG: result_ready={self.result_ready}, download_ready={self.download_ready}")
                    elif isinstance(task_result, str):
                        # Worker retorna apenas o caminho do arquivo
                        self.excel_file_path = task_result
                        print(f"DEBUG: excel_file_path set to (string): {self.excel_file_path}")
                        self.result_summary = "Processamento concluído! Arquivo CSV gerado."
                        self.result_ready = True
                        self.download_ready = True
                        print(f"DEBUG: result_ready={self.result_ready}, download_ready={self.download_ready}")
                    
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
        print(f"DEBUG: initiate_download called - excel_file_path: {self.excel_file_path}, download_ready: {self.download_ready}")
        
        if not self.excel_file_path or not self.download_ready:
            print(f"DEBUG: No file path available for download")
            return rx.toast.error("Arquivo não está pronto para download")
        
        try:
            print(f"DEBUG: Trying to read file: {self.excel_file_path}")
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
    
    async def download_latest_csv(self) -> rx.event.EventSpec:
        """
        Baixa o CSV mais recente da pasta csvs_gerados.
        """
        try:
            import glob
            import os
            
            # Procura pelo CSV mais recente
            csv_pattern = os.path.join("csvs_gerados", "scholar_scraper_*.csv")
            csv_files = glob.glob(csv_pattern)
            
            if not csv_files:
                return rx.toast.error("Nenhum arquivo CSV encontrado")
                
            # Pega o mais recente
            latest_csv = max(csv_files, key=os.path.getctime)
            print(f"DEBUG: Downloading latest CSV: {latest_csv}")
            
            # Lê o conteúdo do arquivo CSV
            with open(latest_csv, 'r', encoding='utf-8') as f:
                csv_content = f.read()
            
            # Escapar o conteúdo CSV para JavaScript
            escaped_content = csv_content.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r')
            filename = os.path.basename(latest_csv)
            
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
            print(f"Erro no download_latest_csv: {e}")
            return rx.toast.error(f"Erro ao baixar arquivo: {e}")