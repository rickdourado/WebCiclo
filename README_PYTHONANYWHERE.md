# WebApp v4 - Ciclo Carioca (PythonAnywhere)

## 📋 Descrição
Versão v4 do WebApp Ciclo Carioca, otimizada para deployment no PythonAnywhere.
Esta versão é uma réplica da v3, mas configurada especificamente para produção.

## 🚀 Instruções de Deploy no PythonAnywhere

### 1. Upload dos Arquivos
- Faça upload de todos os arquivos para o diretório da sua conta PythonAnywhere
- Estrutura recomendada: `/home/seuusuario/ciclo-carioca-v4/`

### 2. Instalação das Dependências
```bash
pip3.10 install --user -r requirements.txt
```

### 3. Configuração do Web App
1. No dashboard do PythonAnywhere, vá em "Web"
2. Clique em "Add a new web app"
3. Escolha "Manual configuration" e Python 3.10
4. Configure o arquivo WSGI:
   - Caminho: `/home/seuusuario/ciclo-carioca-v4/flask_app.py`
   - Ou copie o conteúdo de `flask_app.py` para o arquivo WSGI gerado

### 4. Configuração de Arquivos Estáticos
- URL: `/static/`
- Directory: `/home/seuusuario/ciclo-carioca-v4/static/`

### 5. Variáveis de Ambiente (Opcional)
No dashboard, em "Files" > "Environment variables":
- `SECRET_KEY`: sua_chave_secreta_personalizada
- `FLASK_ENV`: production

## 📁 Estrutura de Arquivos
```
v4/
├── app.py                    # Aplicação Flask principal
├── flask_app.py             # Arquivo WSGI para PythonAnywhere
├── requirements.txt         # Dependências Python
├── README_PYTHONANYWHERE.md # Este arquivo
├── templates/               # Templates HTML
│   ├── course_form.html
│   ├── course_list.html
│   └── course_success.html
└── static/                  # Arquivos estáticos
    ├── css/
    └── js/
```

## 🔧 Diferenças da v3
- Debug mode desabilitado
- Configuração de SECRET_KEY via variável de ambiente
- Arquivo WSGI específico para PythonAnywhere
- Variável `application` exportada para o WSGI
- Requirements.txt com versões específicas

## 🌐 Funcionalidades
- ✅ Formulário de criação de cursos
- ✅ Listagem de cursos criados
- ✅ Página de sucesso após criação
- ✅ Sistema de mensagens flash
- ✅ Design responsivo
- ✅ Integração com órgãos municipais

## 📞 Suporte
Esta versão foi criada especificamente para o projeto Ciclo Carioca - Pref.rio.
Para suporte técnico, consulte a documentação do PythonAnywhere.

---
*Versão: v4 - Otimizada para PythonAnywhere*  
*Data: Janeiro 2025*