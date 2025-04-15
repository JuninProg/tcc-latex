# Estrutura texto TCC

## Brainstorm de assuntos

### Assuntos que são o cerne da pesquisa e não devo esquecer de mencionar

* Reconstrução do painel e API conforme requisitos funcionais e não funcionais anteriormente levantados, com algumas mudanças pontuais em quesitos como estilização (cor vermelha sendo principal como é no app), segurança/infraestrutura onde é obrigatoriadade a comunicação em rede por protocolo HTTPS com certificado SSL, ao invés de como estava antes somente HTTP sem as informações sendo criptografadas, infrigindo as políticas das lojas dos dispositivos móveis (ponto que removeu o aplicativo antigo da loja).
* Essa migração tecnológica do painel e API envolveu a escolha de uma nova linguagem e frameworks, tanto para o backend, quanto para o frontend, tendo em vista a manutenabilidade do projeto ao longo dos anos. Dado que o sistema anterior foi escrito em PHP com Laravel, sendo um monolito responsável tanto pelos endpoints, quanto telas dinâmicas, ao passar do tempo sua manutenção se tornou onerosa pois a maioria dos estudantes do IFRS Campus Osório (responsável pela tecnologia do projeto) não conseguiam avançar na resolução dos problemas, porque em sua base curricular outras ferramentas são ensinadas, tendo que aprender e lidar sozinho (além do professor orientador) com um projeto com grande número de código-fonte.
* A escolha do novo principal framework de desenvolvimento se baseou não só pelo fato dos estudantes aprenderem NodeJS em seu dia a dia escolar, mas também pelo avanço de popularidade de mercado do uso da ferramenta frente o PHP, proporcionando com que os alunos possam atestar experiência posterior em busca de uma vaga na área de desenvolvimento. Pensar também em argumentos de desempenho, curva de aprendizado, etc.
* Com a migração também pensou-se em uma das projeções futuras do aluno José (TCC do app) que seria escalar o sistema de modo que poderíamos aplicar em diferentes regiões geográficas. Pensando também na definição do sistema Pró-Mamá como gerenciador de conteúdo e tomando como base grandes do mercado, como WordPress, a principal funcionalidade é a portabilidade, ou seja, que novos agentes possam instalar e utilizar da ferramenta. Assim, além de separar a API e painel em dois repositórios diferentes para desacoplar frontend e backend, criou-se imagens Docker para cada sistema e um arquivo Docker Compose para além de criar os container das aplicações, sobe o banco de dados postgresql, redis e nginx para servir como load balancer. Tudo isso é possível através de apenas um comando de compose, além da configuração inicial. Para a configuração inicial espera-se que o usuário tenha um domínio e servidor, a partir disso configura-se o certificado (documentar depois as duas formas com cloudflare e certbot) e clona o repositório de infra do Pró-Mamá, basta instalar docker na máquina, preencher as variáveis de ambiente e rodar o sistema. Hoje o aplicativo que temos na loja somente aponta para o sistema da prefeitura de Osório, mas podemos fazer com que o aplicativo seja multitenant e o usuário no cadastro escolhe a prefeitura que deseja reportar. Assim novas prefeituras podem se adequar ao programa facilmente.
* Em Osório o Pró-Mamá surgiu de uma iniciativa da NASF (Núcleo de Saúde da Família do Brasil), existe uma lei que outorga uma verba para que a prefeitura contrate uma equipe multiprofissional para atuar diretamente nas unidades de saúde do município. Essa equipe pode ser composta de: médico, médico-veterinário, psicólogo, nutricionista e fonoaudiólogo. A equipe de Osório criou o programa de aleitamento materno e começou a promever informações sobre o tema com treinamentos para outros colegas da saúde do serviço público, encontros semestrais, eventos, etc. Com isso o IFRS Campus Osório ofereceu uma parceria e foi desenvolvido em 2018 os sistemas para auxiliar na promoção das informações na cidade. Pesquisar mais sobre a lei para criar um paralelo em como o sistema Pró-Mamá pode fazer com que novas prefeituras consigam esse apoio do governo, entender os requisitos.
* Para arquitetura de desenvolvimento ao invés de MVC, escolheu-se o DDD com princípios SOLID. A principal diferença é que ao desacoplar o frontend do backend, não fazia sentido manter camadas de visualização (view) no backend e nem controllers para as telas do painel. Na construção da API os diretórios e arquivos foram separados conforme a arquitetura hexagonal, com camada de domínio com as regras de negócio, interface de comunicação para as rotas, camada de infraestrutura para estruturas externas e camada da aplicação para o fluxo de cada rotina. No painel foi utilizada a mesma abordagem com adaptações onde mantêm-se camadas de domínio e aplicação para cada caso de uso usados nas telas. As telas estão na camada de interface mas com uma forma de factories para construir as dependências. Para carregamento das páginas utilizou um roteamento com lazy loading para que só seja carregado os scripts, html, css do endereço digitado, ao mudar de tela o carregamento dos novos arquivos é feito fazendo com que o desempenho do sistema seja fluído, rápido e leve.

