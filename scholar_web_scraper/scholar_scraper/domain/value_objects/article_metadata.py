"""
Value Object ArticleMetadata - Representa os metadados básicos de um artigo científico.

Este value object encapsula todas as informações básicas extraídas
diretamente do Google Scholar sobre um artigo.
"""

from typing import Optional, List
from dataclasses import dataclass


@dataclass(frozen=True)
class ArticleMetadata:
    """
    Value object que representa metadados de um artigo científico.
    
    Attributes:
        title: Título do artigo
        authors: Lista de autores
        year: Ano de publicação
        abstract: Resumo/abstract do artigo (quando disponível)
        snippet: Trecho/snippet do Google Scholar
        pdf_url: URL direta do PDF (quando disponível)
        doi: DOI do artigo (quando disponível)
        journal: Nome da revista/conference
        citations_count: Número de citações
        scholar_id: ID único no Google Scholar
    """
    
    title: Optional[str] = None
    authors: List[str] = None
    year: Optional[str] = None
    abstract: Optional[str] = None
    snippet: Optional[str] = None
    pdf_url: Optional[str] = None
    doi: Optional[str] = None
    journal: Optional[str] = None
    citations_count: Optional[int] = None
    scholar_id: Optional[str] = None
    
    def __post_init__(self) -> None:
        """Inicializa lista vazia de autores se None."""
        if self.authors is None:
            object.__setattr__(self, 'authors', [])
    
    def is_valid(self) -> bool:
        """
        Verifica se os metadados são válidos para processamento.
        
        Returns:
            True se os metadados têm informações mínimas necessárias
        """
        # Pelo menos título deve estar presente
        if not self.title or not self.title.strip():
            return False
        
        # Pelo menos uma fonte de conteúdo deve estar disponível
        has_content = any([
            self.abstract and self.abstract.strip(),
            self.snippet and self.snippet.strip(),
            self.pdf_url
        ])
        
        return has_content
    
    def get_display_title(self) -> str:
        """Retorna título formatado para exibição."""
        if not self.title:
            return "Título não disponível"
        
        # Limita tamanho do título se muito longo
        if len(self.title) > 100:
            return self.title[:97] + "..."
        
        return self.title
    
    def get_authors_string(self) -> str:
        """
        Retorna autores formatados como string.
        
        Returns:
            String com autores separados por vírgula
        """
        if not self.authors:
            return "Autores não informados"
        
        if len(self.authors) == 1:
            return self.authors[0]
        
        if len(self.authors) <= 3:
            return ", ".join(self.authors)
        
        # Se muitos autores, mostra os primeiros e "et al."
        return f"{', '.join(self.authors[:2])} et al."
    
    def get_year_display(self) -> str:
        """Retorna ano formatado para exibição."""
        if not self.year:
            return "Ano não disponível"
        
        # Remove caracteres extras que possam vir do Scholar
        year_clean = ''.join(filter(str.isdigit, self.year))
        
        if len(year_clean) == 4:
            return year_clean
        
        return self.year  # Retorna original se não conseguir limpar
    
    def has_pdf_available(self) -> bool:
        """Verifica se há URL de PDF disponível."""
        return bool(self.pdf_url and self.pdf_url.strip())
    
    def get_best_content_for_analysis(self) -> str:
        """
        Retorna o melhor conteúdo disponível para análise.
        
        Prioridade: Abstract > Snippet > Título
        
        Returns:
            Melhor conteúdo textual disponível
        """
        if self.abstract and self.abstract.strip():
            return self.abstract.strip()
        
        if self.snippet and self.snippet.strip():
            return self.snippet.strip()
        
        # Como última opção, retorna o título
        return self.title or ""
    
    def get_content_length(self) -> int:
        """Retorna tamanho do conteúdo disponível para análise."""
        content = self.get_best_content_for_analysis()
        return len(content)
    
    def has_sufficient_content(self, min_length: int = 50) -> bool:
        """
        Verifica se há conteúdo suficiente para análise.
        
        Args:
            min_length: Tamanho mínimo de conteúdo em caracteres
            
        Returns:
            True se há conteúdo suficiente
        """
        return self.get_content_length() >= min_length
    
    def is_likely_academic_paper(self) -> bool:
        """
        Verifica indicadores de que é um artigo acadêmico.
        
        Returns:
            True se parece ser um artigo acadêmico
        """
        if not self.title:
            return False
        
        # Indicadores positivos
        academic_indicators = [
            self.doi is not None,
            self.journal is not None,
            self.abstract is not None,
            len(self.authors) >= 1 if self.authors else False,
            self.citations_count is not None
        ]
        
        # Pelo menos 2 indicadores devem estar presentes
        return sum(academic_indicators) >= 2
    
    def to_dict(self) -> dict:
        """
        Converte metadados para dicionário.
        
        Returns:
            Dicionário com metadados
        """
        return {
            "title": self.title,
            "authors": self.authors,
            "year": self.year,
            "abstract": self.abstract,
            "snippet": self.snippet,
            "pdf_url": self.pdf_url,
            "doi": self.doi,
            "journal": self.journal,
            "citations_count": self.citations_count,
            "scholar_id": self.scholar_id,
            "has_pdf": self.has_pdf_available(),
            "content_length": self.get_content_length(),
            "is_academic": self.is_likely_academic_paper()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "ArticleMetadata":
        """
        Cria ArticleMetadata a partir de dicionário.
        
        Args:
            data: Dicionário com dados dos metadados
            
        Returns:
            Instância de ArticleMetadata
        """
        return cls(
            title=data.get("title"),
            authors=data.get("authors", []),
            year=data.get("year"),
            abstract=data.get("abstract"),
            snippet=data.get("snippet"),
            pdf_url=data.get("pdf_url"),
            doi=data.get("doi"),
            journal=data.get("journal"),
            citations_count=data.get("citations_count"),
            scholar_id=data.get("scholar_id")
        )
    
    @classmethod
    def create_minimal(cls, title: str, snippet: str = "") -> "ArticleMetadata":
        """
        Cria metadados mínimos para testes ou casos especiais.
        
        Args:
            title: Título do artigo
            snippet: Snippet opcional
            
        Returns:
            Instância de ArticleMetadata com dados mínimos
        """
        return cls(
            title=title,
            snippet=snippet,
            authors=[],
            year=None
        )