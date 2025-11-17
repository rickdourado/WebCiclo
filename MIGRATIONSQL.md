Explicação da Estrutura
Solução para Múltiplas Turmas
A estrutura resolve seu problema de números diferentes de turmas através de uma relação 1:N (um-para-muitos):

Tabela cursos: Contém os dados gerais do curso
Tabela turmas: Permite múltiplas turmas por curso

Cada turma tem seu próprio endereço, horário e vagas
Usa numero_turma para identificação sequencial
Relaciona-se com curso_id (chave estrangeira)



Exemplo prático (baseado no CSV):

1 Curso: "Curso de Barbeiro Impacta Rio"
4 Turmas diferentes:

Turma 1: Gamboa, 20 vagas, terça-feira
Turma 2: Lapa, 20 vagas, quarta-feira
Turma 3: Jacaré, 20 vagas, terça-feira
Turma 4: Copacabana, 20 vagas, quarta-feira



Vantagens da Estrutura
✅ Flexibilidade: Suporta 1 ou 100 turmas por curso
✅ Normalização: Evita duplicação de dados
✅ Escalabilidade: Fácil adicionar/remover turmas
✅ Consultas eficientes: Views pré-calculadas para performance
✅ Integridade: Triggers mantêm consistência de vagas
✅ Auditoria: Campos de timestamp e status
Estrutura por Modalidade

Presencial: Usa apenas turmas + turmas_dias_semana
Online: Usa apenas plataformas_online + plataformas_dias_semana
Híbrido: Usa ambas as tabelas simultaneamente

Queries de Exemplo
sql-- Buscar todas as turmas de um curso
SELECT * FROM turmas WHERE curso_id = 1;

-- Total de vagas disponíveis de um curso
SELECT SUM(vagas_disponiveis) FROM turmas 
WHERE curso_id = 1 AND status = 'ativa';

-- Cursos com vagas disponíveis
SELECT * FROM vw_cursos_resumo 
WHERE vagas_totais > vagas_ocupadas;

Mapeamento de Campos: HTML → Banco de Dados MySQL
📋 Índice

Tabela: cursos
Tabela: turmas (Presencial/Híbrido)
Tabela: turmas_dias_semana
Tabela: plataformas_online (Online/Híbrido)
Tabela: plataformas_dias_semana
Fluxo de Salvamento


Tabela: cursos
Contém os dados gerais do curso que são únicos e não se repetem
Campo HTML (name)Campo no BancoTipoObservaçõestipo_acaotipo_acaoENUMCurso, Oficina, Palestra, Workshop, EventotitulotituloVARCHAR(255)Nome da ação de formaçãotitulotitulo_originalVARCHAR(255)Cópia para histórico (em caso de duplicação)descricaodescricaoTEXTDescrição melhorada pela IAdescricaodescricao_originalTEXTDescrição original enviadacapa_curso (arquivo)capa_cursoVARCHAR(500)Caminho da imagem salva no servidorinicio_inscricoes_datainicio_inscricoesDATETIMEData de início das inscriçõesfim_inscricoes_datafim_inscricoesDATETIMEData de fim das inscriçõesorgaoorgaoVARCHAR(255)Órgão que oferece o cursotematemaVARCHAR(100)Categoria (Tech, Design, etc.)carga_horariacarga_horariaVARCHAR(100)Carga horária (ex: "40 horas")modalidademodalidadeENUMPresencial, Online ou HíbridoacessibilidadeacessibilidadeENUMacessivel, exclusivo, nao_acessivelrecursos_acessibilidaderecursos_acessibilidadeTEXTDescrição dos recursos (se aplicável)publico_alvopublico_alvoTEXTPúblico-alvo do cursocurso_gratuitocurso_gratuitoENUMsim ou naovalor_curso_inteiravalor_curso_inteiraDECIMAL(10,2)Valor integral (se pago)valor_curso_meiavalor_curso_meiaDECIMAL(10,2)Valor meia-entrada (se pago)requisitos_meiarequisitos_meiaTEXTCondições para meia-entradaoferece_certificadooferece_certificadoENUMsim ou naopre_requisitospre_requisitosTEXTRequisitos para certificadooferece_bolsaoferece_bolsaENUMsim ou naovalor_bolsavalor_bolsaDECIMAL(10,2)Valor da bolsa (se oferece)requisitos_bolsarequisitos_bolsaTEXTRequisitos para bolsainfo_complementaresinfo_complementaresTEXTInformações complementaresinfo_adicionais (textarea)info_adicionaisTEXTInformações adicionais do cursoparceiro_externoparceiro_externoENUMsim ou naoparceiro_nomeparceiro_nomeVARCHAR(255)Nome do parceiro (se aplicável)parceiro_linkparceiro_linkVARCHAR(500)Link do parceiro (se aplicável)parceiro_logo (arquivo)parceiro_logoVARCHAR(500)Logo do parceiro salvo no servidor-statusENUMativo, inativo, rascunho (padrão: ativo)-created_atTIMESTAMPData/hora de criação (automático)-updated_atTIMESTAMPData/hora de atualização (automático)

