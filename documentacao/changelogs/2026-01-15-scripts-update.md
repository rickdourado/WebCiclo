# Atualização - Scripts de Gerenciamento

## Data: 2026-01-15 (Atualização)

### 🔧 Melhorias nos Scripts de Inicialização

#### Script `start.sh` Aprimorado

**Problema resolvido:**

- ❌ Erro "Address already in use" quando a porta 5001 já estava ocupada

**Solução implementada:**

- ✅ Verificação automática da porta 5001
- ✅ Encerramento automático de processos conflitantes
- ✅ Validação de liberação da porta
- ✅ Feedback visual colorido

**Código:**

```bash
# Verifica porta
PID=$(lsof -ti:5001)

# Encerra processo se necessário
if [ ! -z "$PID" ]; then
    kill -9 $PID
    echo "✅ Porta 5001 liberada"
fi
```

#### Novo Script `stop.sh`

**Funcionalidade:**

- Encerra a aplicação WebCiclo de forma limpa
- Verifica e mata processos na porta 5001

**Uso:**

```bash
# Iniciar
./start.sh

# Parar
./stop.sh
```

---

### 📝 Comandos Úteis

```bash
# Verificar se a aplicação está rodando
lsof -ti:5001

# Iniciar aplicação (com limpeza automática de porta)
./start.sh

# Parar aplicação
./stop.sh

# Verificar logs em tempo real
tail -f backend/logs/backend.log
```

---

### ✅ Benefícios

- 🚀 **Inicialização mais confiável**: Não precisa mais matar processos manualmente
- 🎯 **Experiência melhorada**: Feedback visual claro do que está acontecendo
- 🛡️ **Segurança**: Validação de que a porta foi realmente liberada
- 📦 **Simplicidade**: Um único comando para iniciar (`./start.sh`)
