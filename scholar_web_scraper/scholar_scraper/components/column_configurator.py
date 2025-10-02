"""
ColumnConfigurator - Componente para configuração dinâmica de colunas.

Este componente permite ao usuário adicionar, remover e configurar
colunas personalizadas para a planilha de resultados.
"""

import reflex as rx

from scholar_scraper.states.app_state import AppState


def column_row(column: dict, index: int) -> rx.Component:
    """
    Componente para uma linha de configuração de coluna.
    
    Args:
        column: Dicionário com dados da coluna
        index: Índice da coluna na lista
        
    Returns:
        Componente com linha de coluna
    """
    return rx.hstack(
        # Número da coluna
        rx.box(
            rx.text(
                str(index + 1),
                font_weight="bold",
                color="gray.600"
            ),
            width="30px",
            text_align="center"
        ),
        
        # Campo nome da coluna
        rx.vstack(
            rx.input(
                placeholder="Nome da coluna",
                value=column["name"],
                on_change=lambda value: AppState.update_column_name(column["id"], value),
                width="200px",
                is_disabled=column.get("is_required", False)
            ),
            width="200px",
            spacing="0"
        ),
        
        # Seletor de tipo
        rx.vstack(
            rx.select(
                ["text", "boolean"],
                value=column["type"],
                on_change=lambda value: AppState.update_column_type(column["id"], value),
                width="120px",
                is_disabled=column.get("is_required", False)
            ),
            width="120px",
            spacing="0"
        ),
        
        # Campo descrição
        rx.vstack(
            rx.input(
                placeholder="Descrição para IA",
                value=column.get("description", ""),
                on_change=lambda value: AppState.update_column_description(column["id"], value),
                width="300px",
                is_disabled=column.get("is_required", False)
            ),
            width="300px",
            spacing="0"
        ),
        
        # Botão remover (apenas para colunas não obrigatórias)
        rx.cond(
            column.get("is_required", False),
            rx.box(
                rx.text("Obrigatória", font_size="1", color="gray.500"),
                width="80px",
                text_align="center"
            ),
            rx.button(
                rx.icon("trash-2", size=16),
                on_click=lambda: AppState.remove_column(column["id"]),
                color_scheme="red",
                variant="ghost",
                size="1",
                width="80px"
            )
        ),
        
        width="100%",
        align_items="center",
        spacing="1",
        padding="0.5rem",
        border_radius="md",
        background_color=rx.cond(
            column.get("is_required", False),
            "gray.50",
            "white"
        )
    )


def column_header() -> rx.Component:
    """
    Cabeçalho da tabela de colunas.
    
    Returns:
        Componente com cabeçalho
    """
    return rx.hstack(
        rx.text("#", width="30px", font_weight="bold", color="gray.700"),
        rx.text("Nome", width="200px", font_weight="bold", color="gray.700"),
        rx.text("Tipo", width="120px", font_weight="bold", color="gray.700"),
        rx.text("Descrição", width="300px", font_weight="bold", color="gray.700"),
        rx.text("Ação", width="80px", font_weight="bold", color="gray.700"),
        width="100%",
        align_items="center",
        spacing="1",
        padding="0.5rem",
        background_color="gray.100",
        border_radius="md"
    )


def column_configurator() -> rx.Component:
    """
    Componente principal de configuração de colunas.
    
    Returns:
        Componente com configurador de colunas
    """
    return rx.vstack(
        # Título da seção
        rx.hstack(
            rx.heading(
                "Configuração de Colunas",
                size="4"
            ),
            rx.spacer(),
            rx.button(
                rx.icon("plus", size=16),
                "Adicionar Coluna",
                on_click=AppState.add_column,
                color_scheme="blue",
                variant="outline",
                size="1"
            ),
            width="100%",
            align_items="center"
        ),
        
        # Cabeçalho da tabela
        column_header(),
        
        # Lista de colunas
        rx.vstack(
            rx.foreach(
                AppState.columns,
                lambda column, index: column_row(column, index)
            ),
            width="100%",
            spacing="1"
        ),
        
        # Mensagem de erro das colunas
        rx.cond(
            AppState.columns_error != "",
            rx.box(
                rx.text(
                    AppState.columns_error,
                    color="red.500",
                    font_size="1"
                ),
                width="100%",
                padding="0.5rem",
                background_color="red.50",
                border_radius="md",
                border="1px solid",
                border_color="red.200"
            ),
            rx.box()
        ),
        
        # Informações sobre tipos de coluna
        rx.box(
            rx.vstack(
                rx.text(
                    "Tipos de Coluna:",
                    font_weight="bold",
                    color="gray.700"
                ),
                rx.hstack(
                    rx.text("• ", color="blue.500", font_weight="bold"),
                    rx.text(
                        "Texto: ",
                        font_weight="bold",
                        color="gray.700"
                    ),
                    rx.text(
                        "Resposta em texto livre (ex: tecnologias, descrição)",
                        color="gray.600"
                    ),
                    spacing="0"
                ),
                rx.hstack(
                    rx.text("• ", color="green.500", font_weight="bold"),
                    rx.text(
                        "Sim/Não: ",
                        font_weight="bold",
                        color="gray.700"
                    ),
                    rx.text(
                        "Resposta booleana (ex: tem aplicativo?)",
                        color="gray.600"
                    ),
                    spacing="0"
                ),
                align_items="flex-start",
                spacing="1"
            ),
            width="100%",
            padding="0.75rem",
            background_color="gray.50",
            border_radius="md",
            border="1px solid",
            border_color="gray.200"
        ),
        
        width="100%",
        spacing="4",
        align_items="flex-start"
    )


def column_configurator_card() -> rx.Component:
    """
    Configurador de colunas dentro de um card.
    
    Returns:
        Componente com configurador em card
    """
    return rx.box(
        column_configurator(),
        width="100%",
        padding="1.5rem",
        background_color="white",
        border_radius="lg",
        box_shadow="0 1px 3px 0 rgba(0, 0, 0, 0.1)",
        border="1px solid",
        border_color="gray.200"
    )