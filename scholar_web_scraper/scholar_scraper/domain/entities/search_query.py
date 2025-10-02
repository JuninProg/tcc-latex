"""
Entidade SearchQuery - Representa uma consulta de busca no Google Scholar.

Esta entidade encapsula todos os parâmetros de uma busca, incluindo
o texto da consulta, critérios de filtro e configurações de colunas.
"""

from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime
import uuid

from .column_config import ColumnConfig


@dataclass
class SearchQuery:
    """
    Entidade que representa uma consulta de busca.
    
    Attributes:
        id: Identificador único da consulta
        query_text: Texto da pesquisa para o Google Scholar
        filter_criteria: Critérios de filtro para análise via IA
        columns: Lista de configurações de colunas para o resultado
        max_results: Número máximo de resultados a buscar
        created_at: Timestamp de criação da consulta
        user_id: ID do usuário que criou a consulta (opcional)
    """
    
    query_text: str
    filter_criteria: str
    columns: List[ColumnConfig]
    id: str = ""
    max_results: int = 20
    created_at: Optional[datetime] = None
    user_id: Optional[str] = None
    
    def __post_init__(self) -> None:
        """Inicializa valores padrão se não fornecidos."""
        if not self.id:
            self.id = str(uuid.uuid4())
        if self.created_at is None:
            self.created_at = datetime.now()
        
        # Garante que as colunas obrigatórias estejam presentes
        self._ensure_required_columns()
    
    def _ensure_required_columns(self) -> None:
        """Garante que as colunas obrigatórias estejam presentes."""
        required_columns = {"Link", "Atende ao Filtro?"}
        existing_names = {col.name for col in self.columns}
        
        # Adiciona coluna Link se não existir
        if "Link" not in existing_names:
            link_column = ColumnConfig(
                name="Link",
                column_type="text",
                description="URL do artigo no Google Scholar",
                is_required=True
            )
            self.columns.append(link_column)
        
        # Adiciona coluna de filtro se não existir
        if "Atende ao Filtro?" not in existing_names:
            filter_column = ColumnConfig(
                name="Atende ao Filtro?",
                column_type="boolean",
                description="Indica se o artigo atende aos critérios definidos",
                is_required=True
            )
            self.columns.append(filter_column)
    
    def is_valid(self) -> bool:
        """
        Valida se a consulta está válida para execução.
        
        Returns:
            True se a consulta é válida, False caso contrário
        """
        if not self.query_text or not self.query_text.strip():
            return False
        
        if not self.filter_criteria or not self.filter_criteria.strip():
            return False
        
        if not self.columns:
            return False
        
        if self.max_results <= 0 or self.max_results > 100:
            return False
        
        # Valida cada coluna
        for column in self.columns:
            if not column.is_valid():
                return False
        
        return True
    
    def get_validation_errors(self) -> List[str]:
        """
        Retorna lista de erros de validação.
        
        Returns:
            Lista de mensagens de erro
        """
        errors = []
        
        if not self.query_text or not self.query_text.strip():
            errors.append("Texto de pesquisa é obrigatório")
        
        if not self.filter_criteria or not self.filter_criteria.strip():
            errors.append("Critério de filtro é obrigatório")
        
        if not self.columns:
            errors.append("Pelo menos uma coluna deve ser configurada")
        
        if self.max_results <= 0:
            errors.append("Número máximo de resultados deve ser maior que zero")
        elif self.max_results > 100:
            errors.append("Número máximo de resultados não pode exceder 100")
        
        # Valida colunas individuais
        for i, column in enumerate(self.columns):
            if not column.is_valid():
                column_errors = column.get_validation_errors()
                for error in column_errors:
                    errors.append(f"Coluna {i+1}: {error}")
        
        return errors
    
    def get_column_by_name(self, name: str) -> Optional[ColumnConfig]:
        """
        Busca coluna por nome.
        
        Args:
            name: Nome da coluna
            
        Returns:
            ColumnConfig encontrada ou None
        """
        for column in self.columns:
            if column.name == name:
                return column
        return None
    
    def get_boolean_columns(self) -> List[ColumnConfig]:
        """Retorna apenas colunas do tipo boolean."""
        return [col for col in self.columns if col.column_type == "boolean"]
    
    def get_text_columns(self) -> List[ColumnConfig]:
        """Retorna apenas colunas do tipo text."""
        return [col for col in self.columns if col.column_type == "text"]
    
    def to_dict(self) -> dict:
        """
        Converte a consulta para dicionário para serialização.
        
        Returns:
            Dicionário com dados da consulta
        """
        return {
            "id": self.id,
            "query_text": self.query_text,
            "filter_criteria": self.filter_criteria,
            "columns": [col.to_dict() for col in self.columns],
            "max_results": self.max_results,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "user_id": self.user_id
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "SearchQuery":
        """
        Cria SearchQuery a partir de dicionário.
        
        Args:
            data: Dicionário com dados da consulta
            
        Returns:
            Instância de SearchQuery
        """
        columns_data = data.get("columns", [])
        columns = [ColumnConfig.from_dict(col_data) for col_data in columns_data]
        
        created_at = None
        if data.get("created_at"):
            created_at = datetime.fromisoformat(data["created_at"])
        
        return cls(
            id=data.get("id", ""),
            query_text=data["query_text"],
            filter_criteria=data["filter_criteria"],
            columns=columns,
            max_results=data.get("max_results", 20),
            created_at=created_at,
            user_id=data.get("user_id")
        )