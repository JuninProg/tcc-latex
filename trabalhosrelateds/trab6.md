## Resumo Executivo
A tese “GESTASUS: Aplicativo móvel para integração da caderneta da gestante ao SISPRENATAL WEB” descreve o desenvolvimento e avaliação de um protótipo Android que espelha digitalmente a caderneta física da gestante, integrando suas informações registradas no sistema SISPRENATAL Web. Criado em parceria com o Laboratório de Segurança em Computação (LabSEC/UFSC), o app permite que dados sejam transferidos por leitura de QR Code gerado por profissional autorizado, proporcionando acesso offline à caderneta no smartphone. Foram conduzidas avaliações com 22 gestantes e 5 especialistas em enfermagem obstétrica, obtendo alta aceitação e média de 82,85 no SUS (System Usability Scale). Apesar da integração conceitual com o SISPRENATAL, não há menção clara a um painel de gestão web para profissionais nem testes finais em uso rotineiro massivo.

## Justificativas

### Tem Aplicativo: Sim
“O objetivo foi espelhar a caderneta da gestante de papel em dispositivos móveis… Basta ela instalar o aplicativo 'GESTASUS'… A caderneta migrará para o smartphone com todos os registros de saúde.” (Cap. 5.5)

### Tem Painel de Gestão: Não Claro
Há menção à “nova interface da plataforma SISPRENATAL web” para gerar QR Codes e transferir dados, mas não está claro se existe um painel administrativo web dedicado para gestão de conteúdos fora do SISPRENATAL existente.

### Foi Implementado: Sim
“Após reuniões com equipe especializada estabelecemos os requisitos gerais para o aplicativo… desenvolvimento para plataformas iOS® e Android®… protótipo concluído após 180 dias…” (Cap. 5.5)  
Testado por gestantes e especialistas durante a pesquisa.

### Teve usuários: Sim
“Avaliação… com 22 gestantes em acompanhamento do seu pré-natal em um ambulatório de alto risco” (Cap. 5.8)  
Resultados detalham percepções e sugestões das participantes.

### Suporte via profissional de saúde: Sim
“O profissional de saúde, devidamente habilitado… acessar a identidade da gestante e acionar a função 'Gerar GESTASUS'… A paciente poderá mostrar seu smartphone como espelho da caderneta… comunicação com equipe multidisciplinar e centros de referências, telemedicina…” (Discussão e requisitos)

### Integração com prefeituras: Sim
Parceria com “secretaria municipal de saúde de uma cidade do litoral norte catarinense” para campo de estudo e implementação (Cap. 5.2.1).

### Integração com sistemas públicos: Sim
Integração direta com plataforma oficial “SISPRENATAL web” e menção à interoperabilidade com “Brasil Cidadão” e possível e-SUS AB (Cap. 5.5 e Discussão).

### Tecnologias utilizadas
- **Adobe XD**: “Para desenvolvimento do protótipo… utilizamos… a ferramenta ADOBE XD®.” (Cap. 5.5)
- **QR Code**: “A primeira e única funcionalidade… é realizar a leitura de um código QR code…” (Cap. 5.5)
- **Arquitetura HL7**: “…apresentamos… o modelo arquitetural… Fonte – Health Level Seven International (2021)” (Fig. 14-16)
- **SISPRENATAL Web**: Integração com plataforma oficial  
(*Não há menção direta a linguagens de programação específicas no trecho fornecido; foco no design e integração.*)

## Linha CSV
GESTASUS: Aplicativo móvel para integração da caderneta da gestante ao SISPRENATAL WEB;Gestação/Pré-natal;Aplicativo Android que espelha a caderneta da gestante física e integra dados do SISPRENATAL Web por QR Code, validado com gestantes e especialistas;Sim;Não Claro;Sim;Sim;Sim;Sim;Sim;Adobe XD, QR Code, HL7, SISPRENATAL Web;2025;https://repositorio.ufsc.br/bitstream/handle/123456789/264490/PGCF0241-T.pdf?sequence=-1&isAllowed=y
