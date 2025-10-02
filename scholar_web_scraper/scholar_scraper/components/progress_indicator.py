"""
ProgressIndicator - Componente para exibir progresso do processamento.

Este componente mostra o status atual, progresso e informações
detalhadas sobre o processamento dos artigos.
"""

import reflex as rx

from scholar_scraper.states.app_state import AppState


def progress_bar() -> rx.Component:
    """
    Barra de progresso animada.
    
    Returns:
        Componente com barra de progresso
    """
    return rx.box(
        # Container da barra
        rx.box(
            # Barra de progresso preenchida
            rx.box(
                width=f"{AppState.progress_percentage}%",
                height="100%",
                background=rx.cond(
                    AppState.has_error,
                    "linear-gradient(90deg, #fed7d7, #fc8181)",
                    "linear-gradient(90deg, #bee3f8, #4299e1)"
                ),
                border_radius="full",
                transition="all 0.3s ease"
            ),
            width="100%",
            height="8px",
            background_color="gray.200",
            border_radius="full",
            overflow="hidden"
        ),
        
        # Texto de porcentagem
        rx.text(
            f"{AppState.progress_percentage:.0f}%",
            font_size="1",
            font_weight="bold",
            color=rx.cond(
                AppState.has_error,
                "red.600",
                "blue.600"
            ),
            text_align="center",
            margin_top="0.5rem"
        ),
        
        width="100%"
    )


def processing_status() -> rx.Component:
    """
    Status detalhado do processamento.
    
    Returns:
        Componente com status
    """
    return rx.vstack(
        # Status principal
        rx.hstack(
            rx.icon(
                rx.cond(
                    AppState.has_error,
                    "alert-circle",
                    rx.cond(
                        AppState.result_ready,
                        "check-circle",
                        "clock"
                    )
                ),
                size=20,
                color=rx.cond(
                    AppState.has_error,
                    "red.500",
                    rx.cond(
                        AppState.result_ready,
                        "green.500",
                        "blue.500"
                    )
                )
            ),
            rx.text(
                AppState.processing_status,
                font_weight="bold",
                color=rx.cond(
                    AppState.has_error,
                    "red.700",
                    rx.cond(
                        AppState.result_ready,
                        "green.700",
                        "blue.700"
                    )
                )
            ),
            align_items="center",
            spacing="1"
        ),
        
        # Passo atual
        rx.cond(
            AppState.current_step != "",
            rx.text(
                AppState.current_step,
                color="gray.600",
                font_size="1"
            ),
            rx.box()
        ),
        
        # Informações de artigos
        rx.cond(
            AppState.total_articles > 0,
            rx.hstack(
                rx.text(
                    "Artigos:",
                    font_weight="bold",
                    color="gray.700"
                ),
                rx.text(
                    f"{AppState.processed_articles}/{AppState.total_articles}",
                    color="gray.600"
                ),
                spacing="1"
            ),
            rx.box()
        ),
        
        # Última atualização
        rx.cond(
            AppState.last_update != "",
            rx.text(
                f"Última atualização: {AppState.last_update}",
                color="gray.500",
                font_size="xs"
            ),
            rx.box()
        ),
        
        width="100%",
        align_items="flex-start",
        spacing="1"
    )


def error_display() -> rx.Component:
    """
    Exibição de mensagens de erro.
    
    Returns:
        Componente com erro
    """
    return rx.cond(
        AppState.has_error,
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.icon("alert-triangle", size=20, color="red.500"),
                    rx.text(
                        "Erro no Processamento",
                        font_weight="bold",
                        color="red.700"
                    ),
                    align_items="center",
                    spacing="1"
                ),
                rx.text(
                    AppState.error_message,
                    color="red.600",
                    font_size="1"
                ),
                rx.button(
                    "Tentar Novamente",
                    on_click=AppState.clear_error,
                    color_scheme="red",
                    variant="outline",
                    size="1"
                ),
                align_items="flex-start",
                spacing="2"
            ),
            width="100%",
            padding="1rem",
            background_color="red.50",
            border_radius="md",
            border="1px solid",
            border_color="red.200"
        ),
        rx.box()
    )


def success_display() -> rx.Component:
    """
    Exibição de sucesso com opção de download.
    
    Returns:
        Componente com sucesso
    """
    return rx.cond(
        AppState.result_ready,
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.icon("check-circle", size=20, color="green.500"),
                    rx.text(
                        "Processamento Concluído!",
                        font_weight="bold",
                        color="green.700"
                    ),
                    align_items="center",
                    spacing="1"
                ),
                rx.text(
                    "Sua planilha está pronta para download.",
                    color="green.600",
                    font_size="1"
                ),
                rx.button(
                    rx.icon("download", size=16),
                    "Baixar Planilha",
                    on_click=AppState.initiate_download,
                    color_scheme="green",
                    size="3"
                ),
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


def progress_indicator() -> rx.Component:
    """
    Componente principal do indicador de progresso.
    
    Returns:
        Componente completo do progresso
    """
    return rx.vstack(
        # Título
        rx.heading(
            "Status do Processamento",
            size="3",
            margin_bottom="1rem"
        ),
        
        # Barra de progresso (apenas durante processamento)
        rx.cond(
            AppState.is_processing,
            progress_bar(),
            rx.box()
        ),
        
        # Status detalhado
        processing_status(),
        
        # Exibição de erro
        error_display(),
        
        # Exibição de sucesso
        success_display(),
        
        width="100%",
        spacing="4",
        align_items="flex-start"
    )


def progress_indicator_card() -> rx.Component:
    """
    Indicador de progresso dentro de um card.
    
    Returns:
        Componente com indicador em card
    """
    return rx.cond(
        # Só mostra o card se houver algum processamento ou resultado
        AppState.is_processing | AppState.result_ready | AppState.has_error,
        rx.box(
            progress_indicator(),
            width="100%",
            padding="1.5rem",
            background_color="white",
            border_radius="lg",
            box_shadow="0 1px 3px 0 rgba(0, 0, 0, 0.1)",
            border="1px solid",
            border_color="gray.200"
        ),
        rx.box()
    )