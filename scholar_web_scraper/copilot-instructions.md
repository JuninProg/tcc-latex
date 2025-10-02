# Scholar Web Scraper - Copilot Instructions

## Contexto do Projeto

Este é um **web scraper inteligente para artigos científicos** do Google Scholar que utiliza IA (Gemini) para análise e filtragem de conteúdo. O projeto faz parte de um TCC sobre desenvolvimento de aplicações web.

### Objetivo Principal
Criar uma aplicação web que permita buscar artigos no Google Scholar, extrair seu conteúdo (incluindo PDFs), analisar via IA com critérios personalizáveis, e gerar planilhas Excel com os resultados filtrados.

## Arquitetura do Sistema

### Framework Principal: Reflex.dev
- **Reflex.dev**: Framework Python full-stack que substitui Django + frontend tradicional
- **Estado reativo**: Mudanças no estado Python atualizam automaticamente a UI
- **Componentes**: Funções Python que retornam elementos de interface
- **Event Handlers**: Funções que respondem a interações do usuário

### Arquitetura Hexagonal (Ports & Adapters)
```
UI Layer (Reflex) → Application Layer → Domain Layer → Infrastructure Layer
```

- **Domain**: Lógica de negócio pura, sem dependências externas
- **Application**: Orquestração de casos de uso
- **Infrastructure**: Adaptadores para serviços externos (Google Scholar, Gemini, etc.)
- **UI**: Interface Reflex com estados e componentes

## Estrutura de Pastas Detalhada

