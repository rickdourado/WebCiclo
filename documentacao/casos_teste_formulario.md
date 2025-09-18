# Casos de Teste para Formulário de Criação de Curso

## Análise do Formulário

O formulário possui os seguintes campos principais:
- **Informações Básicas**: Título, Descrição, Órgão, Categoria, Modalidade
- **Período de Inscrições**: Data de início e fim
- **Modalidade**: Presencial, Online ou Híbrido (com subformulários específicos)
- **Acessibilidade**: Opções de acessibilidade e recursos
- **Público-alvo**: Descrição do público
- **Valores**: Curso gratuito ou pago (com valores inteira/meia)
- **Certificado**: Oferece certificado e pré-requisitos
- **Bolsa**: Oferece bolsa e requisitos
- **Informações Complementares**: Dados adicionais para inscrição
- **Parceiro Externo**: Informações do parceiro (opcional)

---

## 10 Casos de Teste Aleatórios

### **Caso de Teste 1: Curso Presencial de Tecnologia**
```
Nome do Curso: Introdução à Programação Python
Descrição: Curso básico de programação em Python para iniciantes, abordando conceitos fundamentais de programação, estruturas de dados e desenvolvimento de aplicações simples.
Início das inscrições: 2025-01-15
Fim das inscrições: 2025-02-15
Órgão: Secretaria Municipal de Ciência, Tecnologia e Inovação - SMCT
Categoria: Tech
Modalidade: Presencial
Endereço da unidade: Rua da Liberdade, 123
Bairro: Centro
Número de vagas: 30
Carga Horária: 40 horas
Início das aulas: 2025-02-20
Fim das aulas: 2025-03-20
Horário-Início: 09:00
Horário-Fim: 12:00
Dias de aula: Segunda-feira, Quarta-feira
Acessibilidade: Acessível para pessoas com deficiência
Recursos de Acessibilidade: Rampa de acesso, elevador, material em formato digital
Público-alvo: Servidores públicos interessados em programação
O curso é gratuito?: SIM
Oferece Certificado: SIM
Pré-requisitos para Recebimento de Certificados: Frequência mínima de 75% e aprovação em avaliação final
Oferece Bolsa: NÃO
Informações Complementares: Escolaridade mínima: Ensino Médio completo
Informações adicionais do curso?: NÃO
CURSO OFERECIDO POR PARCEIRO EXTERNO?: NÃO
```

### **Caso de Teste 2: Curso Online de Marketing Digital**
```
Nome do Curso: Marketing Digital para Pequenas Empresas
Descrição: Estratégias de marketing digital para empreendedores e pequenas empresas, incluindo redes sociais, SEO e publicidade online.
Início das inscrições: 2025-01-20
Fim das inscrições: 2025-02-20
Órgão: Secretaria Municipal de Desenvolvimento Econômico – SMDE
Categoria: Marketing
Modalidade: Online
Plataforma Digital: Google Meet
Número de vagas: 50
Carga Horária: 60 horas
Aulas Assíncronas?: NÃO
Início das aulas: 2025-03-01
Fim das aulas: 2025-04-15
Horário-Início: 19:00
Horário-Fim: 21:00
Dias de aula: Terça-feira, Quinta-feira
Acessibilidade: Acessível para pessoas com deficiência
Recursos de Acessibilidade: Legendas automáticas, material em formato acessível
Público-alvo: Empreendedores e pequenos empresários
O curso é gratuito?: NÃO
Valor INTEIRA (R$): 150,00
Valor MEIA (R$): 75,00
Condições para obtenção de meia-entrada: Estudantes e idosos acima de 60 anos
Oferece Certificado: SIM
Pré-requisitos para Recebimento de Certificados: Frequência mínima de 80% e entrega de projeto final
Oferece Bolsa: SIM
Valor da Bolsa (R$): 100,00
Requisitos para a Obtenção da Bolsa: Renda familiar até 2 salários mínimos
Informações Complementares: Necessário ter computador com acesso à internet
Informações adicionais do curso?: SIM
Informações Adicionais do Curso: Curso inclui material didático digital e certificado reconhecido pelo mercado
CURSO OFERECIDO POR PARCEIRO EXTERNO?: SIM
Nome do Parceiro: Instituto de Marketing Digital
Link do Parceiro: https://www.imd.com.br
```

