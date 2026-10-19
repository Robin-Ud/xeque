"""xeque — :Tutor + puzzles de terminal, estilo chess.com. Puro Python, zero deps.

Cada desafio monta uma arena descartável em /tmp e abre um bash DE VERDADE lá
dentro. Você resolve com comandos reais e digita `pronto` (ou `responder X`).
"""
import csv
import difflib
import hashlib
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import date, datetime, timedelta

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
# Tudo de quem joga mora em pessoal/ (fora do git; no note do Matheus é symlink pro
# ~/.pessoal). O resto do DATA_DIR é o que vem do `xeque atualizar`.
PESSOAL = os.path.join(DATA_DIR, 'pessoal')
HIST_CSV = os.path.join(PESSOAL, 'historico.csv')
# Rastros pro tutor (Claude): o puzzle aberto agora e os comandos de cada tentativa.
ATUAL_JSON = os.path.join(PESSOAL, 'atual.json')
TENT_JSONL = os.path.join(PESSOAL, 'tentativas.jsonl')
# ↑ entre puzzles: o bash carrega isto na memória, mas só grava em ctl/hist
# (o check `usou` e o cmds da tentativa continuam vendo só o puzzle atual).
SHELL_HIST = os.path.join(PESSOAL, 'shell_hist')
SHELL_HIST_NATIVO = os.path.join(PESSOAL, 'shell_hist_nativo')
SHELL_HIST_MAX = 2000
# Fichas que você já passou no leitor ou abriu pelo nome: o leitor retoma da primeira que falta.
FICHAS_LIDAS = os.path.join(PESSOAL, 'fichas_lidas.txt')
CAMPOS = ['data_hora', 'modo', 'id', 'rating_item', 'resultado', 'tentativas',
          'dicas', 'segundos', 'comandos', 'rating_antes', 'rating_depois']
META_CMDS = {'pronto', 'dica', 'meta', 'reset', 'desisto', 'responder', 'ficha', 'exit'}
# Duas categorias com Elo separado: livre (o note, com tree/bat/nvim) e nativo
# (a trilha: PATH só com o que você já desbloqueou). Lição não mexe no rating.
LICOES = ('tutor', 'nativo-licao')
BASH = shutil.which('bash') or '/bin/bash'  # absoluto: o PATH da trilha não tem bash
BUSYBOX = shutil.which('busybox')

C = {'b': '\033[1m', 'd': '\033[2m', 'cy': '\033[36m', 'g': '\033[32m',
     'y': '\033[33m', 'r': '\033[31m', 'm': '\033[35m', '0': '\033[0m'}
ROTULO = {'ok': f"{C['g']}✓ limpo", 'ajuda': f"{C['y']}✓ com ajuda",
          'desistiu': f"{C['r']}✗ desistiu", 'abandonou': f"{C['r']}✗ abandonou"}


# ==========================================
# ZONE 1: DATA ENGINES
# ==========================================

def load_json(name: str) -> dict:
    with open(os.path.join(DATA_DIR, name), encoding='utf-8') as f:
        return json.load(f)

def carregar_cfg() -> dict:
    """configs.json (vem do git) com pessoal/configs.json por cima (fica só nesta
    máquina: tema, ajustes pessoais). Um `git pull` nunca briga com o pessoal."""
    cfg = load_json('configs.json')
    if os.path.exists(os.path.join(PESSOAL, 'configs.json')):
        cfg.update(load_json(os.path.join(PESSOAL, 'configs.json')))
    return cfg

# antes de pessoal/ o estado ficava solto na raiz (e o config se chamava configs.local.json)
LEGADO = {n: n for n in ('historico.csv', 'historico.csv.bak', 'tentativas.jsonl', 'atual.json',
                         'shell_hist', 'shell_hist_nativo', 'fichas_lidas.txt', 'tema')}
LEGADO['configs.local.json'] = 'configs.json'

def migrar_pessoal() -> None:
    """Leva o estado da raiz pra pessoal/. Só move o que ainda não existe lá:
    rodar de novo (ou com pessoal/ já preenchido) não sobrescreve nada."""
    os.makedirs(PESSOAL, exist_ok=True)
    for velho, novo in LEGADO.items():
        de, para = os.path.join(DATA_DIR, velho), os.path.join(PESSOAL, novo)
        if os.path.lexists(de) and not os.path.lexists(para):
            shutil.move(de, para)

def read_hist() -> list[dict]:
    try:
        with open(HIST_CSV, encoding='utf-8') as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        return []

def append_hist(row: dict) -> None:
    novo = not os.path.exists(HIST_CSV)
    with open(HIST_CSV, 'a', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS)
        if novo:
            w.writeheader()
        w.writerow(row)

def append_tentativa(row: dict) -> None:
    with open(TENT_JSONL, 'a', encoding='utf-8') as f:
        f.write(json.dumps(row, ensure_ascii=False) + '\n')

def fichas_lidas() -> set[str]:
    try:
        with open(FICHAS_LIDAS, encoding='utf-8') as f:
            return set(f.read().split())
    except FileNotFoundError:
        return set()

def marcar_lida(nome: str) -> None:
    if nome not in fichas_lidas():
        with open(FICHAS_LIDAS, 'a', encoding='utf-8') as f:
            f.write(nome + '\n')

def parse_itens(name: str) -> list[dict]:
    """Lê licoes.md / puzzles.md. Cada item começa com '## id · [rating ·] título'."""
    with open(os.path.join(DATA_DIR, name), encoding='utf-8') as f:
        texto = f.read()
    itens = []
    for bloco in re.split(r'^## ', texto, flags=re.M)[1:]:
        cab, _, corpo = bloco.partition('\n')
        partes = [p.strip() for p in cab.split('·')]
        it = {'id': partes[0], 'titulo': partes[-1], 'rating': None,
              'dicas': [], 'solucao': '', 'tags': [], 'inicio': '',
              'setup': '', 'check': '', 'etapa': None, 'fichas': []}
        if len(partes) == 3:
            it['rating'] = int(partes[1])
        for lang in ('setup', 'check'):
            m = re.search(rf'^```{lang}\n(.*?)^```', corpo, flags=re.S | re.M)
            if m:
                it[lang] = m.group(1)
                corpo = corpo.replace(m.group(0), '')
        meta = []
        for ln in corpo.split('\n'):
            m = re.match(r'^> (\w+): ?(.*)$', ln)
            if not m:
                meta.append(ln)
            elif m.group(1) == 'dica':
                it['dicas'].append(m.group(2))
            elif m.group(1) == 'solucao':
                it['solucao'] += m.group(2) + '\n'
            elif m.group(1) == 'tags':
                it['tags'] = [t.strip() for t in m.group(2).split(',')]
            elif m.group(1) == 'inicio':
                it['inicio'] = m.group(2).strip()
            elif m.group(1) == 'etapa':
                it['etapa'] = int(m.group(2))
            elif m.group(1) == 'fichas':
                it['fichas'] = [f.strip() for f in m.group(2).split(',')]
        it['meta'] = '\n'.join(meta).strip()
        it['pergunta'] = bool(re.search(r'^\s*resp', it['check'], flags=re.M))
        itens.append(it)
    return itens

def carregar_itens(cfg: dict, chave: str) -> list[dict]:
    """O conteúdo base com o tema local por cima: item do tema troca o do base com
    o mesmo id (mesma ordem, histórico continua valendo); id só do tema vai pro fim;
    item novo do base aparece neutro até alguém tematizar."""
    base = parse_itens(cfg[chave])
    if not cfg.get('tema'):
        return base
    tema = os.path.join(PESSOAL, os.path.expanduser(cfg['tema']), cfg[chave])
    if not os.path.exists(tema):
        return base
    troca = {it['id']: it for it in parse_itens(tema)}
    ids = {it['id'] for it in base}
    return [troca.get(it['id'], it) for it in base] + [it for i, it in troca.items() if i not in ids]

