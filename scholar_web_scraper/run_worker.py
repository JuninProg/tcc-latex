#!/usr/bin/env python3
"""
Script para executar worker Celery.

Uso: python run_worker.py
"""

import os
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Carrega variáveis de ambiente
from dotenv import load_dotenv
load_dotenv()

from scholar_scraper.infrastructure.celery_worker import celery_app

if __name__ == "__main__":
    # Configura logging
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("Iniciando Celery Worker...")
    print("CTRL+C para parar")
    
    # Executa worker
    celery_app.worker_main([
        'worker',
        '--loglevel=info',
        '--pool=solo',  # Para desenvolvimento
        '--concurrency=1'
    ])