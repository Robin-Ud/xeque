# xeque ♞

`:Tutor` do terminal + puzzles com rating, estilo chess.com — puro Python, zero deps.

Cada desafio monta uma **arena descartável** em `/tmp` e abre um **bash de verdade**
lá dentro. Você resolve com comandos reais; o xeque confere o resultado
(arquivos, pasta onde você parou, ou a resposta que você deu).

## Instalar

Linux (Mint, Ubuntu, Debian, Fedora, Arch). Funciona com qualquer shell no dia a
dia (fish, zsh...): o xeque abre o bash dele dentro da arena.

```bash
curl -fsSL https://raw.githubusercontent.com/Robin-Ud/xeque/main/SetXeque.sh | bash
```

Instala o que falta (git, python3 ≥ 3.10, busybox), baixa em `~/xeque`, cria o
comando `xeque` e roda o teste na sua máquina. Com `--chave tskey-...` (o Matheus
te manda) ele também libera acesso por ssh via Tailscale, só com chave, depois de
perguntar; `~/xeque/SetXeque.sh --remover-acesso` desfaz.

Atualizar: `xeque atualizar` (git pull). Seus dados ficam na pasta `pessoal/`, fora do
git, e nunca são tocados: histórico, configs e tema. (Instalação de antes da
`pessoal/` migra sozinha no primeiro uso.)

### Tema próprio

O conteúdo base é neutro (faculdade, república, Downloads). Pra deixar com a sua
cara, crie `pessoal/tema/licoes.md`, `pessoal/tema/puzzles.md` ou `pessoal/tema/nativo.md`
com itens de **mesmo id** (o do tema troca o do base; o que faltar vem do base) e
ponha `{"tema": "tema"}` no `pessoal/configs.json`. Rode `xeque validar` depois.

## Uso

```bash
xeque              # menu: trilha, tutor, puzzle, puzzle do dia, stats
xeque trilha       # trilha nativa: próxima lição/puzzle da sua etapa
xeque ficha        # leitor: retoma da primeira ficha não lida (Enter · v volta · q depois)
xeque ficha cmd    # uma ficha (história e camadas POSIX/GNU/Mac), com pager
xeque ficha lista  # todas por etapa, • nas não lidas
xeque tutor        # continua de onde parou (xeque tutor 7 → lição 07)
xeque puzzle       # puzzle perto do seu rating; Enter pro próximo
xeque puzzle p-du  # um puzzle específico
xeque dia          # puzzle do dia (o mesmo o dia inteiro)
xeque stats        # rating, ofensiva, acerto por tema (pior primeiro)
xeque lista        # tudo que existe, por dificuldade
xeque rever        # últimos jogados; o número reabre a lição ou o puzzle
xeque atualizar    # baixa a versão nova (git pull)
```

Dentro da arena:

| comando | faz |
|---|---|
| `pronto` | confere a tarefa |
| `responder X` | responde uma pergunta |
| `dica` | próxima dica (puzzle deixa de contar como limpo) |
| `meta` | relê o enunciado |
| `reset` | recria a arena do zero |
| `desisto` | mostra a solução |
| `ficha [cmd]` | história, camadas e quando não usar um comando (no livre, todas; na trilha, as desbloqueadas); longa abre no `less` (q sai) e fica marcada como lida |

## Deixar pra depois

Não dá pra ler agora? Nas fichas da etapa, `q` para e o leitor guarda onde você
estava (`fichas_lidas.txt`): `xeque ficha` (ou o item 6 do menu) retoma da primeira
não lida, e `v` volta uma. Lição ou puzzle: `exit` **antes de tentar** não conta e
o xeque mostra o comando pra voltar (`xeque trilha n1-a`); a lição volta sozinha
na próxima `xeque trilha`/`xeque tutor`. Sair **depois** de tentar conta como
`abandonou` — senão dava pra fugir de toda derrota. `xeque rever` (item 7) reabre
qualquer um dos últimos jogados.

## Trilha nativa

Pra se virar em qualquer máquina — VM crua, PC alheio, container — sem depender
do que está instalado no seu note. Duas categorias, cada uma com seu Elo:

