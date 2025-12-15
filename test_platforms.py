import requests
from bs4 import BeautifulSoup
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("test_platforms")

BASE_URL = "http://127.0.0.1:5001"

def test_create_course_multiple_platforms():
    session = requests.Session()
    
    # 1. Obter página inicial para pegar CSRF token
    logger.info("Obtendo página inicial...")
    try:
        response = session.get(f"{BASE_URL}/")
    except requests.exceptions.ConnectionError:
        logger.error(f"Não foi possível conectar a {BASE_URL}. O servidor está rodando?")
        return

    if response.status_code != 200:
        logger.error(f"Erro ao acessar home: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrf_token'})
    if not csrf_token:
        logger.error("Token CSRF não encontrado!")
        return
    
    csrf_token = csrf_token['value']
    logger.info(f"Token CSRF obtido: {csrf_token[:10]}...")

    # 2. Dados do formulário para 2 plataformas
    # Nota: campos com [] devem ser passados como lista de tuplas para requests lidar com MultiDict corretamente
    payload = [
        ('csrf_token', csrf_token),
        ('tipo_acao', 'Curso'),
        ('titulo', 'Curso Teste Multiplas Plataformas 11'),
        ('descricao', 'Descrição teste auto'),
        ('inicio_inscricoes_data', '2025-01-01'),
        ('fim_inscricoes_data', '2025-01-10'),
        ('orgao', 'Secretaria Municipal de Ciência, Tecnologia e Inovação - SMCT'),
        ('tema', 'Tech'),
        ('carga_horaria', '20h'),
        ('modalidade', 'Online'),
        ('curso_gratuito', 'sim'),
        ('oferece_certificado', 'nao'),
        ('oferece_bolsa', 'nao'),
        ('acessibilidade', 'nao_acessivel'),
        ('publico_alvo', 'Todos'),
        ('parceiro_externo', 'nao'),
        
        # Plataforma 1 (Campos estáticos/singulares)
        ('plataforma_digital', 'Plataforma 1 (Static)'),
        ('aulas_assincronas', 'sim'),
        ('vagas_unidade[]', '50'), # ID vagas_online, name vagas_unidade[]
        
        # Plataforma 2 (Campos dinâmicos)
        ('plataforma_digital[]', 'Plataforma 2 (Dynamic)'),
        ('aulas_assincronas_2', 'sim'),
        ('vagas_unidade[]', '30'), 
        
        # Campos de data vazios/mockados
        ('inicio_aulas_data[]', '2025-02-01'), # P1
        ('fim_aulas_data[]', '2025-03-01'), # P1
        ('inicio_aulas_data[]', '2025-02-01'), # P2
        ('fim_aulas_data[]', '2025-03-01'), # P2
    ]

    logger.info("Enviando POST com 2 plataformas...")
    response = session.post(f"{BASE_URL}/create_course", data=payload)
    
    if response.status_code == 200:
        logger.info("Solicitação enviada. Verificando resultado...")
        # Verificar se redirecionou para sucesso ou mostrou erro
        if "Curso criado com sucesso" in response.text or "Sucesso" in response.text:
             logger.info("✅ Resposta indica sucesso!")
        else:
             logger.warning("⚠️ Resposta pode não indicar sucesso pleno (verifique logs do servidor).")
             # Salvar resposta para debug
             # with open("debug_response.html", "w") as f:
             #    f.write(response.text)
    else:
        logger.error(f"Erro no POST: {response.status_code}")
        logger.error(response.text[:500])

if __name__ == "__main__":
    test_create_course_multiple_platforms()
