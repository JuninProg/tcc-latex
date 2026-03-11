# Checklist de Conformidade ABNT NBR 14724:2011

## TCC: Migração Tecnológica do Pró-Mamá
**Instituição:** IFRS - Campus Osório  
**Curso:** Análise e Desenvolvimento de Sistemas  
**Aluno:** [Seu nome]  
**Data de verificação:** [Data]

---

## 1. ESTRUTURA GERAL

### Elementos Pré-Textuais
- [ ] Capa (com título, autor, ano, instituição, campus)
- [ ] Verso da capa (com dados de catalogação — gerado por IFRS)
- [ ] Folha de aprovação (assinada por banca)
- [ ] Dedicatória (opcional)
- [ ] Agradecimentos (se houver)
- [ ] Epígrafe (opcional)
- [ ] Resumo em português (100-250 palavras)
- [ ] Abstract em inglês (100-250 palavras)
- [ ] Resumen em espanhol (opcional, se trilíngue)
- [ ] Lista de abreviaturas e siglas (com definições)
- [ ] Lista de símbolos (se houver)
- [ ] Sumário/Índice (gerado automaticamente)

### Elementos Textuais
- [ ] Introdução (com objetivos e justificativa)
- [ ] Capítulos numerados (1, 2, 3, ...)
- [ ] Cada capítulo com seções (1.1, 1.2, 2.1, ...)
- [ ] Desenvolvimento estruturado
- [ ] Conclusão

### Elementos Pós-Textuais
- [ ] Referências (alfabéticas, completas)
- [ ] Apêndices (se houver) — produzidos pelo autor
- [ ] Anexos (se houver) — documentos não proprietários

---

## 2. FORMATAÇÃO

### Fonte e Espaçamento
- [ ] Fonte: Times New Roman ou Helvetica 12pt
- [ ] Espaçamento: 1,5 entre linhas (corpo do texto)
- [ ] Espaçamento simples em:
  - [ ] Citações de bloco (>3 linhas)
  - [ ] Rodapés
  - [ ] Referências
  - [ ] Legendas de figuras/tabelas
- [ ] Parágrafos: 1,25 cm na primeira linha (recuo)

### Margens
- [ ] Esquerda: 3 cm
- [ ] Direita: 2 cm
- [ ] Superior: 2 cm
- [ ] Inferior: 2 cm

### Página
- [ ] Numeração: início em p. 3 ou 4 (após pré-textuais)
- [ ] Posição: canto superior direito
- [ ] Alinhamento: todos os textos justificados (exceto títulos centralizados)

---

## 3. TÍTULOS E SEÇÕES

### Capítulos
- [ ] TÍTULO DO CAPÍTULO (MAIÚSCULAS, centralizado, sem numeração se Introdução)
- [ ] Ou: 1 TÍTULO DO CAPÍTULO (MAIÚSCULAS, se numerado)
- [ ] Sem ponto final em títulos
- [ ] Espaço de uma linha antes e depois do título

### Seções Primárias
- [ ] 1.1 Título de Seção (Maiúsculas na primeira palavra e nomes próprios)
- [ ] Sem ponto final

### Seções Secundárias
- [ ] 1.1.1 Título (Idem)

### Profundidade Máxima
- [ ] Máximo 3 níveis: 1 / 1.1 / 1.1.1
- [ ] Não aprofundar além (usar listas com bullets se necessário)

---

## 4. CITAÇÕES

### Formato
- [ ] Indiretas (parafrasear): (Sobrenome, Ano) ou \cite{Sobrenome_Ano}
- [ ] Diretas curtas (<40 palavras): "...texto..." \cite{Sobrenome_Ano}
- [ ] Diretas longas (≥40 palavras): bloco recuado, simples espaçamento, sem aspas
- [ ] Com página: \cite[p.~10]{Sobrenome_Ano} ou (Sobrenome, 2020, p. 10)

### Pluralidade
- [ ] Dois autores: Silva e Costa (2020)
- [ ] Três ou mais: Silva et al. (2020)
- [ ] Mesma citação, multiplos autores: (Silva, 2020; Costa, 2020)

