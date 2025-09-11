import requests
import os
import json
import sys

"""
Script para testar a conexão com o Notion API

Este script verifica se é possível conectar ao Notion usando o token e database_id fornecidos.
Pode ser usado para diagnosticar problemas de integração entre WebCiclo e Notion.

Uso:
    python test_notion_connection.py [token] [database_id]
    
    Se token e database_id não forem fornecidos, o script tentará carregá-los do arquivo .env
"""

# Função para carregar variáveis de ambiente do arquivo .env
def load_env_vars():
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    env_vars = {}
    
    try:
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        env_vars[key] = value
            return env_vars
        else:
            print(f"Arquivo .env não encontrado em {env_path}")
            return {}
    except Exception as e:
        print(f"Erro ao carregar variáveis de ambiente: {e}")
        return {}

# Função para testar a conexão com a API do Notion
def test_notion_connection(token, database_id):
    print("\n=== Teste de Conexão com Notion API ===")
    print(f"Database ID: {database_id}")
    
    # Configurar headers
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    # Testar acesso à database
    url = f"https://api.notion.com/v1/databases/{database_id}"
    
    try:
        print("\nTentando acessar a database...")
        response = requests.get(url, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Conexão bem-sucedida!")
            data = response.json()
            
            # Extrair título da database
            title = "Sem título"
            if data.get("title") and len(data["title"]) > 0:
                title = data["title"][0].get("plain_text", "Sem título")
            
            print(f"Título da Database: {title}")
            
            # Listar propriedades da database
            print("\nPropriedades da Database:")
            for prop_name, prop_data in data.get("properties", {}).items():
                print(f"  - {prop_name} ({prop_data.get('type', 'desconhecido')})")
            
            # Testar consulta à database
            print("\nTentando consultar registros da database...")
            query_url = f"https://api.notion.com/v1/databases/{database_id}/query"
            query_response = requests.post(query_url, headers=headers, json={"page_size": 3})
            
            if query_response.status_code == 200:
                results = query_response.json().get("results", [])
                print(f"✅ Consulta bem-sucedida! Encontrados {len(results)} registros.")
                
                if results:
                    print("\nPrimeiro registro (amostra):")
                    sample_page = results[0]
                    print(f"  ID: {sample_page.get('id')}")
                    print(f"  URL: {sample_page.get('url')}")
                    print(f"  Criado em: {sample_page.get('created_time')}")
            else:
                print(f"❌ Erro na consulta: {query_response.status_code}")
                print(query_response.text)
            
            return True
        else:
            print("❌ Erro na conexão!")
            print(f"Detalhes: {response.text}")
            
            # Sugestões de solução baseadas no código de erro
            if response.status_code == 401:
                print("\nSugestão: Seu token parece ser inválido ou expirado.")
                print("1. Verifique se copiou o token corretamente")
                print("2. Gere um novo token em https://www.notion.so/my-integrations")
            elif response.status_code == 403:
                print("\nSugestão: Sua integração não tem permissão para acessar esta database.")
                print("1. Verifique se compartilhou a database com sua integração")
                print("2. Abra a database no Notion, clique em 'Share' e adicione sua integração")
            elif response.status_code == 404:
                print("\nSugestão: Database não encontrada.")
                print("1. Verifique se o ID da database está correto")
                print("2. Verifique se a database ainda existe no workspace")
            
            return False
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        return False

# Função principal
def main():
    print("WebCiclo - Teste de Conexão com Notion")
    
    # Verificar argumentos da linha de comando
    if len(sys.argv) == 3:
        token = sys.argv[1]
        database_id = sys.argv[2]
        print("Usando token e database_id fornecidos via linha de comando")
    else:
        # Tentar carregar do arquivo .env
        env_vars = load_env_vars()
        token = env_vars.get("NOTION_TOKEN")
        database_id = env_vars.get("NOTION_DATABASE_ID")
        
        if not token or not database_id:
            print("\n❌ Token ou Database ID não encontrados!")
            print("Por favor, forneça-os como argumentos ou configure no arquivo .env")
            print("\nUso: python test_notion_connection.py [token] [database_id]")
            print("Ou adicione NOTION_TOKEN e NOTION_DATABASE_ID ao arquivo .env")
            return
    
    # Testar conexão
    success = test_notion_connection(token, database_id)
    
    # Exibir resultado final
    print("\n=== Resultado do Teste ===")
    if success:
        print("✅ Conexão com Notion API estabelecida com sucesso!")
        print("Você pode prosseguir com a integração entre WebCiclo e Notion.")
    else:
        print("❌ Falha na conexão com Notion API")
        print("Revise as sugestões acima e tente novamente.")
        print("Para mais informações, consulte o guia de configuração em:")
        print("documentacao/guia_configuracao_notion.md")

# Executar o script
if __name__ == "__main__":
    main()