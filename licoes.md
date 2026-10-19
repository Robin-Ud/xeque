# Lições do tutor

Formato: `## ID · título`, texto da lição (vira o `meta`), `> dica:`, `> solucao:`,
`> inicio:` (pasta onde o shell abre, relativa à arena) e os blocos `setup` / `check`.
Rode `./xeque.sh validar` depois de mexer aqui.

## 01 · Onde estou?
> fichas: pwd, cd, ls

O terminal está sempre **dentro** de uma pasta. Três comandos te orientam:

  $ pwd          mostra onde você está
  $ ls           lista o que tem aqui
  $ cd pasta     entra numa pasta

`cd` aceita um caminho inteiro de uma vez: `cd fotos/2025/marco`.
A tecla **Tab** completa nomes: digite `cd sa` e aperte Tab. Use Tab SEMPRE —
é mais rápido e evita erro de digitação (adeus `cd obisidian`).

Aqui dentro, `~` é a pasta da arena, não a sua home de verdade.
Comandos do xeque: `pronto` confere · `dica` ajuda · `meta` relê · `reset` recomeça.

MISSÃO: entre na pasta `calculo` do ano **2025** de `faculdade/` e digite `pronto` lá dentro.

> dica: `ls` mostra o que tem aqui. O ano fica dentro da faculdade, e a matéria dentro do ano
> dica: dá pra ir num `cd` só, com o caminho inteiro separado por `/` — use Tab em cada parte
> solucao: cd faculdade/2025/calculo

```setup
mkdir -p faculdade/{2024,2025}/{calculo,fisica,quimica} notas
echo "prova 12/10" > faculdade/2025/calculo/lista3.txt
echo "lembrar de devolver o livro" > notas/todo.txt
```

```check
em faculdade/2025/calculo
```

## 02 · Subir, voltar e pular
> fichas: cd

`..` é sempre "a pasta de cima". Dá pra encadear:

  $ cd ..              sobe um nível
  $ cd ../fisica       sobe um e entra em fisica (a "irmã")
  $ cd ../../2024      sobe dois e entra em 2024
  $ cd -               volta pra pasta onde você estava antes
  $ cd                 sozinho (ou cd ~) volta pra casa

Caminho que começa com `/` é **absoluto** (a partir da raiz do sistema).
Todo o resto é **relativo** à pasta onde você está — por isso `pwd` importa.

MISSÃO: você começou em `faculdade/2025/calculo/lista3`. Vá para `faculdade/2024/fisica`
**usando `..`** num cd só (sem passar por `~`).

> inicio: faculdade/2025/calculo/lista3
> dica: conte quantos níveis precisa subir até chegar em `faculdade/`
> dica: subiu até `faculdade/`? O mesmo caminho continua descendo: ano, depois matéria
> solucao: cd ../../../2024/fisica

```setup
mkdir -p faculdade/{2024,2025}/{calculo,fisica}/lista{1,2,3}
```

```check
em faculdade/2024/fisica
usou '..'
```

## 03 · Enxergar de verdade: as flags do ls
> fichas: ls

`ls` sozinho esconde muita coisa. As **flags** (letras com `-`) mudam isso:

  $ ls -l      formato longo: permissões, tamanho, data
  $ ls -h      tamanhos legíveis (4,0K, 12M) — junto com -l
  $ ls -a      mostra os OCULTOS (nomes que começam com .)
  $ ls -S      ordena por tamanho, maior primeiro
  $ ls -t      ordena por data, mais recente primeiro

Flags se juntam: `ls -lhS` = longo, legível, por tamanho.
Camada: -l -a -S -t são POSIX (qualquer máquina); o -h é extra (GNU, Mac e
busybox têm, um Unix velho não).
Esqueceu uma flag? `ls --help | less` ou `man ls` (sai com q).

MISSÃO: tem um arquivo enorme enchendo a pasta `fotos/`. Qual é o nome dele?
Responda com `responder NOME`.

> dica: o que mais ocupa espaço vem primeiro se o ls ordenar por tamanho — olhe as flags acima
> dica: ...mas será que ele aparece? Arquivo oculto começa com ponto, e o ls esconde esses sem a flag certa
> solucao: ls -lhSa fotos
> solucao: responder .cache_miniaturas.db

