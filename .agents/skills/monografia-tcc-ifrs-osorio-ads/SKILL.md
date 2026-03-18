---
name: monografia-tcc-ifrs-osorio-ads
description: Escreve, revisa, estrutura e formata monografias de TCC do Curso Superior de Tecnologia em Analise e Desenvolvimento de Sistemas do IFRS Campus Osorio, especialmente neste template abnTeX2. Use quando o usuario pedir ajuda com TCC, monografia, ABNT, introducao, referencial teorico, metodologia, trabalhos relacionados, desenvolvimento, conclusao, resumo, referencias, banca ou defesa no contexto do IFRS Osorio ADS.
metadata:
  author: knoba
  version: "1.0"
---

# Monografia TCC IFRS Osorio ADS

Use esta skill quando o trabalho for um TCC em formato de monografia do ADS do IFRS Campus Osorio, sobretudo dentro deste repositorio LaTeX.

## Defaults

- Assuma monografia como formato padrao. So mude para relatorio de desenvolvimento de software se o usuario pedir isso explicitamente.
- Neste repositorio, assuma como arquivo principal `abntex2-modelo-ifrs-osorio-ads-tcc.tex`.
- Nao altere `customizacoes-ifrs-osorio.sty` nem a identidade visual institucional sem pedido explicito.
- O template ja resolve boa parte da formatacao ABNT. Priorize conteudo, coerencia, citacoes e estrutura.

## Read Order

1. Leia `references/ifrs-ads-contexto.md` para regras do curso, TCC, banca e implicacoes locais.
2. Leia `references/abnt-ifrs.md` quando mexer em elementos pre-textuais, pos-textuais, citacoes, referencias, resumos ou detalhes de formatacao.
3. Leia `references/escrita-academica.md` quando for escrever, revisar, reestruturar ou avaliar qualidade textual.
4. Leia os arquivos locais relevantes do projeto antes de editar:
   - `abntex2-modelo-ifrs-osorio-ads-tcc.tex`
   - `elementos-pre-textuais/`
   - `elementos-textuais/introducao.tex`
   - `elementos-textuais/capitulo-1-referencial-teorico.tex`
   - `elementos-textuais/capitulo-2-metodologia.tex`
   - `elementos-textuais/capitulo-3-trabalhos-relacionados.tex`
   - `elementos-textuais/capitulo-4-desenvolvimento.tex`
   - `elementos-textuais/conclusao.tex`
   - `elementos-pos-textuais/referencias.bib`

## Thesis Matrix

Antes de redigir trechos longos, consolide ou atualize esta matriz:

```text
Tema:
Problema de pesquisa:
Objetivo geral:
Objetivos especificos:
Justificativa:
Recorte e contexto:
Metodologia:
Artefato ou intervencao desenvolvida:
Fontes ou dados usados:
Resultados ou evidencias disponiveis:
Limitacoes:
Contribuicoes:
```

Se algum campo estiver sem evidencias, sinalize a lacuna em vez de inventar.

## Workflow

Progress:
- [ ] Confirmar tema, problema, objetivos e formato do TCC.
- [ ] Mapear a matriz para os capitulos do repositorio.
- [ ] Escrever ou revisar o capitulo alvo em portugues academico formal.
- [ ] Checar coerencia entre problema, objetivos, metodo e conclusoes.
- [ ] Conferir citacoes no texto e entradas em `referencias.bib`.
- [ ] Compilar ou, se nao for possivel, ao menos validar os arquivos incluidos e a consistencia estrutural.

## Chapter Map

- `elementos-textuais/introducao.tex`
  Contextualize o tema, apresente problema, justificativa, objetivo geral, objetivos especificos e, se ajudar, a organizacao do trabalho. Nao transforme a introducao em revisao bibliografica extensa.
- `elementos-textuais/capitulo-1-referencial-teorico.tex`
  Reuna conceitos, modelos, legislacao, normas e literatura que sustentam a analise. Organize por eixos conceituais, nao por colagem de resumos.