Tabela: turmas
Para modalidades PRESENCIAL e HÍBRIDO - cada linha = uma turma/unidade
🔄 Campos Array (podem ter múltiplos valores)
Campo HTML (name)Campo no BancoObservaçõesendereco_unidade[]endereco_unidadeARRAY no HTML → Uma linha na tabela turmas para cada valorbairro_unidade[]bairro_unidadeARRAY no HTML → Relacionado ao endereço acimavagas_unidade[]vagas_totaisARRAY no HTML → Número de vagas da turmainicio_aulas_data[]inicio_aulasARRAY no HTML → Data de início das aulasfim_aulas_data[]fim_aulas_dataARRAY no HTML → Data de fim das aulashorario_inicio[]horario_inicioARRAY no HTML → Horário de iníciohorario_fim[]horario_fimARRAY no HTML → Horário de fim-curso_idFK para tabela cursos-numero_turmaSequencial (1, 2, 3, ...)-nome_turmaOpcional (ex: "Turma Manhã")-vagas_ocupadasInicia em 0, atualizado por trigger-vagas_disponiveisCampo calculado (vagas_totais - vagas_ocupadas)-statusativa, inativa, cancelada, concluida
📝 Exemplo Prático de Salvamento
HTML envia (arrays):
endereco_unidade[] = ["Rua A, 10", "Rua B, 20", "Rua C, 30"]
bairro_unidade[] = ["Gamboa", "Lapa", "Jacaré"]
vagas_unidade[] = [20, 20, 20]
Banco salva (3 linhas na tabela turmas):
curso_id | numero_turma | endereco_unidade | bairro_unidade | vagas_totais
---------|--------------|------------------|----------------|-------------
   24    |      1       | Rua A, 10        | Gamboa         |     20
   24    |      2       | Rua B, 20        | Lapa           |     20
   24    |      3       | Rua C, 30        | Jacaré         |     20

Tabela: turmas_dias_semana
Dias da semana de cada turma presencial
Campo HTML (name)Campo no BancoObservaçõesdias_aula_presencial[] (checkboxes)dia_semanaCada checkbox marcado = uma linha na tabela-turma_idFK para tabela turmas
📝 Exemplo Prático
HTML envia (checkboxes marcados para Turma 1):
dias_aula_presencial[] = ["Segunda-feira", "Quarta-feira", "Sexta-feira"]
Banco salva (3 linhas na tabela turmas_dias_semana):
turma_id | dia_semana
---------|-------------
    1    | Segunda-feira
    1    | Quarta-feira
    1    | Sexta-feira

