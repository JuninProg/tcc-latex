"""
Páginas da aplicação Reflex.

Este módulo define as páginas principais da aplicação,
incluindo a página única que combina todos os componentes.
"""

import reflex as rx

from scholar_scraper.states.app_state import AppState
from scholar_scraper.components.search_form import search_form_card
from scholar_scraper.components.column_configurator import column_configurator_card
from scholar_scraper.components.progress_indicator import progress_indicator_card
from scholar_scraper.components.action_buttons import action_buttons_card, download_info_display


def help_modal() -> rx.Component:
    """
    Modal de ajuda com instruções de uso.
    
    Returns:
        Componente do modal de ajuda
    """
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                "Ajuda - Scholar Web Scraper",
                margin_bottom="1rem"
            ),
            rx.dialog.description(
                rx.vstack(
                    rx.vstack(
                        # Passo 1
                        rx.box(
                            rx.hstack(
                                rx.text("1.", font_weight="bold", color="blue.600", font_size="4"),
                                rx.text("Configure sua busca", font_weight="bold"),
                                align_items="center",
                                spacing="1"
                            ),
                            rx.text(
                                "• Insira o texto de pesquisa (ex: 'aplicativo aleitamento materno')",
                                margin_left="1.5rem"
                            ),
                            rx.text(
                                "• Defina critérios específicos de filtro para a IA",
                                margin_left="1.5rem"
                            ),
                            rx.text(
                                "• Ajuste o número máximo de resultados (1-100)",
                                margin_left="1.5rem"
                            ),
                            spacing="1"
                        ),
                        
                        # Passo 2
                        rx.box(
                            rx.hstack(
                                rx.text("2.", font_weight="bold", color="blue.600", font_size="4"),
                                rx.text("Personalize as colunas", font_weight="bold"),
                                align_items="center",
                                spacing="1"
                            ),
                            rx.text(
                                "• Adicione colunas personalizadas conforme necessário",
                                margin_left="1.5rem"
                            ),
                            rx.text(
                                "• Escolha entre tipo 'Texto' ou 'Sim/Não'",
                                margin_left="1.5rem"
                            ),
                            rx.text(
                                "• Forneça descrições claras para orientar a IA",
                                margin_left="1.5rem"
                            ),
                            spacing="1"
                        ),
                        
                        # Passo 3
                        rx.box(
                            rx.hstack(
                                rx.text("3.", font_weight="bold", color="blue.600", font_size="4"),
                                rx.text("Execute o processamento", font_weight="bold"),
                                align_items="center",
                                spacing="1"
                            ),
                            rx.text(
                                "• Clique em 'Processar' para iniciar",
                                margin_left="1.5rem"
                            ),
                            rx.text(
                                "• Acompanhe o progresso em tempo real",
                                margin_left="1.5rem"
                            ),
                            rx.text(
                                "• Aguarde a conclusão do processamento",
                                margin_left="1.5rem"
                            ),
                            spacing="1"
                        ),
                        
                        # Passo 4
                        rx.box(
                            rx.hstack(
                                rx.text("4.", font_weight="bold", color="blue.600", font_size="4"),
                                rx.text("Baixe os resultados", font_weight="bold"),
                                align_items="center",
                                spacing="1"
                            ),
                            rx.text(
                                "• Baixe a planilha Excel com os resultados",
                                margin_left="1.5rem"
                            ),
                            rx.text(
                                "• Analise os artigos filtrados pela IA",
                                margin_left="1.5rem"
                            ),
                            spacing="1"
                        ),
                        
                        # Dicas
                        rx.box(
                            rx.text("💡 Dicas Importantes:", font_weight="bold", color="orange.600"),
                            rx.text(
                                "• Seja específico nos critérios de filtro para melhores resultados"
                            ),
                            rx.text(
                                "• O processamento pode levar alguns minutos dependendo do número de artigos"
                            ),
                            rx.text(
                                "• Artigos com PDFs disponíveis terão análise mais detalhada"
                            ),
                            rx.text(
                                "• Arquivos ficam disponíveis por 24 horas após geração"
                            ),
                            background_color="orange.50",
                            padding="1rem",
                            border_radius="md",
                            border="1px solid",
                            border_color="orange.200",
                            spacing="1"
                        ),
                        
                        align_items="flex-start",
                        spacing="3"
                    )
                ),
                rx.dialog.close(
                    rx.button(
                        "Entendi",
                        on_click=AppState.toggle_help,
                        color_scheme="blue"
                    )
                )
            )
        ),
        open=AppState.show_help
    )


def header() -> rx.Component:
    """
    Cabeçalho da aplicação.
    
    Returns:
        Componente do cabeçalho
    """
    return rx.box(
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
                rx.button(
                    rx.icon("help-circle", size=16),
                    "Ajuda",
                    on_click=AppState.toggle_help,
                    variant="ghost",
                    color_scheme="blue"
                ),
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
    )


def footer() -> rx.Component:
    """
    Rodapé da aplicação.
    
    Returns:
        Componente do rodapé
    """
    return rx.box(
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
    )


@rx.page(route="/", title="Scholar Web Scraper")
def index() -> rx.Component:
    """
    Página principal da aplicação.
    
    Returns:
        Componente da página principal
    """
    return rx.box(
        # Cabeçalho
        header(),
        
        # Conteúdo principal
        rx.container(
            rx.vstack(
                # Formulário de busca
                search_form_card(),
                
                # Configurador de colunas
                column_configurator_card(),
                
                # Botões de ação
                action_buttons_card(),
                
                # Indicador de progresso
                progress_indicator_card(),
                
                # Informações de download
                download_info_display(),
                
                width="100%",
                spacing="4",
                padding_y="2rem"
            ),
            max_width="1200px"
        ),
        
        # Rodapé
        footer(),
        
        # Modal de ajuda
        help_modal(),
        
        min_height="100vh",
        background_color="gray.50"
    )