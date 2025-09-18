#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para criar página no Notion com os casos de teste do formulário WebCiclo
"""

import os
import requests
import json
from datetime import datetime

# Configurações do Notion
NOTION_TOKEN = os.getenv('NOTION_TOKEN')
NOTION_DATABASE_ID_FORMULARIO = os.getenv('NOTION_DATABASE_ID_FORMULARIO')

def create_notion_page():
    """Criar página no Notion com os casos de teste"""
    
    if not NOTION_TOKEN or not NOTION_DATABASE_ID_FORMULARIO:
        print("❌ Variáveis de ambiente do Notion não configuradas")
        return False
    
    # URL da API do Notion
    url = f"https://api.notion.com/v1/pages"
    
    # Headers
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    # Conteúdo da página
    page_content = {
        "parent": {
            "database_id": NOTION_DATABASE_ID_FORMULARIO
        },
        "properties": {
            "title": {
                "title": [
                    {
                        "text": {
                            "content": "🧪 Casos de Teste - Formulário WebCiclo"
                        }
                    }
                ]
            }
        },
        "children": [
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "🎯 Objetivo"
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "Validar o funcionamento completo do formulário de criação de curso com 10 casos de teste que cobrem todos os cenários possíveis."
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "📊 Resumo dos Casos"
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "table",
                "table": {
                    "table_width": 6,
                    "has_column_header": True,
                    "has_row_header": False,
                    "children": [
                        {
                            "object": "block",
                            "type": "table_row",
                            "table_row": {
                                "cells": [
                                    [{"text": {"content": "#"}}],
                                    [{"text": {"content": "Nome"}}],
                                    [{"text": {"content": "Modalidade"}}],
                                    [{"text": {"content": "Categoria"}}],
                                    [{"text": {"content": "Tipo"}}],
                                    [{"text": {"content": "Complexidade"}}]
                                ]
                            }
                        },
                        {
                            "object": "block",
                            "type": "table_row",
                            "table_row": {
                                "cells": [
                                    [{"text": {"content": "1"}}],
                                    [{"text": {"content": "Tecnologia Presencial"}}],
                                    [{"text": {"content": "Presencial"}}],
                                    [{"text": {"content": "Tech"}}],
                                    [{"text": {"content": "Gratuito + Certificado"}}],
                                    [{"text": {"content": "Baixa"}}]
                                ]
                            }
                        },
                        {
                            "object": "block",
                            "type": "table_row",
                            "table_row": {
                                "cells": [
                                    [{"text": {"content": "2"}}],
                                    [{"text": {"content": "Marketing Online"}}],
                                    [{"text": {"content": "Online"}}],
                                    [{"text": {"content": "Marketing"}}],
                                    [{"text": {"content": "Pago + Bolsa + Parceiro"}}],
                                    [{"text": {"content": "Alta"}}]
                                ]
                            }
                        },
                        {
                            "object": "block",
                            "type": "table_row",
                            "table_row": {
                                "cells": [
                                    [{"text": {"content": "3"}}],
                                    [{"text": {"content": "Gastronomia Híbrido"}}],
                                    [{"text": {"content": "Híbrido"}}],
                                    [{"text": {"content": "Gastronomia"}}],
                                    [{"text": {"content": "Pago + Não Acessível"}}],
                                    [{"text": {"content": "Média"}}]
                                ]
                            }
                        },
                        {
                            "object": "block",
                            "type": "table_row",
                            "table_row": {
                                "cells": [
                                    [{"text": {"content": "4"}}],
                                    [{"text": {"content": "Design Online Assíncrono"}}],
                                    [{"text": {"content": "Online"}}],
                                    [{"text": {"content": "Design"}}],
                                    [{"text": {"content": "Gratuito"}}],
                                    [{"text": {"content": "Média"}}]
                                ]
                            }
                        },
                        {
                            "object": "block",
                            "type": "table_row",
                            "table_row": {
                                "cells": [
                                    [{"text": {"content": "5"}}],
                                    [{"text": {"content": "Saúde Presencial"}}],
                                    [{"text": {"content": "Presencial"}}],
                                    [{"text": {"content": "Saúde"}}],
                                    [{"text": {"content": "Gratuito + Parceiro"}}],
                                    [{"text": {"content": "Média"}}]
                                ]
                            }
                        },
                        {
                            "object": "block",
                            "type": "table_row",
                            "table_row": {
                                "cells": [
                                    [{"text": {"content": "6"}}],
                                    [{"text": {"content": "Finanças Online"}}],
                                    [{"text": {"content": "Online"}}],
                                    [{"text": {"content": "Finanças"}}],
                                    [{"text": {"content": "Pago + Bolsa"}}],
                                    [{"text": {"content": "Alta"}}]
                                ]
                            }
                        },
                        {
                            "object": "block",
                            "type": "table_row",
                            "table_row": {
                                "cells": [
                                    [{"text": {"content": "7"}}],
                                    [{"text": {"content": "Educação Presencial"}}],
                                    [{"text": {"content": "Presencial"}}],
                                    [{"text": {"content": "Educação"}}],
                                    [{"text": {"content": "Gratuito + Parceiro"}}],
                                    [{"text": {"content": "Média"}}]
                                ]
                            }
                        },
                        {
                            "object": "block",
                            "type": "table_row",
                            "table_row": {
                                "cells": [
                                    [{"text": {"content": "8"}}],
                                    [{"text": {"content": "Cibersegurança Online"}}],
                                    [{"text": {"content": "Online"}}],
                                    [{"text": {"content": "Cibersegurança"}}],
                                    [{"text": {"content": "Gratuito"}}],
                                    [{"text": {"content": "Baixa"}}]
                                ]
                            }
                        },
                        {
                            "object": "block",
                            "type": "table_row",
                            "table_row": {
                                "cells": [
                                    [{"text": {"content": "9"}}],
                                    [{"text": {"content": "Sustentabilidade Híbrido"}}],
                                    [{"text": {"content": "Híbrido"}}],
                                    [{"text": {"content": "Sustentabilidade"}}],
                                    [{"text": {"content": "Pago + Bolsa + Parceiro"}}],
                                    [{"text": {"content": "Alta"}}]
                                ]
                            }
                        },
                        {
                            "object": "block",
                            "type": "table_row",
                            "table_row": {
                                "cells": [
                                    [{"text": {"content": "10"}}],
                                    [{"text": {"content": "Artes Presencial"}}],
                                    [{"text": {"content": "Presencial"}}],
                                    [{"text": {"content": "Artes"}}],
                                    [{"text": {"content": "Pago + Bolsa + Parceiro"}}],
                                    [{"text": {"content": "Alta"}}]
                                ]
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "✅ Validações a Testar"
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "to_do",
                "to_do": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "Campos obrigatórios (13 campos)"
                            }
                        }
                    ],
                    "checked": False
                }
            },
            {
                "object": "block",
                "type": "to_do",
                "to_do": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "Campos condicionais (8 tipos)"
                            }
                        }
                    ],
                    "checked": False
                }
            },
            {
                "object": "block",
                "type": "to_do",
                "to_do": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "Validações de negócio (5 regras)"
                            }
                        }
                    ],
                    "checked": False
                }
            },
            {
                "object": "block",
                "type": "to_do",
                "to_do": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "Modalidades: 4 Presenciais, 4 Online, 2 Híbridos"
                            }
                        }
                    ],
                    "checked": False
                }
            },
            {
                "object": "block",
                "type": "to_do",
                "to_do": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "Cenários: Gratuito/Pago, Com/Sem Bolsa, Com/Sem Parceiro"
                            }
                        }
                    ],
                    "checked": False
                }
            },
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "📁 Arquivos de Referência"
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "casos_teste_formulario.md (dados completos)"
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "dados_teste_estruturados.json (dados estruturados)"
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "instrucoes_teste.md (instruções)"
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "🚀 Como Executar"
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "numbered_list_item",
                "numbered_list_item": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "python app.py"
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "numbered_list_item",
                "numbered_list_item": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "Abrir http://localhost:5001"
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "numbered_list_item",
                "numbered_list_item": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "Copiar dados do arquivo"
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "numbered_list_item",
                "numbered_list_item": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "Preencher formulário manualmente"
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "numbered_list_item",
                "numbered_list_item": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "Testar validações"
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "numbered_list_item",
                "numbered_list_item": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "Documentar resultados"
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "📊 Critérios de Sucesso"
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "to_do",
                "to_do": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "Todos os 10 casos executados"
                            }
                        }
                    ],
                    "checked": False
                }
            },
            {
                "object": "block",
                "type": "to_do",
                "to_do": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "Formulário aceita dados válidos"
                            }
                        }
                    ],
                    "checked": False
                }
            },
            {
                "object": "block",
                "type": "to_do",
                "to_do": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "Validações funcionam corretamente"
                            }
                        }
                    ],
                    "checked": False
                }
            },
            {
                "object": "block",
                "type": "to_do",
                "to_do": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "Arquivos CSV/PDF gerados"
                            }
                        }
                    ],
                    "checked": False
                }
            },
            {
                "object": "block",
                "type": "to_do",
                "to_do": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "Redirecionamento funciona"
                            }
                        }
                    ],
                    "checked": False
                }
            },
            {
                "object": "block",
                "type": "to_do",
                "to_do": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "Mensagens de erro claras"
                            }
                        }
                    ],
                    "checked": False
                }
            }
        ]
    }
    
    try:
        print("🚀 Criando página no Notion...")
        response = requests.post(url, headers=headers, json=page_content)
        
        if response.status_code == 200:
            result = response.json()
            page_id = result['id']
            page_url = result['url']
            
            print("✅ Página criada com sucesso!")
            print(f"📄 ID da página: {page_id}")
            print(f"🔗 URL: {page_url}")
            return True
        else:
            print(f"❌ Erro ao criar página: {response.status_code}")
            print(f"Resposta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return False

def main():
    """Função principal"""
    print("🎓 Uploader de Casos de Teste para Notion")
    print("=" * 50)
    
    # Carregar variáveis de ambiente
    from dotenv import load_dotenv
    load_dotenv('.env')
    
    # Verificar se as variáveis foram carregadas
    global NOTION_TOKEN, NOTION_DATABASE_ID_FORMULARIO
    NOTION_TOKEN = os.getenv('NOTION_TOKEN')
    NOTION_DATABASE_ID_FORMULARIO = os.getenv('NOTION_DATABASE_ID_FORMULARIO')
    
    print(f"🔑 Token carregado: {'✅' if NOTION_TOKEN else '❌'}")
    print(f"🗄️ Database ID carregado: {'✅' if NOTION_DATABASE_ID_FORMULARIO else '❌'}")
    
    # Criar página no Notion
    success = create_notion_page()
    
    if success:
        print("\n🎉 Casos de teste enviados para o Notion com sucesso!")
        print("📋 Acesse sua base 'Formulário de Cadastro de Cursos' para ver a nova página.")
    else:
        print("\n❌ Falha ao enviar para o Notion.")
        print("💡 Verifique as configurações no arquivo .env")

if __name__ == "__main__":
    main()