def parse_fichas(name: str) -> list[dict]:
    """fichas.md: '## nome · ano', '> etapa: N', '> resumo: ...' (uma linha, aparece
    no topo da lição) e o texto (história + camadas + cuidado)."""
    with open(os.path.join(DATA_DIR, name), encoding='utf-8') as f:
        texto = f.read()
    fichas = []
    for bloco in re.split(r'^## ', texto, flags=re.M)[1:]:
        cab, _, corpo = bloco.partition('\n')
        campos = dict(re.findall(r'^> (\w+): ?(.*)$', corpo, flags=re.M))
        fichas.append({'nome': cab.split('·')[0].strip(), 'cab': cab.strip(),
                       'etapa': int(campos.get('etapa', 1)), 'resumo': campos.get('resumo', ''),
                       'texto': re.sub(r'^> \w+:.*\n?', '', corpo, flags=re.M).strip()})
    return fichas


# ==========================================
# ZONE 2: ARENA (sandbox + bash)
# ==========================================

# Helpers disponíveis no ```setup``` (roda com cwd = arena, set -e)
SETUP_PRELUDE = r'''set -e
arq() { mkdir -p "$(dirname "$1")"; cat > "$1"; }
bytes() { mkdir -p "$(dirname "$1")"; head -c "$2" /dev/zero > "$1"; }
quando() { touch -d "$1" "$2"; }
# awk com sorteio portátil: o rand() muda de awk pra awk (gawk, mawk, busybox) e a
# resposta fixa deixaria de bater. rnd() é Park–Miller, exato em double, igual em todos.
# Programa por último: awkr -v s=3 'BEGIN{semente(s); print rnd()}'
awkr() {
  local p="${!#}"
  awk "${@:1:$#-1}" 'function rnd() { _s = (_s * 16807) % 2147483647; return _s / 2147483647 }
function semente(x) { _s = 20260 + x; for (_i = 0; _i < 50 + (x * 37) % 997; _i++) rnd() }
'"$p"
}
gera_estacao() {  # ARQ ANO DIAS SEMENTE → data,tmin,tmax,chuva_mm
  awkr -v ano="$2" -v n="$3" -v s="${4:-1}" 'BEGIN{semente(s); print "data,tmin,tmax,chuva_mm";
    t0=mktime(ano " 01 01 12 00 00");
    for(i=0;i<n;i++){ d=strftime("%Y-%m-%d", t0+i*86400);
      tmin=12+int(rnd()*80)/10; tmax=tmin+8+int(rnd()*100)/10;
      ch=(rnd()<0.35)? int(rnd()*450)/10 : 0;
      printf "%s,%.1f,%.1f,%.1f\n", d,tmin,tmax,ch }}' > "$1"; }
gera_amostras() {  # ARQ N SEMENTE → id,talhao,cultura,aflatoxina_ppb,data
  awkr -v n="$2" -v s="${3:-1}" 'BEGIN{semente(s); print "id,talhao,cultura,aflatoxina_ppb,data";
    split("milho milho milho soja soja feijao sorgo",c," ");
    t0=mktime("2025 03 01 12 00 00");
    for(i=1;i<=n;i++){ cu=c[1+int(rnd()*7)]; t="T" (1+int(rnd()*8));
      a=(cu=="milho")? int(rnd()*450)/10 : int(rnd()*120)/10;
      d=strftime("%Y-%m-%d", t0+int(rnd()*20)*86400);
      printf "A%03d,%s,%s,%.1f,%s\n", i,t,cu,a,d }}' > "$1"; }
gera_gastos() {  # ARQ N SEMENTE → id,morador,categoria,valor,data (as contas da república)
  awkr -v n="$2" -v s="${3:-1}" 'BEGIN{semente(s); print "id,morador,categoria,valor,data";
    split("mercado mercado mercado lanche lanche gas limpeza",c," ");
    split("Ana Bia Caio Duda Edu Fabi Gabi Hugo",m," ");
    t0=mktime("2025 03 01 12 00 00");
    for(i=1;i<=n;i++){ ca=c[1+int(rnd()*7)]; mo=m[1+int(rnd()*8)];
      v=(ca=="mercado")? int(rnd()*450)/10 : int(rnd()*120)/10;
      d=strftime("%Y-%m-%d", t0+int(rnd()*20)*86400);
      printf "G%03d,%s,%s,%.1f,%s\n", i,mo,ca,v,d }}' > "$1"; }
'''

# Helpers disponíveis no ```check``` (roda com cwd = arena; exit 0 = resolvido)
CHECK_PRELUDE = r'''PATH="${XEQUE_PATH_REAL:-$PATH}"  # o check usa o sistema inteiro, nunca o PATH da trilha
ARENA="$XEQUE_ARENA"; CTL="$XEQUE_CTL"; ORIG="$XEQUE_CTL/orig"
norm() { printf '%s' "$1" | tr -s ' \t\n' ' ' | sed 's/^ //; s/ $//'; }
RESPOSTA="$(norm "$(cat "$CTL/resposta" 2>/dev/null)")"
CWD="$(cat "$CTL/cwd" 2>/dev/null)"
falha() { printf '  \033[31m✗\033[0m %s\n' "$*"; exit 1; }
resp() { [ -n "$RESPOSTA" ] || falha "essa é uma pergunta — use: responder SUA_RESPOSTA";
         [ "$RESPOSTA" = "$(norm "$1")" ] || falha "${2:-resposta \"$RESPOSTA\" não confere}"; }
resp_arquivo() { [ -n "$RESPOSTA" ] || falha "essa é uma pergunta — use: responder NOME";
         [ "$(basename -- "$RESPOSTA")" = "$1" ] || falha "não é \"$RESPOSTA\""; }
resp_num() { [ -n "$RESPOSTA" ] || falha "essa é uma pergunta — use: responder NUMERO";
         awk -v a="${RESPOSTA/,/.}" -v b="$1" -v t="${2:-0.05}" 'BEGIN{d=a-b; if(d<0)d=-d; exit !(a ~ /^-?[0-9.]+$/ && d<=t)}' \
           || falha "$RESPOSTA não confere"; }
em() { [ "$CWD" = "$ARENA${1:+/$1}" ] || falha "você está em ${CWD/#$ARENA/~}, não em ~/$1"; }
existe() { [ -e "$1" ] || falha "$1 não existe"; }
sumiu() { [ ! -e "$1" ] || falha "$1 ainda existe"; }
nenhum() { compgen -G "$1" >/dev/null && falha "ainda tem arquivo casando com $1"; return 0; }
usou() { grep -qF -- "$1" "$CTL/hist" 2>/dev/null || falha "a missão pede usar $1"; }
intacto() { for p; do diff -rq "$ORIG/$p" "$ARENA/$p" >/dev/null 2>&1 || falha "$p foi alterado — devia ficar intacto"; done; }
intacto_exceto() {  # todo arquivo original cujo caminho NÃO casa com a regex segue idêntico
  local f
  while IFS= read -r f; do
    cmp -s "$ORIG/$f" "$ARENA/$f" || falha "${f#./} foi alterado ou apagado — não devia"
  done < <(cd "$ORIG" && find . -type f | grep -Ev -- "$1")
}
'''

