---
inclusion: always
---

# Regras Kiro - Projeto Ciclo Carioca

## Contexto do Projeto
Este é o **WebApp v4 - Ciclo Carioca**, um sistema de criação e gerenciamento de cursos para a Prefeitura do Rio de Janeiro. O sistema permite criar, editar, listar e gerenciar cursos com diferentes modalidades (Presencial, Online, Híbrido).

## Arquitetura do Sistema

### Estrutura de Pastas


### Padrões de Código

#### Python/Flask (v3.13+)
- Use **type hints** sempre que possível
- Docstrings no formato Google Style
- Tratamento de exceções com logs detalhados
- Separação clara entre camadas (Service → Repository → Scripts)
- Use f-strings para formatação de strings
- Imports organizados: stdlib → third-party → local

#### Templates HTML
- Use **Jinja2** com escape automático
- Classes CSS semânticas e bem estruturadas
- JavaScript vanilla (sem jQuery)
- Responsividade mobile-first
- Acessibilidade (ARIA labels, alt texts)

#### CSS
- Use **CSS Grid** e **Flexbox** para layouts
- Variáveis CSS para cores e espaçamentos
- Animações suaves com 
- Nomenclatura BEM quando apropriado

## Regras de Desenvolvimento

### 1. Validação e Segurança
- **SEMPRE** validar dados de entrada
- Sanitizar uploads de arquivos
- Usar CSRF protection em formulários
- Logs detalhados para debugging
- Tratamento gracioso de erros

### 2. Experiência do Usuário
- Feedback visual para todas as ações
- Loading states para operações assíncronas
- Mensagens de erro claras e acionáveis
- Confirmações para ações destrutivas
- Tooltips e ajuda contextual

### 3. Performance
- Lazy loading para listas grandes
- Compressão de imagens automática
- Cache de dados quando apropriado
- Minimizar requisições desnecessárias

### 4. Manutenibilidade
- Código autodocumentado
- Funções pequenas e focadas
- Reutilização de componentes
- Testes unitários para lógica crítica

## Funcionalidades Específicas

### Sistema de Cursos
- **Modalidades**: Presencial, Online, Híbrido
- **Múltiplas unidades** para cursos presenciais
- **Persistência Híbrida**: MySQL (Principal) + CSV/PDF (Backup)
- **Geração automática** de CSV e PDF
- **Integração com IA** para melhorar descrições
- **Sistema de status** para marcar cursos inseridos

### Autenticação
- Área pública (visualização e duplicação)
- Área administrativa (CRUD completo)
- Login simples com credenciais configuráveis

### Arquivos Gerados
- **CSV**: Dados estruturados para importação
- **PDF**: Documento formatado para impressão
- **Imagens**: Logos de parceiros e capas de cursos

## Convenções de Nomenclatura

### Variáveis e Funções


### Arquivos e Diretórios


## Tratamento de Erros

### Logs Estruturados


### Mensagens Flash
- : Operações bem-sucedidas
- : Avisos importantes
- : Erros que impedem a operação
- File: dir,	Node: Top	This is the top of the INFO tree

  This (the Directory node) gives a menu of major topics.
  Typing "q" exits, "H" lists all Info commands, "d" returns here,
  "h" gives a primer for first-timers,
  "mEmacs<Return>" visits the Emacs manual, etc.

  In Emacs, you can click mouse button 2 on a menu item or cross reference
  to select it.

* Menu:

Basics
* Common options: (coreutils)Common options.
* Coreutils: (coreutils).       Core GNU (file, text, shell) utilities.
* Date input formats: (coreutils)Date input formats.
* Ed: (ed).                     The GNU line editor
* File permissions: (coreutils)File permissions.
                                Access modes.
* Finding files: (find).        Operating on files matching certain criteria.
* Time: (time).                 time

Compression
* Gzip: (gzip).                 General (de)compression of files (lzw).

Development
* SSIP: (ssip).                 Speech Synthesis Interface Protocol.
* Speech Dispatcher: (speech-dispatcher).
                                Speech Dispatcher.

Editors
* nano: (nano).                 Small and friendly text editor.

GNU organization
* Maintaining Findutils: (find-maint).
                                Maintaining GNU findutils

