# CLAUDE.md

Tutor + puzzles de terminal com rating Elo. Python puro, stdlib, sem packaging.
Pra quem joga aprender shell fazendo — não resolver por ele. Repo público
(github.com/Robin-Ud/xeque); amigos instalam com `SetXeque.sh` e atualizam com `xeque atualizar`.

## Rodar
```bash
xeque                 # symlink ~/.local/bin/xeque → xeque.sh
./xeque_test.sh       # teste isolado em /tmp (não toca historico.csv)
./xeque.sh validar    # só o conteúdo
```

## Estrutura
```
xeque.py        ← script único (4 zonas: data, arena, orquestração, interface)
licoes.md       ← tutor (livre), ordem = ordem do arquivo
puzzles.md      ← puzzles (livre), `## id · rating · título`
nativo.md       ← trilha (nativo): lições e puzzles com `> etapa: N`
fichas.md       ← `## cmd · ano`, `> etapa: N`, `> resumo:`: história + camadas + cuidado
historico.csv   ← append-only (exceção: `recalcular` regrava rating_*); rating atual = último rating_depois da categoria
tentativas.jsonl ← append-only; comandos de cada tentativa (pro tutor revisar)
atual.json      ← só existe com puzzle aberto: id, arena, ctl (o tutor lê)
shell_hist      ← ↑ entre puzzles (últimos 2000); só memória, ctl/hist segue limpo
shell_hist_nativo ← idem, só da trilha (pra ↑ não sugerir tree/bat)
fichas_lidas.txt ← append-only; ficha passada no leitor ou aberta pelo nome (`xeque ficha` retoma da 1ª que falta)
configs.json    ← vai pro git; configs.local.json (fora do git) vai por cima (`carregar_cfg`)
tema/           ← fora do git: itens com o mesmo id trocam os do base (`carregar_itens`)
SetXeque.sh     ← instalador idempotente (apt/dnf/pacman); --chave liga ssh+Tailscale, --remover-acesso desfaz
chaves/matheus.pub ← a chave que o acesso remoto autoriza (~/.ssh/xeque_amigos_ed25519 do Matheus)
```

## Formato de item (licoes.md / puzzles.md)
`> dica:` (várias, em ordem), `> solucao:` (várias linhas, viram um script),
`> tags:`, `> inicio:` (pasta inicial relativa à arena), `> fichas: a, b` (lição:
obrigatório; o resumo de cada ficha vai no topo da missão), blocos ```` ```setup ```` e
```` ```check ````. Setup roda com `set -e` e helpers `arq`, `bytes`, `quando`,
`gera_estacao`, `gera_gastos` (base), `gera_amostras` (tema agro do Matheus) e `awkr`
(SETUP_PRELUDE). Check tem `resp`, `resp_num`,
`resp_arquivo`, `em`, `existe`, `sumiu`, `nenhum`, `usou`, `intacto`,
`intacto_exceto`, `falha` (CHECK_PRELUDE); `$ORIG` = cópia intocada pós-setup.
Item é pergunta se o check chama `resp*`.

## Regras
- Mexeu em conteúdo → `./xeque.sh validar` tem que dar 0 falhas: arena crua
  FALHA no check e a solução PASSA. Respostas fixas em `> solucao: responder X`
  precisam bater com o dado gerado (prefira check calculando em `$ORIG`).
- Dica é escada, nunca a solução: (1) no que pensar, sem comando; (2) qual
  ferramenta/flag, sem a linha montada; (3) formato com buraco `___`, só nos
  difíceis. A solução só aparece no `desisto`. O `validar` reprova dica com trecho
  entre crases ≥80% parecido com uma linha da solução, ou que contenha a resposta.
- Pergunta com resposta única: ao gerar dado aleatório, garanta que não há empate.
- Setup determinístico e igual em qualquer awk: sorteio só com `awkr` +
  `semente(s)`/`rnd()` (o `rand()` muda entre gawk, mawk e busybox e a resposta
  fixa deixaria de bater). Nada de `$RANDOM`.
- Público: nada pessoal no que vai pro git — nem nome de gente real, instituição,
  projeto, senha que pareça de verdade. O base é neutro (faculdade, república,
  Downloads); a cor de cada um vai no `tema/` local. Item novo entra no base, com id
  estável (o histórico e os temas apontam pelo id). Mudou o base → `validar` sem
  o configs.local.json (é o que o `xeque_test.sh` faz) e com ele (o tema mesclado).
- Commit com o e-mail noreply do GitHub (configurado no repo), nunca o gmail.
- HOME=arena dentro do shell; XDG_* continuam na home real (nvim/bat com config).
- `ctl/tutor` existe → o Claude ajudou no meio; conta como +1 dica.
- Rating: score = `nota()` (ok 1, ajuda parcial, resto 0), pesos em configs.json.
  Repetido (`ja_viu`: já fez ok/ajuda/desistiu) → K × `peso_repeticao` se ganhou,
  × `peso_repeticao_perda` se perdeu.
- Não ensinar alias que substitui comando clássico (rg≠grep, fd≠find).
- Duas categorias, Elo separado: `categoria(modo)` → `nativo` (modos `nativo`,
  `nativo-licao`) ou `livre` (`puzzle`, `dia`). Lição (`tutor`, `nativo-licao`) não tem rating.
- Trilha: arena ganha `raiz/bin` com symlinks pro busybox (ou pro /usr/bin na camada
  gnu) só dos `cmds` das etapas 1..N (configs.json → `trilha`). RC e check rodam com
  `$XEQUE_PATH_REAL`. Desbloqueio = `desbloqueio.limpos` ids diferentes ok entre os
  últimos `janela` jogos da etapa. O `validar` roda a solução com o PATH da etapa
  do item; cada etapa precisa de ≥ `limpos` puzzles.
- Ficha: dizer a camada de cada flag (POSIX × GNU × Mac/BSD), uma história curta
  e verdadeira (na dúvida sobre data ou autor, escreva a época: "anos 70"), um
  `> resumo:` de uma linha e uma linha `cuidado` (quando NÃO usar). O `validar`
  cobra resumo, cuidado, e que a lição só aponte ficha que existe na etapa dela.
  No livre todas as fichas valem; na trilha, só as das etapas 1..N.
- Puzzle que exige ferramenta (`usou`) tem que dizer a regra no enunciado ("sem loop").