## Ordem dos tópicos e assuntos que devem ser abordados no TCC

### Introdução

* Amamentação exclusiva e promoção do aleitamento materno, pilares da OMS
* Como surgiu o Pró-Mamá Osório, profissionais, NASF lei de incentivo municipal
* Parceira com IFRS Campus Osório e criação do aplicativo/painel em 2018
* Incoformidade com a LGPD e requisitos de segurança do sistema ocasionaram a remoção do aplicativo das lojas
* Com caráter de continuação o presente trabalho tem como foco reestabelecer o painel e API do sistema Pró-Mamá, o aplicativo ficou de responsabilidade do outro aluno do projeto. Haverá uma migração tecnológica para atender aos requisitos de segurança e manutenabilidade, além de introduzir novas funcionalidades a partir das projeções futuras dos estudantes fundadores do projeto tecnológico e sugestões dos profissionais ao longo do uso da plataforma

### Objetivos

#### Objetivo geral

Migração tecnológica do Painel e API do Pró-Mamá para que os sistemas estejam de acordo com os requisitos de segurança e sejam reestabelecidos para uso dos profissionais de saúde, além dos usuários pelo aplicativo.

#### Objetivos específicos

* A partir dos requisitos funcionais e não-funcionais pré-estabelecidos pelo estudante fundador, realizar revisões e apontamento de mudanças, além de criar novos se necessário
* Planejar a migração tecnológica com a escolha das novas linguagens e frameworks
* Desenhar a arquitetura do Painel e API
* Estruturar banco de dados e operação para migração dos dados retroativos
* Estruturar armazenamento de arquivos e migração das fotos retroativas
* Desenvolver API e Painel
* Adicionar protocolo HTTPS com certificado SSL e criptografia, além de rotinas específicas para a LGPD a fim de estar em conformidade com os requisitos de segurança das lojas
* Consildar princípios de integração contínua e testes automatizados para a manutenção durante o ciclo de vida do software
* Adicionar portabilidade no sistema para que seja um CMS instalável, assim outros municípios podem aderir ao programa

### Justificativa

* Meta-análise, uso de modelos de inter-
venção pela Internet podem melhorar o nível de conhecimento sobre o aleitamento materno e
que o seu domínio está intimamente relacionado ao efeito da amamentação. Ou seja, quanto mais a mãe sabe sobre amamentação melhor sua adesão as boas práticas para contribuir para o desenvolvimento pleno de seu bebê e da saúde de ambos
* O serviço público de saúde deve promover iniciativas de promoção ao aleitamento materno, Pró-Mamá é um exemplo e o aplicativo corrobora com as premissas da OMS
* Desde 2018 10.864 acessos, 1.348 cadastros realizados e mais de 188
dúvidas respondidas Autor (2024).

Criar uma justificativa que tenha esses três pilares: meta-análise e conhecimento x efeito da amamentação, OMS e como as instituições devem ter iniciativas de promoção e explorar os resultados do aplicativo para finalizar o argumento afirmando que se faz necessário com que ele seja posto de volta no ar dado sua contribuição para a sociedade.