Tabela: plataformas_online
Para modalidades ONLINE e HÍBRIDO
Campo HTML (name)Campo no BancoTipoObservaçõesplataforma_digitalplataforma_digitalVARCHAR(255)Nome da plataforma (Zoom, Meet, etc.)vagas_unidade[] (context: online)vagas_totaisINTTotal de vagas onlineaulas_assincronasaulas_assincronasENUMsim ou naoinicio_aulas_data[] (context: online)inicio_aulasDATEApenas se aulas síncronasfim_aulas_data[] (context: online)fim_aulasDATEApenas se aulas síncronashorario_inicio[] (context: online)horario_inicioTIMEApenas se aulas síncronashorario_fim[] (context: online)horario_fimTIMEApenas se aulas síncronas-curso_idINTFK para tabela cursos-link_acessoVARCHAR(500)Link da sala/plataforma (pode ser adicionado depois)-vagas_ocupadasINTInicia em 0, atualizado por trigger-vagas_disponiveisINTCampo calculado-statusENUMativa, inativa
⚠️ Importante: Aulas Assíncronas

Se aulas_assincronas = "sim": campos de data/horário podem ser NULL
Se aulas_assincronas = "nao": campos de data/horário são obrigatórios


Tabela: plataformas_dias_semana
Dias da semana para aulas online síncronas
Campo HTML (name)Campo no BancoObservaçõesdias_aula_online[] (checkboxes)dia_semanaApenas se aulas síncronas-plataforma_idFK para tabela plataformas_online
Funciona igual à tabela turmas_dias_semana, mas para plataformas online.

🔄 Fluxo de Salvamento no Backend
1️⃣ Salvar na tabela cursos
python# Inserir dados gerais do curso
cursor.execute("""
    INSERT INTO cursos (tipo_acao, titulo, descricao, orgao, tema, ...)
    VALUES (%s, %s, %s, %s, %s, ...)
""", (tipo_acao, titulo, descricao, orgao, tema, ...))

curso_id = cursor.lastrowid  # Pegar ID do curso inserido
2️⃣ Se modalidade = PRESENCIAL ou HÍBRIDO
python# Iterar pelos arrays de unidades
enderecos = request.form.getlist('endereco_unidade[]')
bairros = request.form.getlist('bairro_unidade[]')
vagas = request.form.getlist('vagas_unidade[]')
# ... outros arrays