| categoria | PATH | começa em |
|---|---|---|
| **nativo** (`xeque trilha`) | só o que você desbloqueou, via busybox | 400 |
| **livre** (`tutor`, `puzzle`, `dia`) | a máquina inteira: tree, bat, nvim... | 800 |

A trilha começa com `ls mkdir touch cat` (mais os embutidos do shell: cd, pwd,
echo...). Cada etapa abre com as **fichas** (a história de cada comando e o que é
POSIX, GNU ou Mac, e quando NÃO usar) e as lições; cada lição começa com uma linha
por ficha (ano + por quê) — no tutor livre também. Depois vêm os puzzles. **5 puzzles diferentes
limpos entre os últimos 7 da etapa** desbloqueiam a próxima, e o PATH cresce:

andar → mexer → olhar → filtrar → achar → editar → processar → scripts → sistema → gnu

As etapas e os comandos de cada uma ficam em `configs.json` (`trilha`). O
busybox é o mesmo do roteador e do Alpine: se resolve lá, resolve em qualquer
lugar. Na camada `gnu` os comandos passam a ser os do sistema (`/usr/bin`).
Caminho absoluto (`/usr/bin/tree`) ainda funciona — o PATH é treino, não cadeado.

## Rating

Elo, como no chess.com, separado por categoria (livre começa em 800, nativo em 400). Cada puzzle dá uma **nota** de 0 a 1:

| como terminou | nota |
|---|---|
| **limpo** (de primeira, sem dica) | 1 |
| resolveu com ajuda | 1 − 0,25 por dica − 0,15 por erro (mínimo 0,3) |
| desistiu / saiu depois de tentar | 0 |

Ajuda do Claude no meio conta como uma dica. Se a nota passa do que o Elo esperava
pra você naquele puzzle, você sobe: um puzzle difícil resolvido com 1 dica ainda
rende pontos, enquanto um fácil resolvido com ajuda tira alguns. Sair sem tentar
nada não conta. Os 10 primeiros puzzles valem em dobro (K=64), pra achar seu nível rápido.
Repetir um puzzle que você já resolveu (ou cuja solução viu no `desisto`) é assimétrico:
**acertar vale 20%** (lembrar a resposta não é subir de nível) e **errar custa 150%**
(você já devia saber). Abandonar não conta como visto.
Pesos em `configs.json`; mudou → `xeque recalcular` refaz o histórico (guarda `.bak`).

Depois de cada puzzle aparecem **seus comandos** e a **solução de referência** —
a parte que mais ensina é comparar as duas.

## Segurança

Na arena, `HOME` aponta pra própria arena: `cd`, `~` e `rm -rf ~/...` ficam presos
lá. Caminho absoluto (`/home/voce/...`) ainda escapa — é um bash real.

## Arquivos

- `licoes.md` / `puzzles.md` — o conteúdo do livre, em markdown legível (dá pra escrever os seus)
- `nativo.md` / `fichas.md` — a trilha (itens com `> etapa: N`) e as fichas dos comandos
- `configs.json` — rating inicial, K, janela de escolha, etapas da trilha
- `pessoal/` — fora do git, tudo seu:
  - `historico.csv` — append-only, uma linha por tentativa (só o `recalcular` regrava os ratings)
  - `tentativas.jsonl` — os comandos de cada tentativa, pro tutor do Claude comentar (skill `tutor`)
  - `atual.json` — existe só enquanto tem puzzle aberto; é assim que o Claude sabe onde você está
  - `shell_hist` / `shell_hist_nativo` — os comandos de todos os puzzles (um por categoria): a `↑` e o `Ctrl+R` acham o que você fez antes
  - `fichas_lidas.txt` — append-only, uma ficha por linha: o leitor retoma da primeira que falta
  - `configs.json` — (opcional) vai por cima do configs.json: tema, ajustes seus
  - `tema/` — (opcional) seus itens com o mesmo id dos do base
- `SetXeque.sh` — instalador; `chaves/matheus.pub` é a chave que o acesso remoto autoriza
- `xeque_test.sh` — teste isolado em /tmp
