import logging
import os

def setup_logging():
    # Garante que o diretório 'logs/' exista
    os.makedirs("logs", exist_ok=True)

    # Configuração de logging com dois handlers: console e arquivo
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        handlers=[
            logging.StreamHandler(),  # Exibe no terminal
            logging.FileHandler("logs/app.log", encoding="utf-8")  # Salva em arquivo
        ]
    )
