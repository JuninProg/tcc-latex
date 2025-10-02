"""
Aplicação principal do Scholar Web Scraper.

Este é o ponto de entrada da aplicação Reflex que configura
a app, estados e rotas principais.
"""

import reflex as rx

from .states.app_state import AppState
from .pages import index


# Configuração da aplicação
app = rx.App(
    theme=rx.theme(
        appearance="light",
        has_background=True,
        radius="medium",
        accent_color="blue"
    )
)

# Adiciona as páginas
app.add_page(index, route="/", title="Scholar Web Scraper")