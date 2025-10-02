"""
ActionButtons - Componente com botões de ação da aplicação.

Este componente gerencia os botões principais: processar, cancelar,
baixar resultado e limpar formulário.
"""

import reflex as rx

from scholar_scraper.states.app_state import AppState


def main_action_button() -> rx.Component:
    """
    Botão principal de ação (Processar/Tentar Novamente).
    
    Returns:
        Componente do botão principal
    """
    return rx.button(
        rx.cond(
            AppState.is_processing,
            rx.hstack(
                rx.spinner(size="1"),
                rx.text("Processando..."),
                align_items="center",
                spacing="1"
            ),
            rx.hstack(
                rx.icon("search", size=16),
                rx.text(AppState.get_main_action_text),
                align_items="center",
                spacing="1"
            )
        ),
        on_click=AppState.submit_search,
        color_scheme=rx.cond(
            AppState.has_error,
            "orange",
            "blue"
        ),
        size="4",
        width="200px",
        is_disabled=False,
        loading=AppState.is_processing
    )


def cancel_button() -> rx.Component:
    """
    Botão para cancelar processamento.
    
    Returns:
        Componente do botão cancelar
    """
    return rx.cond(
        AppState.is_processing,
        rx.button(
            rx.icon("x", size=16),
            "Cancelar",
            on_click=AppState.cancel_job,
            color_scheme="red",
            variant="outline",
            size="4",
            width="150px"
        ),
        rx.box()
    )


def download_button() -> rx.Component:
    """
    Botão para baixar resultado.
    
    Returns:
        Componente do botão download
    """
    return rx.cond(
        AppState.result_ready & AppState.download_ready,
        rx.button(
            rx.icon("download", size=16),
            "Baixar CSV",
            on_click=AppState.initiate_download,
            color_scheme="green",
            size="4",
            width="200px"
        ),
        rx.box()
    )

def download_latest_button() -> rx.Component:
    """
    Botão para baixar o CSV mais recente (sempre disponível).
    
    Returns:
        Componente do botão download
    """
    return rx.button(
        rx.icon("download", size=16),
        "Baixar Último CSV",
        on_click=AppState.download_latest_csv,
        color_scheme="blue",
        size="4",
        width="200px"
    )


def reset_button() -> rx.Component:
    """
    Botão para limpar/resetar formulário.
    
    Returns:
        Componente do botão reset
    """
    return rx.button(
        rx.icon("refresh-cw", size=16),
        "Nova Busca",
        on_click=AppState.reset_application,
        variant="ghost",
        size="3",
        color_scheme="gray"
    )


def help_button() -> rx.Component:
    """
    Botão para mostrar/ocultar ajuda.
    
    Returns:
        Componente do botão ajuda
    """
    return rx.button(
        rx.icon("help-circle", size=16),
        on_click=AppState.toggle_help,
        variant="ghost",
        size="3",
        color_scheme="gray",
        title="Ajuda"
    )


def action_buttons() -> rx.Component:
    """
    Conjunto principal de botões de ação.
    
    Returns:
        Componente com todos os botões
    """
    return rx.vstack(
        # Botões principais
        rx.hstack(
            main_action_button(),
            cancel_button(),
            download_button(),
            download_latest_button(),
            justify="center",
            align_items="center",
            spacing="4",
            wrap="wrap"
        ),
        
        # Botões secundários
        rx.hstack(
            reset_button(),
            help_button(),
            justify="center",
            align_items="center",
            spacing="4"
        ),
        
        width="100%",
        spacing="4",
        align_items="center"
    )


def floating_action_bar() -> rx.Component:
    """
    Barra de ação flutuante (sticky).
    
    Returns:
        Componente com barra flutuante
    """
    return rx.box(
        action_buttons(),
        width="100%",
        padding="1.5rem",
        background_color="white",
        border_top="1px solid",
        border_color="gray.200",
        box_shadow="0 -2px 4px 0 rgba(0, 0, 0, 0.05)",
        position="sticky",
        bottom="0",
        z_index="10"
    )


def action_buttons_card() -> rx.Component:
    """
    Botões de ação dentro de um card.
    
    Returns:
        Componente com botões em card
    """
    return rx.box(
        action_buttons(),
        width="100%",
        padding="1.5rem",
        background_color="white",
        border_radius="lg",
        box_shadow="0 1px 3px 0 rgba(0, 0, 0, 0.1)",
        border="1px solid",
        border_color="gray.200"
    )


def download_info_display() -> rx.Component:
    """
    Informações detalhadas sobre o download.
    
    Returns:
        Componente com info do download
    """
    return rx.cond(
        AppState.download_ready,
        rx.box(
            rx.vstack(
                rx.text(
                    "Arquivo Pronto para Download",
                    font_weight="bold",
                    color="green.700"
                ),
                rx.hstack(
                    rx.text("📄", font_size="4"),
                    rx.vstack(
                        rx.text(
                            AppState.download_filename,
                            font_weight="medium",
                            color="gray.700"
                        ),
                        rx.text(
                            AppState.get_file_size_display,
                            color="gray.500",
                            font_size="1"
                        ),
                        align_items="flex-start",
                        spacing="0"
                    ),
                    align_items="center",
                    spacing="1"
                ),
                rx.cond(
                    AppState.generated_at != "",
                    rx.text(
                        f"Gerado em: {AppState.generated_at}",
                        color="gray.500",
                        font_size="1"
                    ),
                    rx.box()
                ),
                download_button(),
                align_items="flex-start",
                spacing="2"
            ),
            width="100%",
            padding="1rem",
            background_color="green.50",
            border_radius="md",
            border="1px solid",
            border_color="green.200"
        ),
        rx.box()
    )