#!/usr/bin/env python3
"""
Script de inicialização do Scholar Web Scraper.

Facilita o setup inicial e verificação de dependências.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_python_version():
    """Verifica se a versão do Python é compatível."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ Python 3.9+ é necessário")
        print(f"   Versão atual: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_redis():
    """Verifica se Redis está instalado e rodando."""
    try:
        result = subprocess.run(['redis-cli', 'ping'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0 and 'PONG' in result.stdout:
            print("✅ Redis está rodando")
            return True
        else:
            print("❌ Redis não está respondendo")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ Redis não está instalado ou não está rodando")
        print_redis_install_instructions()
        return False

def print_redis_install_instructions():
    """Imprime instruções de instalação do Redis."""
    system = platform.system()
    print("\n📝 Para instalar o Redis:")
    
    if system == "Darwin":  # macOS
        print("   brew install redis")
        print("   brew services start redis")
    elif system == "Linux":
        print("   sudo apt update && sudo apt install redis-server")
        print("   sudo systemctl start redis-server")
    else:
        print("   Consulte: https://redis.io/download")
    
    print("   Ou use Docker: docker run -d -p 6379:6379 redis:alpine")

def check_chrome():
    """Verifica se Chrome/Chromium está instalado."""
    chrome_paths = [
        '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',  # macOS
        '/usr/bin/google-chrome',  # Linux
        '/usr/bin/chromium-browser',  # Linux
        'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',  # Windows
        'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'  # Windows
    ]
    
    for path in chrome_paths:
        if os.path.exists(path):
            print("✅ Chrome/Chromium encontrado")
            return True
    
    # Tenta executar comando
    try:
        subprocess.run(['google-chrome', '--version'], 
                      capture_output=True, timeout=5)
        print("✅ Chrome encontrado no PATH")
        return True
    except:
        pass
    
    try:
        subprocess.run(['chromium-browser', '--version'], 
                      capture_output=True, timeout=5)
        print("✅ Chromium encontrado no PATH")
        return True
    except:
        pass
    
    print("❌ Chrome/Chromium não encontrado")
    print("   Instale o Google Chrome ou Chromium")
    return False

def check_env_file():
    """Verifica se arquivo .env existe."""
    env_path = Path('.env')
    example_path = Path('.env.example')
    
    if env_path.exists():
        print("✅ Arquivo .env encontrado")
        return True
    elif example_path.exists():
        print("⚠️  Arquivo .env não encontrado")
        print("   Copie .env.example para .env e configure as variáveis")
        return False
    else:
        print("❌ Arquivos .env e .env.example não encontrados")
        return False

def check_gemini_api_key():
    """Verifica se a chave da API do Gemini está configurada."""
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key and api_key != 'your_gemini_api_key_here':
        print("✅ GEMINI_API_KEY configurada")
        return True
    else:
        print("❌ GEMINI_API_KEY não configurada")
        print("   Configure no arquivo .env")
        return False

def install_dependencies():
    """Instala dependências do Python."""
    print("\n📦 Instalando dependências...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'],
                      check=True)
        print("✅ Dependências instaladas")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar dependências")
        return False

def main():
    """Função principal de verificação."""
    print("🔍 Scholar Web Scraper - Verificação de Setup\n")
    
    checks = [
        ("Versão do Python", check_python_version),
        ("Arquivo de configuração", check_env_file),
        ("Redis", check_redis),
        ("Chrome/Chromium", check_chrome),
    ]
    
    all_passed = True
    
    for name, check_func in checks:
        print(f"Verificando {name}...")
        if not check_func():
            all_passed = False
        print()
    
    # Carrega variáveis de ambiente se arquivo existe
    if Path('.env').exists():
        from dotenv import load_dotenv
        load_dotenv()
        
        print("Verificando configurações...")
        if not check_gemini_api_key():
            all_passed = False
        print()
    
    if all_passed:
        print("🎉 Setup completo! Você pode executar:")
        print("   1. python run_worker.py (em um terminal)")
        print("   2. python -m scholar_scraper (em outro terminal)")
    else:
        print("❌ Alguns problemas foram encontrados.")
        print("   Resolva os problemas acima antes de continuar.")
        
        # Oferece instalar dependências se Python está OK
        if check_python_version():
            response = input("\n📦 Deseja instalar as dependências Python? (s/n): ")
            if response.lower() in ['s', 'sim', 'y', 'yes']:
                install_dependencies()

if __name__ == "__main__":
    main()