RC = r'''# como o .bashrc de qualquer distro; na trilha, só pra quem já foi desbloqueado
type -P ls >/dev/null && alias ls='ls --color=auto'
type -P grep >/dev/null && alias grep='grep --color=auto'
history -r "$XEQUE_SHELLHIST" 2>/dev/null
HISTFILE="$XEQUE_CTL/hist"; HISTSIZE=2000; PROMPT_COMMAND='history -a'
PS1='\[\e[1;33m\]♞\[\e[0m\] \[\e[36m\]\w\[\e[0m\] \$ '
# Os comandos do xeque rodam com o PATH completo: na trilha, o seu PATH
# só tem o que você desbloqueou, e o `pronto` não pode depender disso.
_xq() { PATH="$XEQUE_PATH_REAL" "$@"; }
_xq_conta() { echo $(( $(_xq cat "$XEQUE_CTL/$1" 2>/dev/null || echo 0) + 1 )) > "$XEQUE_CTL/$1"; }
meta() { _xq cat "$XEQUE_CTL/meta.txt"; }
dica() {
  local n=$(( $(_xq cat "$XEQUE_CTL/dicas" 2>/dev/null || echo 0) + 1 ))
  if [ -f "$XEQUE_CTL/dica$n.txt" ]; then
    local t=$(_xq ls "$XEQUE_CTL"/dica[0-9]*.txt | _xq wc -l)
    echo $n > "$XEQUE_CTL/dicas"; printf '\e[35mdica %s/%s:\e[0m ' $n $t; _xq cat "$XEQUE_CTL/dica$n.txt"
  else echo "sem mais dicas — 'desisto' mostra a solução"; fi
}
pronto() {
  history -a; printf '%s' "$PWD" > "$XEQUE_CTL/cwd"; _xq_conta tentativas
  if (cd "$XEQUE_ARENA" && "$BASH" "$XEQUE_CTL/check.sh"); then
    : > "$XEQUE_CTL/ok"; printf '\n\e[1;32m✓ resolvido!\e[0m\n'; exit 0
  else printf '\e[33mainda não.\e[0m  \e[2mmeta · dica · reset · desisto\e[0m\n'; fi
}
responder() { printf '%s' "$*" > "$XEQUE_CTL/resposta"; pronto; }
desisto() { : > "$XEQUE_CTL/desistiu"; printf '\n\e[35msolução:\e[0m\n'; _xq cat "$XEQUE_CTL/solucao.txt"; exit 0; }
reset() {
  cd / && _xq rm -rf -- "$XEQUE_ARENA" && _xq cp -a "$XEQUE_CTL/orig" "$XEQUE_ARENA" \
    && cd "$XEQUE_ARENA/$XEQUE_INICIO" && echo "arena recriada do zero."
}
ficha() {  # a história, as camadas (POSIX/GNU/Mac) e o cuidado de cada comando
  local f
  if [ -n "$1" ]; then
    [ -f "$XEQUE_CTL/fichas/$1.txt" ] || { echo "sem ficha de '$1' (ainda)"; return; }
    _xq less -RFX "$XEQUE_CTL/fichas/$1.txt"  # longa: rola com j/k, q sai; curta: só imprime
    _xq grep -qx -- "$1" "$XEQUE_LIDAS" 2>/dev/null || echo "$1" >> "$XEQUE_LIDAS"
  else
    printf 'fichas: '
    for f in "$XEQUE_CTL"/fichas/*.txt; do f=${f##*/}; f=${f%.txt}
      if _xq grep -qx -- "$f" "$XEQUE_LIDAS" 2>/dev/null; then printf '%s ' "$f"; else printf '\e[1m•%s\e[0m ' "$f"; fi
    done
    printf '\n\e[2mficha NOME mostra uma · • = ainda não lida'
    [ "$PATH" != "$XEQUE_PATH_REAL" ] && printf ' · ls $PATH mostra o que você já desbloqueou'
    printf '\e[0m\n'
  fi
}
cd "$XEQUE_ARENA/$XEQUE_INICIO"
meta
'''


def render(texto: str) -> str:
    """Markdown mínimo → ANSI: `código`, **negrito**, linhas '$ ' de exemplo."""
    out = []
    for ln in texto.split('\n'):
        if ln.lstrip().startswith('$ '):
            out.append(C['g'] + ln + C['0'])
            continue
        ln = re.sub(r'`([^`]+)`', C['cy'] + r'\1' + C['0'], ln)
        ln = re.sub(r'\*\*([^*]+)\*\*', C['b'] + r'\1' + C['0'], ln)
        ln = re.sub(r'^(MISSÃO:)', C['b'] + C['y'] + r'\1' + C['0'], ln)
        out.append(ln)
    return '\n'.join(out)

def render_ficha(fi: dict) -> str:
    cor = lambda m: m.group(1) + (C['r'] if m.group(2) == 'cuidado' else C['m']) + m.group(2) + C['0']
    corpo = re.sub(r'^(\s+)(POSIX|GNU|Mac/BSD|busybox|cuidado)\b', cor, fi['texto'], flags=re.M)
    return f"{C['b']}♞ ficha · {fi['cab']}{C['0']}\n\n{render(corpo)}\n"

def resumo_fichas(it: dict, fichas: list[dict]) -> str:
    """O topo da lição: uma linha por ficha (ano + por quê). A inteira: `ficha NOME`."""
    fs = [f for n in it['fichas'] for f in fichas if f['nome'] == n]
    if not fs:
        return ''
    w = max(len(f['cab']) for f in fs)
    linhas = [f"  {C['m']}{f['cab']:<{w}}{C['0']}  {C['d']}{f['resumo']}{C['0']}" for f in fs]
    nomes = ' · '.join(f"ficha {f['nome']}" for f in fs)
    return '\n'.join(linhas) + f"\n  {C['d']}{nomes}: história, camadas e quando não usar{C['0']}\n\n"

def montar_bin(bindir: str, cmds: list[str], camada: str) -> None:
    """O PATH da trilha: um link por comando desbloqueado. Camada busybox → tudo
    aponta pro busybox (ele vê pelo nome com que foi chamado); gnu → o programa do
    sistema, nunca o que está em ~/.local ou ~/.cargo."""
    if camada == 'busybox' and not BUSYBOX:
        gerente = next((g for g in ('apt', 'dnf', 'pacman', 'zypper') if shutil.which(g)), 'apt')
        verbo = '-S' if gerente == 'pacman' else 'install'
        raise RuntimeError(f'a trilha precisa do busybox: sudo {gerente} {verbo} busybox')
    os.makedirs(bindir)
    for c in cmds:
        alvo = BUSYBOX if camada == 'busybox' else shutil.which(c, path='/usr/bin:/bin:/usr/sbin:/sbin')
        if alvo:
            os.symlink(alvo, os.path.join(bindir, c))

def montar_arena(it: dict, path: dict | None = None, fichas: list[dict] = ()) -> tuple[str, str, str]:
    """Cria raiz/{arena,ctl}, roda o setup e guarda a cópia intocada em ctl/orig,
    com as `fichas` em ctl/fichas. Na trilha (`path`), monta também raiz/bin."""
    raiz = tempfile.mkdtemp(prefix='xeque.')
    arena, ctl = os.path.join(raiz, 'arena'), os.path.join(raiz, 'ctl')
    os.makedirs(arena)
    os.makedirs(ctl)
    r = subprocess.run([BASH, '-c', SETUP_PRELUDE + it['setup']], cwd=arena,
                       capture_output=True, text=True)
    if r.returncode != 0:
        shutil.rmtree(raiz)
        raise RuntimeError(f"setup de {it['id']} falhou:\n{r.stderr}")
    shutil.copytree(arena, os.path.join(ctl, 'orig'), symlinks=True)
    with open(os.path.join(ctl, 'check.sh'), 'w') as f:
        f.write(CHECK_PRELUDE + it['check'])
    with open(os.path.join(ctl, 'solucao.txt'), 'w') as f:
        f.write(it['solucao'])
    for i, d in enumerate(it['dicas'], 1):
        with open(os.path.join(ctl, f'dica{i}.txt'), 'w') as f:
            f.write(render(d) + '\n')
    if path:
        montar_bin(os.path.join(raiz, 'bin'), path['cmds'], path['camada'])
    os.makedirs(os.path.join(ctl, 'fichas'))
    for fi in fichas:
        with open(os.path.join(ctl, 'fichas', fi['nome'] + '.txt'), 'w') as f:
            f.write(render_ficha(fi))
    return raiz, arena, ctl