### **Caso de Teste 3: Curso Híbrido de Gastronomia**
```
Nome do Curso: Culinária Brasileira Tradicional
Descrição: Aprenda técnicas de preparo de pratos tradicionais da culinária brasileira, com foco em ingredientes regionais e métodos de cocção.
Início das inscrições: 2025-02-01
Fim das inscrições: 2025-03-01
Órgão: Secretaria Municipal de Cultura - SMC
Categoria: Gastronomia
Modalidade: Híbrido
Endereço da unidade: Av. Rio Branco, 456
Bairro: Cinelândia
Número de vagas: 20
Carga Horária: 80 horas
Início das aulas: 2025-03-15
Fim das aulas: 2025-05-15
Horário-Início: 14:00
Horário-Fim: 18:00
Dias de aula: Sábado
Acessibilidade: Não acessível para Pessoas com Deficiência
Público-alvo: Pessoas interessadas em gastronomia e cultura brasileira
O curso é gratuito?: NÃO
Valor INTEIRA (R$): 300,00
Valor MEIA (R$): 150,00
Condições para obtenção de meia-entrada: Estudantes e profissionais da área de gastronomia
Oferece Certificado: SIM
Pré-requisitos para Recebimento de Certificados: Frequência mínima de 70% e participação em todas as aulas práticas
Oferece Bolsa: NÃO
Informações Complementares: Trazer avental e utensílios básicos de cozinha
Informações adicionais do curso?: SIM
Informações Adicionais do Curso: Curso inclui ingredientes para aulas práticas e visita a restaurantes tradicionais
CURSO OFERECIDO POR PARCEIRO EXTERNO?: NÃO
```

### **Caso de Teste 4: Curso Online Assíncrono de Design**
```
Nome do Curso: Design Gráfico com Canva
Descrição: Aprenda a criar materiais gráficos profissionais usando a plataforma Canva, incluindo logos, banners, posts para redes sociais e apresentações.
Início das inscrições: 2025-01-10
Fim das inscrições: 2025-01-25
Órgão: Secretaria Municipal de Cultura - SMC
Categoria: Design
Modalidade: Online
Plataforma Digital: Plataforma própria
Número de vagas: 100
Carga Horária: 30 horas
Aulas Assíncronas?: SIM
Acessibilidade: Acessível para pessoas com deficiência
Recursos de Acessibilidade: Material em formato acessível e suporte por chat
Público-alvo: Profissionais de comunicação, estudantes e interessados em design
O curso é gratuito?: SIM
Oferece Certificado: SIM
Pré-requisitos para Recebimento de Certificados: Conclusão de todos os módulos e entrega de portfólio final
Oferece Bolsa: NÃO
Informações Complementares: Necessário ter conta no Canva (gratuita)
Informações adicionais do curso?: NÃO
CURSO OFERECIDO POR PARCEIRO EXTERNO?: NÃO
```