```setup
for i in 0412 0413 0417 0420 0425; do bytes fotos/IMG_$i.jpg $(( ${i#0} * 900 )); done
bytes fotos/IMG_0430.jpg 2400000
bytes fotos/.cache_miniaturas.db 9000000
```

```check
resp .cache_miniaturas.db "não — tem um arquivo maior ainda, escondido"
```

## 04 · Criar, copiar, mover, renomear
> fichas: mkdir, touch, cp, mv

  $ mkdir papers            cria pasta (mkdir -p a/b/c cria a árvore toda)
  $ touch nota.md           cria arquivo vazio
  $ cp a.txt b.txt          copia (cp -r pra pastas)
  $ mv a.pdf papers/        MOVE pra dentro da pasta
  $ mv velho.txt novo.txt   RENOMEIA — mv é mover E renomear

Nome com espaço ou parênteses precisa de **aspas**, senão o shell
acha que são vários argumentos:

  $ mv "planilha final (2).xlsx" planilha.xlsx

(O Tab já escapa os espaços pra você: digite `mv plan` + Tab.)

MISSÃO: em `Downloads/`: crie a pasta `papers` (dentro de Downloads) e mova pra
ela os 3 PDFs. Depois renomeie `gastos viagem FINAL (2).xlsx` para `gastos_viagem.xlsx`.

> dica: três passos: criar a pasta, mover os PDFs, renomear a planilha. Entre em `Downloads` primeiro
> dica: o mv aceita vários arquivos de uma vez; o ÚLTIMO argumento é o destino
> dica: o nome da planilha tem espaço e parênteses: aspas em volta dele inteiro, ou comece a digitar e aperte Tab
> solucao: cd Downloads && mkdir papers
> solucao: mv Silva2010_energia.pdf Costa2014_solar.pdf Lima2016_clima.pdf papers/
> solucao: mv "gastos viagem FINAL (2).xlsx" gastos_viagem.xlsx

```setup
mkdir -p Downloads
for f in Silva2010_energia Costa2014_solar Lima2016_clima; do echo "%PDF $f" > Downloads/$f.pdf; done
echo "data,item,valor" > "Downloads/gastos viagem FINAL (2).xlsx"
echo "foto" > Downloads/whatsapp_img.jpg
```

```check
existe Downloads/papers
for f in Silva2010_energia Costa2014_solar Lima2016_clima; do
  cmp -s "$ORIG/Downloads/$f.pdf" "Downloads/papers/$f.pdf" || falha "$f.pdf não está em Downloads/papers"
done
nenhum 'Downloads/*.pdf'
cmp -s "$ORIG/Downloads/gastos viagem FINAL (2).xlsx" Downloads/gastos_viagem.xlsx || falha "falta Downloads/gastos_viagem.xlsx"
sumiu "Downloads/gastos viagem FINAL (2).xlsx"
intacto Downloads/whatsapp_img.jpg
```

## 05 · O * e seus amigos
> fichas: glob

Quando você escreve `*`, quem resolve é o **shell**, ANTES do comando rodar.
O `rm` nunca vê o `*` — recebe a lista de nomes já pronta.

  $ *.jpg        tudo que termina em .jpg
  $ 2024*        tudo que começa com 2024
  $ IMG_04??.jpg ? = exatamente um caractere
  $ t[1-3].txt   um caractere da lista: t1, t2, t3

**Regra de ouro:** antes de `rm` com `*`, rode `echo` com o MESMO padrão.
`echo 2024*` mostra exatamente o que o `rm 2024*` vai apagar. Custa 1 segundo.

MISSÃO: em `fotos/`, apague **só as fotos de 2024**. As de 2025 e as
planilhas ficam.

> dica: `cd fotos` e `ls` — repare em TODOS os nomes que têm 2024, não só nas fotos
> dica: um padrão que só olha o começo do nome leva planilha junto. Ele tem que casar o começo E a extensão — teste com echo
> solucao: cd fotos
> solucao: echo 2024*.jpg
> solucao: rm 2024*.jpg