def env_arena(arena: str, ctl: str, inicio: str, trilha: bool = False) -> dict:
    env = dict(os.environ)
    real = os.path.expanduser('~')
    # HOME = arena: `cd`, `~` e `rm -rf ~/...` ficam presos lá dentro.
    # As XDG apontam pra home real pra nvim/bat manterem sua config.
    env.update({'HOME': arena, 'XEQUE_ARENA': arena, 'XEQUE_CTL': ctl,
                'XEQUE_INICIO': inicio, 'XEQUE_PATH_REAL': env.get('PATH', '/usr/bin:/bin'),
                'XEQUE_SHELLHIST': SHELL_HIST_NATIVO if trilha else SHELL_HIST, 'LESSHISTFILE': '-',
                'XEQUE_LIDAS': FICHAS_LIDAS,
                'XDG_CONFIG_HOME': env.get('XDG_CONFIG_HOME', f'{real}/.config'),
                'XDG_DATA_HOME': env.get('XDG_DATA_HOME', f'{real}/.local/share'),
                'XDG_STATE_HOME': env.get('XDG_STATE_HOME', f'{real}/.local/state'),
                'XDG_CACHE_HOME': env.get('XDG_CACHE_HOME', f'{real}/.cache')})
    if trilha:  # o bin mora ao lado da arena, fora do alcance do `ls`
        env.update({'PATH': os.path.join(os.path.dirname(arena), 'bin'), 'EDITOR': 'vi', 'VISUAL': 'vi'})
    for k in ('PROMPT_COMMAND', 'BASH_ENV', 'ENV'):
        env.pop(k, None)
    return env

def ler_ctl(ctl: str, nome: str, padrao: str = '') -> str:
    try:
        with open(os.path.join(ctl, nome), encoding='utf-8', errors='replace') as f:
            return f.read()
    except FileNotFoundError:
        return padrao

def guardar_shell_hist(novos: str, arquivo: str) -> None:
    linhas = ler_ctl(PESSOAL, os.path.basename(arquivo)).splitlines()
    linhas += [l for l in novos.splitlines() if l.strip()]
    with open(arquivo, 'w', encoding='utf-8') as f:
        f.write(''.join(l + '\n' for l in linhas[-SHELL_HIST_MAX:]))

def jogar(it: dict, modo: str, fichas: list[dict] = (), path: dict | None = None) -> dict:
    """Abre o bash na arena e devolve o que aconteceu lá dentro."""
    raiz, arena, ctl = montar_arena(it, path, fichas)
    tipo = 'pergunta' if it['pergunta'] else 'tarefa'
    rodape = ('responda com: `responder SUA_RESPOSTA`' if it['pergunta']
              else 'quando terminar: `pronto`')
    cab = it['id'] if modo in LICOES else f"{it['id']} · {it['rating']}"
    extra = ' · ficha' if fichas else ''
    meta = (f"\n{C['b']}♞ {cab} — {it['titulo']}{C['0']}  {C['d']}({tipo}){C['0']}\n\n"
            f"{resumo_fichas(it, fichas)}{render(it['meta'])}\n\n{C['d']}{render(rodape)}"
            f"{C['d']} · dica · meta · reset · desisto{extra}{C['0']}\n")
    with open(os.path.join(ctl, 'meta.txt'), 'w') as f:
        f.write(meta)
    rc = os.path.join(ctl, 'rc')
    with open(rc, 'w') as f:
        f.write(RC)
    with open(ATUAL_JSON, 'w') as f:
        json.dump({'id': it['id'], 'modo': modo, 'arena': arena, 'ctl': ctl}, f)
    t0 = time.time()
    try:
        subprocess.run([BASH, '--rcfile', rc, '-i'],
                       env=env_arena(arena, ctl, it['inicio'], bool(path)), cwd=arena)
    finally:
        os.remove(ATUAL_JSON)
    seg = int(time.time() - t0)
    cmds = [c for c in ler_ctl(ctl, 'hist').splitlines()
            if c.strip() and c.split()[0] not in META_CMDS]
    out = {'ok': os.path.exists(os.path.join(ctl, 'ok')),
           'desistiu': os.path.exists(os.path.join(ctl, 'desistiu')),
           'tentativas': int(ler_ctl(ctl, 'tentativas', '0') or 0),
           'dicas': int(ler_ctl(ctl, 'dicas', '0') or 0),
           # o tutor marca ctl/tutor quando ajuda no meio: conta como uma dica
           'tutor': os.path.exists(os.path.join(ctl, 'tutor')),
           'resposta': ler_ctl(ctl, 'resposta'),
           'segundos': seg, 'cmds': cmds}
    out['dicas'] += out['tutor']
    guardar_shell_hist(ler_ctl(ctl, 'hist'), SHELL_HIST_NATIVO if path else SHELL_HIST)
    shutil.rmtree(raiz, ignore_errors=True)
    return out


# ==========================================
# ZONE 3: ORCHESTRATION (rating, escolha, progresso)
# ==========================================

def categoria(modo: str) -> str:
    return 'nativo' if modo.startswith('nativo') else 'livre'

def comando_de(modo: str, iid: str) -> str:
    """O comando que reabre o item — pra voltar depois."""
    sub = {'tutor': 'tutor', 'nativo': 'trilha', 'nativo-licao': 'trilha'}.get(modo, 'puzzle')
    return f'xeque {sub} {iid}'

def rating_atual(hist: list[dict], cfg: dict, cat: str = 'livre') -> int:
    for row in reversed(hist):
        if row['rating_depois'] and categoria(row['modo']) == cat:
            return int(row['rating_depois'])
    return cfg['rating_inicial_nativo' if cat == 'nativo' else 'rating_inicial']

def novo_rating(r: int, rp: int, score: int, n_jogos: int, cfg: dict, repetido: bool = False) -> int:
    """Elo: acima do seu nível, acertar rende mais do que errar custa; abaixo, o contrário.
    Repetido: ganhar vale pouco (você lembra) e perder custa mais (devia saber)."""
    k = cfg['k_provisorio'] if n_jogos < cfg['jogos_provisorios'] else cfg['k']
    esperado = 1 / (1 + 10 ** ((rp - r) / 400))
    if repetido:
        k *= cfg['peso_repeticao'] if score > esperado else cfg['peso_repeticao_perda']
    return round(r + k * (score - esperado))

def nota(resultado: str, tentativas: int, dicas: int, cfg: dict) -> float:
    """Score do Elo: resolver sempre vale algo; cada dica e cada erro descontam."""
    if resultado == 'ok':
        return 1.0
    if resultado == 'ajuda':
        n = 1 - cfg['peso_dica'] * dicas - cfg['peso_erro'] * max(tentativas - 1, 0)
        return max(cfg['nota_minima'], round(n, 2))
    return 0.0  # desistiu / abandonou

def ja_viu(hist: list[dict], pid: str) -> bool:
    """Já resolveu ou viu a solução: repetir vale menos. Abandonou não conta (a solução ficou escondida)."""
    return any(h['modo'] not in LICOES and h['id'] == pid and h['resultado'] in ('ok', 'ajuda', 'desistiu')
               for h in hist)

def resultado_de(res: dict) -> str:
    if res['ok']:
        return 'ok' if res['tentativas'] == 1 and res['dicas'] == 0 else 'ajuda'
    if res['desistiu']:
        return 'desistiu'
    if res['tentativas'] or res['dicas']:
        return 'abandonou'
    return ''  # saiu sem tentar nada: não conta

