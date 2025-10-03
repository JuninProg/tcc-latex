## Resumo Executivo
O trabalho de conclusão de curso “Hora de Mamar! Aplicação Mobile & Web de acompanhamento alimentar infantil direcionado a pais, cuidadores e profissionais de saúde de bebês de 0 a 12 meses” apresenta o desenvolvimento de um WebApp responsivo com foco em registrar e acompanhar dados de alimentação (amamentação, ingestão de líquidos e sólidos) de crianças até 12 meses. A solução inclui recursos de relatórios, central de conhecimento com conteúdos oficiais sobre saúde infantil, registro em tempo real de sessões de amamentação e mecanismos para compartilhamento de dados com médicos e cuidadores. O backend foi implementado em PHP com Symfony, banco de dados relacional, suporte a templates e message broker interno. O sistema foi funcionalmente implementado e pensado para uso doméstico e profissional, mas não foram realizados testes com usuários finais.

## Justificativas

### Tem Aplicativo: Não Claro
O texto descreve um WebApp responsivo (acessível em dispositivos móveis e desktops), mas não menciona desenvolvimento específico como aplicativo nativo Android/iOS.  
“…o resultado aqui produzido foi um WebApp, isto é, um programa apresentado no formato de website, com apresentação visual pensada para dispositivos móveis…” (Cap. 5 Resultados)

### Tem Painel de Gestão: Sim
O WebApp possui funcionalidades administrativas para vincular crianças, adicionar registros de alimentação, gerenciar artigos na “Central de Conhecimento” e gerar relatórios compilados.  
“…os artigos de ajuda foram armazenados no banco de dados e disponibilizado aos usuários na ‘Central de conhecimento’…”  
“…o modelo do relatório construído é compacto, fornecendo os dados compilados para o período que foi selecionado…” (Cap. 5)

### Foi Implementado: Sim
“…o resultado aqui produzido foi um WebApp… Apesar do framework Symfony ter suporte a alguns message brokers… a escolha neste trabalho foi considerar o banco de dados como parte deste sistema… As páginas dentro do software são geradas graças ao templating…” (Cap. 5)  
As figuras mostram telas reais do sistema.

### Teve usuários: Não
Não há relato de execução de testes ou uso real por pais, cuidadores ou profissionais fora do desenvolvimento; foco foi no protótipo funcional.

### Suporte via profissional de saúde: Sim
“…Outra forma de se prover uma atenção adequada às crianças é fornecer ao médico informações precisas… é possível implementar muitas melhorias que aproximem os pais dos médicos, como por exemplo, um mensageiro instantâneo…” (Cap. 6)  
Atualmente há funcionalidade de compartilhamento de relatórios com médicos.

### Integração com prefeituras: Não
Não há menção a uso institucional ou parceria com secretarias municipais.

### Integração com sistemas públicos: Não
Não integra com sistemas nacionais (e-SUS, SISPRENATAL etc.); apenas utiliza conteúdos e diretrizes do Ministério da Saúde e OMS.

### Tecnologias utilizadas
- **Symfony (PHP)**: “…Apesar do framework Symfony ter suporte…” (Cap. 5)  
- **RabbitMQ (suporte opcional)**: “…suporte a alguns message brokers, como o RabbitMQ…” (Cap. 5)  
- **Twig**: “…o Twig fornece funções relacionadas a tradução bidirecional entre Markdown e HTML…” (Cap. 5)  
- **Markdown**: “…U ma boa alternativa se apresentou no Markdown…” (Cap. 5)  
- **Natural Language Toolkit (Python)**: “…Para tanto, lançou-se mão do Natural Language Toolkit, escrito em Python…” (Fundamentação)
- **Banco de dados relacional**: “…armazenados num banco relacional…” (Cap. 5)

## Linha CSV
Hora de Mamar! Aplicação Mobile & Web de acompanhamento alimentar infantil direcionado a pais, cuidadores e profissionais de saúde de bebês de 0 a 12 meses;Aleitamento Materno;WebApp responsivo para registro e acompanhamento da alimentação infantil até 12 meses, com central de conhecimento, relatórios e compartilhamento de dados com médicos;Não Claro;Sim;Sim;Não;Sim;Não;Não;Symfony (PHP), RabbitMQ, Twig, Markdown, Natural Language Toolkit (Python), Banco de dados relacional;2021;https://repositorio.unesp.br/server/api/core/bitstreams/eaaec1cc-863c-41a4-961c-4311c3aa8f56/content
