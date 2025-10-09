# Resumo e Análise Crítica – Artigo "Sistema AcGest para assistência à saúde de gestantes e puérperas na Atenção Primária" (trabrelated5.pdf)

## 1. Contexto e Introdução
### Principais pontos
- O estudo apresenta o desenvolvimento do **AcGest**, um sistema de apoio à atenção pré-natal e puerperal dentro da Atenção Primária à Saúde (APS), com foco na Estratégia Saúde da Família (ESF).
- Surge como resposta ao avanço da informatização do SUS (e-SUS AB) e à necessidade de melhorar a gestão de informações e o acompanhamento materno-infantil.
- Objetivo: criar um sistema integrado entre a rotina dos **Agentes Comunitários de Saúde (ACS)**, gestantes/puérperas e a gestão das Unidades Básicas de Saúde (UBS), facilitando a comunicação, registro e análise das informações.
- Potencial para melhorar indicadores de saúde, otimizar visitas domiciliares, identificar riscos e registrar intercorrências importantes.

### Pontos para análise crítica
- 💡 **Positivo:** Integra múltiplos atores (ACS, gestantes, gestores) num mesmo fluxo de dados.
- 💡 **Positivo:** Alinhamento com diretrizes nacionais e integração potencial com e-SUS AB.
- ⚠️ **Negativo:** Dependência de estrutura tecnológica (smartphones e conectividade) pode ser barreira em territórios mais vulneráveis.
- ⚠️ **Negativo:** Foco inicial voltado ao Android limita o público usuário.

---

## 2. Metodologia
### Principais pontos
- Abordagem: **Design Science Research (DSR)** – método iterativo para construção e avaliação de artefatos tecnológicos.
- Etapas:
  1. Levantamento científico sobre uso de aplicativos em saúde.
  2. Engajamento de profissionais de TI e saúde.
  3. Prototipagem com participação ativa dos desenvolvedores e equipe da UBS.
  4. Desenvolvimento dos módulos no **Android Studio** (Java/XML) e com uso da **Microsoft Power Platform** para integração e gestão de dados em nuvem.
- Sistema dividido em **três módulos**:
  - **Módulo ACS** (registro em campo)
  - **Módulo Gestante/Puérpera** (consulta e comunicação)
  - **Módulo de Gestão** (coordenação e análise de dados)

### Pontos para análise crítica
- 💡 **Positivo:** Uso de metodologia validada no design de soluções tecnológicas.
- 💡 **Positivo:** Participação de equipe multidisciplinar no desenvolvimento.
- ⚠️ **Negativo:** Falta detalhamento do planejamento para fase de testes em campo.
- ⚠️ **Negativo:** Não menciona diretamente estratégia de integração com prontuários eletrônicos já existentes.

---

## 3. Funcionalidades dos Módulos

### Módulo ACS
- Login com CPF/senha.
- Registra dados de gravidez, condições gerais, vacinação e visitas domiciliares.
- Interfaces simples e offline-first, com sincronização posterior.
- Permite coleta de dados como uso de suplementos, exames realizados, intercorrências.
- Alimenta a base de dados acessível pelos demais módulos.

### Módulo Gestante/Puérpera
- Login com CPF e token gerado pelo módulo de gestão.
- Funcionalidades:
  - Consulta ao histórico vacinal e de visitas do ACS.
  - Registro de ocorrências (ex.: sangramento, perda de líquido, dor, ausência de visita).
  - Acompanhamento da resolução das ocorrências com status por cor (verde, amarelo, vermelho).
  - Registro diário de movimentos fetais (RDMF).
- Enfoque em empoderamento da usuária e comunicação ativa com a equipe de saúde.

### Módulo Gestão
- Acesso restrito a profissionais e gestores.
- Gerencia cadastros, profissionais, visitas e ocorrências.
- Permite acompanhamento consolidado dos dados para detectar vazios assistenciais.
- Auxilia na priorização de ações e na coordenação de respostas rápidas.

### Pontos para análise crítica
- 💡 **Positivo:** Estrutura modular bem definida, atendendo diferentes papéis dos usuários.
- 💡 **Positivo:** Função de registro de ocorrências direto pela gestante reduz tempo de resposta.
- ⚠️ **Negativo:** Dependência de registros manuais pelos ACS pode impactar completude dos dados.
- ⚠️ **Negativo:** Segurança de dados é mencionada, mas não detalhada tecnicamente.

---