### `/scholar_scraper/` - Aplicação Reflex
- **app.py**: Setup principal do Reflex (~50 linhas)
- **pages.py**: Página única da aplicação (~100 linhas)
- **states/**: Estados da aplicação (formulário, job, download)
- **components/**: Componentes UI reutilizáveis

### `/domain/` - Lógica de Negócio
- **entities/**: Entidades principais (Article, SearchQuery, etc.)
- **value_objects/**: Objetos de valor (metadados, conteúdo PDF, etc.)
- **services/**: Serviços de domínio (orquestração)
- **interfaces/**: Contratos/portas para adaptadores

### `/infrastructure/` - Adaptadores Externos
- **web_scraping/**: Google Scholar scraping com Selenium
- **pdf_processing/**: Download e extração de texto de PDFs
- **ai_services/**: Integração com Gemini API + mock
- **excel_generation/**: Geração de planilhas
- **celery_tasks/**: Processamento assíncrono

### `/tests/` - Testes
- **test_e2e.py**: Teste principal end-to-end
- **mock_server.py**: Servidor mock para Gemini API
- **fixtures/**: Dados de teste
- **utils/**: Helpers para testes

## Padrões de Código

### 1. Arquivos Pequenos (≤150 linhas)
```python
# ✅ Correto: Arquivo focado em uma responsabilidade
class ArticleMetadata:
    def __init__(self, title: str, authors: List[str]):
        self.title = title
        self.authors = authors
    
    def is_valid(self) -> bool:
        return bool(self.title and self.authors)

# ❌ Evitar: Arquivo com múltiplas responsabilidades
```

### 2. Type Hints Obrigatórios
```python
# ✅ Sempre usar type hints
def extract_pdf_text(pdf_content: bytes) -> Optional[str]:
    return processed_text

# ❌ Evitar funções sem tipos
def extract_pdf_text(pdf_content):
    return processed_text
```

### 3. Padrão de Interfaces
```python
# domain/interfaces/scholar_repository.py
from abc import ABC, abstractmethod
from typing import List
from domain.entities.article import Article

class ScholarRepository(ABC):
    @abstractmethod
    async def search_articles(self, query: str) -> List[Article]:
        pass
```

### 4. Dependency Injection
```python
# ✅ Injeção de dependência
class SearchOrchestrator:
    def __init__(self, 
                 scholar_repo: ScholarRepository,
                 ai_service: AIService):
        self._scholar_repo = scholar_repo
        self._ai_service = ai_service
```

### 5. Error Handling Robusto
```python
# ✅ Tratamento de erro específico
try:
    articles = await self._scholar_repo.search_articles(query)
except ScholarTimeoutError as e:
    logger.warning(f"Scholar timeout: {e}")
    raise SearchError("Timeout na busca do Scholar")
except Exception as e:
    logger.error(f"Erro inesperado: {e}")
    raise SearchError("Erro interno na busca")
```

## Convenções de Desenvolvimento

### Naming Conventions
- **Classes**: PascalCase (`ArticleExtractor`)
- **Funções/métodos**: snake_case (`extract_article_data`)
- **Constantes**: UPPER_SNAKE_CASE (`MAX_RETRY_ATTEMPTS`)
- **Variáveis**: snake_case (`pdf_content`)

### Imports Organization
```python
# Standard library
import asyncio
from typing import Optional, List

# Third party
import reflex as rx
from selenium import webdriver

# Local imports
from domain.entities.article import Article
from infrastructure.web_scraping.rate_limiter import RateLimiter
```

### Logging Padrão
```python
import logging

logger = logging.getLogger(__name__)

def process_article(self, article: Article) -> None:
    logger.info(f"Processando artigo: {article.title}")
    try:
        # processing logic
        logger.debug("Processamento concluído com sucesso")
    except Exception as e:
        logger.error(f"Erro no processamento: {e}")
        raise
```

## Fluxo de Dados Principal

### 1. Entrada do Usuário (Reflex UI)
```python
# states/form_state.py
class FormState(rx.State):
    query_text: str = ""
    filter_criteria: str = ""
    columns: List[dict] = []
    
    def submit_form(self):
        # Validações + início do job assíncrono
        pass
```

### 2. Processamento Assíncrono (Celery)
```python
# infrastructure/celery_tasks/search_task.py
@celery.task
def process_scholar_search(query: str, filters: str, columns: List[dict]):
    # 1. Busca no Google Scholar
    # 2. Extração de PDFs
    # 3. Análise via Gemini
    # 4. Geração de Excel
    pass
```

### 3. Pipeline de Web Scraping
```
Google Scholar → Resultados → Links → PDFs → Texto → Análise IA → Excel
```

## Regras Específicas por Módulo

### Web Scraping (Selenium)
- **Sempre usar rate limiting** entre requests
- **Randomizar delays** para evitar detecção
- **Tratar CAPTCHAs** com retry logic
- **User-Agent rotation** para robustez

```python
# ✅ Correto
await self._rate_limiter.wait()
driver.get(url)
await asyncio.sleep(random.uniform(2, 5))
```

### PDF Processing
- **Download em memória** (BytesIO), nunca salvar localmente
- **Múltiplas estratégias** de extração (PyPDF2 → pdfplumber → OCR)
- **Limpeza de texto** para remover caracteres desnecessários

```python
# ✅ Download em memória
pdf_bytes = BytesIO(response.content)
text = self._extract_text_strategies(pdf_bytes)
```

### Gemini AI Service
- **Prompts dinâmicos** baseados nas colunas configuradas
- **Fallback strategy**: PDF completo → abstract → snippet
- **Rate limiting** respeitando limites da API
- **Response parsing** robusto com validação

### Reflex Components
- **Componentes pequenos** e focados
- **Estados centralizados** nos arquivos de state
- **Validações client-side** sempre que possível
- **Feedback visual** para todas as ações

## Mock Strategy para Testes

### Gemini Mock Service
```python
# infrastructure/ai_services/gemini_mock.py
class GeminiMockService:
    def analyze_article(self, content: str, columns: List[ColumnConfig]) -> Dict:
        # Retorna dados determinísticos baseados em keywords
        # Simula tempo de processamento realista
        # Nunca consome créditos da API real
        pass
```

### Teste E2E Principal
1. **Setup**: Inicia mock server + aplicação
2. **Input**: Simula preenchimento do formulário
3. **Processing**: Monitora progresso do job
4. **Output**: Valida arquivo Excel gerado
5. **Cleanup**: Remove arquivos temporários

## Comandos de Desenvolvimento

### Setup Local
```bash
cd scholar_web_scraper/
python -m venv venv
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
cp .env.example .env
# Editar .env com suas API keys
docker-compose up -d  # Redis
reflex run  # Aplicação
```

### Testes
```bash
pytest tests/test_e2e.py -v  # Teste principal
pytest tests/ -v  # Todos os testes
```

### Celery (desenvolvimento)
```bash
celery -A infrastructure.celery_tasks.celery_config worker --loglevel=info
```

## Considerações de Performance

### Rate Limiting
- **Google Scholar**: 2-5 segundos entre requests
- **Gemini API**: Respeitar limites da API
- **PDF Downloads**: Máximo 3 simultâneos

### Cleanup Automático
- **Arquivos temporários**: Remoção após 24h
- **Logs antigos**: Rotação automática
- **Cache de resultados**: TTL configurável

## Debugging e Logs

### Níveis de Log
- **DEBUG**: Detalhes de execução, dados intermediários
- **INFO**: Fluxo principal, início/fim de operações
- **WARNING**: Problemas não críticos, fallbacks
- **ERROR**: Erros que impedem funcionamento
- **CRITICAL**: Falhas do sistema

### Exemplo de Log Estruturado
```python
logger.info(
    "Iniciando busca no Scholar",
    extra={
        "query": query,
        "max_results": max_results,
        "job_id": job_id
    }
)
```

---

## 🎯 Diretrizes para Desenvolvimento

1. **Sempre começar pelo domínio** (entidades, value objects)
2. **Testes primeiro** para funcionalidades críticas
3. **Refatorar quando arquivo > 150 linhas**
4. **Documentar decisões arquiteturais** importantes
5. **Priorizar robustez** sobre velocidade inicial
6. **Usar type hints** em 100% do código
7. **Logging detalhado** para debugging
8. **Rate limiting** sempre presente em web scraping

Essas instruções devem guiar todo o desenvolvimento do projeto, mantendo consistência e qualidade do código.