GNU Utilities
* dirmngr-client: (gnupg).      X.509 CRL and OCSP client.
* dirmngr: (gnupg).             X.509 CRL and OCSP server.
* gpg-agent: (gnupg).           The secret key daemon.
* gpg2: (gnupg).                OpenPGP encryption and signing tool.
* gpgsm: (gnupg).               S/MIME encryption and signing tool.

Individual utilities
* arch: (coreutils)arch invocation.             Print machine hardware name.
* b2sum: (coreutils)b2sum invocation.           Print or check BLAKE2 digests.
* base32: (coreutils)base32 invocation.         Base32 encode/decode data.
* base64: (coreutils)base64 invocation.         Base64 encode/decode data.
* basename: (coreutils)basename invocation.     Strip directory and suffix.
* basenc: (coreutils)basenc invocation.         Encoding/decoding of data.
* cat: (coreutils)cat invocation.               Concatenate and write files.
* chcon: (coreutils)chcon invocation.           Change SELinux CTX of files.
* chgrp: (coreutils)chgrp invocation.           Change file groups.
* chmod: (coreutils)chmod invocation.           Change access permissions.
* chown: (coreutils)chown invocation.           Change file owners and groups.
* chroot: (coreutils)chroot invocation.         Specify the root directory.
* cksum: (coreutils)cksum invocation.           Print POSIX CRC checksum.
* cmp: (diffutils)Invoking cmp.                 Compare 2 files byte by byte.
* comm: (coreutils)comm invocation.             Compare sorted files by line.
* cp: (coreutils)cp invocation.                 Copy files.
* csplit: (coreutils)csplit invocation.         Split by context.
* cut: (coreutils)cut invocation.               Print selected parts of lines.
* date: (coreutils)date invocation.             Print/set system date and time.
* dd: (coreutils)dd invocation.                 Copy and convert a file.
* df: (coreutils)df invocation.                 Report file system usage.
* diff: (diffutils)Invoking diff.               Compare 2 files line by line.
* diff3: (diffutils)Invoking diff3.             Compare 3 files line by line.
* dir: (coreutils)dir invocation.               List directories briefly.
* dircolors: (coreutils)dircolors invocation.   Color setup for ls.
* dirname: (coreutils)dirname invocation.       Strip last file name component.
* du: (coreutils)du invocation.                 Report file usage.
* echo: (coreutils)echo invocation.             Print a line of text.
* env: (coreutils)env invocation.               Modify the environment.
* expand: (coreutils)expand invocation.         Convert tabs to spaces.
* expr: (coreutils)expr invocation.             Evaluate expressions.
* factor: (coreutils)factor invocation.         Print prime factors
* false: (coreutils)false invocation.           Do nothing, unsuccessfully.
* find: (find)Invoking find.                    Finding and acting on files.
* fmt: (coreutils)fmt invocation.               Reformat paragraph text.
* fold: (coreutils)fold invocation.             Wrap long input lines.
* groups: (coreutils)groups invocation.         Print group names a user is in.
* gunzip: (gzip)Overview.                       Decompression.
* gzexe: (gzip)Overview.                        Compress executables.
* head: (coreutils)head invocation.             Output the first part of files.
* hostid: (coreutils)hostid invocation.         Print numeric host identifier.
* hostname: (coreutils)hostname invocation.     Print or set system name.
* id: (coreutils)id invocation.                 Print user identity.
* install: (coreutils)install invocation.       Copy files and set attributes.
* join: (coreutils)join invocation.             Join lines on a common field.
* kill: (coreutils)kill invocation.             Send a signal to processes.
* link: (coreutils)link invocation.             Make hard links between files.
* ln: (coreutils)ln invocation.                 Make links between files.
* locate: (find)Invoking locate.                Finding files in a database.
* logname: (coreutils)logname invocation.       Print current login name.
* ls: (coreutils)ls invocation.                 List directory contents.
* md5sum: (coreutils)md5sum invocation.         Print or check MD5 digests.
* mkdir: (coreutils)mkdir invocation.           Create directories.
* mkfifo: (coreutils)mkfifo invocation.         Create FIFOs (named pipes).
* mknod: (coreutils)mknod invocation.           Create special files.
* mktemp: (coreutils)mktemp invocation.         Create temporary files.
* mv: (coreutils)mv invocation.                 Rename files.
* nice: (coreutils)nice invocation.             Modify niceness.
* nl: (coreutils)nl invocation.                 Number lines and write files.
* nohup: (coreutils)nohup invocation.           Immunize to hangups.
* nproc: (coreutils)nproc invocation.           Print the number of processors.
* numfmt: (coreutils)numfmt invocation.         Reformat numbers.
* od: (coreutils)od invocation.                 Dump files in octal, etc.
* paste: (coreutils)paste invocation.           Merge lines of files.
* patch: (diffutils)Invoking patch.             Apply a patch to a file.
* pathchk: (coreutils)pathchk invocation.       Check file name portability.
* pr: (coreutils)pr invocation.                 Paginate or columnate files.
* printenv: (coreutils)printenv invocation.     Print environment variables.
* printf: (coreutils)printf invocation.         Format and print data.
* ptx: (coreutils)ptx invocation.               Produce permuted indexes.
* pwd: (coreutils)pwd invocation.               Print working directory.
* readlink: (coreutils)readlink invocation.     Print referent of a symlink.
* realpath: (coreutils)realpath invocation.     Print resolved file names.
* rm: (coreutils)rm invocation.                 Remove files.
* rmdir: (coreutils)rmdir invocation.           Remove empty directories.
* runcon: (coreutils)runcon invocation.         Run in specified SELinux CTX.
* sdiff: (diffutils)Invoking sdiff.             Merge 2 files side-by-side.
* seq: (coreutils)seq invocation.               Print numeric sequences
* sha1sum: (coreutils)sha1sum invocation.       Print or check SHA-1 digests.
* sha2: (coreutils)sha2 utilities.              Print or check SHA-2 digests.
* shred: (coreutils)shred invocation.           Remove files more securely.
* shuf: (coreutils)shuf invocation.             Shuffling text files.
* sleep: (coreutils)sleep invocation.           Delay for a specified time.
* sort: (coreutils)sort invocation.             Sort text files.
* split: (coreutils)split invocation.           Split into pieces.
* stat: (coreutils)stat invocation.             Report file(system) status.
* stdbuf: (coreutils)stdbuf invocation.         Modify stdio buffering.
* stty: (coreutils)stty invocation.             Print/change terminal settings.
* sum: (coreutils)sum invocation.               Print traditional checksum.
* sync: (coreutils)sync invocation.             Sync files to stable storage.
* tac: (coreutils)tac invocation.               Reverse files.
* tail: (coreutils)tail invocation.             Output the last part of files.
* tee: (coreutils)tee invocation.               Redirect to multiple files.
* test: (coreutils)test invocation.             File/string tests.
* timeout: (coreutils)timeout invocation.       Run with time limit.
* touch: (coreutils)touch invocation.           Change file timestamps.
* tr: (coreutils)tr invocation.                 Translate characters.
* true: (coreutils)true invocation.             Do nothing, successfully.
* truncate: (coreutils)truncate invocation.     Shrink/extend size of a file.
* tsort: (coreutils)tsort invocation.           Topological sort.
* tty: (coreutils)tty invocation.               Print terminal name.
* uname: (coreutils)uname invocation.           Print system information.
* unexpand: (coreutils)unexpand invocation.     Convert spaces to tabs.
* uniq: (coreutils)uniq invocation.             Uniquify files.
* unlink: (coreutils)unlink invocation.         Removal via unlink(2).
* updatedb: (find)Invoking updatedb.            Building the locate database.
* uptime: (coreutils)uptime invocation.         Print uptime and load.
* users: (coreutils)users invocation.           Print current user names.
* vdir: (coreutils)vdir invocation.             List directories verbosely.
* wc: (coreutils)wc invocation.                 Line, word, and byte counts.
* who: (coreutils)who invocation.               Print who is logged in.
* whoami: (coreutils)whoami invocation.         Print effective user ID.
* xargs: (find)Invoking xargs.                  Operating on many files.
* yes: (coreutils)yes invocation.               Print a string indefinitely.
* zcat: (gzip)Overview.                         Decompression to stdout.
* zdiff: (gzip)Overview.                        Compare compressed files.
* zforce: (gzip)Overview.                       Force .gz extension on files.
* zgrep: (gzip)Overview.                        Search compressed files.
* zmore: (gzip)Overview.                        Decompression output by pages.

