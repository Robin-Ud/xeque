#!/bin/bash
# Teste isolado em /tmp — o historico.csv real não é tocado.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEST_DIR="$(mktemp -d /tmp/xeque_test.XXXXXX)"
cp "$SCRIPT_DIR"/{xeque.py,configs.json,licoes.md,puzzles.md,nativo.md,fichas.md} "$TEST_DIR/"
cd "$TEST_DIR" || exit 1
falhas=0
# arenas de um xeque aberto em outro terminal não contam como sobra do teste
antes=$(ls -d /tmp/xeque.*/ 2>/dev/null)
ok()  { echo "  ✓ $1"; }
nok() { echo "  ✗ $1"; falhas=$((falhas+1)); }

echo "🧪 Teste — dados reais não serão modificados ($TEST_DIR)"
echo; echo "--- 1. conteúdo: solução de cada item passa, arena crua falha"
python3 xeque.py validar | tail -1
python3 xeque.py validar >/dev/null && ok "validar" || nok "validar"

echo; echo "--- 2. fluxo real: bash interativo alimentado por stdin"
printf 'ls Downloads/*.pdf | wc -l\nresponder 7\n' | python3 xeque.py puzzle p-conta-pdf >/dev/null 2>&1
grep -q ',puzzle,p-conta-pdf,400,ok,1,0,' pessoal/historico.csv && ok "acerto limpo registrado" || nok "acerto limpo"
r1=$(tail -1 pessoal/historico.csv | cut -d, -f11 | tr -d "\r")
[ "$r1" -gt 800 ] && ok "rating subiu: 800 → $r1" || nok "rating devia subir ($r1)"

tail -1 pessoal/tentativas.jsonl | grep -q '"cmds": \["ls Downloads/\*.pdf | wc -l"\]' && ok "comandos guardados em tentativas.jsonl" || nok "tentativas.jsonl"
[ -e pessoal/atual.json ] && nok "atual.json devia sumir no fim" || ok "atual.json some no fim"

printf '%s\n' "[ -f $TEST_DIR/pessoal/atual.json ] && touch \"\$XEQUE_CTL/tutor\"" 'responder 7' | python3 xeque.py puzzle p-conta-pdf >/dev/null 2>&1
grep -q ',p-conta-pdf,400,ajuda,1,1,' pessoal/historico.csv && ok "atual.json no meio + ajuda do tutor conta como dica" || nok "atual.json / tutor"

printf 'responder 99\ndica\nresponder 7\n' | python3 xeque.py puzzle p-conta-pdf >/dev/null 2>&1
grep -q ',p-conta-pdf,400,ajuda,2,1,' pessoal/historico.csv && ok "erro + dica = 'ajuda'" || nok "ajuda"
r2=$(tail -1 pessoal/historico.csv | cut -d, -f11 | tr -d "\r")
[ "$r2" -lt "$r1" ] && ok "rating caiu: $r1 → $r2" || nok "rating devia cair ($r1 → $r2)"

printf 'dica\nfind projeto -type d -empty -delete\npronto\n' | python3 xeque.py puzzle p-vazias >/dev/null 2>&1
r3=$(tail -1 pessoal/historico.csv | cut -d, -f11 | tr -d "\r")
grep -q ',p-vazias,1050,ajuda,1,1,' pessoal/historico.csv && [ "$r3" -gt "$r2" ] \
  && ok "difícil com 1 dica ainda sobe: $r2 → $r3" || nok "ajuda acima do rating devia subir ($r2 → $r3)"

printf 'responder 20\n' | python3 xeque.py puzzle p-datas >/dev/null 2>&1
d1=$(tail -1 pessoal/historico.csv | awk -F, '{print $11-$10}')
printf 'responder 20\n' | python3 xeque.py puzzle p-datas >/dev/null 2>&1
d2=$(tail -1 pessoal/historico.csv | awk -F, '{print $11-$10}')
[ "$d2" -gt 0 ] && [ $((d2 * 3)) -lt "$d1" ] && ok "repetido vale bem menos: +$d1 → +$d2" || nok "repetição devia valer menos (+$d1 → +$d2)"

python3 -c '
import json, xeque as x; c = json.load(open("configs.json"))
for rp in (600, 1300):
    g, p = x.novo_rating(961, rp, 1, 99, c) - 961, x.novo_rating(961, rp, 0, 99, c) - 961
    assert (g > -p) == (rp > 961), (rp, g, p)
pn, pr = x.novo_rating(961, 961, 0, 99, c) - 961, x.novo_rating(961, 961, 0, 99, c, True) - 961
assert pr < pn < 0, (pn, pr)
' && ok "acima do nível ganha > perde, abaixo o contrário; repetido perde mais" || nok "assimetria do rating"

printf 'desisto\n' | python3 xeque.py puzzle p-part >/dev/null 2>&1
grep -q ',p-part,500,desistiu,' pessoal/historico.csv && ok "desistência registrada" || nok "desisto"