- `elementos-textuais/capitulo-2-metodologia.tex`
  Explique como o trabalho foi conduzido: tipo de pesquisa, procedimentos, ferramentas, criterios, avaliacao, limitacoes e aspectos eticos quando houver.
- `elementos-textuais/capitulo-3-trabalhos-relacionados.tex`
  Compare trabalhos, sistemas ou estudos relacionados com criterios claros. Evite descrever cada trabalho isoladamente sem analise comparativa.
- `elementos-textuais/capitulo-4-desenvolvimento.tex`
  Mostre o que foi projetado, implementado, configurado, testado e validado. Explique decisoes tecnicas importantes e relacione-as aos objetivos do TCC.
- `elementos-textuais/conclusao.tex`
  Retome objetivos, sintetize contribuicoes, reconheca limitacoes e proponha trabalhos futuros. Nao introduza teoria nova nem resultados nao discutidos antes.

## Writing Rules

- Nunca invente citacoes, resultados, metricas, leis, entrevistas, testes, validacoes ou dados de uso.
- Se faltar evidencia, escreva de forma condicional ou marque como pendencia.
- Prefira paragrafos coesos a listas no texto final da monografia, salvo quando a propria secao pedir enumeracao.
- Mantenha paragrafos equilibrados. No PDF final, prefira paragrafos entre 4 e 5 linhas; 6 linhas sao aceitaveis apenas quando a coesao exigir. Se ficar curto demais ou ultrapassar esse limite sem necessidade, reescreva e redistribua o conteudo.
- Use tom academico, preciso e sem linguagem promocional.
- Diferencie claramente:
  - referencial teorico = o que a literatura diz;
  - metodologia = como este trabalho foi conduzido;
  - desenvolvimento = o que o autor fez e observou;
  - conclusao = o que os resultados permitem afirmar.
- Em trabalhos de continuacao, separe cenario anterior, limitacoes herdadas, decisoes do presente trabalho e resultados do presente trabalho.
- Para projetos em saude, educacao ou servico publico, destaque relevancia social apenas quando houver base documental ou bibliografica.
- Prefira parafrase fundamentada a citacoes diretas longas.
- Sugira figuras, quadros e tabelas quando ajudarem a comparacao, arquitetura, cronologia ou resultados.

## Gotchas

- O curso aceita monografia ou relatorio de desenvolvimento de software, mas este repositorio e este pedido do usuario apontam para monografia.
- O PPC do ADS Osorio exige TCC individual, com orientacao, banca e defesa publica; escreva como trabalho academico formal, nao como documentacao interna de projeto.
- O template ja contem capa, folha de rosto, resumo, abstract, sumario e capitulos separados. Reaproveite essa estrutura em vez de criar outra.
- Nao trate listagem de tecnologias como substituto de analise. Sempre explique criterio de escolha, papel no trabalho e implicacoes.
- Todo objetivo especifico introduzido deve reaparecer no desenvolvimento e ser retomado na conclusao.

## Quality Check

1. O problema de pesquisa esta explicito e compativel com o objetivo geral?
2. Cada objetivo especifico aparece desenvolvido em alguma secao do trabalho?
3. A metodologia descreve o que foi feito de modo verificavel e sem virar diario cronologico?
4. Os trabalhos relacionados comparam ou so descrevem?
5. O desenvolvimento apresenta decisoes e evidencias, e nao apenas catalogo de ferramentas?
6. A conclusao responde aos objetivos e assume limites sem criar afirmacoes novas?
7. Toda citacao do texto possui entrada correspondente em `elementos-pos-textuais/referencias.bib`?
8. Os paragrafos permanecem, em geral, entre 4 e 5 linhas no PDF final, admitindo 6 apenas quando necessario?
9. Se houver compilacao local, o PDF gera sem erros bloqueantes?