Kernel
* GRUB: (grub).                 The GRand Unified Bootloader
* grub-dev: (grub-dev).         The GRand Unified Bootloader Dev
* grub-install: (grub)Invoking grub-install.
                                Install GRUB on your drive
* grub-mkconfig: (grub)Invoking grub-mkconfig.
                                Generate GRUB configuration
* grub-mkpasswd-pbkdf2: (grub)Invoking grub-mkpasswd-pbkdf2.
* grub-mkrelpath: (grub)Invoking grub-mkrelpath.
* grub-mkrescue: (grub)Invoking grub-mkrescue.
                                Make a GRUB rescue image
* grub-mount: (grub)Invoking grub-mount.
                                Mount a file system using GRUB
* grub-probe: (grub)Invoking grub-probe.
                                Probe device information
* grub-script-check: (grub)Invoking grub-script-check.

Libraries
* RLuserman: (rluserman).       The GNU readline library User's Manual.

Math
* bc: (bc).                     An arbitrary precision calculator language.

Miscellaneous
* dc: (dc).                     Arbitrary precision RPN "Desktop Calculator".

Network applications
* Wget: (wget).                 Non-interactive network downloader.

Sound
* SSIP: (ssip).                 Speech Synthesis Interface Protocol.
* Say for Speech Dispatcher: (spd-say).
                                Say.