printf 'exit\n' | python3 xeque.py puzzle p-oculto 2>&1 | grep -q 'volta com:.*xeque puzzle p-oculto' \
  && ok "sair sem tentar diz como voltar" || nok "comando de volta"
grep -q 'p-oculto' pessoal/historico.csv && nok "sair sem tentar não devia contar" || ok "sair sem tentar não conta"

printf '%s\n' "meta > $TEST_DIR/meta01" "ficha cd > $TEST_DIR/ficha_cd" 'cd faculdade/2025/calculo' pronto \
  | python3 xeque.py tutor 1 >/dev/null 2>&1
grep -q ',tutor,01,,ok,' pessoal/historico.csv && ok "lição do tutor registrada" || nok "tutor"
grep -q 'ficha pwd · ficha cd · ficha ls' meta01 && grep -q 'cuidado' ficha_cd \
  && ok "lição do livre mostra o resumo das fichas e tem ficha com cuidado" || nok "fichas no livre"
grep -qx cd pessoal/fichas_lidas.txt && ok "ficha aberta na arena fica marcada como lida" || nok "fichas_lidas.txt"

printf '\nv\n\nq\n' | python3 xeque.py ficha >/dev/null 2>&1   # posix → (v) posix → busybox, q
grep -qx posix pessoal/fichas_lidas.txt && ! grep -qx busybox pessoal/fichas_lidas.txt \
  && ok "leitor: Enter marca, v volta, q para" || nok "leitor de fichas"
printf 'q\n' | python3 xeque.py ficha 2>&1 | grep -q 'busybox ·' && ok "leitor retoma da primeira não lida" || nok "retomar fichas"
python3 xeque.py ficha lista | grep -q '•busybox' && ok "ficha lista marca as não lidas" || nok "ficha lista"
printf '\n' | python3 xeque.py rever | grep -q 'xeque tutor 01' && ok "rever lista os últimos jogados" || nok "rever"

echo; echo "--- 3. trilha: PATH por etapa, Elo separado, desbloqueio"
printf '%s\n' "type -P grep >/dev/null || echo sem > $TEST_DIR/semgrep" \
  "ficha ls > $TEST_DIR/ficha_ls" 'ls -l $PATH' 'responder busybox' | python3 xeque.py trilha n1-a >/dev/null 2>&1
grep -q ',nativo-licao,n1-a,,ok,1,0,' pessoal/historico.csv && ok "lição da trilha passa com o PATH restrito" || nok "lição n1-a"
[ -e semgrep ] && ok "etapa 1 não tem grep" || nok "grep vazou pro PATH da etapa 1"
grep -q 'Unix V1' ficha_ls && ok "ficha dentro da arena" || nok "ficha ls"
rl=$(python3 -c 'import json, xeque as x; print(x.rating_atual(x.read_hist(), json.load(open("configs.json"))))')
printf 'ls -R predio\nresponder sala_6\n' | python3 xeque.py trilha n1-p1 >/dev/null 2>&1
grep -q ',nativo,n1-p1,300,ok,1,0,.*,400,' pessoal/historico.csv && ok "puzzle nativo começa do rating próprio (400)" || nok "rating nativo"
[ "$(python3 -c 'import json, xeque as x; print(x.rating_atual(x.read_hist(), json.load(open("configs.json"))))')" = "$rl" ] \
  && ok "livre não muda com puzzle nativo ($rl)" || nok "puzzle nativo mexeu no rating livre"
printf 'exit\n' | python3 xeque.py trilha n2-p1 2>&1 | grep -q 'etapa 2' && ok "etapa 2 bloqueada no começo" || nok "bloqueio de etapa"
python3 -c '
import json, xeque as x; c = json.load(open("configs.json")); nat = x.parse_itens("nativo.md")
ids = [p["id"] for p in x.puzzles_da_etapa(nat, 1)]
h = lambda i, r: {"modo": "nativo", "id": i, "resultado": r, "rating_depois": "1"}
assert x.etapa_atual([h(i, "ok") for i in ids[:4]], nat, c) == 1
assert x.etapa_atual([h(i, "ok") for i in ids[:5]], nat, c) == 2
assert x.etapa_atual([h(ids[0], "ok")] * 5, nat, c) == 1            # repetir o mesmo não vale
assert x.etapa_atual([h(i, "ok") for i in ids[:5]] + [h(ids[5], "ajuda")] * 3, nat, c) == 1  # janela de 7
assert "grep" not in x.cmds_ate(c, 1) and "grep" in x.cmds_ate(c, 4)
' && ok "desbloqueio: 5 limpos diferentes nos últimos 7" || nok "regra de desbloqueio"
printf 'reset\nls -R predio\nresponder sala_6\n' | python3 xeque.py trilha n1-p1 >/dev/null 2>&1
tail -1 pessoal/historico.csv | grep -q ',nativo,n1-p1,300,ok,' && ok "reset funciona com o PATH restrito" || nok "reset na trilha"

