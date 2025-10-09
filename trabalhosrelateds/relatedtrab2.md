# Resumo dos Trabalhos Relacionados – TCC Sistema AMAR (trabrelated2.pdf)

## 1. Revisão de Escopo sobre mHealth em países de baixa e média renda
### Principais pontos
- Objetivo: identificar tecnologias mHealth utilizadas para acompanhar o desenvolvimento infantil (0 a 3 anos) em países de baixa/média renda.
- Metodologia: protocolo registrado seguindo PRISMA-P e PRISMA-ScR; abordagem PCC (população, conceito, contexto).
- Fontes: PubMed, Scopus, Embase, Bireme; combinando descritores de telemedicina, desenvolvimento infantil e países LMIC.
- Critérios: estudos com aplicativos/mensagens de texto para rastreio, monitoramento ou instrução; amostras de crianças ≤ 3 anos; revistos por pares.
- Amostra e achados: predominância de aplicativos; poucas intervenções com avaliação de confiabilidade entre avaliadores; falta de testes longitudinais e dados de custo-efetividade.
- Limitação destacada: maioria dos estudos com foco em viabilidade e aceitabilidade; carência de mensuração robusta de impacto e custo.

### Pontos para análise crítica
- 💡 **Positivo:** Protocolo robusto e registro prévio; uso de múltiplas bases e combinação ampla de descritores.
- 💡 **Positivo:** Mapeamento inicial útil para identificar oportunidades e lacunas.
- ⚠️ **Negativo:** Pouca heterogeneidade nas estratégias (quase todas baseadas em apps); potencial enviesamento por popularidade dessa abordagem.
- ⚠️ **Negativo:** Ausência de dados consistentes sobre custo, implementação e resultados clínicos a longo prazo.
- ⚠️ **Negativo:** Muitas iniciativas sem validação de confiabilidade entre avaliadores, limitando uso clínico.

---

## 2. Metodologia participativa para desenvolvimento do Sistema AMAR
### Principais pontos
- Design de interação participativo com quatro etapas: 
  1. Definição de requisitos
  2. Projeto de design
  3. Protótipo funcional
  4. Avaliação
- Participação contínua de desenvolvedores, designers, fisioterapeutas e famílias no processo.
- Conteúdo e layout baseado na Caderneta de Saúde da Criança.
- Identificação de dificuldades na utilização da CSC: não preenchimento, baixa adesão, falta de treinamento e interesse.
- Objetivo: possibilitar acompanhamento compartilhado entre famílias e profissionais, incluindo dados antropométricos, marcos de desenvolvimento e orientações personalizadas.

### Pontos para análise crítica
- 💡 **Positivo:** Metodologia centrada no usuário potencializa alinhamento às necessidades reais.
- 💡 **Positivo:** Base em instrumento oficial do Ministério da Saúde favorece adoção e padronização.
- ⚠️ **Negativo:** Depende de mudança cultural e engajamento dos profissionais para preencher dados corretamente.
- ⚠️ **Negativo:** Risco de replicar problemas de desuso observados na CSC se não houver incentivo e treinamento.

---

## 3. Desenvolvimento técnico do Sistema AMAR
### Principais pontos
- Módulos: Web (profissionais) e Mobile (famílias).
- Front-end com design responsivo; back-end em JavaScript.
- Banco de dados PostgreSQL 12.5; API Django Rest Framework 3.12.4.
- Funções: acompanhar dados de crescimento/desenvolvimento; oferecer dicas; permitir registro e consulta por ambos os públicos.
- Armazenamento e gerenciamento com segurança e conformidade com LGPD.
- Avaliação de validade de conteúdo por 10 profissionais de saúde e 10 famílias → Índice de Validade de Conteúdo ≥ 80% em todas as questões.
- Feedback positivo sobre clareza, relevância e utilidade.

### Pontos para análise crítica
- 💡 **Positivo:** Conformidade com padrões técnicos e legais; arquitetura escalável.
- 💡 **Positivo:** Validação com usuários-alvo reforça aplicabilidade.
- ⚠️ **Negativo:** Teste limitado a um número pequeno de participantes; ausência de análise de desempenho em campo a longo prazo.
- ⚠️ **Negativo:** Não foi mensurada interoperabilidade com sistemas oficiais (e-SUS) no teste final.

---

## 4. Perspectivas e conclusões da tese
### Principais pontos
- Ferramentas mHealth têm potencial para melhorar acompanhamento infantil, mas há falta de dados de implementação e impacto.
- Sistema AMAR: viável e aceitável de acordo com participantes.
- Perspectiva: uso do banco de dados para algoritmos de rastreio de risco; expansão para outros locais no Brasil após testes de usabilidade e confiabilidade.
- Conclusão: conteúdo adequado para monitorar desenvolvimento infantil com participação ativa das famílias e suporte dos profissionais.