* Speech Dispatcher: (speech-dispatcher).
                                Speech Dispatcher.

Texinfo documentation system
* info stand-alone: (info-stnd).
                                Read Info documents without Emacs.

Text creation and manipulation
* Diffutils: (diffutils).       Comparing and merging files.
* grep: (grep).                 Print lines that match patterns.
* sed: (sed).                   Stream EDitor.  : Informações gerais

## Integração com IA (Gemini)

### Melhoramento de Descrições
- Usar IA para enriquecer descrições de cursos
- Manter descrição original separada
- Fallback gracioso se IA falhar
- Rate limiting para evitar abuse

## Deployment

### PythonAnywhere
- Configuração via 
- Logs específicos para debug
- Verificação de host para comportamentos específicos
- Middleware para tratamento de requests

## Boas Práticas Específicas

### 1. Formulários Dinâmicos
- JavaScript para adicionar/remover campos
- Validação client-side + server-side
- Preservar dados em caso de erro
- UX intuitiva para múltiplas unidades

### 2. Gestão de Arquivos
- Nomes únicos com timestamps
- Limpeza de arquivos órfãos
- Validação de tipos e tamanhos
- Redimensionamento automático de imagens

### 3. API Design
- Endpoints RESTful
- Respostas JSON consistentes
- Status codes apropriados
- Documentação inline

## Debugging e Manutenção

### Logs Importantes
- Criação/edição de cursos
- Uploads de arquivos
- Erros de validação
- Operações de IA

### Monitoramento
- Tamanho dos diretórios de arquivos
- Performance das operações de IA
- Erros recorrentes
- Uso de recursos

---
# Regras do Projeto WebCiclo
1. **SEMPRE** Execute um comando no terminal por vez, ao invés de utilizar &&, para evitar erros.
2. **SEMPRE** Execute o comando conda activate ciclo quando um terminal for aberto.
3. **SEMPRE** seguir a estrutura de arquivos definida abaixo
5. **SEMPRE** seguir as convenções de nomenclatura e organização
6. **SEMPRE** aplicar as regras de desenvolvimento sem exceção
7. **SEMPRE** ative o ambiente virtual correto: Venv ("source .venv/bin/activate")
8. **SEMPRE** unifique os changelogs usando primeiramente o dia em que foram feitos, mantendo o padrão AAAA-MM-DD.md. Os logs deverão ser armazenados na pasta documentacao/logs
9. **SEMPRE** que precisar criar um script para uma tarefa temporária, delete-o depois
10. **SEMPRE** que criar um arquivo de documentação, coloque-o na pasta documentacao.

**Lembre-se**: Este sistema é usado pela Prefeitura do Rio de Janeiro para gerenciar cursos públicos. Priorize sempre a **confiabilidade**, **usabilidade** e **acessibilidade**.
