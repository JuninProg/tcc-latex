## Resumo Executivo
A tese “AMAR – Aplicativo de Monitoramento, Acompanhamento e Rastreio do Desenvolvimento Infantil – um estudo de desenvolvimento e validade do conteúdo” descreve o projeto e validação de conteúdo de um sistema **web e mobile** direcionado a apoiar o cuidado compartilhado entre famílias e profissionais de saúde no acompanhamento do crescimento e desenvolvimento infantil.

O desenvolvimento seguiu metodologia de **design de interação participativo**, envolvendo quatro etapas:
1. **Identificação das necessidades dos usuários** – levantamento de requisitos com base na Caderneta de Saúde da Criança e literatura científica.
2. **Projeto de design da solução** – elaboração de 33 telas para AMAR Web e 61 telas para AMAR Mobile (Adobe XD).
3. **Construção do protótipo funcional** – front-end em React 17.0.2, API em Django Rest Framework 3.12.4, banco PostgreSQL 12.5.
4. **Avaliação de conteúdo** – 10 profissionais de saúde e 10 famílias participaram, com Índice de Validade de Conteúdo (IVC) ≥ 90% para quase todos os itens (exceto “O conteúdo atende diferentes tipos de famílias?”, IVC = 80% para ambos os públicos).

O **AMAR Web** destina-se a uso profissional, com cadastro, histórico gestacional e de parto, anamnese, dados antropométricos, vacinas, desenvolvimento, prescrições e observações. O **AMAR Mobile** permite acesso às informações pelos pais/cuidadores, com possibilidade de registrar marcos de desenvolvimento e receber vídeos/textos de estimulação.

O sistema está validado quanto ao conteúdo, implementado como protótipo funcional, mas ainda não passou por estudos de implementação ou integração com sistemas públicos.

## Justificativas

### Tem Aplicativo: Sim
Inclui módulo mobile para famílias e módulo web para profissionais.

### Tem Painel de Gestão: Sim
Módulo web para cadastro e acompanhamento detalhado, com gestão de registros e visualização de curvas de crescimento, desenvolvimento e histórico.

### Foi Implementado: Sim
Protótipo funcional construído e apresentado nas telas; front-end, API e banco de dados operacionais.

### Teve usuários: Sim
Participaram 10 famílias e 10 profissionais de saúde na etapa de avaliação.

### Suporte via profissional de saúde: Sim
Módulo web para uso profissional e desenvolvimento conduzido com profissionais da saúde infantil; conteúdos embasados em diretrizes do Ministério da Saúde e sociedades científicas.

### Integração com prefeituras: Não
Não há menção a parcerias específicas com secretarias municipais de saúde.

### Integração com sistemas públicos: Não
Não está integrado tecnicamente a sistemas como e-SUS; utiliza como referência conteúdos da Caderneta de Saúde da Criança.

### Tecnologias utilizadas
- **React 17.0.2** (front-end web)
- **Django Rest Framework 3.12.4** (API)
- **PostgreSQL 12.5** (banco de dados)
- **Adobe XD** (design de telas)
- **Design de interação participativo** como metodologia

## Linha CSV
AMAR – Aplicativo de Monitoramento, Acompanhamento e Rastreio do Desenvolvimento Infantil – um estudo de desenvolvimento e validade do conteúdo;Desenvolvimento Infantil;Sistema web e aplicativo mobile para acompanhamento compartilhado do crescimento e desenvolvimento infantil, com módulos para profissionais e famílias, validado quanto ao conteúdo;Sim;Sim;Sim;Sim;Sim;Não;Não;React, Django Rest Framework, PostgreSQL, Adobe XD;2021;https://repositorio.ufrn.br/server/api/core/bitstreams/34e3a6de-a6ba-4452-96c0-085683542fb3/content