### Referencial Teórico

O que não pode faltar

* Aleitamento materno
* LGPD
* NodeJs / ReactJs
* Docker e Docker Compose
* HTTP x HTTPS
* API REST
* Arquitetura hexagonal
* DDD
* SOLID
* Integração contínua
* Testes automatizados
* CMS
* Aplicações multitenant
* Segurança da informação

### Trabalhos relacionados

#### O que eu já escrevi

* Pesquisa de mercado utilizando a W3Techs para elencar os principais sistemas gerenciadores de conteúdo, não introduzi muito bem porque fiz essa pesquisa, relacionar melhor com o trabalho feito que é o painel e api.
* Listei WordPress, Wix e Shopify, detalhando cada um e por fim coloquei comparações com o Pró-Mamá, ficou um monólogo chato

Ficou sem contexto e coloca o painel pró-mamá numa categoria que não faz sentido, não é objetivo do presente trabalho ser generalista e atender quaisquer demandas como os CMS do mercado.

#### O que investiguei

* Envei e-mail para mais de 50 instituições que desenvolveram aplicativos de saúde similares para ver se utilizavam um CMS ou como era a estrutura do sistema, não obtive resposta de ninguém
* A segunda pesquisa foi de relacionar os maiores CMS do mercado, porém não abordei corretamente e nem citei o Pró-Mamá antigo

#### Ideias do que escrever

* Introduzir melhor a pesquisa de trabalhos relacionados, citar que foi feita a pesquisa por e-mail sem sucesso
* Após isso, dizer que o painel e API se enquadram em um sistema gerenciador de conteúdo, mas o foco do Pró-Mamá é ser específico para a promoção do aleitamento materno, não como o WordPress que é generalista um CMS que pode ser utilizado para qualquer tipo de site, mas com foco em blogs e portfólios
* O uso de sistemas referência no mercado foi para entender como tornar o Pró-Mamá um sistema portável que tenha as principais características de um CMS
* Não fazer um monólogo descrevendo cada sistema como WordPress, Wix, Shopify, mas um texto corrido e coeso que tenha início, meio e fim citando cada trabalho relacionado, a forma de pesquisa, comparações e o que é diferente no sistema do presente trabalho

### Metodologia

* Levantamento documental
* Metodologia de desenvolvimento
  a. Para a fase de reconstrução do painel e API foi utilizado o modelo incremental
  b. Para a fase de sustentação e evolução do sistema foi utilizado o modelo de Kanban com princípios Agile
* Análise de requisitos
  a. Utilizar como referência o trabalho do Lucas e citar os requisitos que foram alterados, tanto funcionais quanto não funcionais 
  b. Citar os requisitos que foram adicionados
  c. Citar os requisitos que foram removidos
* Arquitetura de software
  a. escolhas anteriores e atuais, uma abordagem de introdução para falar sobre a nova arquitetura do sistema
  b. Citar a escolha do NodeJS e ReactJS
  c. trazer alguns Diagramas UML, sequência e caso de uso para elucidar mudanças estruturais e importantes
    - Citar a separação do frontend e backend
  d. padrões para a codificação
    - Citar a arquitetura hexagonal, DDD, SOLID
  e. infraestrutura
    - Citar a escolha da base de dados PostgreSQL e migração do MySQL, uso do Redis
    - Citar a escolha do Docker e Docker Compose
    - Citar a escolha do HTTPS e SSL, Nginx, Cloudflare e Certbot
  f. integração contínua
    - Citar a escolha do GitHub Actions, princípios de CI/CD
  g. testes e resultados
    - Citar a escolha do Jest e Cypress (ainda não há Cypress, mas testes de integração e unitários foram realizados)
    - Testes unitários e integrados
    - Testes de carga (não foi feito mas seria legal porque o trabalho anterior fez)
    - Testes de usabilidade (não foi feito por ngm e é um bom ponto para trazer)
    - Testes de segurança (foram realizados)
  h. observabilidade
    - Citar o uso de logs com Winston e Morgan
    - Logs visualizados pelo Docker
    - Uso da elastick stack com Kibana e alertas (n foi feito mas com o que tem é muito fácil, problema é consumo de memória)
  t. Documentação 
    - Citar o uso do Swagger para documentar a API com OpenAPI 3.0
    - Repositório de infraestrutura contém arquivos e desenhos dos fluxos do Pró-Mamá e processos de desenvolvimento