## 4. Resultados preliminares e discussão
### Principais pontos
- Aplicativo pronto para testes de usabilidade e efetividade.
- Registro de software no **INPI** (núm. BR512020026554 para módulo gestante).
- Testado em ambiente simulado por pesquisadores e equipe de saúde, com dados fictícios.
- Observado bom funcionamento técnico e interface simples.
- Reconhece necessidade de próxima etapa de **validação com usuários reais** para ajustes.
- Inspirado em experiências positivas de outros apps (GestAção, PreNeonatal+, estudos na Nigéria), mas com diferencial de envolver ACS.

### Pontos para análise crítica
- 💡 **Positivo:** Protótipo funcional com perspectiva de avaliação em campo.
- 💡 **Positivo:** Benchmarking com aplicativos semelhantes demonstra atenção ao estado da arte.
- ⚠️ **Negativo:** Ainda sem dados empíricos de impacto real sobre indicadores de saúde.
- ⚠️ **Negativo:** Limitação tecnológica (Android-only) e necessidade de instalação individual nos dispositivos de ACS e gestantes.

---

## 5. Conclusão
- O AcGest tem potencial para otimizar processos de trabalho na APS e melhorar a comunicação com gestantes/puérperas.
- Diferenciais:
  - Modularidade.
  - Integração ACS–gestante–gestão.
  - Baixo custo e acessibilidade via dispositivos móveis básicos.
- Necessário implementar:
  - Testes de campo robustos.
  - Estratégias de capacitação dos usuários.
  - Análises de custo-benefício e impacto.
  - Planos para integração com sistemas nacionais (e-SUS AB).
- Risco: adoção depende fortemente da adesão dos ACS e das gestantes ao uso regular.

---

## Referência BibTeX
```bibtex
@article{Costa2023AcGest,
  author    = {Costa, Anne Carolinne de Carvalho and Carlos, Fernanda Beatriz Maia and Silva, Brendo Jackson Leite da and Silva, José Victor Cassiano da and Filho, Edilson Miguel de Azevedo and Pinto, Jan Erik Mont Gomery and Cobucci, Ricardo Ney},
  title     = {Sistema AcGest para assistência à saúde de gestantes e puérperas na Atenção Primária},
  journal   = {Revista Saúde Digital e Tecnologias Educacionais},
  year      = {2023},
  volume    = {11},
  number    = {1},
  pages     = {1688--1698},
  doi       = {10.16891/2317-434X.v11.e1.a2023.pp1688-1698},
  url       = {https://doi.org/10.16891/2317-434X.v11.e1.a2023.pp1688-1698}
}

#################################################

A Estratégia e-SUS atenção básica (AB) conta
com dois sistemas de softwares para a captação de dados,
sendo eles: o sistema com Coleta de Dados Simplificada
(CDS-AB) e o sistema com Prontuário Eletrônico do
Cidadão (PECAB), que alimentam o novo Sistema de
Informação em Saúde para a Atenção Básica (SISAB), que
substitui o Sistema de Informação da Atenção Básica
(SIAB) e atende aos diversos cenários de informatização e
conectividade nas unidades de saúde da APS
(BRASIL,2016).

O AcGEST foi desenvolvido usando o ambiente
de desenvolvimento integrado (IDE) do Android Studio
Arctic Fox, versão 2020.3.1 patch 3, codificado usando a
linguagem Java, com scripts XML para telas, permissões
e demais layouts. Portanto, o aplicativo está disponível
somente para celulares Android.

O sistema proposto foi dividido em três módulos
de funcionamento: dois aplicativos para smartphones e um
aplicativo Web de gestão.

 Um aplicativo será direcionado
para gestantes/puérperas e outro para os ACS. O último
módulo será o de gestão e acompanhamento, direcionado
para a equipe de enfermeiros e gestores da ESF

Os dados são inseridos pelos profissionais de saúde através do módulo de gestão, e assim que o cadastro da gestante é feito é disponibilizado o link e acesso para o módulo da gestante/puérpera, que pode ser acessado através do smartphone.

Importante frisar que o
cadastro do prontuário da gestante/puérpera será feito na
UBS através do módulo de gestão

 cada consulta
realizada, o enfermeiro, o médico ou o ACS que
acompanham a gestante utilizarão o cartão da gestante
para verificar e incluir os resultados dos exames nos seus
devidos módulos (aplicativos). Através desse módulo, a
equipe de saúde poderá consolidar as visitas domiciliares
realizadas pelos ACS que estão sob sua responsabilidade
no final de cada mês.

 partir das Lista de Cadastro de Gestantes, os
profissionais da unidade de saúde poderão cadastrar/editar
os dados de gestantes e acessar as Informações