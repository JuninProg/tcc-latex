"""Configuração do Reflex para Scholar Web Scraper."""

import reflex as rx

config = rx.Config(
    app_name="scholar_scraper",
    backend_host="0.0.0.0", 
    backend_port=8000,
    frontend_port=3000,
)