for i in range(len(enderecos)):
    # Inserir cada turma
    cursor.execute("""
        INSERT INTO turmas 
        (curso_id, numero_turma, endereco_unidade, bairro_unidade, 
         vagas_totais, inicio_aulas, fim_aulas, horario_inicio, horario_fim)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (curso_id, i+1, enderecos[i], bairros[i], vagas[i], ...))
    
    turma_id = cursor.lastrowid
    
    # Inserir dias da semana dessa turma
    dias_marcados = request.form.getlist('dias_aula_presencial[]')
    for dia in dias_marcados:
        cursor.execute("""
            INSERT INTO turmas_dias_semana (turma_id, dia_semana)
            VALUES (%s, %s)
        """, (turma_id, dia))
3️⃣ Se modalidade = ONLINE ou HÍBRIDO
python# Inserir plataforma online
plataforma = request.form.get('plataforma_digital')
vagas_online = request.form.get('vagas_unidade[]')  # contexto online
assincronas = request.form.get('aulas_assincronas')

cursor.execute("""
    INSERT INTO plataformas_online 
    (curso_id, plataforma_digital, vagas_totais, aulas_assincronas, ...)
    VALUES (%s, %s, %s, %s, ...)
""", (curso_id, plataforma, vagas_online, assincronas, ...))

plataforma_id = cursor.lastrowid

# Se aulas síncronas, inserir dias da semana
if assincronas == 'nao':
    dias_online = request.form.getlist('dias_aula_online[]')
    for dia in dias_online:
        cursor.execute("""
            INSERT INTO plataformas_dias_semana (plataforma_id, dia_semana)
            VALUES (%s, %s)
        """, (plataforma_id, dia))

🎯 Resumo Visual: Relacionamentos
cursos (1)
    ├── turmas (N) ────────────► Presencial/Híbrido
    │   └── turmas_dias_semana (N)
    │
    └── plataformas_online (N) ► Online/Híbrido
        └── plataformas_dias_semana (N)
Legenda:

(1) = Um registro
(N) = Múltiplos registros
► = Usado para essa modalidade


📊 Exemplo Completo: Curso Híbrido
Dados do Formulário HTML:
titulo = "Curso de Python"
modalidade = "Híbrido"
endereco_unidade[] = ["Rua A, 10", "Rua B, 20"]
bairro_unidade[] = ["Centro", "Lapa"]
vagas_unidade[] = [30, 30]  (presencial)
plataforma_digital = "Google Meet"
vagas_unidade[] = 100  (online)
Salvamento no Banco:
1 linha em cursos:
id=1, titulo="Curso de Python", modalidade="Híbrido"
2 linhas em turmas:
curso_id=1, numero_turma=1, endereco="Rua A, 10", bairro="Centro", vagas=30
curso_id=1, numero_turma=2, endereco="Rua B, 20", bairro="Lapa", vagas=30
1 linha em plataformas_online:
curso_id=1, plataforma="Google Meet", vagas=100
Total de vagas do curso: 30 + 30 + 100 = 160 vagas

💡 Dicas de Implementação
Validação no Backend
python# Verificar se arrays têm mesmo tamanho
enderecos = request.form.getlist('endereco_unidade[]')
bairros = request.form.getlist('bairro_unidade[]')
vagas = request.form.getlist('vagas_unidade[]')

if len(enderecos) != len(bairros) != len(vagas):
    return "Erro: dados inconsistentes"
Consultar Curso com Turmas
sql-- Buscar curso com todas as turmas
SELECT 
    c.*,
    t.numero_turma,
    t.endereco_unidade,
    t.bairro_unidade,
    t.vagas_totais,
    GROUP_CONCAT(tds.dia_semana) as dias_semana
FROM cursos c
LEFT JOIN turmas t ON c.id = t.curso_id
LEFT JOIN turmas_dias_semana tds ON t.id = tds.turma_id
WHERE c.id = 24
GROUP BY t.id;
Atualizar Curso (Edit)
python# 1. Deletar turmas antigas (cascade deleta dias_semana)
cursor.execute("DELETE FROM turmas WHERE curso_id = %s", (curso_id,))

# 2. Deletar plataformas antigas (cascade deleta dias_semana)
cursor.execute("DELETE FROM plataformas_online WHERE curso_id = %s", (curso_id,))

# 3. Inserir novas turmas/plataformas (mesmo processo do create)

🔍 Campos que NÃO estão no HTML mas são úteis no Banco
CampoTabelaUsostatuscursos, turmas, plataformas_onlineControlar visibilidade/estadovagas_ocupadasturmas, plataformas_onlineAtualizado por triggers ao inscrevervagas_disponiveisturmas, plataformas_onlineCalculado automaticamente (GENERATED)created_atTodasAuditoria/históricoupdated_atTodasControle de alteraçõesnumero_turmaturmasSequencial para identificaçãonome_turmaturmasOpcional, facilita identificaçãolink_acessoplataformas_onlineLink da sala online (pode ser adicionado depois)

✅ Checklist de Implementação

 Criar todas as tabelas no MySQL
 Implementar triggers de atualização de vagas
 Criar views para consultas rápidas
 Adaptar backend para salvar arrays corretamente
 Validar tamanhos dos arrays
 Implementar upload de imagens (capa_curso, parceiro_logo)
 Criar índices para performance
 Testar modalidade Presencial
 Testar modalidade Online
 Testar modalidade Híbrido
 Implementar função de duplicação de curso
 Criar página de edição de curso

