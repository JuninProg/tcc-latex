"""
Value Object PDFContent - Representa o conteúdo extraído de um PDF.

Este value object encapsula o texto extraído de um PDF de artigo científico,
incluindo metadados sobre o processo de extração.
"""

from typing import Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class ExtractionMethod(Enum):
    """Métodos de extração de texto de PDF."""
    PYPDF2 = "pypdf2"
    PDFPLUMBER = "pdfplumber"
    OCR = "ocr"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class PDFContent:
    """
    Value object que representa conteúdo extraído de um PDF.
    
    Attributes:
        full_text: Texto completo extraído do PDF
        page_count: Número de páginas do PDF
        extraction_method: Método usado para extrair o texto
        extraction_confidence: Confiança na qualidade da extração (0.0-1.0)
        extracted_at: Timestamp da extração
        file_size_bytes: Tamanho do arquivo PDF em bytes
        language_detected: Idioma detectado no texto (opcional)
        has_images: Indica se o PDF contém imagens
        error_message: Mensagem de erro se extração parcial
    """
    
    full_text: str
    page_count: int
    extraction_method: ExtractionMethod
    extraction_confidence: float = 1.0
    extracted_at: Optional[datetime] = None
    file_size_bytes: Optional[int] = None
    language_detected: Optional[str] = None
    has_images: bool = False
    error_message: Optional[str] = None
    
    def __post_init__(self) -> None:
        """Inicializa timestamp se não fornecido."""
        if self.extracted_at is None:
            object.__setattr__(self, 'extracted_at', datetime.now())
    
    @property
    def text(self) -> str:
        """Compatibilidade: retorna full_text."""
        return self.full_text
    
    def is_valid(self) -> bool:
        """
        Verifica se o conteúdo extraído é válido.
        
        Returns:
            True se o conteúdo é válido para uso
        """
        if not self.full_text or not self.full_text.strip():
            return False
        
        # Texto muito curto pode indicar falha na extração
        if len(self.full_text.strip()) < 100:
            return False
        
        # Confiança muito baixa pode indicar problemas
        if self.extraction_confidence < 0.3:
            return False
        
        return True
    
    def get_text_length(self) -> int:
        """Retorna tamanho do texto extraído."""
        return len(self.full_text) if self.full_text else 0
    
    def get_word_count(self) -> int:
        """Estima número de palavras no texto."""
        if not self.full_text:
            return 0
        
        # Estimativa simples baseada em espaços
        return len(self.full_text.split())
    
    def get_text_preview(self, max_chars: int = 200) -> str:
        """
        Retorna preview do texto extraído.
        
        Args:
            max_chars: Número máximo de caracteres no preview
            
        Returns:
            Preview do texto com "..." se truncado
        """
        if not self.full_text:
            return ""
        
        if len(self.full_text) <= max_chars:
            return self.full_text
        
        return self.full_text[:max_chars-3] + "..."
    
    def get_clean_text(self) -> str:
        """
        Retorna texto limpo para análise.
        
        Remove caracteres especiais, múltiplos espaços, etc.
        
        Returns:
            Texto limpo e normalizado
        """
        if not self.full_text:
            return ""
        
        # Remove quebras de linha excessivas
        text = " ".join(self.full_text.split())
        
        # Remove caracteres de controle
        text = "".join(char for char in text if ord(char) >= 32)
        
        return text.strip()
    
    def extract_abstract_section(self) -> Optional[str]:
        """
        Tenta extrair seção de abstract/resumo do texto.
        
        Returns:
            Texto do abstract se encontrado, None caso contrário
        """
        if not self.full_text:
            return None
        
        text_lower = self.full_text.lower()
        
        # Palavras-chave para identificar abstract
        abstract_keywords = [
            "abstract", "resumo", "resumen", "résumé",
            "summary", "overview"
        ]
        
        for keyword in abstract_keywords:
            start_idx = text_lower.find(keyword)
            if start_idx != -1:
                # Busca até próxima seção ou fim do texto
                search_start = start_idx + len(keyword)
                
                # Procura por indicadores de fim de abstract
                end_keywords = [
                    "introduction", "introdução", "1.", "keywords",
                    "palavras-chave", "1 introduction"
                ]
                
                end_idx = len(self.full_text)
                for end_keyword in end_keywords:
                    found_end = text_lower.find(end_keyword, search_start)
                    if found_end != -1 and found_end < end_idx:
                        end_idx = found_end
                
                # Extrai possível abstract
                possible_abstract = self.full_text[search_start:end_idx].strip()
                
                # Valida se parece um abstract (tamanho razoável)
                if 50 <= len(possible_abstract) <= 2000:
                    return possible_abstract
        
        return None
    
    def get_quality_score(self) -> float:
        """
        Calcula score de qualidade da extração.
        
        Returns:
            Score de 0.0 a 1.0 indicando qualidade
        """
        if not self.is_valid():
            return 0.0
        
        score = self.extraction_confidence
        
        # Penaliza textos muito curtos
        if self.get_text_length() < 500:
            score *= 0.7
        
        # Bonifica extrações não-OCR
        if self.extraction_method != ExtractionMethod.OCR:
            score *= 1.1
        
        # Bonifica se não há mensagem de erro
        if not self.error_message:
            score *= 1.05
        
        return min(score, 1.0)
    
    def to_dict(self) -> dict:
        """
        Converte conteúdo PDF para dicionário.
        
        Returns:
            Dicionário com dados do conteúdo
        """
        return {
            "text_length": self.get_text_length(),
            "word_count": self.get_word_count(),
            "page_count": self.page_count,
            "extraction_method": self.extraction_method.value,
            "extraction_confidence": self.extraction_confidence,
            "quality_score": self.get_quality_score(),
            "extracted_at": self.extracted_at.isoformat() if self.extracted_at else None,
            "file_size_bytes": self.file_size_bytes,
            "language_detected": self.language_detected,
            "has_images": self.has_images,
            "has_error": bool(self.error_message),
            "error_message": self.error_message,
            "text_preview": self.get_text_preview(100)
        }
    
    @classmethod
    def create_failed(cls, error_message: str) -> "PDFContent":
        """
        Cria instância para PDF que falhou na extração.
        
        Args:
            error_message: Mensagem descrevendo o erro
            
        Returns:
            Instância de PDFContent com erro
        """
        return cls(
            full_text="",
            page_count=0,
            extraction_method=ExtractionMethod.UNKNOWN,
            extraction_confidence=0.0,
            error_message=error_message
        )
    
    @classmethod
    def create_successful(
        cls, 
        text: str, 
        method: ExtractionMethod,
        page_count: int = 1,
        confidence: float = 1.0
    ) -> "PDFContent":
        """
        Cria instância para extração bem-sucedida.
        
        Args:
            text: Texto extraído
            method: Método de extração usado
            page_count: Número de páginas
            confidence: Confiança na extração
            
        Returns:
            Instância de PDFContent bem-sucedida
        """
        return cls(
            full_text=text,
            page_count=page_count,
            extraction_method=method,
            extraction_confidence=confidence
        )