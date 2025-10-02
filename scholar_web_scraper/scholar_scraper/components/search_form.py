"""
SearchForm - Componente do formulário principal de busca.

Este componente renderiza o formulário de entrada com campos para
texto de pesquisa, critérios de filtro e número máximo de resultados.
"""

import reflex as rx
from typing import List

from scholar_scraper.states.app_state import AppState


def search_form() -> rx.Component:
    """
    Componente do formulário principal de busca.
    
    Returns:
        Componente Reflex com formulário de busca
    """
    return rx.vstack(
        # Título da seção
        rx.heading(
            "Configuração de Busca",
            size="4",
            margin_bottom="1rem"
        ),
        
        # Campo de texto de pesquisa
        rx.vstack(
            rx.text(
                "Texto de Pesquisa *",
                font_weight="bold",
                color="gray.700"
            ),
            rx.input(
                placeholder="Ex: aplicativo aleitamento materno",
                value=AppState.query_text,
                on_change=AppState.update_query_text,
                width="100%",
                border_color=rx.cond(
                    AppState.query_text_error != "",
                    "red.400",
                    "gray.300"
                )
            ),
            rx.text(
                AppState.query_text_error,
                color="red.500",
                font_size="1",
                margin_top="0.25rem"
            ),
            width="100%",
            align_items="flex-start",
            spacing="1"
        ),
        
        # Campo de critérios de filtro
        rx.vstack(
            rx.text(
                "Critérios de Filtro *",
                font_weight="bold",
                color="gray.700"
            ),
            rx.text_area(
                placeholder="Ex: artigos que apresentam implementação real de aplicativo, não apenas protótipos",
                value=AppState.filter_criteria,
                on_change=AppState.update_filter_criteria,
                width="100%",
                min_height="80px",
                border_color=rx.cond(
                    AppState.filter_criteria_error != "",
                    "red.400",
                    "gray.300"
                )
            ),
            rx.text(
                AppState.filter_criteria_error,
                color="red.500",
                font_size="1",
                margin_top="0.25rem"
            ),
            width="100%",
            align_items="flex-start",
            spacing="1"
        ),
        
        # Campo de número máximo de resultados
        rx.vstack(
            rx.text(
                "Máximo de Resultados",
                font_weight="bold",
                color="gray.700"
            ),
            rx.hstack(
                rx.input(
                    type="number",
                    value=AppState.max_results,
                    on_change=AppState.update_max_results,
                    min=1,
                    max=5000,
                    width="120px"
                ),
                rx.text(
                    "artigos (1-5000)",
                    color="gray.600",
                    font_size="1"
                ),
                align_items="center",
                spacing="1"
            ),
            width="100%",
            align_items="flex-start",
            spacing="1"
        ),
        
        # Campos de filtro por ano
        rx.vstack(
            rx.text(
                "Filtro por Ano de Publicação",
                font_weight="bold",
                color="gray.700"
            ),
            rx.hstack(
                rx.vstack(
                    rx.text(
                        "Ano Mínimo",
                        font_size="1",
                        color="gray.600"
                    ),
                    rx.input(
                        type="number",
                        value=AppState.year_min,
                        on_change=AppState.update_year_min,
                        min=1900,
                        max=2030,
                        width="100px",
                        placeholder="2022"
                    ),
                    spacing="1",
                    align_items="flex-start"
                ),
                rx.vstack(
                    rx.text(
                        "Ano Máximo",
                        font_size="1",
                        color="gray.600"
                    ),
                    rx.input(
                        type="number",
                        value=AppState.year_max,
                        on_change=AppState.update_year_max,
                        min=1900,
                        max=2030,
                        width="100px",
                        placeholder="2025"
                    ),
                    spacing="1",
                    align_items="flex-start"
                ),
                spacing="4",
                align_items="flex-start"
            ),
            rx.text(
                "Deixe em branco para não filtrar por ano",
                color="gray.500",
                font_size="1",
                font_style="italic"
            ),
            width="100%",
            align_items="flex-start",
            spacing="1"
        ),
        
        # Informações de ajuda
        rx.box(
            rx.text(
                "💡 Dica: Seja específico nos critérios de filtro para obter resultados mais relevantes.",
                color="blue.600",
                font_size="1",
                font_style="italic"
            ),
            width="100%",
            padding="0.75rem",
            background_color="blue.50",
            border_radius="md",
            border="1px solid",
            border_color="blue.200"
        ),
        
        width="100%",
        spacing="3",
        align_items="flex-start"
    )


def search_form_card() -> rx.Component:
    """
    Formulário de busca dentro de um card.
    
    Returns:
        Componente com formulário em card
    """
    return rx.box(
        search_form(),
        width="100%",
        padding="1.5rem",
        background_color="white",
        border_radius="lg",
        box_shadow="0 1px 3px 0 rgba(0, 0, 0, 0.1)",
        border="1px solid",
        border_color="gray.200"
    )