### **Caso de Teste 5: Curso Presencial de Saúde**
```
Nome do Curso: Primeiros Socorros Básicos
Descrição: Curso prático de primeiros socorros para situações de emergência, incluindo técnicas de RCP, controle de hemorragias e atendimento a vítimas de acidentes.
Início das inscrições: 2025-02-15
Fim das inscrições: 2025-03-15
Órgão: Secretaria Municipal de Saúde - SMS
Categoria: Saúde
Modalidade: Presencial
Endereço da unidade: Rua das Flores, 789
Bairro: Tijuca
Número de vagas: 25
Carga Horária: 16 horas
Início das aulas: 2025-03-20
Fim das aulas: 2025-03-23
Horário-Início: 08:00
Horário-Fim: 12:00
Dias de aula: Quinta-feira, Sexta-feira, Sábado, Domingo
Acessibilidade: Acessível para pessoas com deficiência
Recursos de Acessibilidade: Intérprete de Libras disponível mediante solicitação
Público-alvo: Servidores públicos e população em geral
O curso é gratuito?: SIM
Oferece Certificado: SIM
Pré-requisitos para Recebimento de Certificados: Participação em todas as aulas práticas e aprovação em avaliação
Oferece Bolsa: NÃO
Informações Complementares: Idade mínima: 16 anos
Informações adicionais do curso?: SIM
Informações Adicionais do Curso: Certificado válido por 2 anos, conforme normas do Corpo de Bombeiros
CURSO OFERECIDO POR PARCEIRO EXTERNO?: SIM
Nome do Parceiro: Corpo de Bombeiros Militar do Rio de Janeiro
Link do Parceiro: https://www.cbm.rj.gov.br
```

### **Caso de Teste 6: Curso Online de Finanças**
```
Nome do Curso: Educação Financeira Pessoal
Descrição: Aprenda a organizar suas finanças pessoais, fazer investimentos conscientes e planejar o futuro financeiro com segurança.
Início das inscrições: 2025-01-05
Fim das inscrições: 2025-01-20
Órgão: Secretaria Municipal de Fazenda - SMF
Categoria: Finanças
Modalidade: Online
Plataforma Digital: Microsoft Teams
Número de vagas: 75
Carga Horária: 45 horas
Aulas Assíncronas?: NÃO
Início das aulas: 2025-02-01
Fim das aulas: 2025-03-15
Horário-Início: 18:30
Horário-Fim: 20:30
Dias de aula: Segunda-feira, Quarta-feira
Acessibilidade: Acessível para pessoas com deficiência
Recursos de Acessibilidade: Material em formato acessível e legendas
Público-alvo: Servidores públicos e população interessada em educação financeira
O curso é gratuito?: NÃO
Valor INTEIRA (R$): 200,00
Valor MEIA (R$): 100,00
Condições para obtenção de meia-entrada: Estudantes, aposentados e pessoas com deficiência
Oferece Certificado: SIM
Pré-requisitos para Recebimento de Certificados: Frequência mínima de 75% e entrega de plano financeiro pessoal
Oferece Bolsa: SIM
Valor da Bolsa (R$): 150,00
Requisitos para a Obtenção da Bolsa: Renda familiar até 3 salários mínimos e comprovação de necessidade
Informações Complementares: Necessário ter acesso à internet e conhecimentos básicos de informática
Informações adicionais do curso?: SIM
Informações Adicionais do Curso: Curso inclui planilhas de controle financeiro e consultoria individual
CURSO OFERECIDO POR PARCEIRO EXTERNO?: NÃO
```

### **Caso de Teste 7: Curso Presencial de Educação**
```
Nome do Curso: Metodologias Ativas de Ensino
Descrição: Capacitação para educadores sobre metodologias ativas de ensino, incluindo aprendizagem baseada em projetos, sala de aula invertida e gamificação.
Início das inscrições: 2025-02-10
Fim das inscrições: 2025-03-10
Órgão: Secretaria Municipal de Educação - SME
Categoria: Educação
Modalidade: Presencial
Endereço da unidade: Rua da Educação, 321
Bairro: Maracanã
Número de vagas: 40
Carga Horária: 120 horas
Início das aulas: 2025-03-15
Fim das aulas: 2025-06-15
Horário-Início: 13:00
Horário-Fim: 17:00
Dias de aula: Terça-feira, Quinta-feira
Acessibilidade: Acessível para pessoas com deficiência
Recursos de Acessibilidade: Material em Braille, rampa de acesso e elevador
Público-alvo: Professores da rede municipal de ensino
O curso é gratuito?: SIM
Oferece Certificado: SIM
Pré-requisitos para Recebimento de Certificados: Frequência mínima de 80%, entrega de projeto final e apresentação de aula prática
Oferece Bolsa: NÃO
Informações Complementares: Necessário ser professor efetivo da rede municipal
Informações adicionais do curso?: SIM
Informações Adicionais do Curso: Curso reconhecido pelo MEC e válido para progressão funcional
CURSO OFERECIDO POR PARCEIRO EXTERNO?: SIM
Nome do Parceiro: Universidade Federal do Rio de Janeiro - UFRJ
Link do Parceiro: https://www.ufrj.br
```

