import os
import logging
import requests
from dotenv import load_dotenv
from supabase import create_client, Client

# Configuração de Logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Carrega as variáveis de ambiente
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
ZAPI_INSTANCE = os.getenv("ZAPI_INSTANCE")
ZAPI_TOKEN = os.getenv("ZAPI_TOKEN")

# Validação
if not all([SUPABASE_URL, SUPABASE_KEY, ZAPI_INSTANCE, ZAPI_TOKEN]):
    logging.error("Erro: Variáveis de ambiente ausentes no arquivo .env.")
    exit(1)