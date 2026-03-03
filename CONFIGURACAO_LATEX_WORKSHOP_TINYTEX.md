# Setup do LaTeX Workshop + TinyTeX (Windows)

Documento baseado no passo a passo executado no projeto, sem etapas extras.

## 1) Links usados

1. Documentação oficial da extensão LaTeX Workshop: https://github.com/James-Yu/LaTeX-Workshop/wiki/Install
2. Guia de instalação oficial: https://github.com/James-Yu/LaTeX-Workshop/wiki/Install
3. TeX Live: https://www.tug.org/texlive/
4. TeX Live para Windows (com links para Linux e macOS): https://www.tug.org/texlive/windows.html
5. Easy install (Windows .exe): https://mirror.ctan.org/systems/texlive/tlnet/install-tl-windows.exe
6. TinyTeX (documentação oficial): https://yihui.org/tinytex/
7. Chocolatey (instalação): https://chocolatey.org/install
8. Update do tlmgr: https://mirror.ctan.org/systems/texlive/tlnet/update-tlmgr-latest.exe

## 2) Primeira tentativa (TeX Live completo)

1. Baixado e executado o instalador `.exe` do TeX Live (easy install).
2. Instalação feita avançando os diálogos sem alterar configurações.
3. Observação: essa abordagem funcionou como caminho inicial, mas demora muito (horas).

## 3) Abordagem usada no final (TinyTeX)

Objetivo: compilar no VS Code, ler o log e instalar pacotes faltantes com `tlmgr install <pkgname>`.

1. Instalar Chocolatey.
2. Abrir PowerShell em modo administrador.
3. Executar:

```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

4. Fechar e abrir novamente o PowerShell em modo administrador.
5. Executar:

```powershell
choco install tinytex
```

6. Responder `A` para aceitar tudo e instalar.
7. Validar instalação:

```powershell
pdflatex -version
```

## 4) VS Code + LaTeX Workshop

1. Instalar a extensão **LaTeX Workshop** no VS Code.
2. Criar a pasta `.vscode` no repositório (se não existir) e criar/editar `.vscode/settings.json` com:

```json
{
  "editor.formatOnSave": true,
  "[latex]": {
    "editor.wordWrap": "on",
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "James-Yu.latex-workshop"
  },
  "latex-workshop.latex.tools": [
    {
      "name": "latexmk",
      "command": "latexmk",
      "args": [
        "-synctex=1",
        "-interaction=nonstopmode",
        "-file-line-error",
        "-pdf",
        "-outdir=%OUTDIR%",
        "%DOC%"
      ]
    }
  ],
  "latex-workshop.latex.recipes": [
    {
      "name": "latexmk 🔃",
      "tools": [
        "latexmk"
      ]
    }
  ]
}
```

3. Abrir o arquivo principal `.tex` (neste caso: `abntex2-modelo-ifrs-osorio-ads-tcc.tex`).
4. Salvar com `Ctrl + S` para disparar a compilação.
5. Ao erro `spawn latexmk ENOENT`, abrir os logs de debug da extensão (popup inferior direito ou aba **TEX**).

## 5) Correções feitas via `tlmgr`

1. Atualizar `tlmgr`:
   - Baixar `update-tlmgr-latest.exe`: https://mirror.ctan.org/systems/texlive/tlnet/update-tlmgr-latest.exe
   - No PowerShell administrador, ir até `Downloads` e executar:

```powershell
.\update-tlmgr-latest.exe --upgrade
```

2. Depois executar:

```powershell
tlmgr update --self --all
```

3. Trocar repositório:

```powershell
tlmgr option repository http://mirror.ctan.org/systems/texlive/tlnet
```

4. Instalar `latexmk`:

```powershell
tlmgr install latexmk
```

5. Instalar com verbose:

```powershell
tlmgr -v install latexmk
```

6. Nos erros seguintes de compilação, instalar os pacotes abaixo:

```powershell
tlmgr install abntex2
tlmgr install memoir
tlmgr install xpatch
tlmgr install textcase
tlmgr install enumitem
tlmgr install tex-gyre
tlmgr install lastpage
tlmgr install pgf
tlmgr install microtype
tlmgr install lipsum
tlmgr install listings
tlmgr install caption
tlmgr install makeindex
tlmgr install babel
tlmgr install babel-portuges
```

## 6) Resultado

Após instalar os pacotes faltantes e ajustar o arquivo principal, o PDF compilou com sucesso.