def escolher_puzzle(puzzles: list[dict], hist: list[dict], r: int, cfg: dict) -> dict:
    limpos = {h['id'] for h in hist if h['modo'] not in LICOES and h['resultado'] == 'ok'}
    tentados = {h['id'] for h in hist if h['modo'] not in LICOES}
    pool = ([p for p in puzzles if p['id'] not in tentados]
            or [p for p in puzzles if p['id'] not in limpos] or puzzles)
    pool.sort(key=lambda p: abs(p['rating'] - r))
    return random.choice(pool[:cfg['janela_escolha']])

def puzzle_do_dia(puzzles: list[dict], dia: date) -> dict:
    h = int(hashlib.sha1(dia.isoformat().encode()).hexdigest(), 16)
    return puzzles[h % len(puzzles)]

def ofensiva(hist: list[dict]) -> int:
    dias = {h['data_hora'][:10] for h in hist}
    d = date.today()
    if d.isoformat() not in dias:
        d -= timedelta(days=1)
    n = 0
    while d.isoformat() in dias:
        n += 1
        d -= timedelta(days=1)
    return n

def proxima_licao(licoes: list[dict], hist: list[dict]) -> dict | None:
    feitas = {h['id'] for h in hist if h['modo'] in LICOES and h['resultado'] in ('ok', 'ajuda')}
    return next((l for l in licoes if l['id'] not in feitas), None)

# --- trilha (categoria nativo) ---

def cmds_ate(cfg: dict, n: int) -> list[str]:
    """O PATH da etapa n: tudo que as etapas 1..n desbloquearam."""
    return cfg['sempre'] + [c for e in cfg['trilha'][:n] for c in e['cmds']]

def puzzles_da_etapa(itens: list[dict], n: int) -> list[dict]:
    return [p for p in itens if p['etapa'] == n and p['rating']]

def licoes_da_etapa(itens: list[dict], n: int) -> list[dict]:
    return [l for l in itens if l['etapa'] == n and not l['rating']]

def limpos_recentes(hist: list[dict], itens: list[dict], cfg: dict, n: int) -> int:
    """Puzzles DIFERENTES da etapa resolvidos limpos entre os últimos `janela` jogos dela."""
    ids = {p['id'] for p in puzzles_da_etapa(itens, n)}
    jogos = [h for h in hist if h['modo'] == 'nativo' and h['id'] in ids][-cfg['desbloqueio']['janela']:]
    return len({h['id'] for h in jogos if h['resultado'] == 'ok'})

def etapa_atual(hist: list[dict], itens: list[dict], cfg: dict) -> int:
    n = 1
    while n < len(cfg['trilha']) and limpos_recentes(hist, itens, cfg, n) >= cfg['desbloqueio']['limpos']:
        n += 1
    return n

def path_da_etapa(cfg: dict, fichas: list[dict], n: int) -> dict:
    return {'cmds': cmds_ate(cfg, n), 'camada': cfg['trilha'][n - 1]['camada'],
            'fichas': [f for f in fichas if f['etapa'] <= n]}

def proximo_da_trilha(itens: list[dict], hist: list[dict], cfg: dict) -> dict | None:
    """Lições da etapa atual primeiro (na ordem do arquivo), depois puzzles dela."""
    n = etapa_atual(hist, itens, cfg)
    if l := proxima_licao(licoes_da_etapa(itens, n), hist):
        return l
    ps = puzzles_da_etapa(itens, n)
    return escolher_puzzle(ps, hist, rating_atual(hist, cfg, 'nativo'), cfg) if ps else None

def registrar(it: dict, modo: str, res: dict, cfg: dict) -> None:
    resultado = resultado_de(res)
    if not resultado:
        print(f"{C['d']}saiu sem tentar — não contou. volta com:{C['0']} {C['cy']}{comando_de(modo, it['id'])}{C['0']}")
        return
    hist = read_hist()
    antes = depois = ''
    s = nota(resultado, res['tentativas'], res['dicas'], cfg)
    licao = modo in LICOES
    repetido = not licao and ja_viu(hist, it['id'])
    if not licao:
        cat = categoria(modo)
        jogos = sum(1 for h in hist if h['rating_depois'] and categoria(h['modo']) == cat)
        antes = rating_atual(hist, cfg, cat)
        depois = novo_rating(antes, it['rating'], s, jogos, cfg, repetido)
    append_hist({'data_hora': datetime.now().isoformat(timespec='seconds'), 'modo': modo,
                 'id': it['id'], 'rating_item': it['rating'] or '', 'resultado': resultado,
                 'tentativas': res['tentativas'], 'dicas': res['dicas'],
                 'segundos': res['segundos'], 'comandos': len(res['cmds']),
                 'rating_antes': antes, 'rating_depois': depois})
    append_tentativa({'data_hora': datetime.now().isoformat(timespec='seconds'),
                      'modo': modo, 'id': it['id'], 'resultado': resultado,
                      'tentativas': res['tentativas'], 'dicas': res['dicas'],
                      'tutor': res['tutor'], 'resposta': res['resposta'],
                      'cmds': res['cmds']})
    rotulo = ROTULO[resultado]
    if resultado == 'ajuda' and not licao:
        rotulo += f" (nota {s:g})"
    if repetido:
        rotulo += (f" {C['d']}(repetido: ganho ×{cfg['peso_repeticao']:g},"
                   f" perda ×{cfg['peso_repeticao_perda']:g})")
    linha = f"\n{rotulo}{C['0']}  {C['d']}{res['segundos']}s · {len(res['cmds'])} comandos{C['0']}"
    if not licao:
        delta = depois - antes
        cor = C['g'] if delta >= 0 else C['r']
        linha += f"  {cat} {antes} {cor}{delta:+d}{C['0']} → {C['b']}{depois}{C['0']}"
    print(linha)
    if res['cmds']:
        print(f"{C['d']}seus comandos:{C['0']}")
        for c in res['cmds'][-6:]:
            print(f"  {C['cy']}{c}{C['0']}")
    if res['ok']:  # abandonou: não entrega a solução, dá pra voltar depois
        print(f"{C['d']}solução de referência:{C['0']}")
        for c in it['solucao'].strip().splitlines():
            print(f"  {C['g']}{c}{C['0']}")

def recalcular(cfg: dict) -> None:
    """Refaz rating_antes/depois do histórico inteiro com a fórmula atual.
    Única exceção ao append-only; o original vai pra historico.csv.bak."""
    hist = read_hist()
    if not hist:
        print('histórico vazio.')
        return
    velho = {c: rating_atual(hist, cfg, c) for c in ('livre', 'nativo')}
    r = {c: rating_atual([], cfg, c) for c in velho}
    jogos = dict.fromkeys(velho, 0)
    for i, h in enumerate(hist):
        if h['modo'] in LICOES or not h['rating_depois']:
            continue
        c = categoria(h['modo'])
        s = nota(h['resultado'], int(h['tentativas']), int(h['dicas']), cfg)
        h['rating_antes'] = r[c]
        r[c] = novo_rating(r[c], int(h['rating_item']), s, jogos[c], cfg, ja_viu(hist[:i], h['id']))
        h['rating_depois'] = r[c]
        jogos[c] += 1
    shutil.copy2(HIST_CSV, HIST_CSV + '.bak')
    with open(HIST_CSV, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS)
        w.writeheader()
        w.writerows(hist)
    for c in velho:
        if jogos[c]:
            print(f"{c} {velho[c]} → {C['b']}{r[c]}{C['0']}")
    print(f"{C['d']}(original em historico.csv.bak){C['0']}")