### Sequência
- [ ] Sem citação orfã (parágrafo acadêmico tem pelo menos 1)
- [ ] Todas as citações têm entrada em `referencias.bib`
- [ ] Nenhuma referência órfã (listada mas não usada no texto)

---

## 5. FIGURAS

### Numeração
- [ ] Figuras numeradas sequencialmente: Figura 1, Figura 2, ...
- [ ] Separação por capítulo (opcional): Figura 1.1, Figura 1.2, Figura 2.1

### Estrutura
- [ ] Legenda ACIMA da imagem
- [ ] Legenda em tamanho reduzido (10pt)
- [ ] Fonte obrigatória ABAIXO da figura
- [ ] Referência no texto ANTES da figura

### Exemplo Correto
```
A arquitetura geral do sistema é apresentada na Figura 1.

Figura 1 — Arquitetura em camadas do Pró-Mamá
[IMAGEM AQUI]
Fonte: Elaborado pelo autor

Conforme observa-se...
```

### Qualidade
- [ ] Imagens legíveis em impressão (mínimo 300 dpi)
- [ ] Sem distorções ou deformações
- [ ] Cor apenas se necessário (considerar impressão B&W)

---

## 6. TABELAS

### Numeração
- [ ] Tabelas numeradas sequencialmente: Tabela 1, Tabela 2, ...
- [ ] Separação por capítulo (opcional): Tabela 1.1, etc.

### Estrutura
- [ ] Título ABAIXO da tabela (ÚNICO elemento que diferencia de figura)
- [ ] Título em tamanho reduzido (10pt)
- [ ] Fonte obrigatória ABAIXO do título
- [ ] Referência no texto ANTES da tabela
- [ ] Bordas/linhas necessárias para clareza

### Exemplo Correto
```
Conforme apresentado na Tabela 1:

Tabela 1 — Comparação entre tecnologias
[TABELA AQUI]
Fonte: [Elaborado pelo autor / Referência específica]

Observa-se que...
```

---

## 7. REFERÊNCIAS

### Ordem
- [ ] Alfabética por sobrenome do autor
- [ ] Segunda linha com recuo (hanging indent)

### Elementos Obrigatórios
- [ ] Autor(es) [SOBRENOME, Iniciais.]
- [ ] Ano de publicação [YYYY]
- [ ] Título [exato como publicado]
- [ ] Editora ou fonte
- [ ] Edição [se não for 1ª]
- [ ] Data de acesso [para URL]

### Formatos por Tipo

#### Livro
```
SOBRENOME, Iniciais. Título do livro. Editora, Ano.
```

#### Capítulo de Livro
```
SOBRENOME, Iniciais. Título do capítulo. In: ORGANIZADOR, Iniciais. Título do livro. Editora, Ano. p. XX-YY.
```

#### Artigo em Periódico
```
SOBRENOME, Iniciais. Título do artigo. Título da Revista, v. X, n. X, p. XX-YY, mês Ano.
```

#### Tese/Dissertação
```
SOBRENOME, Iniciais. Título da tese. Tipo (Mestrado/Doutorado em Área), Instituição, Ano.
```

#### URL
```
SOBRENOME, Iniciais. Título da página. Disponível em: <http://...>. Acesso em: DD mês Ano.
```

### Validação
- [ ] Todas as citações no texto estão nas referências
- [ ] Todas as referências foram citadas no texto (nenhuma órfã)
- [ ] Formatação consistente entre entradas
- [ ] Maiúsculas corretas (títulos de livros, não artigos)

---

## 8. ABREVIATURAS E SIGLAS

- [ ] Primeira menção: termo completo seguido de sigla [SIGLA]
- [ ] Menções subsequentes: apenas SIGLA
- [ ] Exemplo: "Lei Geral de Proteção de Dados [LGPD]. A LGPD estabelece..."
- [ ] Lista de abreviaturas: ordem alfabética com definições
- [ ] IFRS, HTTP, API, LGPD, etc.: não precisam ser interrupidas

