import os
import logging
import requests
from dotenv import load_dotenv

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
    # Busca os contatos cadastrados no Supabase usando a API REST nativa (HTTP/1.1)

    # O Supabase expõe automaticamente suas tabelas neste endpoint:
    url = f"{SUPABASE_URL}/rest/v1/contatos"
    
    # Autenticação padrão que o Supabase exige
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }
    
    # Filtros: seleciona as colunas e limita a 3 registros
    params = {
        "select": "nome,telefone",
        "limit": 3
    }

    try:
        logging.info("Conectando ao Supabase via API REST Nativa...")
        resposta = requests.get(url, headers=headers, params=params, timeout=10)
        
        if resposta.status_code == 200:
            return resposta.json()
        else:
            logging.error(f"Erro na API do Supabase: Status {resposta.status_code} - {resposta.text}")
            return []
            
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro de conexão com o Supabase: {e}")
        return []

def enviar_mensagem_zapi(nome: str, telefone: str):
    # Envia a mensagem padronizada via API da Z-API
    
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
    
def main():
    logging.info("Iniciando o fluxo integrado b2bflow...")
    contatos = buscar_contatos()

    if not contatos:
        logging.warning("Nenhum contato encontrado ou falha na consulta ao banco.")
        return

    logging.info(f"{len(contatos)} contato(s) retornado(s). Iniciando envios...")
    
    for contato in contatos:
        nome = contato.get("nome")
        telefone = contato.get("telefone")

        if nome and telefone:
            enviar_mensagem_zapi(nome, telefone)
        else:
            logging.warning(f"Registro inválido ignorado: {contato}")

    logging.info("Fluxo finalizado com sucesso!")

if __name__ == "__main__":
    main()