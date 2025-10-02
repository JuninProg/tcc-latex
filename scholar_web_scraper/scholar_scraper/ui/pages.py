"""
Páginas da aplicação Reflex.

Define a página principal que combina todos os componentes
e estados da aplicação.
"""

import reflex as rx
from scholar_scraper.states.app_state import AppState


def index_page() -> rx.Component:
    """
    Página principal da aplicação.
    
    Returns:
        Componente Reflex com interface completa
    """
    return rx.box(
        # Cabeçalho
        rx.box(
            rx.hstack(
                rx.hstack(
                    rx.icon("search", size=32, color="blue.500"),
                    rx.vstack(
                        rx.text(
                            "Scholar Web Scraper",
                            font_size="2xl",
                            font_weight="bold",
                            color="gray.800"
                        ),
                        rx.text(
                            "Busca inteligente de artigos científicos com análise por IA",
                            color="gray.600",
                            font_size="1"
                        ),
                        align_items="flex-start",
                        spacing="0"
                    ),
                    align_items="center",
                    spacing="4"
                ),
                rx.spacer(),
                rx.hstack(
                    rx.text(
                        f"v{AppState.app_version}",
                        color="gray.500",
                        font_size="1"
                    ),
                    align_items="center",
                    spacing="4"
                ),
                width="100%",
                align_items="center"
            ),
            width="100%",
            padding="1.5rem",
            background_color="white",
            border_bottom="1px solid",
            border_color="gray.200",
            box_shadow="0 1px 2px 0 rgba(0, 0, 0, 0.05)"
        ),
        
        # Conteúdo principal
        rx.container(
            rx.vstack(
                # Formulário de busca
                rx.box(
                    rx.vstack(
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
                                placeholder="Ex: machine learning healthcare, sistemas recomendação",
                                value=AppState.query_text,
                                on_change=AppState.update_query_text,
                                width="100%",
                                border_color=rx.cond(
                                    AppState.query_text_error != "",
                                    "red.400",
                                    "gray.300"
                                )
                            ),
                            rx.cond(
                                AppState.query_text_error != "",
                                rx.text(
                                    AppState.query_text_error,
                                    color="red.500",
                                    font_size="1",
                                    margin_top="0.25rem"
                                ),
                                rx.box()
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
                                placeholder="Ex: estudos com implementação prática, não apenas revisões teóricas",
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
                            rx.cond(
                                AppState.filter_criteria_error != "",
                                rx.text(
                                    AppState.filter_criteria_error,
                                    color="red.500",
                                    font_size="1",
                                    margin_top="0.25rem"
                                ),
                                rx.box()
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
                                    max=100,
                                    width="120px"
                                ),
                                rx.text(
                                    "artigos (1-100)",
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
                        
                        width="100%",
                        spacing="3",
                        align_items="flex-start"
                    ),
                    width="100%",
                    padding="1.5rem",
                    background_color="white",
                    border_radius="lg",
                    box_shadow="0 1px 3px 0 rgba(0, 0, 0, 0.1)",
                    border="1px solid",
                    border_color="gray.200"
                ),
                
                # Indicador de progresso (condicional)
                rx.cond(
                    AppState.is_processing,
                    rx.box(
                        rx.vstack(
                            rx.heading(
                                "Processamento em Andamento",
                                size="3",
                                margin_bottom="1rem"
                            ),
                            rx.progress(
                                value=AppState.progress_percentage,
                                width="100%",
                                color_scheme="blue"
                            ),
                            rx.text(
                                AppState.progress_message,
                                color="gray.600",
                                text_align="center",
                                font_size="1"
                            ),
                            width="100%",
                            spacing="4",
                            align_items="center"
                        ),
                        width="100%",
                        padding="1.5rem",
                        background_color="blue.50",
                        border_radius="lg",
                        border="1px solid",
                        border_color="blue.200"
                    ),
                    rx.box()  # Componente vazio quando não está processando
                ),
                
                # Resultado do download (condicional)
                rx.cond(
                    AppState.download_ready,
                    rx.box(
                        rx.vstack(
                            rx.heading(
                                "Processamento Concluído!",
                                size="3",
                                color="green.600",
                                margin_bottom="1rem"
                            ),
                            rx.text(
                                AppState.result_summary,
                                color="gray.700",
                                text_align="center",
                                margin_bottom="1rem"
                            ),
                            rx.button(
                                rx.hstack(
                                    rx.icon("download", size=16),
                                    rx.text("Baixar CSV"),
                                    align_items="center",
                                    spacing="1"
                                ),
                                on_click=AppState.download_excel,
                                color_scheme="green",
                                size="4"
                            ),
                            width="100%",
                            spacing="4",
                            align_items="center"
                        ),
                        width="100%",
                        padding="1.5rem",
                        background_color="green.50",
                        border_radius="lg",
                        border="1px solid",
                        border_color="green.200"
                    ),
                    rx.box()  # Componente vazio quando não há resultado
                ),
                
                # Botões de ação
                rx.box(
                    rx.vstack(
                        # Botões principais
                        rx.hstack(
                            rx.button(
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
                                        rx.text("Processar"),
                                        align_items="center",
                                        spacing="1"
                                    )
                                ),
                                on_click=AppState.submit_search,
                                color_scheme="blue",
                                size="4",
                                width="200px",
                                is_disabled=False,
                                loading=AppState.is_processing
                            ),
                            rx.button(
                                "Debug: Imprimir Valores",
                                on_click=AppState.debug_print_values,
                                color_scheme="gray",
                                size="2",
                                width="150px"
                            ),
                            justify="center",
                            align_items="center",
                            spacing="4"
                        ),
                        
                        width="100%",
                        spacing="4",
                        align_items="center"
                    ),
                    width="100%",
                    padding="1.5rem",
                    background_color="white",
                    border_radius="lg",
                    box_shadow="0 1px 3px 0 rgba(0, 0, 0, 0.1)",
                    border="1px solid",
                    border_color="gray.200"
                ),
                
                width="100%",
                spacing="4",
                padding_y="2rem"
            ),
            max_width="800px"
        ),
        
        # Rodapé
        rx.box(
            rx.text(
                "Desenvolvido como parte do TCC - Análise Inteligente de Artigos Científicos",
                color="gray.500",
                font_size="1",
                text_align="center"
            ),
            width="100%",
            padding="2rem",
            background_color="gray.50",
            border_top="1px solid",
            border_color="gray.200"
        ),
        
        min_height="100vh",
        background_color="gray.50"
    )