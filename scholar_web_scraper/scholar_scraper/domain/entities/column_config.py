"""
Entidade ColumnConfig - Representa a configuração de uma coluna na planilha de resultados.

Esta entidade define como uma coluna deve ser estruturada, incluindo
seu nome, tipo, descrição e se é obrigatória.
"""

from typing import Optional, List
from dataclasses import dataclass
from enum import Enum
import uuid


class ColumnType(Enum):
    """Tipos de coluna disponíveis."""
    TEXT = "text"
    BOOLEAN = "boolean"


@dataclass
class ColumnConfig:
    """
    Entidade que representa a configuração de uma coluna.
    
    Attributes:
        id: Identificador único da coluna
        name: Nome da coluna (usado no cabeçalho da planilha)
        column_type: Tipo da coluna (text ou boolean)
        description: Descrição da coluna para o prompt da IA
        is_required: Indica se a coluna é obrigatória
        order: Ordem da coluna na planilha
        default_value: Valor padrão para a coluna (opcional)
    """
    
    name: str
    column_type: str
    description: str = ""
    id: str = ""
    is_required: bool = False
    order: int = 0
    default_value: Optional[str] = None
    
    def __post_init__(self) -> None:
        """Inicializa valores padrão se não fornecidos."""
        if not self.id:
            self.id = str(uuid.uuid4())
        
        # Gera descrição padrão se não fornecida
        if not self.description:
            self.description = self._generate_default_description()
        
        # Valida o tipo da coluna
        if self.column_type not in [ct.value for ct in ColumnType]:
            raise ValueError(f"Tipo de coluna inválido: {self.column_type}")
    
    def _generate_default_description(self) -> str:
        """Gera descrição padrão baseada no nome e tipo da coluna."""
        if self.column_type == ColumnType.BOOLEAN.value:
            return f"Indica se o artigo possui/atende ao critério: {self.name}"
        else:
            return f"Informação sobre: {self.name}"
    
    def is_valid(self) -> bool:
        """
        Valida se a configuração da coluna está válida.
        
        Returns:
            True se a configuração é válida, False caso contrário
        """
        if not self.name or not self.name.strip():
            return False
        
        if self.column_type not in [ct.value for ct in ColumnType]:
            return False
        
        if len(self.name) > 100:
            return False
        
        if len(self.description) > 500:
            return False
        
        return True
    
    def get_validation_errors(self) -> List[str]:
        """
        Retorna lista de erros de validação.
        
        Returns:
            Lista de mensagens de erro
        """
        errors = []
        
        if not self.name or not self.name.strip():
            errors.append("Nome da coluna é obrigatório")
        elif len(self.name) > 100:
            errors.append("Nome da coluna não pode exceder 100 caracteres")
        
        if self.column_type not in [ct.value for ct in ColumnType]:
            valid_types = [ct.value for ct in ColumnType]
            errors.append(f"Tipo da coluna deve ser um de: {', '.join(valid_types)}")
        
        if len(self.description) > 500:
            errors.append("Descrição da coluna não pode exceder 500 caracteres")
        
        return errors
    
    def is_boolean_type(self) -> bool:
        """Verifica se a coluna é do tipo boolean."""
        return self.column_type == ColumnType.BOOLEAN.value
    
    def is_text_type(self) -> bool:
        """Verifica se a coluna é do tipo text."""
        return self.column_type == ColumnType.TEXT.value
    
    def get_prompt_instruction(self) -> str:
        """
        Gera instrução específica para o prompt da IA.
        
        Returns:
            Instrução formatada para o prompt
        """
        if self.is_boolean_type():
            return f'"{self.name}": responda apenas "sim" ou "não" - {self.description}'
        else:
            return f'"{self.name}": texto descritivo - {self.description}'
    
    def format_value_for_excel(self, value: str) -> str:
        """
        Formata valor para inserção na planilha Excel.
        
        Args:
            value: Valor a ser formatado
            
        Returns:
            Valor formatado para Excel
        """
        if not value:
            return self.default_value or ""
        
        if self.is_boolean_type():
            # Normaliza valores boolean
            value_lower = value.lower().strip()
            if value_lower in ["sim", "yes", "true", "1", "verdadeiro"]:
                return "Sim"
            elif value_lower in ["não", "nao", "no", "false", "0", "falso"]:
                return "Não"
            else:
                return "Não definido"
        
        # Para colunas de texto, retorna o valor limpo
        return str(value).strip()
    
    def to_dict(self) -> dict:
        """
        Converte a configuração para dicionário para serialização.
        
        Returns:
            Dicionário com dados da configuração
        """
        return {
            "id": self.id,
            "name": self.name,
            "column_type": self.column_type,
            "description": self.description,
            "is_required": self.is_required,
            "order": self.order,
            "default_value": self.default_value
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "ColumnConfig":
        """
        Cria ColumnConfig a partir de dicionário.
        
        Args:
            data: Dicionário com dados da configuração
            
        Returns:
            Instância de ColumnConfig
        """
        return cls(
            id=data.get("id", ""),
            name=data["name"],
            column_type=data["column_type"],
            description=data.get("description", ""),
            is_required=data.get("is_required", False),
            order=data.get("order", 0),
            default_value=data.get("default_value")
        )
    
    @classmethod
    def create_required_link_column(cls) -> "ColumnConfig":
        """Cria a coluna obrigatória 'Link'."""
        return cls(
            name="Link",
            column_type=ColumnType.TEXT.value,
            description="URL do artigo no Google Scholar",
            is_required=True,
            order=999  # Última coluna
        )
    
    @classmethod
    def create_required_filter_column(cls) -> "ColumnConfig":
        """Cria a coluna obrigatória 'Atende ao Filtro?'."""
        return cls(
            name="Atende ao Filtro?",
            column_type=ColumnType.BOOLEAN.value,
            description="Indica se o artigo atende aos critérios de filtro definidos",
            is_required=True,
            order=998  # Penúltima coluna
        )