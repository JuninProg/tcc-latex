# Scholar Web Scraper

Sistema inteligente de busca e análise de artigos científicos do Google Scholar com IA integrada.

## Funcionalidades

- 🔍 **Busca automatizada** no Google Scholar
- 🤖 **Análise por IA** usando Google Gemini
- 📊 **Geração de planilhas** Excel personalizadas
- ⚡ **Processamento assíncrono** com Celery + Redis
- 🎯 **Filtros inteligentes** baseados em critérios customizáveis
- 📄 **Extração de PDF** com múltiplas estratégias
- 🖥️ **Interface web** moderna com Reflex.dev

## Requisitos

- Python 3.9+
- Redis Server
- Google Chrome/Chromium (para Selenium)
- Google Gemini API Key

## Instalação

### 1. Clone o repositório

```bash
git clone <repository-url>
cd scholar_web_scraper
```

### 2. Instale dependências

```bash
pip install -r requirements.txt
```

### 3. Configure variáveis de ambiente

Copie o arquivo de exemplo e configure:

```bash
cp .env.example .env
```

Edite o arquivo `.env` e configure:

```env
GEMINI_API_KEY=sua_chave_gemini_aqui
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### 4. Inicie o Redis

**macOS (com Homebrew):**
```bash
brew install redis
brew services start redis
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server
```

**Docker:**
```bash
docker run -d -p 6379:6379 redis:alpine
```

## Execução

### 1. Inicie o Worker Celery

Em um terminal:

```bash
python run_worker.py
```

### 2. Inicie a aplicação web

Em outro terminal:

```bash
python -m scholar_scraper
```

A aplicação estará disponível em: `http://localhost:3000`

## Uso

1. **Configure a busca:**
   - Digite o texto de pesquisa (ex: "aplicativo aleitamento materno")
   - Defina critérios de filtro detalhados
   - Ajuste o número máximo de resultados (1-100)

2. **Execute o processamento:**
   - Clique em "Processar"
   - Acompanhe o progresso em tempo real
   - Aguarde a conclusão (pode levar alguns minutos)

3. **Baixe os resultados:**
   - Clique em "Baixar Planilha Excel"
   - A planilha contém artigos analisados e classificados pela IA

## Arquitetura

O projeto segue arquitetura hexagonal com separação clara de responsabilidades:

```
scholar_scraper/
├── domain/              # Entidades e objetos de valor
├── infrastructure/      # Implementações técnicas
├── states/             # Estados do Reflex
├── ui/                 # Componentes de interface
└── app.py              # Ponto de entrada
```

### Componentes principais:

- **GoogleScholarDriver**: Web scraping com Selenium
- **PDFProcessor**: Extração de texto de PDFs
- **GeminiClient**: Integração com IA do Google
- **ExcelGenerator**: Criação de planilhas formatadas
- **CeleryWorker**: Processamento assíncrono

## Desenvolvimento

### Estrutura do projeto

- **Arquitetura hexagonal** para baixo acoplamento
- **Máximo 150 linhas** por arquivo
- **Type hints** e documentação completa
- **Tratamento de erros** robusto

### Executar em modo desenvolvimento

```bash
# Com auto-reload
reflex run --env dev

# Worker com reload
watchdog -w scholar_scraper python run_worker.py
```

### Testes

```bash
# Executar testes
python -m pytest tests/

# Com cobertura
python -m pytest tests/ --cov=scholar_scraper
```

## Configuração Avançada

### Variáveis de ambiente disponíveis:

```env
# API Configuration
GEMINI_API_KEY=your_api_key

# Celery/Redis
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Scraping Configuration
SCHOLAR_MAX_CONCURRENT_REQUESTS=1
SCHOLAR_REQUEST_DELAY=2.0
SCHOLAR_PDF_TIMEOUT=30
SCHOLAR_MAX_PDF_PAGES=50

# Debug
SCHOLAR_DEBUG=false
SCHOLAR_LOG_LEVEL=INFO
```

### Personalizar colunas de análise

Edite `scholar_scraper/states/app_state.py` na função `submit_search()` para modificar as colunas padrão da análise.

## Solução de Problemas

### Redis não conecta
```bash
# Verificar se Redis está rodando
redis-cli ping
# Deve retornar: PONG
```

### ChromeDriver não encontrado
```bash
# Instalar via Homebrew (macOS)
brew install chromedriver

# Ou baixar manualmente de:
# https://chromedriver.chromium.org/
```

### Erro de API do Gemini
- Verifique se a chave da API está correta
- Confirme se você tem créditos disponíveis
- Teste a conexão com: `curl -H "Authorization: Bearer YOUR_KEY" https://generativelanguage.googleapis.com/v1/models`

### Worker Celery não processa
- Verifique se Redis está rodando
- Confirme se as variáveis de ambiente estão corretas
- Reinicie o worker: `Ctrl+C` e execute `python run_worker.py` novamente

## Limitações

- **Rate limiting**: Respeita limitações do Google Scholar
- **PDFs protegidos**: Alguns PDFs podem não ser extraídos
- **API Limits**: Sujeito aos limites da API do Gemini
- **Idioma**: Otimizado para artigos em português e inglês

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Faça commit das mudanças
4. Push para a branch
5. Abra um Pull Request

## Licença

Este projeto é parte de um TCC acadêmico. Consulte o orientador sobre uso e distribuição.

## Suporte

Para dúvidas e suporte:
- Abra uma issue no repositório
- Consulte a documentação técnica
- Entre em contato com o desenvolvedor