echo; echo "--- 4. arena: HOME presa, sem vazar pra home real"
printf 'echo "$HOME" > /tmp/xeque_test_home\nexit\n' | python3 xeque.py puzzle p-part >/dev/null 2>&1
case "$(cat /tmp/xeque_test_home)" in /tmp/xeque.*/arena) ok "HOME = arena";; *) nok "HOME vazou: $(cat /tmp/xeque_test_home)";; esac
rm -f /tmp/xeque_test_home
[ "$(ls -d /tmp/xeque.*/ 2>/dev/null)" != "$antes" ] && nok "sobrou arena em /tmp" || ok "arenas limpas"

printf 'history > /tmp/xeque_test_hist\nexit\n' | python3 xeque.py puzzle p-part >/dev/null 2>&1
grep -q 'ls Downloads/\*.pdf | wc -l' /tmp/xeque_test_hist && ok "↑ lembra comandos de puzzles anteriores" || nok "shell_hist não carregou"
rm -f /tmp/xeque_test_hist

python3 xeque.py stats >/dev/null && ok "stats roda" || nok "stats"

rat() { python3 -c 'import json, xeque as x; c = json.load(open("configs.json")); print(x.rating_atual(x.read_hist(), c, "livre"), x.rating_atual(x.read_hist(), c, "nativo"))'; }
rf=$(rat)
sed -i 's/,[0-9]\+,[0-9]\+\r$/,1,1\r/' pessoal/historico.csv   # estraga todos os ratings
python3 xeque.py recalcular >/dev/null
[ -e pessoal/historico.csv.bak ] && [ "$(rat)" = "$rf" ] \
  && ok "recalcular refaz livre e nativo separados ($rf) e guarda .bak" || nok "recalcular ($rf → $(rat))"

echo; echo "--- 5. tema local, pessoal/configs.json, sorteio portátil"
mkdir -p pessoal/tema
printf '%s\n' '## p-conta-pdf · 400 · Quantos PDFs do tema?' '' 'TEMA' '' '> solucao: responder 3' '' \
  '```check' 'resp 3' '```' '' '## p-extra · 500 · Só do tema' '' 'X' '' '> solucao: responder 1' '' '```check' 'resp 1' '```' > pessoal/tema/puzzles.md
printf '{"tema": "tema", "rating_inicial": 900}\n' > pessoal/configs.json
python3 -c '
import xeque as x; c = x.carregar_cfg(); ps = x.carregar_itens(c, "puzzles"); base = x.parse_itens("puzzles.md")
assert c["rating_inicial"] == 900 and c["licoes"] == "licoes.md"
assert ps[0]["titulo"] == "Quantos PDFs do tema?" and ps[-1]["id"] == "p-extra" and len(ps) == len(base) + 1
assert [p["id"] for p in ps[1:-1]] == [p["id"] for p in base[1:]]
assert x.carregar_itens(c, "licoes") == x.parse_itens("licoes.md")   # sem tema/licoes.md: base puro
' && ok "tema troca pelo id e herda o resto; pessoal/configs.json vai por cima" || nok "tema / pessoal/configs.json"
rm -rf pessoal/tema pessoal/configs.json

# instalação antiga: estado solto na raiz e configs.local.json → vai tudo pra pessoal/ sem sobrescrever
mkdir -p mig/tema && cp xeque.py configs.json licoes.md puzzles.md nativo.md fichas.md mig/
cp pessoal/historico.csv mig/ && echo cd > mig/fichas_lidas.txt
printf '{"tema": "tema", "rating_inicial": 900}\n' > mig/configs.local.json
mkdir -p mig/pessoal && echo ls > mig/pessoal/fichas_lidas.txt
(cd mig && python3 xeque.py stats >/dev/null 2>&1)
[ -f mig/pessoal/historico.csv ] && [ ! -e mig/historico.csv ] && [ -f mig/pessoal/configs.json ] \
  && [ ! -e mig/configs.local.json ] && [ -d mig/pessoal/tema ] && cmp -s pessoal/historico.csv mig/pessoal/historico.csv \
  && grep -qx ls mig/pessoal/fichas_lidas.txt && [ -e mig/fichas_lidas.txt ] \
  && ok "migra a raiz pra pessoal/ e não sobrescreve o que já está lá" || nok "migrar_pessoal"

if command -v busybox >/dev/null; then
  mkdir -p bbawk && ln -s "$(command -v busybox)" bbawk/awk
  python3 -c 'import xeque as x; print(x.SETUP_PRELUDE)' > prelude.sh
  gera='. ./prelude.sh; gera_gastos /dev/stdout 50 7; gera_estacao /dev/stdout 2025 40 3'
  a=$(bash -c "$gera"); b=$(PATH="$PWD/bbawk:$PATH" bash -c "$gera")
  [ -n "$a" ] && [ "$a" = "$b" ] && ok "sorteio igual em qualquer awk (sistema × busybox)" || nok "rnd() mudou de awk pra awk"
fi

echo
cd / && rm -rf "$TEST_DIR"
[ $falhas -eq 0 ] && echo "✅ tudo certo" || { echo "❌ $falhas falha(s)"; exit 1; }