```setup
mkdir -p fotos
for d in 2024-03-12 2024-03-15 2024-04-02 2025-03-10 2025-03-22; do
  for t in t1 t2; do echo "jpg $d $t" > fotos/${d}_$t.jpg; done
done
echo "item,valor" > fotos/gastos2024.csv
echo "item,valor" > fotos/gastos2025.csv
```

```check
nenhum 'fotos/2024-*.jpg'
intacto_exceto '^\./fotos/2024-.*\.jpg$'
```

## 06 · rm sem medo (e com respeito)
> fichas: rm, glob

`rm` não manda pra lixeira: apagou, sumiu.

  $ rm arquivo         apaga arquivo
  $ rm -r pasta        apaga pasta e tudo dentro
  $ rm -i *.log        pergunta um por um
  $ trash-put coisa    lixeira de verdade — do pacote trash-cli: só existe
                       se alguém instalou; numa VM, não conte com ele

`rm -rf *` apaga TUDO da pasta em que você está. Se você estiver na pasta
errada, é assim que uma home inteira some. Hábito que salva:

  1. escreva o caminho **explícito** (`rm -rf lixo/*`), não confie no `pwd`
  2. `echo` antes do `rm`

Detalhe: o `*` **não pega ocultos** (nomes com ponto na frente).
Pra esses use `.[!.]*` (POSIX), ou deixe o `find lixo -mindepth 1 -delete`
resolver (-mindepth e -delete são extras: GNU, Mac e busybox têm).

MISSÃO: você está em `projeto/src`. Esvazie a pasta `~/lixo` (apague tudo lá
dentro, inclusive subpastas e ocultos), mas a pasta `lixo` continua existindo.
Nada fora dela pode ser tocado.

