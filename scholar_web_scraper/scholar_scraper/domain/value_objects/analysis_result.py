"""
Value Object AnalysisResult - Representa o resultado da análise via IA.

Este value object encapsula os resultados da análise feita pela IA (Gemini)
sobre um artigo científico, incluindo dados estruturados para as colunas.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class AnalysisResult:
    """
    Value object que representa resultado da análise via IA.
    
    Attributes:
        column_data: Dados estruturados para cada coluna configurada
        meets_filter: Indica se o artigo atende ao filtro definido
        confidence_score: Confiança na análise (0.0-1.0)
        analysis_model: Modelo de IA usado para análise
        analyzed_at: Timestamp da análise
        tokens_used: Número de tokens consumidos na análise
        processing_time_seconds: Tempo de processamento em segundos
        error_message: Mensagem de erro se análise parcial
        justification: Justificativa da decisão de filtro
    """
    
    column_data: Dict[str, str]
    meets_filter: bool
    confidence_score: float = 1.0
    analysis_model: str = "gemini-2.0-flash-exp"
    analyzed_at: Optional[datetime] = None
    tokens_used: Optional[int] = None
    processing_time_seconds: Optional[float] = None
    error_message: Optional[str] = None
    justification: Optional[str] = None
    
    def __post_init__(self) -> None:
        """Inicializa timestamp se não fornecido."""
        if self.analyzed_at is None:
            object.__setattr__(self, 'analyzed_at', datetime.now())
    
    def is_valid(self) -> bool:
        """
        Verifica se o resultado da análise é válido.
        
        Returns:
            True se o resultado é válido para uso
        """
        if not self.column_data:
            return False
        
        # Deve ter pelo menos dados para colunas obrigatórias
        required_columns = {"Link", "Atende ao Filtro?"}
        available_columns = set(self.column_data.keys())
        
        # Se há colunas obrigatórias, elas devem estar presentes
        if required_columns and not required_columns.issubset(available_columns):
            return False
        
        # Confiança muito baixa pode indicar problemas
        if self.confidence_score < 0.1:
            return False
        
        return True
    
    def get_column_value(self, column_name: str) -> Optional[str]:
        """
        Obtém valor de uma coluna específica.
        
        Args:
            column_name: Nome da coluna
            
        Returns:
            Valor da coluna ou None se não encontrada
        """
        return self.column_data.get(column_name)
    
    def get_boolean_value(self, column_name: str) -> Optional[bool]:
        """
        Obtém valor boolean de uma coluna.
        
        Args:
            column_name: Nome da coluna
            
        Returns:
            True/False baseado no valor da coluna
        """
        value = self.get_column_value(column_name)
        if not value:
            return None
        
        value_lower = value.lower().strip()
        
        if value_lower in ["sim", "yes", "true", "1", "verdadeiro"]:
            return True
        elif value_lower in ["não", "nao", "no", "false", "0", "falso"]:
            return False
        
        return None
    
    def get_formatted_value(self, column_name: str, column_type: str) -> str:
        """
        Obtém valor formatado para uma coluna específica.
        
        Args:
            column_name: Nome da coluna
            column_type: Tipo da coluna (text ou boolean)
            
        Returns:
            Valor formatado para exibição
        """
        value = self.get_column_value(column_name)
        
        if not value:
            return ""
        
        if column_type == "boolean":
            bool_value = self.get_boolean_value(column_name)
            if bool_value is True:
                return "Sim"
            elif bool_value is False:
                return "Não"
            else:
                return "Não definido"
        
        # Para colunas de texto, retorna valor limpo
        return str(value).strip()
    
    def get_filter_result_display(self) -> str:
        """Retorna resultado do filtro formatado para exibição."""
        return "Sim" if self.meets_filter else "Não"
    
    def has_error(self) -> bool:
        """Verifica se houve erro na análise."""
        return bool(self.error_message)
    
    def get_quality_indicators(self) -> Dict[str, Any]:
        """
        Retorna indicadores de qualidade da análise.
        
        Returns:
            Dicionário com métricas de qualidade
        """
        return {
            "confidence_score": self.confidence_score,
            "has_error": self.has_error(),
            "columns_analyzed": len(self.column_data),
            "has_justification": bool(self.justification),
            "processing_time": self.processing_time_seconds,
            "tokens_efficiency": (
                self.tokens_used / len(self.column_data) 
                if self.tokens_used and self.column_data 
                else None
            )
        }
    
    def validate_column_completeness(self, expected_columns: List[str]) -> List[str]:
        """
        Valida se todas as colunas esperadas foram preenchidas.
        
        Args:
            expected_columns: Lista de nomes de colunas esperadas
            
        Returns:
            Lista de colunas faltantes
        """
        available_columns = set(self.column_data.keys())
        expected_set = set(expected_columns)
        
        missing_columns = expected_set - available_columns
        return list(missing_columns)
    
    def to_dict(self) -> dict:
        """
        Converte resultado da análise para dicionário.
        
        Returns:
            Dicionário com dados do resultado
        """
        return {
            "column_data": self.column_data,
            "meets_filter": self.meets_filter,
            "filter_display": self.get_filter_result_display(),
            "confidence_score": self.confidence_score,
            "analysis_model": self.analysis_model,
            "analyzed_at": self.analyzed_at.isoformat() if self.analyzed_at else None,
            "tokens_used": self.tokens_used,
            "processing_time_seconds": self.processing_time_seconds,
            "has_error": self.has_error(),
            "error_message": self.error_message,
            "justification": self.justification,
            "quality_indicators": self.get_quality_indicators()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "AnalysisResult":
        """
        Cria AnalysisResult a partir de dicionário.
        
        Args:
            data: Dicionário com dados do resultado
            
        Returns:
            Instância de AnalysisResult
        """
        analyzed_at = None
        if data.get("analyzed_at"):
            analyzed_at = datetime.fromisoformat(data["analyzed_at"])
        
        return cls(
            column_data=data["column_data"],
            meets_filter=data["meets_filter"],
            confidence_score=data.get("confidence_score", 1.0),
            analysis_model=data.get("analysis_model", "gemini-2.0-flash-exp"),
            analyzed_at=analyzed_at,
            tokens_used=data.get("tokens_used"),
            processing_time_seconds=data.get("processing_time_seconds"),
            error_message=data.get("error_message"),
            justification=data.get("justification")
        )
    
    @classmethod
    def create_failed(cls, error_message: str) -> "AnalysisResult":
        """
        Cria resultado para análise que falhou.
        
        Args:
            error_message: Mensagem descrevendo o erro
            
        Returns:
            Instância de AnalysisResult com erro
        """
        return cls(
            column_data={},
            meets_filter=False,
            confidence_score=0.0,
            error_message=error_message
        )
    
    @classmethod
    def create_successful(
        cls,
        column_data: Dict[str, str],
        meets_filter: bool,
        confidence: float = 1.0,
        justification: str = ""
    ) -> "AnalysisResult":
        """
        Cria resultado para análise bem-sucedida.
        
        Args:
            column_data: Dados das colunas analisadas
            meets_filter: Se atende ao filtro
            confidence: Confiança na análise
            justification: Justificativa da decisão
            
        Returns:
            Instância de AnalysisResult bem-sucedida
        """
        return cls(
            column_data=column_data,
            meets_filter=meets_filter,
            confidence_score=confidence,
            justification=justification
        )