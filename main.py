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

def buscar_contatos() -> list:
    # Busca os contatos cadastrados no Supabase limitando a 3 registros
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        logging.info("Conectando ao Supabase para buscar contatos...")
        
        resposta = supabase.table("contatos").select("nome, telefone").limit(3).execute()
        return resposta.data
    except Exception as e:
        logging.error(f"Erro ao buscar dados no Supabase: {e}")
        return []

def enviar_mensagem_zapi(nome: str, telefone: str):
    """Envia a mensagem padronizada via API da Z-API."""
    url = f"https://api.z-api.io/instances/{ZAPI_INSTANCE}/token/{ZAPI_TOKEN}/send-text"
    
    headers = {"Content-Type": "application/json"}
    
    payload = {
        "phone": telefone,
        "message": f"Olá, {nome} tudo bem com você?"
    }

    try:
        logging.info(f"Disparando mensagem para {nome} ({telefone})...")
        resposta = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if resposta.status_code in [200, 201]:
            logging.info(f"Sucesso: Mensagem enviada para {nome}!")
        else:
            logging.error(f"Falha ao enviar para {nome}. Status: {resposta.status_code}")
            
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro de conexão com a Z-API ao tentar enviar para {nome}: {e}")