### **Caso de Teste 8: Curso Online de Cibersegurança**
```
Nome do Curso: Segurança da Informação para Servidores Públicos
Descrição: Fundamentos de segurança da informação, proteção de dados pessoais e boas práticas de segurança digital no ambiente de trabalho público.
Início das inscrições: 2025-01-15
Fim das inscrições: 2025-02-15
Órgão: Secretaria Municipal de Integridade, Transparência e Proteção de Dados - SMIT
Categoria: Cibersegurança
Modalidade: Online
Plataforma Digital: Zoom
Número de vagas: 60
Carga Horária: 50 horas
Aulas Assíncronas?: NÃO
Início das aulas: 2025-02-20
Fim das aulas: 2025-04-20
Horário-Início: 14:00
Horário-Fim: 16:00
Dias de aula: Segunda-feira, Quarta-feira, Sexta-feira
Acessibilidade: Acessível para pessoas com deficiência
Recursos de Acessibilidade: Legendas automáticas e material em formato acessível
Público-alvo: Servidores públicos de todas as secretarias
O curso é gratuito?: SIM
Oferece Certificado: SIM
Pré-requisitos para Recebimento de Certificados: Frequência mínima de 85% e aprovação em avaliação de segurança
Oferece Bolsa: NÃO
Informações Complementares: Necessário ter acesso aos sistemas corporativos
Informações adicionais do curso?: SIM
Informações Adicionais do Curso: Curso obrigatório para servidores que lidam com dados pessoais
CURSO OFERECIDO POR PARCEIRO EXTERNO?: NÃO
```

### **Caso de Teste 9: Curso Híbrido de Sustentabilidade**
```
Nome do Curso: Gestão Ambiental Urbana
Descrição: Capacitação em gestão ambiental urbana, sustentabilidade e práticas de preservação do meio ambiente em áreas urbanas.
Início das inscrições: 2025-02-20
Fim das inscrições: 2025-03-20
Órgão: Secretaria Municipal do Ambiente e Clima - SMAC
Categoria: Sustentabilidade
Modalidade: Híbrido
Endereço da unidade: Av. Beira-Mar, 654
Bairro: Flamengo
Número de vagas: 35
Carga Horária: 90 horas
Início das aulas: 2025-04-01
Fim das aulas: 2025-07-01
Horário-Início: 09:00
Horário-Fim: 13:00
Dias de aula: Sábado
Acessibilidade: Acessível para pessoas com deficiência
Recursos de Acessibilidade: Rampa de acesso, elevador e material em formato digital
Público-alvo: Servidores públicos e profissionais da área ambiental
O curso é gratuito?: NÃO
Valor INTEIRA (R$): 250,00
Valor MEIA (R$): 125,00
Condições para obtenção de meia-entrada: Estudantes e profissionais de ONGs ambientais
Oferece Certificado: SIM
Pré-requisitos para Recebimento de Certificados: Frequência mínima de 75% e entrega de projeto de sustentabilidade
Oferece Bolsa: SIM
Valor da Bolsa (R$): 200,00
Requisitos para a Obtenção da Bolsa: Renda familiar até 2,5 salários mínimos e interesse comprovado em sustentabilidade
Informações Complementares: Necessário ter conhecimentos básicos de biologia
Informações adicionais do curso?: SIM
Informações Adicionais do Curso: Curso inclui visitas técnicas a parques e unidades de conservação
CURSO OFERECIDO POR PARCEIRO EXTERNO?: SIM
Nome do Parceiro: Instituto Estadual do Ambiente - INEA
Link do Parceiro: https://www.inea.rj.gov.br
```