### Pontos para análise crítica
- 💡 **Positivo:** Visão estratégica de uso de dados para rastreio automatizado; possibilidade de expansão nacional.
- 💡 **Positivo:** Enfoque em educação em saúde baseada em evidências.
- ⚠️ **Negativo:** Dependência da adesão contínua pelos profissionais e famílias; risco de baixa sustentabilidade caso não haja integração a políticas públicas.
- ⚠️ **Negativo:** Necessidade de ampliar amostra em estudos futuros para garantir validade externa dos achados.

---

## Referência BibTeX

```bibtex
@phdthesis{Farias2025SistemaAMAR,
  author    = {Farias, Gabriela Gomes Ferreira},
  title     = {Sistema AMAR: aplicação web e móvel para acompanhamento compartilhado do desenvolvimento infantil entre família e profissionais de saúde},
  school    = {Universidade Federal do Rio Grande do Norte},
  year      = {2025},
  address   = {Natal},
  type      = {Tese (Doutorado em Ciências da Saúde)},
  url       = {https://repositorio.ufrn.br/handle/123456789/XXXXX},
  note      = {Orientadores: Renata Mosca e De Wet Swanepoel}
}

################################################

Tese pós fisioterapia

No Brasil, a saúde digital foi definida como uma das dimensões fundamentais do SUS
e instituída a partir de estratégias como o Conecte SUS, que apresenta dois projetos de base
para a sua estruturação: (1) a Rede Nacional de Dados em Saúde (RNDS) e (2) o Programa de
Apoio à Informatização e Qualificação dos Dados da Atenção Primária de Saúde, ambos com
o objetivo de favorecer a troca de informações entre os setores e serviços de saúde e otimizar o
cuidado continuado[4]. Outra estratégia é o e-SUS, cujo objetivo é a reestruturação das
informações da Atenção Primária através do Coleta de Dados Simplificada (CDS) e Prontuário
Eletrônico do Cidadão (PEC), que são dois sistemas para a captação dos dados de saúde dos
cidadãos 

O modo web profissionais de saúde
* Cadastrar família, pesquisar paciente, visualizar atendimentos, iniciar novo atendimento, cadastrar no sitstema, visualizar cadastro criança, atualizar dados cadastrais, recuperar senha, gerenciar usuários
O app
* Realiza login, atualiza dados cadastrais, recupera senha, visualizar atendimentos, inserir dados desenvolvimento infantil, visualizar tutorial de uso, dicas e orientações

Principal ponto de problema é que o profissional de saúde tem que cadastrar as famílias no sistema, o que demanda tempo e pode ser um entrave para a adesão. E também é preciso gerar as credenciais de acesso para as famílias conseguirem utilizar o aplicativo, outro ponto de atrito.

O profissional vai ter que preencher a ferramenta além de seus sistemas oficiais, o que pode ser um entrave para a adesão. Esse é um ponto chave, pois no Pró-Mamá temos o mesmo problema, pois não integramos com nenhuma entidade oficial. A forma que resolvemos pro município foi fazer com que os dados que precisassem ser cadastrados fossem atemporais ou com baixa frequência de atualização, pois foi montada uma cartilha de informações pelos profissionais de saúde e subimos no sistema. O profissional não precisa cadastrar família, pois a mãe pode baixar o app livremente nas lojas e se auto cadastrar. O profisisonal só precisa responder as dúvidas que são enviadas, atualizar as informações quando necessário (como número do posto que mudar) e cadastrar novos lembretes se desejar.

No AMAR web, destinado ao uso de
profissionais de saúde, foram desenvolvidos 5 domínios onde poderão ser preenchidas as
seguintes informações: cadastro das crianças; histórico da gestação e do momento do parto,
anamnese das consultas, dados antropométricos, vacinas, desenvolvimento, prescrições e
observações

Neste domínio, as famílias serão
estimuladas a acompanharem os marcos do desenvolvimento e sinalizarem quando estes forem
alcançados pelos seus filhos

A versão mobile é destinada para os cuidadores. Após receberem o login, senha e
permissão do profissional de saúde para o seu uso, os cuidadores poderão adicionar outros
dados cadastrais como xxxx. Além disso, será possível visualizar as informações preenchidas
durante as consultas, avaliar o desenvolvimento do seu filho e receber dicas sobre como
estimular sua criança.