def dica_entrega(it: dict) -> str:
    """Motivo se alguma dica entrega a solução ou a resposta; '' se tá ok."""
    def norm(t): return ' '.join(t.split())
    linhas = [norm(l) for l in it['solucao'].split('\n') if l.strip()]
    resps = [l.split(' ', 1)[1] for l in linhas if l.startswith('responder ')]
    cmds = [l for l in linhas if not l.startswith(('cd ', 'responder '))]
    for n, d in enumerate(it['dicas'], 1):
        for trecho in re.findall(r'`([^`]+)`', d):
            for c in cmds:
                if difflib.SequenceMatcher(None, norm(trecho), c).ratio() >= 0.8:
                    return f'dica {n} entrega a solução: `{trecho}`'
        for r in resps:
            if re.search(r'(?<![\w.])' + re.escape(r) + r'(?![\w.])', d, re.I):
                return f'dica {n} entrega a resposta: {r}'
    return ''


def fichas_faltando(it: dict, tem: list[dict]) -> str:
    """Lição tem que apontar as fichas dos comandos que ensina, e elas têm que existir
    (na trilha: já desbloqueadas na etapa da lição)."""
    if not it['rating'] and not it['fichas']:
        return 'lição sem `> fichas:`'
    nomes = {f['nome'] for f in tem}
    falta = [n for n in it['fichas'] if n not in nomes]
    return f"`> fichas:` aponta pra ficha que não existe nessa etapa: {' '.join(falta)}" if falta else ''

def validar(itens: list[dict], cfg: dict | None = None, fichas: list[dict] | None = None) -> int:
    """Pra cada item: arena crua tem que FALHAR no check; com a solução, PASSAR;
    e nenhuma dica pode entregar a solução ou a resposta. Na trilha (`cfg`), a
    solução roda só com o PATH da etapa do item: prova que dá pra resolver ali."""
    erros = 0
    for it in itens:
        if motivo := dica_entrega(it):
            erros += 1
            print(f"  {C['r']}FALHOU{C['0']}  {it['id']:<16} {it['titulo']}\n       {motivo}")
            continue
        path = path_da_etapa(cfg, fichas or [], it['etapa']) if cfg else None
        tem = path['fichas'] if path else fichas or []
        if motivo := fichas_faltando(it, tem):
            erros += 1
            print(f"  {C['r']}FALHOU{C['0']}  {it['id']:<16} {it['titulo']}\n       {motivo}")
            continue
        raiz, arena, ctl = montar_arena(it, path, tem)
        env = env_arena(arena, ctl, it['inicio'], bool(path))
        chk = [BASH, os.path.join(ctl, 'check.sh')]
        with open(os.path.join(ctl, 'cwd'), 'w') as f:
            f.write(os.path.join(arena, it['inicio']).rstrip('/'))
        cru = subprocess.run(chk, cwd=arena, env=env, capture_output=True, text=True)
        sol = ('responder() { printf "%s" "$*" > "$XEQUE_CTL/resposta"; }\n'
               f'cd "$XEQUE_ARENA/$XEQUE_INICIO"\n{it["solucao"]}\n'
               'printf "%s" "$PWD" > "$XEQUE_CTL/cwd"\n')
        with open(os.path.join(ctl, 'hist'), 'w') as f:
            f.write(it['solucao'])
        rs = subprocess.run([BASH, '-c', sol], cwd=arena, env=env, capture_output=True, text=True)
        fim = subprocess.run(chk, cwd=arena, env=env, capture_output=True, text=True)
        ok = cru.returncode != 0 and fim.returncode == 0
        erros += not ok
        marca = f"{C['g']}ok{C['0']}" if ok else f"{C['r']}FALHOU{C['0']}"
        print(f"  {marca}  {it['id']:<16} {it['titulo']}")
        if not ok:
            if cru.returncode == 0:
                print('       arena crua já passa no check')
            print('       ' + (rs.stderr + fim.stdout + fim.stderr).strip().replace('\n', '\n       '))
        shutil.rmtree(raiz, ignore_errors=True)
    return erros


# ==========================================
# ZONE 4: INTERFACE
# ==========================================

def faixa(hist: list[dict], cat: str = 'livre') -> str:
    rs = [int(h['rating_depois']) for h in hist if h['rating_depois'] and categoria(h['modo']) == cat][-20:]
    if len(rs) < 2:
        return ''
    lo, hi = min(rs), max(rs)
    barras = '▁▂▃▄▅▆▇█'
    return ''.join(barras[int((r - lo) / (hi - lo or 1) * 7)] for r in rs)

def linha_trilha(hist: list[dict], nativo: list[dict], cfg: dict) -> str:
    n = etapa_atual(hist, nativo, cfg)
    e, d = cfg['trilha'][n - 1], cfg['desbloqueio']
    prog = (f"{limpos_recentes(hist, nativo, cfg, n)}/{d['limpos']} limpos pra etapa {n + 1}"
            if n < len(cfg['trilha']) else 'fim da trilha')
    return f"etapa {n}/{len(cfg['trilha'])} · {e['nome']} ({e['camada']}) · {prog}"

def tela_stats(puzzles: list[dict], licoes: list[dict], nativo: list[dict], cfg: dict) -> None:
    hist = read_hist()
    rn = rating_atual(hist, cfg, 'nativo')
    print(f"\n{C['b']}nativo {rn}{C['0']}  {C['cy']}{faixa(hist, 'nativo')}{C['0']}  {linha_trilha(hist, nativo, cfg)}")
    n = etapa_atual(hist, nativo, cfg)
    print(f"  {C['d']}PATH: {' '.join(cmds_ate(cfg, n))}{C['0']}")
    jog = [h for h in hist if categoria(h['modo']) == 'livre' and h['modo'] not in LICOES]
    r = rating_atual(hist, cfg)
    pico = max([int(h['rating_depois']) for h in jog] or [r])
    limpos = sum(h['resultado'] == 'ok' for h in jog)
    print(f"\n{C['b']}livre {r}{C['0']}  pico {pico}  {C['cy']}{faixa(hist)}{C['0']}")
    print(f"puzzles jogados {len(jog)} · limpos {limpos}"
          f" ({100 * limpos // max(len(jog), 1)}%) · resolvidos {len({h['id'] for h in jog if h['resultado'] in ('ok', 'ajuda')})}/{len(puzzles)}")
    print(f"tutor {len({h['id'] for h in hist if h['modo'] == 'tutor'})}/{len(licoes)} · ofensiva {ofensiva(hist)} dia(s)")
    tags = {p['id']: p['tags'] for p in puzzles}
    por_tag: dict[str, list[int]] = {}
    for h in jog:
        for t in tags.get(h['id'], []):
            por_tag.setdefault(t, []).append(h['resultado'] == 'ok')
    if por_tag:
        print(f"\n{C['d']}acerto limpo por tema (pior primeiro):{C['0']}")
        for t, v in sorted(por_tag.items(), key=lambda kv: sum(kv[1]) / len(kv[1])):
            pct = 100 * sum(v) // len(v)
            cor = C['g'] if pct >= 70 else C['y'] if pct >= 40 else C['r']
            print(f"  {t:<12} {cor}{'█' * (pct // 10):<10}{C['0']} {pct:3d}%  ({len(v)})")
    print()

def rodar(it: dict, modo: str, cfg: dict, fichas: list[dict] = (), path: dict | None = None) -> None:
    res = jogar(it, modo, fichas, path)
    registrar(it, modo, res, cfg)

def anunciar(n: int, cfg: dict, fichas: list[dict]) -> None:
    """Abertura da etapa: o que entrou no PATH e as fichas novas."""
    e = cfg['trilha'][n - 1]
    novos = e['cmds'] + (cfg['sempre'] if n == 1 else [])
    titulo = 'seu PATH começa com' if n == 1 else 'PATH ganhou'
    topo = (f"{C['b']}{C['y']}🔓 etapa {n} · {e['nome']}{C['0']}  {C['d']}({e['camada']}){C['0']}  "
            f"{titulo}: {C['cy']}{' '.join(novos)}{C['0']}\n")
    print('\n' + topo)
    fs = [f for f in fichas if f['etapa'] == n]
    # sem terminal (teste com stdin em pipe), o input() engoliria os comandos do bash
    if not sys.stdin.isatty():
        for fi in fs:
            print(render_ficha(fi))
    elif any(f['nome'] not in fichas_lidas() for f in fs):
        ler_fichas(fs, topo)