---

## 9. ESTRUTURA POR CAPÍTULO

### Introdução
- [ ] Contextualização histórica
- [ ] Delimitação do problema
- [ ] Objetivo geral (1 objetivo)
- [ ] Objetivos específicos (3-5 objetivos com verbos no infinitivo)
- [ ] Justificativa (relevância teórica, prática, social)
- [ ] Organização do trabalho (breve descrição dos capítulos)

### Capítulo de Fundamentação/Referencial Teórico
- [ ] Mínimo 3-5 conceitos principais
- [ ] Cada conceito: 1-2 páginas
- [ ] Estrutura por conceito: Definição → Contexto → Aplicação no TCC
- [ ] Cada conceito com mínimo 3-5 citações

### Capítulo de Trabalhos Relacionados
- [ ] Análise de N trabalhos académicos (≥5)
- [ ] Não é mera descrição; é análise crítica
- [ ] Tabela comparativa
- [ ] Síntese das lacunas identificadas
- [ ] Como o TCC diferencia-se

### Capítulo de Metodologia
- [ ] Tipo de pesquisa
- [ ] Abordagem (qualitativa, quantitativa, mista)
- [ ] Métodos de coleta de dados
- [ ] Instrumentos (questionários, análise documental, etc.)
- [ ] Población/amostra
- [ ] Cronograma
- [ ] Decisões técnicas (se aplicável)

### Capítulo(s) de Desenvolvimento
- [ ] Estruturado em tópicos temáticos
- [ ] Cada tópico: Problema → Solução → Justificativa → Resultados
- [ ] Tabelas para requisitos, arquitetura, configurações
- [ ] Diagramas para arquitetura, fluxos
- [ ] Métricas quando aplicável

### Conclusão
- [ ] Retoma cada objetivo específico (demonstra se foi atingido)
- [ ] Síntese dos resultados principais
- [ ] Contribuições técnicas/acadêmicas
- [ ] Limitações encontradas
- [ ] Sugestões para pesquisas futuras

---

## 10. VALIDAÇÃO FINAL

### Antes de Submeter
- [ ] Arquivo PDF gerado sem erros
- [ ] Sumário/Índice sincronizado
- [ ] Todas as referências cruzadas funcionam
- [ ] Numeração de páginas contínua
- [ ] Figuras/tabelas legíveis
- [ ] Nenhuma "linha órfã" (última linha de parágrafo sozinha)

### Review Lingüístico
- [ ] Sem erros de digitação (use spell-check)
- [ ] Sem inconsistências de termo (ex: "aplicativo" vs. "app")
- [ ] Parágrafos com variação de tamanho
- [ ] Sem frases muito longas (max 25-30 palavras)

### Review Técnico
- [ ] Coesão entre capítulos (sem contradições)
- [ ] Objetivos específicos cobertos no desenvolvimento
- [ ] Conclusão retoma evidências do desenvolvimento
- [ ] Sem conceitos "flutuantes" (todos têm conexão)

---

## Score de Conformidade ABNT

| Categoria | Perto | % Compl. | Status |
|-----------|-------|----------|--------|
| Estrutura geral | [ ] [ ] [ ] | __% | ☐ OK |
| Formatação | [ ] [ ] [ ] | __% | ☐ OK |
| Citações | [ ] [ ] [ ] | __% | ☐ OK |
| Referências | [ ] [ ] [ ] | __% | ☐ OK |
| Figuras/Tabelas | [ ] [ ] [ ] | __% | ☐ OK |
| Seções/Capítulos | [ ] [ ] [ ] | __% | ☐ OK |
| **TOTAL** | | **__% ** | ☐ **PRONTO** |

**Critério de Aceitação:** ≥ 95% de conformidade

---

**Notas finais:**
- Este checklist é iterativo; use-o em cada revisão
- Se tiver dúvidas sobre um item, consulte os agentes `tcc-writer` ou `abnt-reviewer`
- Mantenha backup do arquivo `.tex` antes de grandes edições
