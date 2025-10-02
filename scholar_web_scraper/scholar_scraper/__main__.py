"""
Ponto de entrada principal da aplicação Scholar Web Scraper.

Executa: python -m scholar_scraper
"""

from scholar_scraper.app import app

if __name__ == "__main__":
    app.compile()
    app.run()