def ler_fichas(fs: list[dict], topo: str = '') -> None:
    """Uma ficha por tela, a partir da primeira não lida: Enter passa (e marca lida),
    v volta uma, q deixa o resto pra depois (`xeque ficha` retoma)."""
    lidas = fichas_lidas()
    i = next((k for k, f in enumerate(fs) if f['nome'] not in lidas), 0)
    while i < len(fs):
        fi = fs[i]
        if sys.stdout.isatty():
            print('\033[2J\033[H', end='')
        falta = sum(f['nome'] not in lidas for f in fs)
        print(f"{topo}{C['d']}ficha {i + 1}/{len(fs)} · etapa {fi['etapa']} · {falta} pra ler{C['0']}\n")
        print(render_ficha(fi))
        try:
            op = input(f"{C['d']}[Enter] próxima · v volta · q depois {C['0']}").strip().lower()
        except EOFError:
            op = 'q'
        if op in ('q', 'n', '0'):
            break
        if op == 'v':
            i = max(i - 1, 0)
            continue
        marcar_lida(fi['nome'])
        lidas.add(fi['nome'])
        i += 1
    if falta := sum(f['nome'] not in lidas for f in fs):
        print(f"\n{C['y']}faltam {falta} ficha(s){C['0']} {C['d']}— retome com{C['0']} {C['cy']}xeque ficha{C['0']}")

def loop_trilha(nativo: list[dict], fichas: list[dict], cfg: dict, pid: str | None = None) -> None:
    while True:
        hist = read_hist()
        n = etapa_atual(hist, nativo, cfg)
        if pid:
            it = next((x for x in nativo if x['id'] == pid), None)
            if not it:
                print(f'{pid} não existe na trilha — veja `xeque lista`')
                return
            if it['etapa'] > n:
                print(f"{pid} é da etapa {it['etapa']}; você está na {n}. Desbloqueie antes.")
                return
        else:
            it = proximo_da_trilha(nativo, hist, cfg)
        if not it:
            print(f"\n{C['y']}etapa {n} ainda em construção — peça pro Claude escrever a próxima leva.{C['0']}")
            return
        licao = not it['rating']
        if licao and it is licoes_da_etapa(nativo, it['etapa'])[0] and not any(h['id'] == it['id'] for h in hist):
            anunciar(it['etapa'], cfg, fichas)
        path = path_da_etapa(cfg, fichas, max(n, it['etapa']))
        rodar(it, 'nativo-licao' if licao else 'nativo', cfg, path['fichas'], path)
        if (novo := etapa_atual(read_hist(), nativo, cfg)) > n:
            print(f"\n{C['b']}{C['g']}🔓 desbloqueou a etapa {novo} · {cfg['trilha'][novo - 1]['nome']}!{C['0']}"
                  f"  {C['d']}as fichas aparecem na primeira lição dela{C['0']}")
        if pid or not continuar():
            return

def continuar(prompt: str = 'próximo? [Enter / q] ') -> bool:
    try:
        return input(f"\n{C['d']}{prompt}{C['0']}").strip().lower() not in ('q', 'n', '0')
    except EOFError:
        return False

def loop_tutor(licoes: list[dict], fichas: list[dict], cfg: dict, n: str | None = None) -> None:
    while True:
        if n:
            l = next((x for x in licoes if x['id'] == n.zfill(2)), None)
            n = None
        else:
            l = proxima_licao(licoes, read_hist())
        if not l:
            print(f"\n{C['g']}tutor concluído! agora é com os puzzles: xeque puzzle{C['0']}")
            return
        rodar(l, 'tutor', cfg, fichas)
        if not continuar('próxima lição? [Enter / q] '):
            return

def loop_puzzle(puzzles: list[dict], fichas: list[dict], cfg: dict, pid: str | None = None) -> None:
    while True:
        hist = read_hist()
        p = (next((x for x in puzzles if x['id'] == pid), None) if pid
             else escolher_puzzle(puzzles, hist, rating_atual(hist, cfg), cfg))
        if not p:
            print(f'puzzle {pid} não existe — veja `xeque lista`')
            return
        rodar(p, 'puzzle', cfg, fichas)
        if pid or not continuar():
            return

def menu(licoes: list[dict], puzzles: list[dict], nativo: list[dict], fichas: list[dict], cfg: dict) -> None:
    while True:
        hist = read_hist()
        r, rn = rating_atual(hist, cfg), rating_atual(hist, cfg, 'nativo')
        prox = proxima_licao(licoes, hist)
        trilha = proximo_da_trilha(nativo, hist, cfg)
        dia = puzzle_do_dia(puzzles, date.today())
        feito = any(h['modo'] == 'dia' and h['data_hora'][:10] == date.today().isoformat()
                    for h in hist)
        feitas = len({h['id'] for h in hist if h['modo'] == 'tutor' and h['resultado'] in ('ok', 'ajuda')})
        pra_ler = len(pendentes(abertas(fichas, hist, nativo, cfg)))
        print(f"\n{C['b']}♞ xeque{C['0']} — puzzles de terminal · 🔥 {ofensiva(hist)} dia(s)")
        print(f"  nativo {C['b']}{rn}{C['0']} {C['cy']}{faixa(hist, 'nativo')}{C['0']}  {C['d']}{linha_trilha(hist, nativo, cfg)}{C['0']}")
        print(f"  livre  {C['b']}{r}{C['0']} {C['cy']}{faixa(hist)}{C['0']}  {C['d']}tutor {feitas}/{len(licoes)}{C['0']}\n")
        if trilha:
            prox_t = (f"lição {trilha['id']} · {trilha['titulo']}" if not trilha['rating']
                      else f"puzzle (perto de {rn})")
        else:
            prox_t = 'próxima etapa em construção'
        if pra_ler:
            prox_t += f' · {pra_ler} fichas pra ler'
        print(f"  1  trilha  {C['d']}{prox_t}{C['0']}")
        print(f"  2  tutor   {C['d']}livre · {prox['id'] + ' · ' + prox['titulo'] if prox else 'concluído ✓'}{C['0']}")
        print(f"  3  puzzle  {C['d']}livre · perto de {r}{C['0']}")
        print(f"  4  do dia  {C['d']}{'feito ✓' if feito else dia['titulo'] + ' · ' + str(dia['rating'])}{C['0']}")
        print(f"  5  stats")
        print(f"  6  fichas  {C['d']}{f'{pra_ler} pra ler' if pra_ler else 'todas lidas ✓ · relê do começo'}{C['0']}")
        print(f"  7  rever   {C['d']}últimos jogados: reabre lição ou puzzle{C['0']}")
        print(f"  0  sair")
        try:
            op = input('\n> ').strip()
        except EOFError:
            return
        if op == '1':
            loop_trilha(nativo, fichas, cfg)
        elif op == '2':
            loop_tutor(licoes, fichas, cfg)
        elif op == '3':
            loop_puzzle(puzzles, fichas, cfg)
        elif op == '4':
            rodar(dia, 'dia', cfg, fichas)
        elif op == '5':
            tela_stats(puzzles, licoes, nativo, cfg)
        elif op == '6':
            tela_fichas(fichas, None, abertas(fichas, hist, nativo, cfg))
        elif op == '7':
            tela_rever(licoes, puzzles, nativo, fichas, cfg)
        elif op in ('0', 'q'):
            return

