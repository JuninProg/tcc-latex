# Scholar Web Scraper

Um web scraper inteligente para artigos científicos do Google Scholar com análise via IA (Gemini) e geração de planilhas personalizáveis.

## 🎯 Funcionalidades

- 🔍 **Busca automatizada** no Google Scholar
- 📄 **Extração de PDFs** em memória (sem armazenamento local)
- 🤖 **Análise via IA** com critérios personalizáveis
- 📊 **Planilhas dinâmicas** com colunas configuráveis
- ⚡ **Processamento assíncrono** com feedback em tempo real
- 🎨 **Interface web moderna** com Reflex.dev

## 🏗️ Arquitetura

- **Frontend**: Reflex.dev (Python full-stack)
- **Backend**: Arquitetura hexagonal
- **Processamento**: Celery + Redis
- **Web Scraping**: Selenium + BeautifulSoup
- **IA**: Google Gemini API
- **Dados**: Pandas + OpenPyXL

## 🚀 Setup Local

### Pré-requisitos
- Python 3.9+
- Docker e Docker Compose
- Chrome/Chromium (para Selenium)

### Instalação

1. **Clone e navegue para o projeto**:
```bash
cd scholar_web_scraper/
```

2. **Crie e ative o ambiente virtual**:
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# ou
.\venv\Scripts\activate  # Windows
```

3. **Instale as dependências**:
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente**:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

5. **Inicie os serviços Docker**:
```bash
docker-compose up -d
```

6. **Execute a aplicação**:
```bash
reflex run
```

A aplicação estará disponível em: http://localhost:3000

## ⚙️ Configuração

### Variáveis de Ambiente (.env)

```env
# Gemini AI Configuration
GEMINI_API_KEY=your-gemini-api-key-here
GEMINI_MODEL=gemini-2.0-flash-exp

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# Selenium Configuration
SELENIUM_HEADLESS=True
SELENIUM_TIMEOUT=30
```

### Google Gemini API Key

1. Acesse [Google AI Studio](https://aistudio.google.com/)
2. Crie uma nova API key
3. Adicione a chave no arquivo `.env`

## 📖 Como Usar

1. **Acesse a aplicação** em http://localhost:3000
2. **Preencha o formulário**:
   - Texto de pesquisa (ex: "aplicativo aleitamento materno")
   - Filtro de relevância (ex: "artigos com implementação real")
   - Configure as colunas desejadas
3. **Clique em "Processar"** e aguarde
4. **Baixe a planilha** quando o processamento terminar

### Exemplo de Colunas

- Título (texto)
- Tem aplicativo? (sim/não)
- Tem painel/gestão? (sim/não)
- Tecnologias (texto)
- Data de publicação (texto)
- Autores (texto)
- Link (sempre presente)
- Atende ao filtro? (sempre presente)

## 🧪 Testes

### Teste E2E Principal
```bash
pytest tests/test_e2e.py -v
```

### Todos os testes
```bash
pytest tests/ -v
```

### Executar com mock da IA
```bash
# O teste E2E automaticamente usa o mock service
# para não consumir créditos da API Gemini
pytest tests/test_e2e.py::test_complete_pipeline
```

## 🔧 Desenvolvimento

### Estrutura do Projeto
```
scholar_web_scraper/
├── scholar_scraper/          # App Reflex
├── domain/                   # Lógica de negócio
├── infrastructure/           # Adaptadores externos
└── tests/                    # Testes
```

### Executar Celery Worker (desenvolvimento)
```bash
celery -A infrastructure.celery_tasks.celery_config worker --loglevel=info
```

### Monitoring Redis
```bash
docker-compose exec redis redis-cli monitor
```

### Logs
```bash
tail -f scholar_scraper.log
```

## 📋 Pipeline de Processamento

1. **Busca no Google Scholar** → Extrai lista de artigos
2. **Navegação individual** → Acessa página de cada artigo
3. **Download de PDFs** → Baixa conteúdo em memória
4. **Extração de texto** → PyPDF2 → pdfplumber → OCR
5. **Análise via IA** → Gemini processa com prompts dinâmicos
6. **Geração de planilha** → Excel com colunas personalizadas

## 🚧 Status do Projeto

- [x] Estrutura base criada
- [x] Configuração Docker
- [x] Documentação Copilot
- [ ] Entidades de domínio
- [ ] Estados Reflex
- [ ] Componentes UI
- [ ] Web scraping Google Scholar
- [ ] Processamento de PDFs
- [ ] Integração Gemini
- [ ] Geração de planilhas
- [ ] Teste E2E

## 📝 Contribuição

Este projeto segue as diretrizes do arquivo `copilot-instructions.md`. Antes de contribuir:

1. Leia as instruções completas no arquivo
2. Mantenha arquivos ≤150 linhas
3. Use type hints obrigatórios
4. Siga a arquitetura hexagonal
5. Teste sempre com o mock service

## 📄 Licença

Este projeto é parte de um TCC acadêmico.

---

Para mais detalhes de desenvolvimento, consulte o arquivo `copilot-instructions.md`.