* Portabilidade
  a. Falar sobre construação da infraestrutura como código para que seja possível reproduzir o sistema completo do Pró-Mamá: API, painel, banco de dados, redis e nginx com apenas um comando de compose
  b. Falar sobre a construção do sistema ser multitenant, onde o usuário pode escolher a prefeitura que deseja reportar
  c. Falar sobre o aplicativo não estar preparado para ser multitenant, mas que o sistema backend já está preparado para isso

-- Tem muitos tópicos em arquitetura, selecionar os mais relevantes e não esquecer de comparar com as escolhas anteriores para ficar mais claro para o leitor o caráter de continuação e o que foi mudado
-- A ideia do tópico de metodologia é uma análise geral do que foi pesquisado, levantado e feito, não é para ser um passo a passo de cada etapa do desenvolvimento, mas sim uma visão geral do que foi feito e como foi feito

### Desenvolvimento

Talvez seguir pela ordem cronológica e separar o painel e API

1. Cenário preexistente
    a. O que era o painel e API
      - Aplicação PHP com Laravel
    b. O que foi feito no painel e API
      - Os requisitios funcionais e não funcionais foram levantados, documentados e implantados
    c. O que não foi feito no painel e API
      - Escalabilidade e segurança
    d. O que não funcionava no painel e API
      - Sistema de notificações (push notification)
    e. O que não era seguro no painel e API
      - Todas as rotas eram inseguras, não tinha HTTPS
      - Havia um sistema de autenticação JWT e hasheamento de senhas
    f. O que não era escalável no painel e API
      - Sistema monolítico, não tinha separação de frontend e backend
    g. Resultados
      - Sistema foi premiado em 2019 pelo banco do brasil pela iniciativa
      - Houve um bom número de cadastros e acessos, na casa dos milhares
      - Houveram mais de 200 dúvidas respondidas para todos, fora os atendimentos feitos pelos profissionais de saúde
      - O sistema ficou no ar por uns 3 anos (rever informação)
2. Falta de manutenção
    a. Apesar de haver um projeto de extensão na instituição, de todos os estudantes que passaram pelo projeto, nenhum havia conseguido dar continuidade, o que fez com que o sistema ficasse obsoleto
    b. A partir da implantação da LGPD o aplicativo ficou fora do ar, pois o sistema não atendia aos requisitos de segurança
    c. Entendimento de quas as linguagens utilizadas para o desenvolvimento do sistema não eram lecionadas na instituição, por isso a falta de progresso
3. Decisão de reconstrução
    a. Reunião inicial do projeto com o professor orientador e os alunos
    b. Proposta de reconstrução para os profissionais de saúde levando em consideração as sugestões deles
    c. Definição de prazos e expectativas
    d. Definição de metas e objetivos
4. Separação das responsabilidades
    a. Separação do trabalho e o que era mais importante de ser entregue primeiro
      - Painel e infraestrutura responsabilidade do autor do trabalho
      - API responsabilidade de ambos os alunos
      - Aplicativo colega do projeto
    b. Decisão de colocar o aplicativo de volta na loja o quanto antes
    c. Priorização do desenvolvimento da API, infraestrutura e aplicativo em paralelo
5. Planejamento
    a. Construção dos protótipos do painel no Figma
    b. Padrões de desenvolvimento e de projeto
    c. Desenho geral da arquitetura da API e infraestrutura
    d. Listagem das tarefas e ordem de prioridade para primeira entrega em produção
     - Construção do boilerplate da API e formas para que seu desenvolvimento fosse colaborativo
     - Construção do boilerplate do painel e telas iniciais básicas
     - Repositório de infraestrutura com API e painel, usando Docker e Docker Compose
    e. Estrutura do banco de dados e migração do legado
    f. Estrutura do armazenamento de arquivos e migração do legado
    g. Perspectiva do primeiro deploy e visão macro de cada entregável no calendário