def abertas(fichas: list[dict], hist: list[dict], nativo: list[dict], cfg: dict) -> list[dict]:
    """As fichas que a trilha já te mostrou (etapas 1..atual): é o que o leitor percorre."""
    return path_da_etapa(cfg, fichas, etapa_atual(hist, nativo, cfg))['fichas']

def pendentes(fs: list[dict]) -> list[dict]:
    lidas = fichas_lidas()
    return [f for f in fs if f['nome'] not in lidas]

def paginar(texto: str) -> None:
    """less -RFX: rola se for longo, sai sozinho se couber, não apaga a tela no fim."""
    less = shutil.which('less')
    if sys.stdout.isatty() and less:
        subprocess.run([less, '-RFX'], input=texto, text=True)
    else:
        print(texto)

def tela_fichas(fichas: list[dict], nome: str | None, abertas: list[dict]) -> None:
    """Sem nome: o leitor retoma da primeira não lida. `lista`: todas por etapa. NOME: uma."""
    if nome == 'lista':
        lidas = fichas_lidas()
        for n in sorted({f['etapa'] for f in fichas}):
            nomes = [f['nome'] if f['nome'] in lidas else f"{C['b']}•{f['nome']}{C['0']}"
                     for f in fichas if f['etapa'] == n]
            print(f"  etapa {n}: {' '.join(nomes)}")
        print(f"  {C['d']}• = ainda não lida · xeque ficha retoma a leitura · xeque ficha NOME abre uma{C['0']}")
    elif nome:
        fi = next((f for f in fichas if f['nome'] == nome), None)
        if not fi:
            print(f'sem ficha de {nome} — veja `xeque ficha lista`')
            return
        paginar(render_ficha(fi))
        marcar_lida(nome)
    else:
        ler_fichas(abertas)

def tela_rever(licoes: list[dict], puzzles: list[dict], nativo: list[dict], fichas: list[dict], cfg: dict) -> None:
    """Os últimos itens jogados, do mais recente; o número reabre."""
    titulos = {i['id']: i['titulo'] for i in licoes + puzzles + nativo}
    recentes: dict[str, dict] = {}
    for h in reversed(read_hist()):
        recentes.setdefault(comando_de(h['modo'], h['id']), h)
        if len(recentes) == 10:
            break
    if not recentes:
        print('nada jogado ainda.')
        return
    print()
    for k, (cmd, h) in enumerate(recentes.items(), 1):
        print(f"  {k:>2}  {C['cy']}{cmd:<24}{C['0']} {titulos.get(h['id'], '?')[:38]:<38} "
              f"{C['d']}{h['data_hora'][:10]}{C['0']}  {ROTULO.get(h['resultado'], '')}{C['0']}")
    try:
        op = input(f"\n{C['d']}número reabre (Enter volta) {C['0']}").strip()
    except EOFError:
        return
    if not op.isdigit() or not 1 <= int(op) <= len(recentes):
        return
    cmd, h = list(recentes.items())[int(op) - 1]
    sub = cmd.split()[1]
    if sub == 'trilha':
        loop_trilha(nativo, fichas, cfg, h['id'])
    elif sub == 'tutor':
        loop_tutor(licoes, fichas, cfg, h['id'])
    else:
        loop_puzzle(puzzles, fichas, cfg, h['id'])

def atualizar() -> None:
    """git pull do motor e do conteúdo base. Seus dados (histórico, tema,
    configs) ficam em pessoal/, fora do git, e não são tocados."""
    antes = subprocess.run(['git', '-C', DATA_DIR, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    if subprocess.run(['git', '-C', DATA_DIR, 'pull', '--ff-only', '-q']).returncode != 0:
        print(f"{C['r']}não deu pra atualizar{C['0']} — mexeu em algum arquivo do git? `git -C {DATA_DIR} status`")
        return
    subprocess.run(['git', '-C', DATA_DIR, '--no-pager', 'log', '--oneline', f'{antes}..HEAD'])
    print(f"{C['g']}xeque atualizado.{C['0']}")

def main() -> None:
    migrar_pessoal()
    cfg = carregar_cfg()
    licoes = carregar_itens(cfg, 'licoes')
    puzzles = carregar_itens(cfg, 'puzzles')
    nativo = carregar_itens(cfg, 'nativo')
    fichas = parse_fichas(cfg['fichas'])
    a = sys.argv[1:]
    cmd = a[0] if a else ''
    arg = a[1] if len(a) > 1 else None
    if cmd == 'trilha':
        loop_trilha(nativo, fichas, cfg, arg)
    elif cmd == 'tutor':
        loop_tutor(licoes, fichas, cfg, arg)
    elif cmd == 'puzzle':
        loop_puzzle(puzzles, fichas, cfg, arg)
    elif cmd == 'dia':
        rodar(puzzle_do_dia(puzzles, date.today()), 'dia', cfg, fichas)
    elif cmd == 'stats':
        tela_stats(puzzles, licoes, nativo, cfg)
    elif cmd == 'ficha':
        tela_fichas(fichas, arg, abertas(fichas, read_hist(), nativo, cfg))
    elif cmd == 'rever':
        tela_rever(licoes, puzzles, nativo, fichas, cfg)
    elif cmd == 'lista':
        for n, e in enumerate(cfg['trilha'], 1):
            itens = [i for i in nativo if i['etapa'] == n]
            if itens:
                print(f"  {C['b']}trilha {n} · {e['nome']}{C['0']}  {C['d']}{' '.join(e['cmds'])}{C['0']}")
            for i in itens:
                print(f"    {i['id']:<10} {i['rating'] or '':>4}  {i['titulo']}")
        print(f"  {C['b']}livre{C['0']}")
        for l in licoes:
            print(f"  tutor {l['id']:<6}      {l['titulo']}")
        for p in sorted(puzzles, key=lambda p: p['rating']):
            print(f"  {p['id']:<12} {p['rating']:>4}  {p['titulo']}  {C['d']}{', '.join(p['tags'])}{C['0']}")
    elif cmd == 'recalcular':
        recalcular(cfg)
    elif cmd == 'atualizar':
        atualizar()
    elif cmd == 'validar':
        e = 0
        for n in range(1, len(cfg['trilha']) + 1):
            ps = puzzles_da_etapa(nativo, n)
            if ps and len(ps) < cfg['desbloqueio']['limpos']:
                e += 1
                print(f"  {C['r']}FALHOU{C['0']}  etapa {n} tem {len(ps)} puzzles; desbloquear pede {cfg['desbloqueio']['limpos']} diferentes")
        for i in nativo:
            if not i['etapa'] or i['etapa'] > len(cfg['trilha']):
                e += 1
                print(f"  {C['r']}FALHOU{C['0']}  {i['id']} sem `> etapa:` válida")
        for fi in fichas:
            if not fi['resumo'] or not re.search(r'^\s+cuidado\b', fi['texto'], flags=re.M):
                e += 1
                print(f"  {C['r']}FALHOU{C['0']}  ficha {fi['nome']} sem `> resumo:` ou sem linha `cuidado`")
        print(f"{C['b']}trilha{C['0']}")
        e += validar([i for i in nativo if i['etapa']], cfg, fichas)
        print(f"{C['b']}lições{C['0']}")
        e += validar(licoes, fichas=fichas)
        print(f"{C['b']}puzzles{C['0']}")
        e += validar(puzzles, fichas=fichas)
        print(f"\n{e} falha(s)")
        sys.exit(1 if e else 0)
    elif cmd in ('', 'menu'):
        menu(licoes, puzzles, nativo, fichas, cfg)
    else:
        print('uso: xeque [trilha [ID] | tutor [N] | puzzle [ID] | dia | stats | ficha [NOME|lista] | rever | lista | atualizar | recalcular | validar]')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
