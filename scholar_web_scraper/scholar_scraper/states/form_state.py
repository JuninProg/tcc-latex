"""
FormState - Estado do formulário principal da aplicação Reflex.

Este estado gerencia o formulário de busca, incluindo texto da pesquisa,
critérios de filtro e configuração dinâmica de colunas.
"""

import reflex as rx
from typing import List, Dict, Any, Optional
import uuid

from ..domain.entities.search_query import SearchQuery
from ..domain.entities.column_config import ColumnConfig


class FormState(rx.State):
    """Estado do formulário principal."""
    
    # Campos do formulário
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
    
    def __init__(self):
        """Inicializa o estado com colunas padrão."""
        super().__init__()
        self._initialize_default_columns()
    
    def _initialize_default_columns(self) -> None:
        """Inicializa colunas padrão obrigatórias."""
        default_columns = [
            {
                "id": str(uuid.uuid4()),
                "name": "Título",
                "type": "text",
                "description": "Título do artigo científico",
                "is_required": False,
                "order": 1
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Autores",
                "type": "text", 
                "description": "Lista de autores do artigo",
                "is_required": False,
                "order": 2
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Tem aplicativo?",
                "type": "boolean",
                "description": "Indica se o artigo menciona desenvolvimento de aplicativo",
                "is_required": False,
                "order": 3
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Link",
                "type": "text",
                "description": "URL do artigo no Google Scholar",
                "is_required": True,
                "order": 998
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Atende ao Filtro?",
                "type": "boolean",
                "description": "Indica se o artigo atende aos critérios definidos",
                "is_required": True,
                "order": 999
            }
        ]
        self.columns = default_columns
    
    def update_query_text(self, value: str) -> None:
        """Atualiza texto da pesquisa."""
        self.query_text = value
        self._validate_query_text()
        self._update_form_validity()
    
    def update_filter_criteria(self, value: str) -> None:
        """Atualiza critérios de filtro."""
        self.filter_criteria = value
        self._validate_filter_criteria()
        self._update_form_validity()
    
    def update_max_results(self, value: int) -> None:
        """Atualiza número máximo de resultados."""
        if 1 <= value <= 100:
            self.max_results = value
    
    def add_column(self) -> None:
        """Adiciona nova coluna ao formulário."""
        new_column = {
            "id": str(uuid.uuid4()),
            "name": "",
            "type": "text",
            "description": "",
            "is_required": False,
            "order": len(self.columns) + 1
        }
        
        # Insere antes das colunas obrigatórias
        insert_position = len(self.columns) - 2  # Antes de Link e Filtro
        self.columns = (
            self.columns[:insert_position] + 
            [new_column] + 
            self.columns[insert_position:]
        )
        self._validate_columns()
        self._update_form_validity()
    
    def remove_column(self, column_id: str) -> None:
        """Remove coluna pelo ID."""
        # Não permite remover colunas obrigatórias
        column_to_remove = None
        for col in self.columns:
            if col["id"] == column_id:
                column_to_remove = col
                break
        
        if column_to_remove and not column_to_remove.get("is_required", False):
            self.columns = [col for col in self.columns if col["id"] != column_id]
            self._validate_columns()
            self._update_form_validity()
    
    def update_column_name(self, column_id: str, name: str) -> None:
        """Atualiza nome de uma coluna."""
        for col in self.columns:
            if col["id"] == column_id:
                col["name"] = name
                break
        self._validate_columns()
        self._update_form_validity()
    
    def update_column_type(self, column_id: str, column_type: str) -> None:
        """Atualiza tipo de uma coluna."""
        if column_type in ["text", "boolean"]:
            for col in self.columns:
                if col["id"] == column_id:
                    col["type"] = column_type
                    break
            self._validate_columns()
            self._update_form_validity()
    
    def update_column_description(self, column_id: str, description: str) -> None:
        """Atualiza descrição de uma coluna."""
        for col in self.columns:
            if col["id"] == column_id:
                col["description"] = description
                break
        self._validate_columns()
        self._update_form_validity()
    
    def _validate_query_text(self) -> None:
        """Valida texto da pesquisa."""
        if not self.query_text.strip():
            self.query_text_error = "Texto de pesquisa é obrigatório"
        elif len(self.query_text.strip()) < 3:
            self.query_text_error = "Texto de pesquisa deve ter pelo menos 3 caracteres"
        else:
            self.query_text_error = ""
    
    def _validate_filter_criteria(self) -> None:
        """Valida critérios de filtro."""
        if not self.filter_criteria.strip():
            self.filter_criteria_error = "Critério de filtro é obrigatório"
        elif len(self.filter_criteria.strip()) < 10:
            self.filter_criteria_error = "Critério deve ser mais específico (mín. 10 caracteres)"
        else:
            self.filter_criteria_error = ""
    
    def _validate_columns(self) -> None:
        """Valida configuração das colunas."""
        errors = []
        
        # Verifica se há pelo menos uma coluna não obrigatória
        user_columns = [col for col in self.columns if not col.get("is_required", False)]
        if not user_columns:
            errors.append("Adicione pelo menos uma coluna personalizada")
        
        # Valida cada coluna
        for i, col in enumerate(self.columns):
            if not col.get("name", "").strip():
                errors.append(f"Coluna {i+1}: Nome é obrigatório")
            elif len([c for c in self.columns if c["name"] == col["name"]]) > 1:
                errors.append(f"Coluna {i+1}: Nome duplicado")
        
        self.columns_error = "; ".join(errors)
    
    def _update_form_validity(self) -> None:
        """Atualiza estado de validade do formulário."""
        self.form_is_valid = (
            not self.query_text_error and
            not self.filter_criteria_error and
            not self.columns_error and
            bool(self.query_text.strip()) and
            bool(self.filter_criteria.strip())
        )
    
    def get_search_query(self) -> Optional[SearchQuery]:
        """
        Constrói SearchQuery a partir do estado atual.
        
        Returns:
            SearchQuery se válido, None caso contrário
        """
        if not self.form_is_valid:
            return None
        
        # Converte colunas para ColumnConfig
        column_configs = []
        for col_data in self.columns:
            column_config = ColumnConfig(
                id=col_data["id"],
                name=col_data["name"],
                column_type=col_data["type"],
                description=col_data.get("description", ""),
                is_required=col_data.get("is_required", False),
                order=col_data.get("order", 0)
            )
            column_configs.append(column_config)
        
        return SearchQuery(
            query_text=self.query_text.strip(),
            filter_criteria=self.filter_criteria.strip(),
            columns=column_configs,
            max_results=self.max_results,
            year_min=getattr(self, 'year_min', None),
            year_max=getattr(self, 'year_max', None)
        )
    
    def reset_form(self) -> None:
        """Reseta o formulário para estado inicial."""
        self.query_text = ""
        self.filter_criteria = ""
        self.max_results = 20
        self.query_text_error = ""
        self.filter_criteria_error = ""
        self.columns_error = ""
        self.form_is_valid = False
        self._initialize_default_columns()
    
    def get_form_data_summary(self) -> Dict[str, Any]:
        """Retorna resumo dos dados do formulário."""
        return {
            "query_text": self.query_text,
            "filter_criteria": self.filter_criteria,
            "max_results": self.max_results,
            "total_columns": len(self.columns),
            "user_columns": len([col for col in self.columns if not col.get("is_required", False)]),
            "is_valid": self.form_is_valid,
            "has_errors": bool(self.query_text_error or self.filter_criteria_error or self.columns_error)
        }