6. Desenvolvimento
    a. Configuração do ambiente
        - Ambiente de desenvolvimento local
        - Ambiente de produção
        - Ambiente de testes (poderia ter mas é o local)
        - Controle de versão
        - Uso de Docker e Docker Compose
        - Uso de Typescript, ESLint e Prettier
    b. Boilerplates
        - Adoção do modelo DDD com cada caso de uso sendo um diretório na API, uso de factories para injeção de dependência com o uso do inversão de controle. Framework awilix do NodeJs
        - Adoção de clean architecture no painel, com cada tela sendo um diretório e cada caso de uso sendo um arquivo dentro do diretório, uso de factories para injeção de dependência com o uso do inversão de controle. Feito na mão cada instância
    c. Documentação dinâmica
        - Para a colaboração na API foi utilizado o Swagger com OpenAPI 3.0, com o uso de DTOs declarados, a definição de schemas é feita automatizada e o Swagger gera a documentação automaticamente a partir da lib express swagger-ui-express
    d. Testes
        - Testes unitários e integrados com o uso do Jest, com a lib supertest para fazer as requisições e verificar os resultados
        - Trazer os outros testes aq
    e. Integração contínua
        - Criação do repositório de infraestrutura com o uso do Docker e Docker Compose, com o uso do GitHub Actions para fazer o deploy automático da API e painel
    f. Codificação
        * Painel
            - Página de autenticação, recuperação de senha, exclusão do usuário
            - Página inicial, gráficos com dados de uso do sistema
            - Página de informação
            - Página de perguntas frequentes
            - Página de fale conosco
            - Página de notificações
        * API
            - Mapa de rotas
            - Requisições e respostas
            - Background jobs com Redis para o sistema de notificação
            - Padrão OUTBOX para o sistema de notificação
            - Sistema de autenticação com JWT
            - Sistema de upload de arquivos no servidor
            - Sistema de envio de e-mail
        * Infraestrutura
            - Criação do repositório de infraestrutura com o uso do Docker e Docker Compose
            - Nginx como load balancer
            - PostgreSQL como banco de dados
            - Redis para cache e sistema de notificação
            - Certificado SSL com o uso do Cloudflare e Certbot
            - Configuração do HTTPS e criptografia
            - Configuração do domínio
            - Client para o banco de dados
    g. Segurança
        - Protocolo HTTPS com certificado SSL
        - Hasheamento de senhas
        - Autenticação e autorização (role "mom" e "admin")
        - Rotinas para a LGPD (termos de uso, política de privacidade, exclusão de dados)
        - Criptografia de dados
        - Proteção contra ataques de força bruta (poderia ter algo relacionado porque o sistema sofre alguns ataques)
        - Poderia realizar pentest, mas não foi feito
    h. Implantação
        - Configuração única do domínio com os apontamentos A e políticas para o certificado SSL da Cloudflare
        - Com o servidor virtual em mãos, configuração única do Git e instalação do Docker
        - Clonar o repositório de infraestrutura, preencher as variáveis de ambiente e token de acesso para o CI/CD
        - Configuração única da infraestrutura e docker compose up para inicializar os containers, nginx, banco de dados, tudo será provisionado
        - Configuração no GitHub Actions para o deploy automático da API e painel
    i. Manutenção do sistema
        - Criação do board de issues do GitHub para o gerenciamento das tarefas
        - Documentação do processo de desenvolvimento e ciclo de vida do software para futuras manutenções
        - Passagem de conhecimento para os próximos alunos do projeto e criar ecossistema de desenvolvimento

### Conclusão

* O que foi feito
* O que não foi feito
* O que poderia ser feito
* O que não foi feito e poderia ser feito
* O que foi aprendido
* O que não foi aprendido
* O que foi ensinado
* O que não foi ensinado
* O que foi documentado

### Projeções futuras