> inicio: projeto/src
> dica: cuidado: `rm -rf *` AQUI apagaria o seu código. Use o caminho `~/lixo/`
> dica: depois do primeiro rm, rode `ls -a ~/lixo` — sobrou alguma coisa?
> dica: o * não pega ocultos. A explicação acima tem um padrão que pega: ponto, depois algo que NÃO é ponto
> solucao: echo ~/lixo/* ~/lixo/.[!.]*
> solucao: rm -rf ~/lixo/* ~/lixo/.[!.]*

```setup
mkdir -p projeto/src lixo/rascunhos/velhos
echo "print('oi')" > projeto/src/main.py
echo "# meu projeto" > projeto/README.md
for i in 1 2 3; do echo "lixo $i" > lixo/tmp$i.txt; done
echo x > lixo/rascunhos/a.md; echo y > lixo/rascunhos/velhos/b.md
echo "segredo velho" > lixo/.oculto_antigo
```

```check
[ -d lixo ] || falha "a pasta lixo tinha que continuar existindo"
[ -z "$(ls -A lixo)" ] || falha "lixo ainda tem: $(ls -A lixo | tr '\n' ' ')"
intacto projeto
```

## 07 · Olhar dentro: cat, head, tail, less, wc
> fichas: cat, head, tail, less, wc

  $ cat arq          despeja o arquivo inteiro
  $ head arq         10 primeiras linhas (head -n 3 → 3 primeiras)
  $ tail arq         10 últimas (tail -n 1 → só a última)
  $ less arq         navega: espaço desce, /palavra busca, q sai
  $ wc -l arq        conta linhas

`tail -n +2 arq` = "do começo da linha 2 em diante" — o jeito clássico de
pular o cabeçalho de um CSV.

MISSÃO: `estacao.csv` tem dados diários da estação meteorológica, com uma
linha de cabeçalho. Quantos **dias** de dados tem ali?

> dica: `head -3 estacao.csv` pra ver o formato
> dica: contar linhas você já viu acima. Mas a missão pede DIAS: toda linha é um dia?
> solucao: wc -l estacao.csv
> solucao: responder 213

```setup
gera_estacao estacao.csv 2025 213 7
```

```check
resp 213 "conta de novo — lembre que a 1ª linha é cabeçalho"
```

## 08 · Procurar texto: grep
> fichas: grep

  $ grep palavra arq      linhas que contêm "palavra"
  $ grep -i palavra arq   ignorando maiúscula/minúscula
  $ grep -c palavra arq   só conta as linhas
  $ grep -r palavra pasta procura em todos os arquivos, recursivo
  $ grep -l palavra *     só o NOME dos arquivos que casam
  $ grep -v palavra arq   o contrário: linhas que NÃO contêm
  $ grep -n palavra arq   mostra o número da linha

Camada: -i -c -l -v -n são POSIX. O -r não é — GNU, Mac e busybox têm, mas um
Unix velho não; lá o jeito é `find pasta -type f -exec grep -l palavra {} +`.
O `rg` (ripgrep) não é nativo: rápido, mas não conte com ele fora da sua máquina.

MISSÃO: na pasta `notas/` (e subpastas), em quantas notas aparece
"monitoria" — escrita de qualquer jeito, maiúscula ou minúscula?

> dica: procure recursivamente na pasta. Mas e "Monitoria"? e "MONITORIA"?
> dica: três flags resolvem: recursivo, ignorar caixa e mostrar só o nome do arquivo. Dá pra juntar as três num `-abc`
> solucao: grep -ril monitoria notas
> solucao: responder 5

```setup
arq notas/calculo.md <<'E'
# Cálculo
Inscrição na monitoria até sexta.
E
arq notas/rotina.md <<'E'
Terça e quinta: Monitoria de física, 14h.
E
arq notas/mercado.md <<'E'
Arroz, feijão, café. Nada de monitor por aqui.
E
arq notas/facul/reuniao.md <<'E'
Professor pediu: MONITORIA de cálculo vs física.
E
arq notas/facul/edital.md <<'E'
Edital das monitorias abertas.
E
arq notas/facul/refs.md <<'E'
Livro do Stewart — lista da monitoria.
E
arq notas/bike.md <<'E'
Trocar a corrente da bike.
E
```

```check
resp 5 "não confere — tem notas em subpasta e com MAIÚSCULA também"
```

## 09 · O cano: |
> fichas: pipe

O `|` (pipe) liga a saída de um comando na entrada do próximo.
É a ideia mais poderosa do terminal: comandos pequenos, encadeados.

  $ ls | wc -l                      quantos itens tem aqui
  $ grep pizza pedidos.csv | head -3   os 3 primeiros pedidos de pizza
  $ grep pizza pedidos.csv | grep Ana  pizza E da Ana

Leia da esquerda pra direita: "pega isso, ENTÃO filtra, ENTÃO conta".

MISSÃO: em `gastos.csv` (as contas da república), quantos gastos são de
**mercado feitos pelo Caio**? (colunas: id,morador,categoria,valor,data)

> dica: `grep mercado gastos.csv` primeiro, olhe o que sai
> dica: agora filtre de novo pelo morador e conte as linhas que sobraram — tudo num cano só
> solucao: grep mercado gastos.csv | grep ',Caio,' | wc -l
> solucao: responder 4

```setup
gera_gastos gastos.csv 120 3
```

```check
resp "$(grep ',Caio,mercado,' "$ORIG/gastos.csv" | wc -l)"
```

## 10 · Redirecionar: > e >>
> fichas: redir

A saída que iria pra tela pode ir pra um arquivo:

  $ ls > lista.txt          cria/SOBRESCREVE lista.txt
  $ date >> log.txt         ACRESCENTA no fim (não apaga o que tinha)
  $ cmd 2> erros.txt        manda só os erros

Cuidado: `>` num arquivo que já existe **zera** ele antes. `>>` acrescenta.

MISSÃO: crie `resumo.txt` com duas linhas: na 1ª, o **número** de gastos de
mercado em `gastos.csv`; na 2ª, o número de gastos de lanche. Só os números.

> dica: o grep tem uma flag que imprime só a contagem, em vez das linhas
> dica: o primeiro vai com `>`, o segundo com `>>`
> solucao: grep -c mercado gastos.csv > resumo.txt
> solucao: grep -c lanche gastos.csv >> resumo.txt

```setup
gera_gastos gastos.csv 80 5
```

```check
existe resumo.txt
esperado="$(grep -c mercado "$ORIG/gastos.csv"; grep -c lanche "$ORIG/gastos.csv")"
[ "$(tr -d ' ' < resumo.txt)" = "$esperado" ] || falha "resumo.txt devia ser:
$esperado
mas está:
$(cat resumo.txt)"
intacto gastos.csv
```

## 11 · Cortar, ordenar, contar
> fichas: cut, sort, uniq

  $ cut -d, -f2 arq.csv     só a 2ª coluna (-d, = separador vírgula)
  $ sort                    ordena (sort -n numérico, -r invertido)
  $ uniq -c                 conta repetições VIZINHAS (por isso: sort antes!)
  $ head -1                 fica só com a primeira

A receita mais famosa do terminal — "o que mais aparece?":

  $ cut -d, -f2 arq | sort | uniq -c | sort -rn | head

MISSÃO: em `bandejao.csv` (dia,prato,preco,data), qual prato o bandejão
serviu em **mais dias**?

> dica: o prato é a coluna 2; o cut separa colunas (`-d` é o separador)
> dica: agora é a receita "o que mais aparece?" da explicação, trocando a coluna e o arquivo
> solucao: cut -d, -f2 bandejao.csv | sort | uniq -c | sort -rn | head -3
> solucao: responder feijoada

```setup
{ echo "dia,prato,preco,data"
  i=1
  for c in strogonofe feijoada feijoada strogonofe lasanha feijoada strogonofe omelete feijoada strogonofe feijoada lasanha feijoada strogonofe omelete feijoada strogonofe feijoada lasanha feijoada strogonofe; do
    echo "D$i,$c,$(( (i * 7) % 23 + 4 )).5,2025-10-$(( i % 28 + 1 ))"; i=$((i+1))
  done; } > bandejao.csv
```

```check
resp feijoada
```

## 12 · find: achar o que se perdeu
> fichas: find

`find` procura arquivos por nome, tipo, tamanho, data...

  $ find . -name 'nota.md'        pelo nome exato, a partir daqui
  $ find . -iname '*.pdf'         padrão, ignorando caixa
  $ find . -type d -name cache    só pastas
  $ find . -size +10M             maiores que 10 MB
  $ find . -mtime -7              modificados nos últimos 7 dias

**Aspas no padrão!** `find . -name '*.pdf'` — sem aspas, o shell expande o
`*` antes e o find recebe outra coisa.

Camada: -name -type -size -mtime são POSIX; o -iname é extra (GNU, Mac e
busybox têm).

MISSÃO: o PDF `contrato_estagio.pdf` se perdeu em algum lugar daqui.
Ache e mova pra `~/estagio/`.

> dica: o find procura pelo nome a partir de uma pasta — `.` é "daqui"
> dica: copie o caminho que o find mostrou e use num mv com destino `estagio/`
> solucao: find . -name contrato_estagio.pdf
> solucao: mv Documentos/facul/estatistica/aulas/antigas/contrato_estagio.pdf estagio/

```setup
mkdir -p estagio Downloads/velhos Documentos/facul/{estatistica,quimica}/aulas/antigas Documentos/jogos
for d in Downloads Downloads/velhos Documentos/facul/estatistica/aulas Documentos/facul/quimica/aulas; do
  echo "%PDF aula" > $d/aula_$(echo $d | md5sum | cut -c1-4).pdf
done
echo "%PDF contrato" > Documentos/facul/estatistica/aulas/antigas/contrato_estagio.pdf
echo "%PDF outro" > Downloads/contrato_estagio_RASCUNHO.pdf
```

```check
cmp -s "$ORIG/Documentos/facul/estatistica/aulas/antigas/contrato_estagio.pdf" estagio/contrato_estagio.pdf \
  || falha "estagio/contrato_estagio.pdf não está lá (ou não é o certo)"
sumiu Documentos/facul/estatistica/aulas/antigas/contrato_estagio.pdf
intacto_exceto 'antigas/contrato_estagio\.pdf$'
```

## 13 · E-se: &&, || e ;
> fichas: encadear

Todo comando termina com um código: 0 = deu certo, outro = falhou.
Você pode encadear decisões:

  $ mkdir bkp && cp -r notas bkp/   cp SÓ roda se o mkdir deu certo
  $ cd pasta || echo "não existe"   echo só roda se o cd falhou
  $ cmd1 ; cmd2                     roda os dois, aconteça o que acontecer

Esse é o jeito seguro em scripts: `cd pasta && rm -rf *` nunca apaga no lugar
errado — se o `cd` falhar, o `rm` nem roda.

MISSÃO: numa linha só, com `&&`: crie a pasta `backup` e copie a pasta
`notas` inteira pra dentro dela.

> dica: copiar pasta precisa de `cp -r`
> solucao: mkdir backup && cp -r notas backup/

```setup
mkdir -p notas/facul
echo "cálculo" > notas/a.md; echo "física" > notas/facul/b.md
```

```check
usou '&&'
diff -r "$ORIG/notas" backup/notas >/dev/null 2>&1 || falha "backup/notas não é uma cópia completa de notas/"
intacto notas
```

## 14 · for: repetir pra cada arquivo
> fichas: for

  $ for f in *.txt; do echo "achei $f"; done

`f` vira cada nome, um por vez. Use SEMPRE `"$f"` com aspas (nome com espaço).
Truques de nome, que o bash faz sozinho:

  $ ${f%.JPG}       tira ".JPG" do FIM     IMG_1.JPG → IMG_1
  $ ${f#IMG_}       tira "IMG_" do COMEÇO  IMG_1.JPG → 1.JPG

Ensaie com `echo` antes:

  $ for f in *.JPG; do echo mv "$f" "${f%.JPG}.jpg"; done

Tirou o `echo`, executou de verdade.

Camada: o for e o `${f%...}` / `${f#...}` são POSIX (qualquer sh). O `${f//a/b}`
(troca tudo) e o `{1..5}` são do bash: num `#!/bin/sh` do Ubuntu, quebram.

MISSÃO: as fotos de `camera/` vieram com `.JPG` maiúsculo. Renomeie todas
para `.jpg` minúsculo (o resto do nome igual).

> dica: `cd camera` e ensaie o laço com echo, como no exemplo
> dica: tem foto com espaço no nome — as aspas em "$f" não são opcionais
> solucao: cd camera
> solucao: for f in *.JPG; do mv "$f" "${f%.JPG}.jpg"; done

```setup
mkdir -p camera
for n in DSC_0040 DSC_0041 "DSC 0042" DSC_0043 por_do_sol; do echo "img $n" > "camera/$n.JPG"; done
```

```check
nenhum 'camera/*.JPG'
for n in DSC_0040 DSC_0041 "DSC 0042" DSC_0043 por_do_sol; do
  cmp -s "$ORIG/camera/$n.JPG" "camera/$n.jpg" || falha "falta camera/$n.jpg"
done
```

## 15 · Scripts: chmod +x e ./
> fichas: chmod, sh

Um script é um arquivo de texto com comandos. Pra rodar ele precisa de
permissão de **execução** (o `x` do `ls -l`):

  $ ls -l backup.sh       -rw-r--r--  → sem x, não executa
  $ chmod +x backup.sh    dá permissão de execução
  $ ./backup.sh           roda — o ./ diz "este aqui, da pasta atual"

Sem o `./`, o shell só procura nas pastas do `$PATH` — nunca na pasta atual.
(É por isso que seus scripts moram em `~/.local/bin`, que está no PATH.)

MISSÃO: `backup.sh` está pronto mas não executa. Dê permissão de execução e
rode ele (ele cria o `backup_ok.txt`).

> dica: `ls -l backup.sh` — tem x?
> dica: o chmod dá a permissão (o `+` adiciona); depois rode com `./` na frente do nome
> solucao: chmod +x backup.sh
> solucao: ./backup.sh

```setup
cat > backup.sh <<'E'
#!/bin/bash
echo "backup feito em $(date +%F)" > backup_ok.txt
echo "✓ backup ok"
E
chmod -x backup.sh
```

```check
[ -x backup.sh ] || falha "backup.sh ainda não é executável"
existe backup_ok.txt
```