### **Caso de Teste 10: Curso Presencial de Artes**
```
Nome do Curso: Teatro para Iniciantes
Descrição: Introdução ao teatro, técnicas de interpretação, expressão corporal e desenvolvimento da criatividade através da arte dramática.
Início das inscrições: 2025-01-25
Fim das inscrições: 2025-02-25
Órgão: Secretaria Municipal de Cultura - SMC
Categoria: Artes
Modalidade: Presencial
Endereço da unidade: Rua das Artes, 987
Bairro: Lapa
Número de vagas: 20
Carga Horária: 100 horas
Início das aulas: 2025-03-01
Fim das aulas: 2025-06-01
Horário-Início: 18:00
Horário-Fim: 21:00
Dias de aula: Terça-feira, Quinta-feira
Acessibilidade: Acessível para pessoas com deficiência
Recursos de Acessibilidade: Intérprete de Libras e material em formato acessível
Público-alvo: Jovens e adultos interessados em teatro e expressão artística
O curso é gratuito?: NÃO
Valor INTEIRA (R$): 400,00
Valor MEIA (R$): 200,00
Condições para obtenção de meia-entrada: Estudantes, idosos e pessoas com deficiência
Oferece Certificado: SIM
Pré-requisitos para Recebimento de Certificados: Frequência mínima de 80% e participação em apresentação final
Oferece Bolsa: SIM
Valor da Bolsa (R$): 300,00
Requisitos para a Obtenção da Bolsa: Renda familiar até 2 salários mínimos e interesse artístico comprovado
Informações Complementares: Idade mínima: 16 anos, máximo: 60 anos
Informações adicionais do curso?: SIM
Informações Adicionais do Curso: Curso inclui apresentação pública no teatro municipal
CURSO OFERECIDO POR PARCEIRO EXTERNO?: SIM
Nome do Parceiro: Teatro Municipal do Rio de Janeiro
Link do Parceiro: https://www.theatromunicipal.rj.gov.br
```

---

## Observações para Testes

### Campos Obrigatórios em Todos os Casos:
- Nome do Curso
- Descrição
- Início e fim das inscrições
- Órgão
- Categoria
- Modalidade
- Acessibilidade
- Público-alvo
- Curso gratuito/pago
- Oferece certificado
- Oferece bolsa
- Informações adicionais (sim/não)
- Parceiro externo (sim/não)

### Campos Condicionais:
- **Modalidade Presencial/Híbrido**: Endereço, bairro, vagas, carga horária, datas e horários de aula, dias da semana
- **Modalidade Online**: Plataforma digital, vagas, carga horária, aulas assíncronas, datas/horários (se síncrono)
- **Curso Pago**: Valores inteira/meia, condições para meia-entrada
- **Oferece Certificado**: Pré-requisitos para certificado
- **Oferece Bolsa**: Valor da bolsa, requisitos para bolsa
- **Acessibilidade**: Recursos de acessibilidade (se acessível ou exclusivo)
- **Informações Adicionais**: Campo de informações adicionais (se sim)
- **Parceiro Externo**: Nome do parceiro, logo, link (se sim)

### Validações Importantes:
1. Datas de fim devem ser posteriores às datas de início
2. Horário de fim deve ser posterior ao horário de início
3. Pelo menos um dia da semana deve ser selecionado
4. Valores monetários devem estar no formato correto
5. URLs de parceiros devem ser válidas
6. Campos obrigatórios não podem estar vazios
