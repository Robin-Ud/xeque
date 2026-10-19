# Puzzles

Formato: `## id · rating · título`, enunciado, `> tags:`, `> dica:`, `> solucao:`,
`> inicio:` e blocos `setup` / `check`. O rating diz a dificuldade (Elo).
Rode `./xeque.sh validar` depois de mexer aqui.

## p-conta-pdf · 400 · Quantos PDFs?

Quantos arquivos `.pdf` tem direto na pasta `Downloads/` (sem contar subpastas)?

> tags: glob, pipe
> dica: duas partes: listar só os PDFs, depois contar quantas linhas saíram
> dica: o * casa qualquer começo de nome; o wc conta linhas com uma flag; o | liga um no outro
> solucao: ls Downloads/*.pdf | wc -l
> solucao: responder 7

```setup
mkdir -p Downloads/antigos
for i in 1 2 3 4 5 6 7; do echo pdf > Downloads/paper_$i.pdf; done
for i in 1 2; do echo pdf > Downloads/antigos/velho_$i.pdf; done
echo img > Downloads/foto.jpg; echo x > Downloads/notas_pdf.txt
```

```check
resp 7
```

## p-ultimo-dia · 450 · O último dia

Qual foi a temperatura **máxima** (coluna `tmax`) no último dia de `estacao.csv`?

> tags: tail, cut
> dica: primeiro descubra em que posição está a coluna tmax — olhe a primeira linha
> dica: o head mostra o começo; o irmão dele mostra o fim. Com a última linha na tela, conte as vírgulas
> solucao: head -1 estacao.csv
> solucao: tail -1 estacao.csv | cut -d, -f3
> solucao: responder 30.0

```setup
gera_estacao estacao.csv 2025 180 11
```

```check
resp "$(tail -1 "$ORIG/estacao.csv" | cut -d, -f3)"
```

## p-part · 500 · Downloads quebrados

Apague de `Downloads/` todos os downloads que não terminaram: os arquivos
`.part` e `.crdownload`. Todo o resto fica.

> tags: glob, rm
> dica: um padrão com * por extensão pega todos de uma vez. Ensaie com echo antes: ele mostra o que casou
> dica: são duas extensões, então dois padrões — o rm aceita vários no mesmo comando
> solucao: rm Downloads/*.part Downloads/*.crdownload

```setup
mkdir -p Downloads
for f in ubuntu.iso.part video_aula.mp4.part dados.zip.crdownload; do echo x > "Downloads/$f"; done
for f in ubuntu.iso tabela.pdf apostila.part1.pdf part_list.txt; do echo y > "Downloads/$f"; done
```

```check
nenhum 'Downloads/*.part'
nenhum 'Downloads/*.crdownload'
intacto_exceto '\.(part|crdownload)$'
```

## p-oculto · 550 · Senha escondida

A senha do wifi da república está num arquivo **oculto** dentro de `config/`.
Qual é a senha?

> tags: ls, ocultos
> dica: "oculto" no Linux é só um nome que começa com ponto, e o ls normal esconde esses
> dica: tem uma flag do ls que mostra *all*. Achou o arquivo? Leia com cat
> solucao: ls -a config
> solucao: cat config/.wifi_casa
> solucao: responder pao-de-queijo-42

```setup
mkdir -p config
echo "tema=escuro" > config/app.conf
echo "rede=Republica_5G" > config/rede.txt
printf 'ssid=Republica_5G\nsenha=pao-de-queijo-42\n' > config/.wifi_casa
```

```check
resp pao-de-queijo-42 "resposta é só a senha"
```

## p-aspas · 600 · O PDF com parênteses

Em `relatorios/` tem duas versões do relatório. Apague `relatório final (1).pdf`
— a cópia — e deixe o `relatório final.pdf` original.

> tags: aspas, rm
> dica: sem aspas o shell vê 3 palavras: `relatório`, `final`, `(1).pdf`
> dica: junte tudo numa palavra só: aspas em volta do caminho INTEIRO, ou comece o nome e aperte Tab
> solucao: rm "relatorios/relatório final (1).pdf"

```setup
mkdir -p relatorios
echo v1 > "relatorios/relatório final.pdf"
echo v1 > "relatorios/relatório final (1).pdf"
echo v0 > "relatorios/relatório.pdf"
```

```check
sumiu "relatorios/relatório final (1).pdf"
intacto_exceto 'final \(1\)\.pdf$'
```

## p-palavras · 600 · Limite do resumo

O resumo do trabalho pode ter no máximo 250 palavras. Quantas **palavras** tem
`resumo.txt`?

> tags: wc
> dica: o wc conta mais coisas além de linhas
> dica: olhe o `wc --help`: uma das flags conta *words*
> solucao: wc -w resumo.txt
> solucao: responder 263

```setup
awk 'BEGIN{split("o consumo de energia das casas de estudantes foi medido em tres cidades paulistas",w," ");
  for(i=0;i<263;i++) printf "%s%s", w[i%14+1], (i%11==10 ? "\n" : " "); print ""}' > resumo.txt
```

```check
resp "$(wc -w < "$ORIG/resumo.txt")"
```

## p-linha-42 · 650 · Linha 42

O que está escrito na linha **42** de `diario.txt`? Responda o texto da linha.

> tags: head, sed
> dica: dá pra montar com dois comandos que você conhece: um pega as N primeiras linhas, o outro as N últimas
> dica: das 42 primeiras, você quer só a última — ligue os dois com |
> solucao: sed -n 42p diario.txt
> solucao: responder dia 42 chuva forte no bloco 1

```setup
for i in $(seq 1 80); do
  case $((i % 4)) in 0) e="sol";; 1) e="nublado";; 2) e="chuva forte";; 3) e="garoa";; esac
  echo "dia $i $e no bloco $(( i % 7 + 1 ))"
done > diario.txt
```

```check
resp "$(sed -n 42p "$ORIG/diario.txt")"
```

## p-maiusculas · 650 · Trabalho, TRABALHO ou trabalho?

Quantas linhas de `agenda.txt` falam de **trabalho**, escrito de qualquer jeito
(`Trabalho`, `TRABALHO`, `trabalho`...)?

> tags: grep
> dica: o grep normal diferencia maiúscula de minúscula: pra ele, Trabalho e trabalho são palavras diferentes
> dica: tem uma flag que ignora a caixa (*ignore case*) e outra que conta as linhas em vez de mostrar. Dá pra juntar as duas
> solucao: grep -ic trabalho agenda.txt
> solucao: responder 6

```setup
arq agenda.txt <<'EOF'
03/10 Trabalho de cálculo pra sexta
03/10 lavar a roupa
04/10 TRABALHO: mandar pro grupo
05/10 choveu, fiquei em casa
05/10 a Bia vai trabalhar até tarde
06/10 revisar o trabalho de física
07/10 Prova e trabalho na mesma semana
08/10 perguntar pro professor sobre o TRABALHO final
09/10 mercado ok
10/10 entrega do Trabalho adiada
EOF
```

```check
resp "$(grep -ic trabalho "$ORIG/agenda.txt")"
```

## p-anexar · 650 · Sem apagar a agenda

Acrescente a linha `17/10 devolver o livro na biblioteca` no **fim** de
`agenda.txt`. Tudo que já estava escrito tem que continuar lá.

> tags: redirect
> dica: dá pra escrever num arquivo pelo shell de dois jeitos: um começa do zero, o outro continua de onde parou
> dica: o echo imprime a linha; a seta dupla manda ela pro fim do arquivo (a simples zera o arquivo antes!)
> solucao: echo "17/10 devolver o livro na biblioteca" >> agenda.txt

```setup
arq agenda.txt <<'EOF'
14/10 dentista às 15h
15/10 pagar a conta de luz
16/10 prova de cálculo
EOF
```

```check
n=$(wc -l < "$ORIG/agenda.txt")
head -n "$n" agenda.txt | cmp -s - "$ORIG/agenda.txt" || falha "o que já estava escrito mudou (usou > em vez de >>?)"
[ "$(tail -n 1 agenda.txt)" = "17/10 devolver o livro na biblioteca" ] || falha "a última linha não é a anotação"
[ "$(wc -l < agenda.txt)" -eq $((n + 1)) ] || falha "era pra ter exatamente uma linha a mais"
```

## p-grep-v · 700 · Tudo menos mercado

Em `gastos.csv`, quantos gastos **não** são de mercado? (o cabeçalho não conta)

> tags: grep, pipe
> dica: pense ao contrário: em vez de achar o que não é mercado, jogue o mercado fora. E cuidado com a primeira linha
> dica: o grep tem uma flag que inverte o filtro (`man grep`, procure *invert*) e outra que conta. O cabeçalho sai com tail começando numa linha N
> solucao: tail -n +2 gastos.csv | grep -vc mercado
> solucao: responder 85

```setup
gera_gastos gastos.csv 140 17
```

```check
resp "$(tail -n +2 "$ORIG/gastos.csv" | grep -vc mercado)"
```

## p-cat-wc · 700 · Volume do vault

Quantas linhas somam, juntas, todas as notas `.md` da pasta `vault/`
(só as que estão direto nela, sem subpastas)?

> tags: cat, pipe
> dica: contar linhas de um arquivo você já sabe. O truque é virar várias notas num texto só
> dica: o cat aceita vários arquivos de uma vez e emenda tudo na saída
> solucao: cat vault/*.md | wc -l
> solucao: responder 38

```setup
mkdir -p vault/arquivo
for n in 3 8 12 15; do seq 1 $n | sed 's/^/linha /' > vault/nota$n.md; done
seq 1 50 > vault/arquivo/velha.md
seq 1 9 > vault/rascunho.txt
```

```check
resp 38
```

## p-backup · 700 · Backup antes de mexer

Antes de revisar a tese, faça um backup: copie a pasta `tese/` **inteira**, com
subpastas, para `backup/tese`. A original fica como está.

> tags: cp
> dica: copiar pasta é diferente de copiar arquivo: o cp precisa descer em tudo que tem dentro
> dica: a flag é a mesma ideia do rm que apaga pasta (*recursive*). A pasta backup/ já existe
> solucao: cp -r tese backup/

```setup
mkdir -p backup
arq tese/main.tex <<<'\input{capitulos/cap1}'
arq tese/capitulos/cap1.tex <<<'Introdução'
arq tese/capitulos/cap2.tex <<<'Material e métodos'
arq tese/figuras/mapa.txt <<<'(figura)'
arq tese/.latexmkrc <<<'$pdf_mode = 1;'
```

```check
intacto tese
[ -d backup/tese ] || falha "não existe backup/tese"
diff -r "$ORIG/tese" backup/tese >/dev/null 2>&1 || falha "backup/tese não é uma cópia completa de tese/ (sobrou ou faltou algo)"
```

## p-nao-exec · 750 · Quem não roda?

Dos scripts em `bin/`, um **não** tem permissão de execução. Qual?

> tags: permissoes, ls
> dica: permissão aparece na listagem LONGA do ls, naquela coluna tipo `-rw-r--r--`
> dica: o x é o de execução. Compare as linhas: qual não tem nenhum x?
> solucao: ls -l bin
> solucao: responder sync_zotero.sh

```setup
mkdir -p bin
for s in backup.sh sync_zotero.sh wallpaper.sh limpa_downloads.sh; do printf '#!/bin/bash\necho %s\n' $s > bin/$s; chmod +x bin/$s; done
chmod -x bin/sync_zotero.sh
```

```check
resp_arquivo sync_zotero.sh
```

## p-recente · 800 · O mais novo

Qual arquivo de `Downloads/` foi modificado **por último**?

> tags: ls
> dica: o ls sabe ordenar por outras coisas além do nome. Qual delas serve aqui?
> dica: procure no `man ls` a flag que ordena por *time* — o mais novo vem primeiro
> solucao: ls -lt Downloads | head -3
> solucao: responder boleto_luz.pdf

```setup
mkdir -p Downloads
for f in aula03.pdf foto_praia.jpg boleto_luz.pdf zzz_ultimo_alfabetico.txt edital.pdf; do echo x > Downloads/$f; done
quando '2026-09-01 10:00' Downloads/aula03.pdf
quando '2026-10-01 10:00' Downloads/foto_praia.jpg
quando '2026-10-13 21:40' Downloads/boleto_luz.pdf
quando '2026-08-11 08:00' Downloads/zzz_ultimo_alfabetico.txt
quando '2026-10-10 10:00' Downloads/edital.pdf
```

```check
resp_arquivo boleto_luz.pdf
```

## p-direto · 800 · Direto pra resposta

Quantos itens tem dentro de `fotos/`, **contando os ocultos**? Desta vez, o
número tem que ir **direto** do comando pro `responder`: sem você digitar o número.

> tags: subst, ocultos, pipe
> dica: duas partes: primeiro um comando que imprime só o número. Depois, um jeito de o shell colar essa saída dentro do responder
> dica: o ls tem uma flag que mostra ocultos SEM o . e o ..; o wc conta. Pra colar a saída de um comando dentro de outro existe o $( )
> solucao: responder "$(ls -A fotos | wc -l)"

```setup
mkdir -p fotos/editadas
for i in 1 2 3 4 5 6; do echo jpg > fotos/IMG_00$i.jpg; done
echo cache > fotos/.thumbs.db
echo x > fotos/.directory
```

```check
resp "$(ls -A "$ORIG/fotos" | wc -l)"
usou '$('
```

## p-diff · 850 · O que mudou?

Você tem `relatorio_v1.txt` e `relatorio_v2.txt`. Só **uma** linha mudou entre
eles. Qual é o **número** dessa linha?

> tags: diff
> dica: existe um comando feito pra comparar dois arquivos linha a linha — o nome é o começo de *difference*
> dica: a saída começa com algo tipo `NcM`: linha no 1º arquivo, uma letra (c = change), linha no 2º
> solucao: diff relatorio_v1.txt relatorio_v2.txt
> solucao: responder 23

```setup
for i in $(seq 1 40); do echo "parágrafo $i: resultados da prática de titulação"; done > relatorio_v1.txt
sed '23s/prática de titulação/prática de titulação (corrigido: média 18,4 mL)/' relatorio_v1.txt > relatorio_v2.txt
```

```check
resp 23
```

## p-chaves · 850 · Pastas do semestre

Organize o semestre: dentro de `semestre/`, uma pasta pra cada matéria
(`calculo`, `fisica`, `quimica`), e dentro de **cada** matéria as pastas `provas` e
`listas`. São 6 pastas no fim.

**Regra:** um comando só, **sem loop** e sem digitar o nome de nenhuma pasta duas vezes.

> tags: mkdir, chaves
> dica: o mkdir cria várias pastas de uma vez, e uma flag faz ele criar os pais que faltam
> dica: o shell expande uma lista entre chaves em várias palavras: experimente `echo x{1,2,3}`. Dá pra usar duas listas no mesmo caminho
> dica: formato: mkdir -p semestre/{___}/{___}
> solucao: mkdir -p semestre/{calculo,fisica,quimica}/{provas,listas}

```setup
mkdir -p notas
```

```check
for c in calculo fisica quimica; do
  for s in provas listas; do [ -d "semestre/$c/$s" ] || falha "falta semestre/$c/$s"; done
done
usou '{'
```

## p-tar · 900 · Dentro do pacote

Quantas linhas tem o `chuva.csv` que está dentro de `dados_2024.tar.gz`?

> tags: tar, wc
> dica: primeiro descubra o que tem dentro do pacote sem extrair; depois extraia e conte
> dica: no tar, `-t` lista e `-x` extrai; `-z` é o gzip e o `-f` vem logo antes do nome do pacote
> solucao: tar -xzf dados_2024.tar.gz
> solucao: wc -l dados/chuva.csv
> solucao: responder 367

```setup
mkdir -p dados
gera_estacao dados/chuva.csv 2024 366 2
echo "estação meteorológica da escola" > dados/LEIAME.txt
tar -czf dados_2024.tar.gz dados
rm -rf dados
```

```check
resp "$(tar -xzOf "$ORIG/dados_2024.tar.gz" dados/chuva.csv | wc -l)"
```

## p-calor · 950 · O dia mais quente

Em `estacao.csv` (data,tmin,tmax,chuva_mm), em que **data** foi registrada a
maior temperatura máxima?

> tags: sort, cut
> dica: ordene pela coluna da máxima; o maior valor fica numa das pontas
> dica: o sort precisa de três coisas: separador (`-t`), coluna (`-k`) e que é número (`-n`). Depois, a última linha
> solucao: sort -t, -k3 -n estacao.csv | tail -1
> solucao: responder 2025-02-18

```setup
gera_estacao estacao.csv 2025 120 23
sed -i 's/^2025-02-18,\([0-9.]*\),[0-9.]*,/2025-02-18,\1,38.4,/' estacao.csv
```

```check
resp 2025-02-18
```

## p-du · 1000 · Quem come o disco?

Qual subpasta de `Dropbox/` ocupa mais espaço no total (somando tudo dentro)?

> tags: du
> dica: `ls -l` mostra o tamanho do arquivo, não do conteúdo da pasta
> dica: existe um comando de *disk usage* que soma tudo dentro. `-s` dá um total por pasta, `-h` mostra em K/M/G
> dica: fica mais fácil ordenado — o sort tem uma flag que entende K, M e G
> solucao: du -sh Dropbox/* | sort -h
> solucao: responder videos

```setup
mkdir -p Dropbox/{fotos,videos,papers,planilhas}
for i in $(seq 1 30); do bytes Dropbox/fotos/f$i.jpg 120000; done
bytes Dropbox/videos/viagem_praia.mp4 6000000
for i in $(seq 1 12); do bytes Dropbox/papers/p$i.pdf 300000; done
bytes Dropbox/planilhas/custos.xlsx 40000
```

```check
resp_arquivo videos
```

## p-datas · 1000 · Dias de gasto

Em quantos **dias diferentes** teve gasto em `gastos.csv`?
(colunas: id,morador,categoria,valor,data)

> tags: cut, sort, uniq
> dica: três passos: separar só a coluna da data, tirar as repetições, contar
> dica: o cut separa a coluna; `sort -u` ordena e tira os repetidos
> dica: antes de contar: o cabeçalho também virou uma "data" diferente?
> solucao: tail -n +2 gastos.csv | cut -d, -f5 | sort -u | wc -l
> solucao: responder 20

```setup
gera_gastos gastos.csv 90 31
```

```check
resp "$(tail -n +2 "$ORIG/gastos.csv" | cut -d, -f5 | sort -u | wc -l)"
```

## p-vazias · 1050 · Pastas fantasmas

Apague **todas as pastas vazias** dentro de `projeto/` — inclusive as que
ficarem vazias depois que você apagar as de dentro. Arquivo nenhum some.

> tags: find
> dica: o find acha por tipo e por condição, não só por nome. Liste as vazias antes de apagar
> dica: tipo pasta é `-type d`; vazia é `-empty`
> dica: o find também apaga o que achou, se terminar com a ação certa — e vai de dentro pra fora, então a que esvazia cai junto
> solucao: find projeto -type d -empty -delete

```setup
mkdir -p projeto/{src/util,docs/antigo/mais_antigo,build/tmp/obj,dados}
echo x > projeto/src/main.py; echo y > projeto/dados/a.csv; echo z > projeto/README.md
```

```check
[ -z "$(find projeto -type d -empty)" ] || falha "ainda tem pasta vazia: $(find projeto -type d -empty | tr '\n' ' ')"
intacto_exceto '^$'
```

## p-pesados · 1050 · Vídeos pesados

Quantos arquivos dentro de `midia/`, em **qualquer** subpasta, têm **mais de 1 MB**?

> tags: find
> dica: o find filtra por muito mais coisa que nome, inclusive tamanho
> dica: procure -size no man find: o + quer dizer "maior que" e a unidade vai colada no número (k, M, G). Depois é contar as linhas
> solucao: find midia -type f -size +1M | wc -l
> solucao: responder 4

```setup
bytes midia/viagem/praia.mp4 2500000
bytes midia/viagem/trilha.mp4 4000000
bytes midia/viagem/thumb.jpg 60000
bytes midia/aulas/calculo.mp4 3000000
bytes midia/aulas/slides.pdf 400000
bytes midia/celular/2025/show.mp4 2200000
bytes midia/celular/2025/foto.jpg 500000
bytes midia/celular/audio.ogg 150000
```

```check
resp "$(find "$ORIG/midia" -type f -size +1M | wc -l)"
```

## p-maior · 1100 · O maior de todos

Qual é o **maior arquivo** em qualquer lugar dentro de `Dropbox/` (em qualquer
subpasta, a qualquer profundidade)? Responda o nome do arquivo.

> tags: find, sort
> dica: `ls -lS` só olha uma pasta. `find` olha todas
> dica: o find imprime o tamanho de cada arquivo com `-printf` — procure `%s` no `man find`
> dica: com tamanho e caminho em cada linha, é ordenar numérico e pegar a última
> solucao: find Dropbox -type f -printf '%s %p\n' | sort -n | tail -1
> solucao: responder filme_4k.mkv

```setup
mkdir -p Dropbox/a/b/c Dropbox/fotos Dropbox/x
bytes Dropbox/fotos/grande.jpg 3000000
bytes Dropbox/x/backup.zip 4000000
bytes Dropbox/a/b/c/filme_4k.mkv 5200000
bytes Dropbox/a/planilha.xlsx 90000
```

```check
resp_arquivo filme_4k.mkv
```

## p-so-tex · 1100 · Só sobra o .tex

Em `rascunhos/` (e nas subpastas) tem de tudo: `.aux`, `.log`, `.pdf`, `.tex`...
Apague **todos os arquivos que não são `.tex`**. As pastas continuam, e nada fora
de `rascunhos/` muda.

> tags: find, rm
> dica: inverta: liste com find quem vai ser apagado, e só confie na lista quando não tiver nenhum .tex nela. Cuidado: tem oculto
> dica: -type f pega só arquivos; -not nega o teste que vem logo depois; a ação de apagar vai sempre no fim
> solucao: find rascunhos -type f -not -name '*.tex' -delete

```setup
mkdir -p rascunhos/capitulos/velhos tese
for e in tex aux log pdf; do
  echo "artigo $e" > rascunhos/artigo.$e
  for c in cap1 cap2; do echo "$c $e" > rascunhos/capitulos/$c.$e; done
done
echo cap0 > rascunhos/capitulos/velhos/cap0.tex
echo gz > rascunhos/capitulos/velhos/cap0.synctex.gz
echo '$pdf_mode = 1;' > rascunhos/.latexmkrc
echo bak > rascunhos/notas.tex.bak
mkdir -p rascunhos/figuras && echo png > rascunhos/figuras/mapa.png
echo 'pdf de verdade' > tese/artigo.pdf
```

```check
sobra="$(find rascunhos -type f -not -name '*.tex')"
[ -z "$sobra" ] || falha "ainda tem: $(echo $sobra)"
while IFS= read -r d; do [ -d "$d" ] || falha "$d sumiu — as pastas ficam"; done < <(cd "$ORIG" && find rascunhos -type d)
while IFS= read -r f; do cmp -s "$ORIG/$f" "$f" || falha "$f foi apagado — esse é .tex"; done < <(cd "$ORIG" && find rascunhos -name '*.tex')
intacto_exceto '^\./rascunhos/'
```

## p-prefixo · 1150 · Etiqueta nas fotos

Coloque o prefixo `praia_` no nome de todas as fotos `.jpg` de `viagem/`
(ex.: `IMG_01.jpg` → `praia_IMG_01.jpg`). Outros arquivos não mudam.

> tags: for, mv
> dica: o shell repete o mesmo comando pra cada arquivo. Ensaie com echo na frente: assim ele só imprime
> dica: é um laço for com mv dentro; o nome novo é o prefixo grudado no $f — e tem nome com espaço
> dica: `for f in *.jpg; do echo mv ___ ___; done` — lista certa? Tire o echo
> solucao: cd viagem
> solucao: for f in *.jpg; do mv "$f" "praia_$f"; done

```setup
mkdir -p viagem
for n in IMG_01 IMG_02 IMG_03 "IMG 04 por do sol" IMG_05; do echo "foto $n" > "viagem/$n.jpg"; done
echo "obs" > viagem/anotacoes.txt
```

```check
for n in IMG_01 IMG_02 IMG_03 "IMG 04 por do sol" IMG_05; do
  cmp -s "$ORIG/viagem/$n.jpg" "viagem/praia_$n.jpg" || falha "falta viagem/praia_$n.jpg"
  sumiu "viagem/$n.jpg"
done
intacto viagem/anotacoes.txt
```

## p-especies · 1150 · Lista de filmes

A Ana e o Rui anotaram os filmes que querem ver: `filmes_ana.txt` e
`filmes_rui.txt` (um por linha, com repetições). Crie `filmes.txt` com
**todos os filmes dos dois, sem repetir, em ordem alfabética**.

> tags: sort, redirect
> dica: três coisas: juntar os dois, ordenar e tirar os repetidos. Por fim, salvar em arquivo
> dica: o sort aceita vários arquivos de uma vez e tem a flag que você usou pra tirar repetidos. Pra salvar, a seta
> solucao: sort -u filmes_ana.txt filmes_rui.txt > filmes.txt

```setup
printf '%s\n' matrix interestelar coraline matrix up matrix coraline > filmes_ana.txt
printf '%s\n' parasita interestelar amelie matrix whiplash interestelar > filmes_rui.txt
```

```check
existe filmes.txt
cmp -s filmes.txt <(sort -u "$ORIG/filmes_ana.txt" "$ORIG/filmes_rui.txt") \
  || falha "filmes.txt não é a lista única e ordenada dos dois"
intacto filmes_ana.txt filmes_rui.txt
```

## p-excel · 1150 · Planilha do Excel

O Excel exportou `boletim.csv` com **ponto e vírgula** separando as colunas.
Crie `boletim_virgula.csv` igualzinho, só que com **vírgula** no lugar de cada
`;`. O original fica intacto.

> tags: tr, redirect
> dica: é trocar um caractere por outro no arquivo inteiro e salvar o resultado em outro arquivo
> dica: tem um comando que *traduz* caracteres (tr). Ele não abre arquivo sozinho: só lê da entrada (com < ou com cat e |)
> solucao: tr ';' ',' < boletim.csv > boletim_virgula.csv

```setup
arq boletim.csv <<'EOF'
aluno;p1;p2;faltas
Ana;7;8;2
Bia;9;6;0
Caio;5;7;4
Duda;8;9;1
Edu;6;5;3
EOF
```

```check
existe boletim_virgula.csv
cmp -s boletim_virgula.csv <(tr ';' ',' < "$ORIG/boletim.csv") \
  || falha "boletim_virgula.csv não é o original com ; trocado por ,"
intacto boletim.csv
```

## p-grep-r · 1200 · Onde eu anotei?

Uma das notas em `obsidian/` (em alguma subpasta) tem a frase
"ponto de fusão". Qual é o nome do arquivo?

> tags: grep
> dica: você não sabe a subpasta, então a busca tem que descer em todas
> dica: o grep tem uma flag de busca recursiva e outra que mostra só o nome do arquivo. Frase com espaço vai entre aspas
> solucao: grep -rl "ponto de fusão" obsidian
> solucao: responder naftaleno.md

```setup
mkdir -p obsidian/{"5 facul"/{quimica,calculo},projetos,diario}
echo "ponto de ebulição da água ao nível do mar" > "obsidian/5 facul/quimica/ebulicao.md"
echo "derivada: inclinação da reta no ponto x0" > "obsidian/5 facul/calculo/derivada.md"
echo "naftaleno: ponto de fusão em torno de 80 °C" > obsidian/projetos/naftaleno.md
echo "hoje fui ao ponto de ônibus" > obsidian/diario/2026-10-13.md
```

```check
resp_arquivo naftaleno.md
```

## p-mtime · 1250 · Só o que é novo

Crie a pasta `recentes/` e mova pra ela todos os arquivos de `Downloads/`
modificados nos **últimos 7 dias**. Os mais velhos ficam onde estão.

> tags: find
> dica: o find filtra pela idade do arquivo. Liste os recentes e confira antes de mover qualquer coisa
> dica: `-mtime` conta em dias; o sinal de menos quer dizer "menos de"
> dica: o find roda um comando pra cada achado com `-exec ... {} \;` — o {} vira o nome do arquivo
> solucao: mkdir recentes
> solucao: find Downloads -type f -mtime -7 -exec mv {} recentes/ \;

```setup
mkdir -p Downloads
n=0
for d in 1 2 4 5 12 20 40 90; do
  n=$((n+1)); f="Downloads/arquivo_${n}.pdf"; echo $d > "$f"; quando "$d days ago" "$f"
done
```

```check
existe recentes
for f in "$ORIG"/Downloads/*; do
  b=$(basename "$f")
  if [ -n "$(find "$f" -mtime -7)" ]; then
    [ -e "recentes/$b" ] || falha "$b é recente e devia estar em recentes/"
  else
    [ -e "Downloads/$b" ] || falha "$b é velho e devia continuar em Downloads/"
  fi
done
```

## p-mais-comum · 1250 · A mais tocada

Qual música aparece **mais vezes** em `tocadas.txt`, o histórico do player?

> tags: sort, uniq
> dica: conte quantas vezes cada música aparece, depois ordene pela contagem
> dica: o uniq tem uma flag que conta, mas ele só junta linhas iguais que estão *vizinhas*, por isso o sort vem antes. E o sort entende número com -n
> dica: formato: sort ___ | uniq ___ | sort ___ | tail -1
> solucao: sort tocadas.txt | uniq -c | sort -n | tail -1
> solucao: responder evidencias

```setup
awkr 'BEGIN{semente(17); n=split("evidencias:9 garota-de-ipanema:8 aquarela:7 trem-bala:6 epitafio:4", e, " ");
  for(i=1;i<=n;i++){ split(e[i], p, ":"); for(j=0;j<p[2];j++) l[++k]=p[1] }
  for(i=k;i>1;i--){ j=1+int(rnd()*i); t=l[i]; l[i]=l[j]; l[j]=t }
  for(i=1;i<=k;i++) print l[i] }' > tocadas.txt
```

```check
resp "$(sort "$ORIG/tocadas.txt" | uniq -c | sort -n | tail -1 | awk '{print $2}')"
```

## p-traco · 1300 · O arquivo chamado -f

Alguém criou em `bagunca/` um arquivo chamado **`-f`**. Apague só ele.
(Spoiler: `rm -f` não vai funcionar como você quer.)

> tags: rm, aspas
> dica: o rm acha que `-f` é uma flag. Como dizer "isso aqui é um NOME"?
> dica: existe um marcador que diz "acabaram as flags". Ou escreva o caminho de um jeito que não comece com traço
> solucao: cd bagunca
> solucao: rm -- -f

```setup
mkdir -p bagunca
echo x > bagunca/-f
echo y > bagunca/importante.txt
echo z > bagunca/f
```

```check
[ ! -e "bagunca/-f" ] || falha "bagunca/-f ainda existe"
intacto_exceto '/-f$'
```

## p-ferrugem · 1300 · A matéria atrasada

Em `notas/`, qual arquivo tem **mais linhas** que mencionam `revisar`?

> tags: grep, sort
> dica: o grep conta linhas por arquivo quando você passa vários arquivos de uma vez
> dica: o -c com vários arquivos imprime arquivo:contagem. Pra ordenar pelo número que vem depois dos dois-pontos, o sort precisa saber o separador (-t) e a coluna (-k)
> solucao: grep -c revisar notas/*.md | sort -t: -k2 -n | tail -1
> solucao: responder calculo.md

```setup
mkdir -p notas
lin() { f=$1; n=$2; shift 2; for i in $(seq 1 "$n"); do echo "$* ($i)"; done >> "notas/$f"; }
lin calculo.md 6 "revisar a lista de limites"
lin calculo.md 3 "aula normal"
lin fisica.md 4 "revisar cinemática"
lin fisica.md 1 "revisar revisar revisar revisar revisar revisar revisar"
lin quimica.md 4 "revisar estequiometria"
lin ingles.md 2 "revisar verbos"
lin historia.md 4 "ler o capítulo"
```

```check
resp_arquivo calculo.md
```

## p-sed · 1350 · Erro de digitação em massa

O nome do orientador saiu errado — `Gustav0`, com **zero** — em várias notas de
`tcc/`. Troque por `Gustavo` em todas. Nada mais muda.

> tags: sed
> dica: primeiro descubra em quais arquivos o erro aparece, pra conferir no fim
> dica: o sed troca com `s/velho/novo/`; um `g` no fim troca todas da linha
> dica: sem `-i` o sed só imprime o resultado; com `-i` grava no arquivo
> solucao: sed -i 's/Gustav0/Gustavo/g' tcc/*.md

```setup
mkdir -p tcc
printf 'Reunião com prof. Gustav0\nGustav0 sugeriu mudar o título\n' > tcc/reuniao.md
printf 'Orientação: Gustav0 (Depto. de Física)\n' > tcc/plano.md
printf 'Nada aqui, só Gustavo certo\n' > tcc/ok.md
printf 'Gustav0, Gustav0 e Gustav0 de novo\n' > tcc/repetido.md
```

```check
for f in "$ORIG"/tcc/*.md; do
  b=$(basename "$f")
  [ "$(sed 's/Gustav0/Gustavo/g' "$f")" = "$(cat "tcc/$b")" ] || falha "tcc/$b não ficou certo"
done
```

## p-junta · 1400 · Juntar estações

Junte todos os CSVs de `estacoes/` num só: `todas.csv` (na pasta atual, `~`),
com **um** cabeçalho no topo e depois as linhas de dados de todas as estações.

> tags: head, tail, redirect
> dica: o cabeçalho vem de um arquivo só; os dados vêm de todos, sem o cabeçalho de cada um
> dica: `>` cria o arquivo e `>>` acrescenta no fim — são dois comandos
> dica: `tail -n +2` começa da linha 2; com vários arquivos ele imprime o nome de cada, e `-q` cala isso
> solucao: head -1 estacoes/campinas.csv > todas.csv
> solucao: tail -q -n +2 estacoes/*.csv >> todas.csv

```setup
mkdir -p estacoes
gera_estacao estacoes/campinas.csv 2025 30 1
gera_estacao estacoes/curitiba.csv 2025 30 2
gera_estacao estacoes/recife.csv 2025 30 3
```

```check
existe todas.csv
[ "$(head -1 todas.csv)" = "data,tmin,tmax,chuva_mm" ] || falha "a 1ª linha devia ser o cabeçalho"
[ "$(grep -c '^data,' todas.csv)" = 1 ] || falha "tem mais de um cabeçalho no meio"
[ "$(tail -n +2 todas.csv | sort)" = "$(tail -q -n +2 "$ORIG"/estacoes/*.csv | sort)" ] || falha "as linhas de dados não batem"
```

## p-soma · 1450 · Chuva de março

Quantos **mm** choveu no total em **março de 2025**, segundo `estacao.csv`?
(1 casa decimal)

> tags: awk, grep
> dica: duas etapas: filtrar só as linhas de março, depois somar a coluna da chuva
> dica: as datas começam com 2025-03; no grep, `^` casa só o começo da linha
> dica: o awk soma assim: `{s+=$N} END {print s}` — falta escolher o N e o separador
> solucao: grep '^2025-03' estacao.csv | awk -F, '{s+=$4} END {print s}'
> solucao: responder 235.8

```setup
gera_estacao estacao.csv 2025 151 41
```

```check
resp_num "$(awk -F, '$1 ~ /^2025-03/ {s+=$4} END {printf "%.1f", s}' "$ORIG/estacao.csv")"
```

## p-media · 1500 · Média do mercado

Qual a **média** de valor (R$) dos gastos de **mercado** em
`gastos.csv`? (1 casa decimal)

> tags: awk
> dica: média é soma dividida pela quantidade; o awk faz as duas na mesma passada
> dica: `awk -F,` usa vírgula de separador; uma condição antes das chaves filtra as linhas
> dica: `{s+=$4; n++} END {...}` — falta imprimir a divisão com 1 casa (`printf "%.1f\n"`)
> solucao: awk -F, '$3=="mercado" {s+=$4; n++} END {printf "%.1f\n", s/n}' gastos.csv
> solucao: responder 21.6

```setup
gera_gastos gastos.csv 160 59
```

```check
resp_num "$(awk -F, '$3=="mercado" {s+=$4; n++} END {printf "%.1f", s/n}' "$ORIG/gastos.csv")"
```

## p-sem-espaco · 1500 · Nome sem espaço

Os livros em `kindle/` têm espaço no nome, e isso atrapalha no terminal. Renomeie
**todos** trocando cada espaço por `_` (ex.: `Dom Casmurro Machado.azw3` →
`Dom_Casmurro_Machado.azw3`). Conteúdo e extensão não mudam.

> tags: for, mv, aspas
> dica: é a mesma operação pra cada arquivo: um for com mv. O difícil é calcular o nome novo a partir do antigo
> dica: o bash troca texto dentro de uma variável: ${var//de/para} troca TODAS as ocorrências. Teste com echo antes do mv, e aspas em tudo
> dica: formato: for f in kindle/*; do mv "$f" "${___}"; done
> solucao: for f in kindle/*' '*; do mv "$f" "${f// /_}"; done

```setup
mkdir -p kindle
for t in "Dom Casmurro Machado" "O Hobbit Tolkien" "Calculo vol 1 Stewart" "Fisica Basica Halliday" "manual_geladeira"; do
  echo "$t" > "kindle/$t.azw3"
done
```

```check
nenhum 'kindle/* *'
[ "$(ls kindle | wc -l)" -eq 5 ] || falha "eram 5 arquivos em kindle/"
for f in "$ORIG"/kindle/*; do
  n="kindle/$(basename "$f" | tr ' ' _)"
  cmp -s "$f" "$n" || falha "falta $n (ou o conteúdo mudou)"
done
```

## p-pior-talhao · 1550 · Quem estourou

Qual morador tem **mais gastos acima de R$ 20** em `gastos.csv`?

> tags: awk, sort, uniq
> dica: filtre só os gastos acima de 20, depois conte quantos cada morador tem
> dica: o awk filtra comparando coluna com número; cuidado com o cabeçalho
> dica: contar repetidos é a receita da lição 11: cut, sort, uniq -c, sort -rn
> solucao: awk -F, 'NR>1 && $4 > 20' gastos.csv | cut -d, -f2 | sort | uniq -c | sort -rn | head -3
> solucao: responder Caio

```setup
gera_gastos gastos.csv 200 8
```

```check
resp "$(awk -F, 'NR>1 && $4 > 20' "$ORIG/gastos.csv" | cut -d, -f2 | sort | uniq -c | sort -rn | head -1 | awk '{print $2}')"
```

## p-por-ano · 1600 · Arquivar por ano

As fotos de `fotos/` se chamam `AAAA-MM-DD_algo.jpg`. Mova cada uma para uma
subpasta com o ano dela: `fotos/2023/`, `fotos/2024/`...

> tags: for, mv
> dica: cada foto precisa de duas coisas: a pasta do ano existir e o mv pra dentro dela. Num laço
> dica: `${f%%-*}` corta tudo a partir do PRIMEIRO `-`: `2024-03-12_x.jpg` → `2024`
> dica: `for f in *.jpg; do mkdir -p ___ && mv ___ ___; done`
> solucao: cd fotos
> solucao: for f in *.jpg; do mkdir -p "${f%%-*}" && mv "$f" "${f%%-*}/"; done

```setup
mkdir -p fotos
for d in 2023-11-02_aniversario 2023-12-24_natal 2024-03-12_praia 2024-03-12_por-do-sol 2024-07-01_formatura 2025-01-15_praia 2025-10-12_show 2026-02-03_trilha; do
  echo "$d" > "fotos/$d.jpg"
done
```

```check
nenhum 'fotos/*.jpg'
for f in "$ORIG"/fotos/*.jpg; do
  b=$(basename "$f"); a=${b%%-*}
  cmp -s "$f" "fotos/$a/$b" || falha "falta fotos/$a/$b"
done
```

## p-duplicatas · 1700 · Papers repetidos

Em `papers/` tem PDFs **repetidos** — mesmo conteúdo, nomes diferentes.
Apague as cópias, deixando **um** de cada.

> tags: md5sum, sort, uniq
> dica: o nome não ajuda — compare o CONTEÚDO. Arquivos iguais têm a mesma impressão digital (hash)
> dica: o md5sum calcula o hash de cada um; ordenando, os iguais ficam lado a lado
> dica: o uniq com `-w32` compara só os 32 primeiros caracteres (o hash); `man uniq` tem a flag que mostra todas as repetidas
> solucao: md5sum papers/* | sort | uniq -w32 -D
> solucao: rm "papers/Silva2010 (1).pdf" papers/Lima2016_copy.pdf papers/download.pdf papers/download_2.pdf

```setup
mkdir -p papers
echo "conteudo silva"  > papers/Silva2010_energia.pdf
echo "conteudo silva"  > "papers/Silva2010 (1).pdf"
echo "conteudo lima"   > papers/Lima2016_clima.pdf
echo "conteudo lima"   > papers/Lima2016_copy.pdf
echo "conteudo costa"  > papers/Costa2014_solar.pdf
echo "conteudo costa"  > papers/download.pdf
echo "conteudo costa"  > papers/download_2.pdf
echo "conteudo rocha"  > papers/Rocha1998_revisao.pdf
```

```check
unicos_orig=$(cat "$ORIG"/papers/* | sort -u | wc -l)
unicos=$(cat papers/* 2>/dev/null | sort -u | wc -l)
total=$(ls papers | wc -l)
[ "$unicos" = "$unicos_orig" ] || falha "você apagou a última cópia de algum paper"
[ "$total" = "$unicos" ] || falha "ainda tem $((total - unicos)) cópia(s) sobrando"
```

## p-log-hora · 1800 · A hora do caos

`site.log` é o log do servidor do site. Em que **hora do dia** aconteceram mais linhas de
`ERROR`? Responda só a hora, com dois dígitos (ex.: `09`).

> tags: grep, cut, sort, uniq
> dica: filtre as linhas de ERROR e olhe algumas: onde fica a hora?
> dica: a hora está sempre na mesma posição — `cut -c` corta por posição de caractere
> dica: depois, a receita de contar repetidos da lição 11
> solucao: grep ERROR site.log | cut -c12-13 | sort | uniq -c | sort -rn | head -3
> solucao: responder 03

```setup
awkr 'BEGIN{semente(5); split("INFO INFO INFO INFO WARN ERROR",lv," ");
  for(i=0;i<600;i++){ h=int(rnd()*24); l=lv[1+int(rnd()*6)];
    if(h==3 && rnd()<0.6) l="ERROR";
    printf "2026-10-%02d %02d:%02d:%02d %s %s\n", 1+int(rnd()*13), h, int(rnd()*60), int(rnd()*60), l, (l=="ERROR")?"database timeout":"ok" }}' | sort > site.log
```

```check
resp "$(grep ERROR "$ORIG/site.log" | cut -c12-13 | sort | uniq -c | sort -rn | head -1 | awk '{print $2}')"
```

## p-exceto-cache · 1900 · Faxina seletiva

Apague todos os arquivos `.tmp` em **qualquer lugar** de `projeto/` — **exceto**
os que estão dentro de pastas chamadas `cache` (essas o programa usa).

> tags: find
> dica: liste todos os .tmp com find; depois tire da lista os de cache. Só apague com a lista certa
> dica: `-not` nega o teste seguinte; `-path` casa o caminho inteiro com um padrão
> dica: o padrão do -path é "qualquer coisa, /cache/, qualquer coisa" — no fim, a ação que apaga
> solucao: find projeto -name '*.tmp' -not -path '*/cache/*' -delete

```setup
mkdir -p projeto/{src,build/obj,cache,src/modulo/cache,docs}
for d in projeto projeto/src projeto/build/obj projeto/docs; do echo t > $d/lixo.tmp; done
echo t > projeto/build/obj/b.tmp
for d in projeto/cache projeto/src/modulo/cache; do echo keep > $d/indice.tmp; done
echo code > projeto/src/main.py; echo n > projeto/docs/notas.tmp.md
```

```check
[ -z "$(find projeto -name '*.tmp' -not -path '*/cache/*')" ] || falha "ainda tem: $(find projeto -name '*.tmp' -not -path '*/cache/*' | tr '\n' ' ')"
intacto_exceto '\.tmp$'
intacto projeto/cache projeto/src/modulo/cache
```
