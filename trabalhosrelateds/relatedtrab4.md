# Resumo e Análise Crítica – Artigo "Aplicativo web para o acompanhamento de gestantes e puérperas: produção tecnológica" (trabrelated4.pdf)

## 1. Contexto e Introdução
### Principais pontos
- As tecnologias digitais têm ganhado espaço na saúde, especialmente com uso crescente de dispositivos móveis (smartphones e tablets).
- Aplicativos móveis têm sido usados para educação em saúde, acompanhamento remoto, agendamento e monitoramento clínico.
- Apesar de existir oferta de apps na área materno-infantil, poucos contemplam de forma sistemática o cuidado puerperal e o acompanhamento estruturado de gestantes.
- O estudo se propôs a produzir e validar um protótipo de aplicativo web ("Gestar Care®") para essa finalidade.

### Pontos para análise crítica
- 💡 **Positivo:** Contextualização clara da lacuna de soluções para o período puerperal.
- 💡 **Positivo:** Enfoque em atender demandas reais identificadas por usuários e profissionais.
- ⚠️ **Negativo:** Limitação por ainda não apresentar avaliação de impacto em desfechos de saúde.
- ⚠️ **Negativo:** Possível barreira cultural ou tecnológica ao uso continuado pela população-alvo.

---

## 2. Metodologia
### Principais pontos
- Estudo de produção tecnológica, do tipo prototipagem, em cinco etapas:
  1. **Identificação da relevância** do app por meio de círculos de conversa com 9 profissionais (7 enfermeiros, 1 dentista, 1 psicóloga) e 2 usuárias.
  2. **Modelagem** do protótipo em parceria com profissional de TI.
  3. **Validação da prototipagem** via técnica Delphi com dois usuários e nove profissionais experientes em saúde materna.
  4. **Design e implementação** do app com tecnologias livres e padrão multiplataforma (Python+Django, MySQL, Bootstrap), hospedagem em nuvem.
  5. **Registro do app** no Instituto Nacional de Propriedade Industrial (INPI) (código BR512019002855-4).

- Critérios avaliados: funcionalidade, confidencialidade, acessibilidade, usabilidade, flexibilidade, viabilidade, inovação e empreendedorismo.

### Pontos para análise crítica
- 💡 **Positivo:** Uso da técnica Delphi aumenta robustez da validação de conteúdo.
- 💡 **Positivo:** Adoção de metodologias ágeis (SCRUM/Trello) no desenvolvimento.
- ⚠️ **Negativo:** Apenas duas usuárias finais participaram da validação; amostra reduzida.
- ⚠️ **Negativo:** Validação inicial focou na percepção, não no uso prolongado em campo.

---

## 3. Resultados
### Principais pontos
- **Funcionalidades:** Área do cliente (usuária), área administrativa (gestão) e área do enfermeiro clínico, com integração de prontuário eletrônico, comunicação por vídeo/texto/áudio e registro formal em prontuário.
- Percentual de concordância da validação:
  - Funcionalidade: 99%
  - Confidencialidade/Acessibilidade: 100%
  - Viabilidade: 85% na primeira rodada Delphi, 100% na segunda
  - Inovação: 100%
- Principais ajustes a partir das sugestões:
  - Inclusão de múltiplas formas de pagamento (cartão, boleto, PIX).
  - Modificações de linguagem e funcionalidades para melhor adequação.
- Serviços gratuitos mantidos no período inicial.
- Hospedagem em servidor Linux na nuvem, compatibilidade com Android e iOS.

### Pontos para análise crítica
- 💡 **Positivo:** Alta concordância nas dimensões avaliadas, indicando boa aceitação.
- 💡 **Positivo:** Estrutura funcional clara para diferentes perfis de usuário.
- ⚠️ **Negativo:** Ainda não testado com uso maciço em ambientes diversos.
- ⚠️ **Negativo:** Aspectos de integração com sistemas oficiais como e-SUS não relatados.

---

## 4. Discussão
### Principais pontos
- O app busca profissionalizar o atendimento que muitas vezes ocorre via canais informais (ex.: WhatsApp®).
- Armazena prontuários eletrônicos com bloqueio de edição após fechamento da consulta, garantindo segurança e rastreabilidade.
- Permite videochamadas, envio de fotos e vídeos, texto e áudio entre profissional e usuária.
- É considerado funcional, acessível, confiável, viável e inovador, especialmente útil em contexto de pandemia.
- Ressalta potencial para:
  - Aumentar adesão ao pré-natal, puericultura e consultas pós-parto.
  - Valorizar e dar mais autonomia à atuação da enfermagem.
- Principais limitações: dependência de profissionais de TI, ajustes contínuos, necessidade de mais avaliações de campo.

### Pontos para análise crítica
- 💡 **Positivo:** Alinhamento com tendência de telemedicina e acompanhamento remoto.
- 💡 **Positivo:** Garantia de registro seguro das consultas, seguindo regras legais.
- ⚠️ **Negativo:** Falta de dados quantitativos sobre impacto em indicadores clínicos.
- ⚠️ **Negativo:** Ausência de avaliação econômica ou estudo de custo-efetividade.

---

## 5. Conclusão
- O Gestar Care® é apresentado como uma ferramenta tecnológica com acesso fácil, rápido e seguro, capaz de:
  - Minimizar riscos e tempo de espera em atendimentos presenciais.
  - Ampliar adesão a consultas do pré-natal e pós-parto.
  - Criar novo espaço de atuação profissional para enfermeiros.
- Potencial para fortalecer o vínculo enfermeiro-paciente e qualificar o cuidado.
- Sugere prosseguimento com implantação mais ampla e estudos de usabilidade, impacto e custo-benefício.

---

## Referência BibTeX

```bibtex
@article{Silva2022GestarCare,
  author    = {Silva, Lenise Dutra da and Bär, Karen Ariane and Zamberlan, Alexandre de Oliveira and Ben, Luiza Watanabe Dal and Sasso, Garace Marcon Dal and Backes, Dirce Stein},
  title     = {Aplicativo web para o acompanhamento de gestantes e puérperas: produção tecnológica},
  journal   = {Online Brazilian Journal of Nursing},
  year      = {2022},
  volume    = {21},
  pages     = {e20226529},
  doi       = {10.17665/1676-4285.20226529},
  url       = {https://doi.org/10.17665/1676-4285.20226529}
}

###################################

the initial sketch of the
app's prototype was defined, which was
deposited in the “Easy Easy App” Platform.

a) Main
screen/Client site: user’s access to the care,
medical chart, professionals, registration,
financial and health information icons;

b) Administrative area: used by the nurse-
managers to carry out registration and
approval of the service requested by the user,
as well as directing the appointment to a clinical
nurse and general management of the system

c) Clinical nurse area: in this area, the nurse
will receive notification of care, make a video
call or answer by text or audio and record the
care provided in the medical chart, as well as
registration and closure of the appointment.

offer free
availability of the services related to the
information on the app's page and the fees for
the consultations, according to the price table
of the acting professional.

web app using free technologies compatible
with computers and mobile devices (Android
and iOS).

cadastramento da mãe através do site, diferente dos outros que precisam que o profissional cadastre a paciente.

can store the
electronic medical charts, in which each service
provided is recorded by such professional, in
the format of evolution, diagnosis or
prescription