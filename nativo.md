# Trilha nativa

Formato igual ao de `licoes.md`/`puzzles.md`, mais `> etapa: N`. Sem rating = lição
(roda na ordem do arquivo, antes dos puzzles da etapa); com rating = puzzle.
O PATH da arena só tem os comandos das etapas 1..N (configs.json → `trilha`), via
busybox. O `validar` roda cada solução com o PATH da etapa do item: se ela usar
um comando que ainda não foi desbloqueado, falha.

## n1-a · Sua caixa de ferramentas
> etapa: 1
> fichas: posix, busybox, ls

Aqui o shell é o bash de sempre, mas o **PATH** está quase vazio. PATH é a
lista de pastas onde o shell procura um comando quando você digita o nome dele.
O que não está lá dá `command not found` — igual numa VM crua.

Comando é de dois tipos:

  $ type cd        embutido (builtin): faz parte do próprio shell, existe sempre
  $ type -a ls     tudo que responde pelo nome ls: um apelido e um programa
  $ echo $PATH     onde o shell procura
  $ ls --help      aqui não tem man: todo comando explica as flags com --help

Apelido (alias) é um atalho de texto: `ls` vira `ls --color=auto` antes de rodar.
Quase toda distro já vem com esse no `.bashrc`. O programa de verdade é um
arquivo numa pasta do PATH — e é ele que importa numa máquina alheia.

Embutidos que você já tem: `cd`, `pwd`, `echo`, `printf`, `type`, `test`.
O resto vem por etapa. `ficha` lista as histórias; `ficha ls` mostra uma.

MISSÃO: liste com detalhes (`-l`) a pasta do seu PATH e descubra **pra onde
aponta** o `ls` que você está usando. Responda o nome do programa (sem a pasta).

> dica: no `ls -l`, uma seta `->` no fim da linha quer dizer que aquele nome é um atalho pra outro arquivo
> dica: aqui o PATH é uma pasta só, então dá pra passar ele direto pro ls com o $ na frente
> solucao: ls -l $PATH
> solucao: responder busybox

```setup
mkdir -p notas
```

```check
resp_arquivo busybox
```

## n1-b · Andar sem tree
> etapa: 1
> fichas: ls, cd

O `tree` não existe aqui, nem na maioria das VMs. O substituto nativo é o `ls -R`:

  $ ls -R          lista tudo, pasta por pasta (cada pasta vira um título com : no fim)
  $ ls -a          inclui os ocultos (nomes que começam com .)
  $ ls -l          detalhes: permissão, dono, tamanho, data
  $ ls -F          marca pasta com / (útil quando não tem cor)
  $ cd -           volta pra pasta anterior
  $ cd             volta pra casa (~)

Tab completa nomes, `..` sobe um nível, caminho que começa com `/` é absoluto.

MISSÃO: em algum lugar dentro de `faculdade/` tem um arquivo `gabarito.txt`. Ache
com o `ls -R`, **entre na pasta dele** e digite `pronto` lá.

> dica: o ls -R imprime o caminho de cada pasta (terminado em :) e embaixo o que tem nela
> dica: achou? o caminho do título serve pro cd, sem os : do fim
> solucao: ls -R faculdade
> solucao: cd faculdade/2024/fisica/lista2

```setup
mkdir -p faculdade/{2024,2025}/{calculo,fisica}/lista{1,2,3}
echo "1a 2c 3b 4d" > faculdade/2024/fisica/lista2/gabarito.txt
echo "prova 12/10" > faculdade/2025/calculo/lista1/prova.txt
echo "entrega 03/03" > faculdade/2024/calculo/lista3/entrega.txt
```

```check
em faculdade/2024/fisica/lista2
```

## n1-c · Criar coisas
> etapa: 1
> fichas: mkdir, touch, redir, echo

  $ mkdir -p a/b/c          cria a pasta e as mães que faltarem
  $ touch nota.txt          cria arquivo vazio (se existe, só atualiza a data)
  $ echo "texto" > a.txt    escreve num arquivo — APAGA o que tinha
  $ echo "mais" >> a.txt    acrescenta no fim
  $ cat a.txt               mostra o conteúdo

`>` e `>>` não são programas: quem redireciona é o shell, então funcionam em
qualquer lugar. As chaves também são do shell, que expande antes de rodar:

  $ echo t{1,2,3}           vira: t1 t2 t3
  $ echo t{1..5}            vira: t1 t2 t3 t4 t5
  $ mkdir -p x/{a,b}/{c,d}  4 pastas de uma vez

(Chaves são do bash, zsh e ksh — o `sh` puro do POSIX não expande.)

MISSÃO: crie `agenda/2025/provas.txt` contendo exatamente estas duas linhas:

    calculo 12/10
    fisica 20/10

> dica: primeiro a pasta (com as mães), depois o arquivo
> dica: a primeira linha com >, a segunda com >> — com > de novo você apagaria a primeira
> solucao: mkdir -p agenda/2025
> solucao: echo "calculo 12/10" > agenda/2025/provas.txt
> solucao: echo "fisica 20/10" >> agenda/2025/provas.txt

```setup
mkdir -p notas
```

```check
existe agenda/2025/provas.txt
[ "$(cat agenda/2025/provas.txt)" = "$(printf 'calculo 12/10\nfisica 20/10')" ] \
  || falha "o provas.txt não tem exatamente as duas linhas (cat pra conferir)"
```

## n1-p1 · 300 · Achados e perdidos
> etapa: 1

Em qual **sala** está o arquivo `achados.txt`, dentro de `predio/`?
Responda o nome da pasta da sala.

> tags: ls
> dica: o ls tem uma flag que entra em todas as subpastas
> dica: procure o nome do arquivo e olhe o título (terminado em :) acima dele
> solucao: ls -R predio
> solucao: responder sala_6

```setup
mkdir -p predio/bloco_a/sala_{1,2,3,4} predio/bloco_b/sala_{5,6,7,8}
echo "guarda-chuva preto, garrafa azul" > predio/bloco_b/sala_6/achados.txt
echo "projetor ok" > predio/bloco_a/sala_2/equipamentos.txt
echo "limpeza: terça" > predio/bloco_b/sala_8/avisos.txt
```

```check
resp_arquivo sala_6
```

## n1-p2 · 350 · O que está escondido
> etapa: 1

Quantos itens **ocultos** (arquivos ou pastas) tem direto dentro de `config/`?

> tags: ls, ocultos
> dica: o ls sozinho esconde tudo que começa com ponto
> dica: o -a mostra também o . e o .. (que não contam); a versão maiúscula da flag já tira os dois
> solucao: ls -A config
> solucao: responder 4

```setup
mkdir -p config/.cache config/temas
echo "rede=Casa" > config/.wifi
echo "escuro" > config/.tema
echo "ctrl+t" > config/.atalhos
echo "ok" > config/leiame.txt
```

```check
resp "$(ls -A "$ORIG/config" | grep -c '^\.')"
```

## n1-p3 · 400 · A senha da biblioteca
> etapa: 1

A senha do wifi da biblioteca está escrita num arquivo oculto, dentro de alguma
pasta oculta em `~`. Qual é a senha?

> tags: ls, ocultos, cat
> dica: o ls -R não entra em pasta oculta sozinho: junte ele com a flag dos ocultos
> dica: achou o arquivo? o cat mostra o que tem dentro
> solucao: ls -aR
> solucao: cat .config/rede/.wifi_biblioteca
> solucao: responder livro2026

```setup
mkdir -p .config/rede .config/tema documentos
printf 'rede=Biblioteca\nsenha=livro2026\n' > .config/rede/.wifi_biblioteca
printf 'rede=Casa\n' > .config/rede/casa.conf
echo "cor=verde" > .config/tema/atual
echo "lembrar: trocar senha" > documentos/todo.txt
```

```check
resp livro2026
```

## n1-p4 · 400 · Mais um dia no diário
> etapa: 1

O `diario.txt` já tem dois dias anotados. Acrescente a linha `dia 3 mercado`
**no fim**, sem apagar nada do que já tem.

> tags: redirect
> dica: um sinal de > sozinho reescreve o arquivo inteiro
> dica: o echo escreve a linha; o redirecionamento duplo acrescenta no fim
> solucao: echo "dia 3 mercado" >> diario.txt

```setup
printf 'dia 1 mudança\ndia 2 faxina\n' > diario.txt
```

```check
existe diario.txt
[ "$(cat diario.txt)" = "$(printf 'dia 1 mudança\ndia 2 faxina\ndia 3 mercado')" ] \
  || falha "diario.txt devia ter os dois dias de antes e o dia 3 no fim (cat pra conferir)"
```

## n1-p5 · 450 · Pastas do semestre
> etapa: 1

Crie dentro de `semestre/` uma pasta pra cada matéria (`calculo`, `fisica`, `quimica`)
e, dentro de **cada** matéria, as pastas `provas` e `listas`.

**Regra:** um comando só, **sem loop** e sem digitar nenhum nome de pasta duas vezes.

> tags: mkdir, chaves
> dica: o mkdir cria várias pastas de uma vez, e uma flag cria as mães que faltam
> dica: o shell transforma uma lista entre chaves em várias palavras, e dá pra usar duas listas no mesmo caminho
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

## n1-p6 · 500 · Listas entregues
> etapa: 1

Dentro de `listas/`, crie os arquivos vazios `l1.ok`, `l2.ok`... até `l8.ok`.

**Regra:** um comando só, sem loop e sem digitar os oito nomes.

> tags: touch, chaves
> dica: o touch cria vários arquivos de uma vez, um por argumento
> dica: as chaves também geram sequência de números, com dois pontos entre o começo e o fim
> solucao: touch listas/l{1..8}.ok

```setup
mkdir -p listas
```

```check
for i in 1 2 3 4 5 6 7 8; do
  [ -f "listas/l$i.ok" ] || falha "falta listas/l$i.ok"
  [ -s "listas/l$i.ok" ] && falha "listas/l$i.ok devia estar vazio"
done
[ "$(ls listas | wc -l)" = 8 ] || falha "listas/ tem coisa a mais além dos 8"
usou '{'
```

## n1-p7 · 550 · O relatório mais novo
> etapa: 1

Qual arquivo de `relatorios/` foi **modificado por último**?

> tags: ls
> dica: o ls ordena por nome, mas tem flag pra ordenar por data
> dica: com -l junto você vê as datas e confere
> solucao: ls -lt relatorios
> solucao: responder visita_tecnica.txt

```setup
mkdir -p relatorios
for f in abril.txt zebra_final.txt estagio.txt visita_tecnica.txt laboratorio.txt; do echo x > relatorios/$f; done
quando '2025-04-30 10:00' relatorios/abril.txt
quando '2025-06-01 09:00' relatorios/zebra_final.txt
quando '2025-08-15 16:20' relatorios/estagio.txt
quando '2025-09-02 08:45' relatorios/visita_tecnica.txt
quando '2025-07-10 11:00' relatorios/laboratorio.txt
```

```check
resp_arquivo visita_tecnica.txt
```

## n1-p8 · 600 · Juntando o relatório
> etapa: 1

O relatório veio picado em `parte1.txt`, `parte2.txt` e `parte3.txt`. Junte os
três, **nessa ordem**, num arquivo `relatorio.txt`. As partes ficam como estão.

> tags: cat, redirect
> dica: o nome cat vem de concatenate: juntar
> dica: ele aceita vários arquivos e escreve um atrás do outro; falta mandar a saída pro arquivo novo
> solucao: cat parte1.txt parte2.txt parte3.txt > relatorio.txt

```setup
printf 'RELATÓRIO DA VIAGEM DE CAMPO 2025\nTurma de Geografia\n' > parte1.txt
printf '\nônibus: R$ 1.200\nhotel: R$ 3.400\n' > parte2.txt
printf '\nobs: choveu no segundo dia\n' > parte3.txt
```

```check
existe relatorio.txt
cat "$ORIG/parte1.txt" "$ORIG/parte2.txt" "$ORIG/parte3.txt" | cmp -s - relatorio.txt \
  || falha "relatorio.txt não é parte1 + parte2 + parte3, nessa ordem"
intacto parte1.txt parte2.txt parte3.txt
```

## n1-p9 · 650 · O mais pesado
> etapa: 1

Qual é o **maior** arquivo direto em `Downloads/`, **contando os ocultos**?

> tags: ls, ocultos
> dica: o ls tem flag pra ordenar por tamanho e flag pra mostrar ocultos — dá pra juntar as duas
> dica: com -l você vê os tamanhos e confere quem ficou no topo
> solucao: ls -lAS Downloads
> solucao: responder .video_viagem.mp4

```setup
mkdir -p Downloads
bytes Downloads/filme.mkv 3000000
bytes Downloads/.video_viagem.mp4 4500000
bytes Downloads/planilha.xlsx 80000
bytes Downloads/.cache_miniaturas 20000
bytes Downloads/manual.pdf 900000
```

```check
resp_arquivo .video_viagem.mp4
```

## n1-p10 · 700 · Nomes com espaço
> etapa: 1

Crie a pasta `trabalho em grupo` e, dentro dela, o arquivo vazio `notas 2025.txt`
— com os espaços, exatamente assim.

> tags: aspas, mkdir, touch
> dica: pro shell, espaço separa argumentos: sem cuidado, isso vira três pastas
> dica: aspas em volta transformam o nome inteiro num argumento só
> solucao: mkdir "trabalho em grupo"
> solucao: touch "trabalho em grupo/notas 2025.txt"

```setup
mkdir -p notas
```

```check
for p in trabalho em grupo; do
  [ -e "$p" ] && falha "apareceu '$p' sozinho: o espaço separou o nome em pedaços (rm -r ele e tente de novo)"
done
[ -d "trabalho em grupo" ] || falha "falta a pasta 'trabalho em grupo'"
[ -f "trabalho em grupo/notas 2025.txt" ] || falha "falta 'notas 2025.txt' dentro dela"
```

## n2-a · Copiar e mover
> etapa: 2
> fichas: cp, mv

  $ cp a.txt b.txt          copia (se b.txt existe, é sobrescrito SEM perguntar)
  $ cp a.txt pasta/         copia pra dentro da pasta, com o mesmo nome
  $ cp -R fotos fotos_bak   copia a pasta inteira (R = recursivo)
  $ mv velho.txt novo.txt   renomeia
  $ mv *.pdf papers/        move vários pra dentro de uma pasta
  $ cp -i ... / mv -i ...   pergunta antes de sobrescrever

No Unix não existe "renomear" à parte: é mover pro mesmo lugar com outro nome.

MISSÃO: faça um backup da pasta `dados/` chamado `dados_2025` e depois renomeie
`notas.txt` para `notas_antigas.txt`.

> dica: copiar pasta precisa da flag recursiva
> dica: renomear é o mv do nome velho pro nome novo
> solucao: cp -R dados dados_2025
> solucao: mv notas.txt notas_antigas.txt

```setup
mkdir -p dados/brutos
printf 'aluno,nota\nAna,8\nBia,9\n' > dados/notas.csv
echo "leitura 1" > dados/brutos/sensor.txt
echo "comprar cartucho" > notas.txt
```

```check
[ -d dados_2025 ] || falha "falta a pasta dados_2025"
diff -r "$ORIG/dados" dados_2025 >/dev/null || falha "dados_2025 não é cópia completa de dados/"
intacto dados
existe notas_antigas.txt
sumiu notas.txt
```

## n2-b · Apagar sem medo
> etapa: 2
> fichas: rm, glob, rmdir

Não existe lixeira no terminal. Três hábitos salvam:

  $ echo rm *.tmp     ENSAIA: mostra no que o * vai virar, sem apagar nada
  $ rm -i arquivo     pergunta antes de cada um
  $ rmdir pasta       só apaga pasta VAZIA — o jeito seguro
  $ rm -r pasta       apaga a pasta e tudo dentro (sem volta)

Quem troca o `*` pelos nomes é o **shell**, antes do rm rodar: o rm nem vê o
asterisco. Por isso o `echo` mostra exatamente o que seria apagado.

MISSÃO: em `projeto/` tem vários `.tmp` misturados com o trabalho. Apague todos
os `.tmp` que estão direto em `projeto/` — e nada mais. Ensaie antes.

> dica: o mesmo comando com echo na frente mostra a lista sem apagar
> dica: o asterisco casa qualquer começo de nome; o .tmp fixa o final
> solucao: echo rm projeto/*.tmp
> solucao: rm projeto/*.tmp

```setup
mkdir -p projeto/figuras
for f in a b c d; do echo lixo > projeto/$f.tmp; done
echo "texto" > projeto/capitulo1.md
echo "texto" > projeto/capitulo2.md
echo "tmp de verdade" > projeto/figuras/grafico.tmp
echo "x" > projeto/tmp_notas.txt
```

```check
nenhum 'projeto/*.tmp'
intacto_exceto '^\./projeto/[^/]*\.tmp$'
```

## n2-c · Atalhos
> etapa: 2
> fichas: ln

  $ ln -s faculdade/2025 atual  cria 'atual' apontando pra faculdade/2025 (symlink)
  $ ls -l                       mostra: atual -> faculdade/2025
  $ ln a.txt b.txt            hard link: b.txt vira OUTRO NOME do mesmo arquivo

Symlink é um bilhete com um caminho escrito: se o alvo some, ele quebra. Hard
link é o mesmo arquivo com dois nomes: apagar um não apaga o outro.
Você já usa symlinks nesta trilha: o seu PATH é feito deles (`ls -l $PATH`).

MISSÃO: crie em `~` um atalho (symlink) chamado `hoje` que leve pra
`faculdade/2025/calculo`. Teste com `cd hoje` antes do pronto.

> dica: a flag -s faz symlink; sem ela é hard link (que não funciona com pasta)
> dica: a ordem é a mesma do cp: primeiro o que já existe, depois o nome novo
> solucao: ln -s faculdade/2025/calculo hoje

```setup
mkdir -p faculdade/{2024,2025}/{calculo,fisica}
echo "prova 12/10" > faculdade/2025/calculo/prova.txt
```

```check
[ -L hoje ] || falha "hoje não é um symlink"
[ hoje -ef faculdade/2025/calculo ] || falha "hoje não leva pra faculdade/2025/calculo"
```

## n2-p1 · 450 · Relatório final
> etapa: 2

Renomeie `relatorio final.txt` para `relatorio_final.txt`.

> tags: mv, aspas
> dica: renomear é mover pro mesmo lugar com outro nome
> dica: o nome antigo tem espaço: proteja com aspas, ou com \ antes do espaço
> solucao: mv "relatorio final.txt" relatorio_final.txt

```setup
printf 'semestre 2025\nmédia 7,8\n' > "relatorio final.txt"
echo "rascunho" > rascunho.txt
```

```check
existe relatorio_final.txt
sumiu "relatorio final.txt"
cmp -s "$ORIG/relatorio final.txt" relatorio_final.txt || falha "o conteúdo mudou"
```

## n2-p2 · 500 · Fotos no lugar
> etapa: 2

Mova todas as fotos `.jpg` que estão em `Downloads/` para a pasta `fotos/`.
O resto de `Downloads/` fica onde está.

> tags: mv, glob
> dica: o mv aceita vários arquivos e, no fim, a pasta de destino
> dica: um asterisco seguido da extensão casa todas as fotos
> solucao: mv Downloads/*.jpg fotos/

```setup
mkdir -p Downloads fotos
for i in 1 2 3 4 5; do echo jpg > Downloads/IMG_00$i.jpg; done
echo pdf > Downloads/artigo.pdf
echo jpg > Downloads/capa.jpeg
echo x > Downloads/jpg_lista.txt
```

```check
nenhum 'Downloads/*.jpg'
for f in "$ORIG"/Downloads/*.jpg; do
  b=$(basename "$f"); cmp -s "$f" "fotos/$b" || falha "fotos/$b não chegou"
done
intacto_exceto '\.jpg$'
```

## n2-p3 · 550 · Rabos de editor
> etapa: 2

Alguns editores deixam cópias de segurança com um `~` no fim do nome
(`calculo.txt~`). Apague todas elas de `notas/` sem tocar em mais nada.

> tags: rm, glob
> dica: ensaie com echo na frente antes de apagar
> dica: o asterisco casa o começo; o caractere do fim vem logo depois dele
> solucao: echo rm notas/*~
> solucao: rm notas/*~

```setup
mkdir -p notas
for f in calculo fisica quimica; do echo "$f" > notas/$f.txt; echo "velho" > "notas/$f.txt~"; done
echo "~ no meio" > "notas/a~b.txt"
```

```check
nenhum 'notas/*~'
intacto_exceto '~$'
```

## n2-p4 · 600 · Só as vazias
> etapa: 2

Dentro de `velho/` tem quatro pastas. Apague as que estão **vazias** e só elas.

> tags: rmdir
> dica: tem um comando que só apaga pasta vazia e recusa as outras
> dica: pode mandar todas de uma vez: as cheias dão erro e ficam
> solucao: rmdir velho/*

```setup
mkdir -p velho/a velho/b velho/c velho/d
echo "importante" > velho/b/nota.txt
echo "foto" > velho/d/foto.jpg
```

```check
sumiu velho/a
sumiu velho/c
intacto velho/b velho/d
```

## n2-p5 · 650 · Atalho pro ano
> etapa: 2

Crie `~/atual` como symlink para `faculdade/2025` e, **entrando pelo atalho**, crie
lá dentro a pasta `provas`.

> tags: ln
> dica: ln com a flag de symlink; primeiro o que já existe, depois o nome novo
> dica: o atalho funciona como a pasta: dá pra usar ele no caminho do mkdir
> solucao: ln -s faculdade/2025 atual
> solucao: mkdir atual/provas

```setup
mkdir -p faculdade/2024 faculdade/2025/listas
```

```check
[ -L atual ] || falha "atual não é symlink"
[ atual -ef faculdade/2025 ] || falha "atual não leva pra faculdade/2025"
[ -d faculdade/2025/provas ] || falha "falta faculdade/2025/provas"
```

## n2-p6 · 700 · Potes trocados
> etapa: 2

Os arquivos `pote_acucar.txt` e `pote_sal.txt` estão com os nomes
trocados: um tem o conteúdo do outro. Destroque. No fim, só esses dois arquivos.

> tags: mv
> dica: com dois nomes só, um sobrescreve o outro: precisa de um terceiro lugar no meio
> dica: três mv — um nome temporário segura o primeiro enquanto você move o segundo
> solucao: mv pote_acucar.txt tmp
> solucao: mv pote_sal.txt pote_acucar.txt
> solucao: mv tmp pote_sal.txt

```setup
printf 'conteúdo: sal\nmarca: Cisne\n' > pote_acucar.txt
printf 'conteúdo: açúcar\nmarca: União\n' > pote_sal.txt
```

```check
cmp -s "$ORIG/pote_sal.txt" pote_acucar.txt || falha "pote_acucar.txt ainda não tem o conteúdo do açúcar"
cmp -s "$ORIG/pote_acucar.txt" pote_sal.txt || falha "pote_sal.txt ainda não tem o conteúdo do sal"
[ "$(ls -A | wc -l)" = 2 ] || falha "sobrou arquivo a mais (o temporário?)"
```

## n2-p7 · 750 · Entrega dos dados
> etapa: 2

Crie a pasta `entrega/` com uma cópia de **todos os `.csv`** que estão nas
subpastas de `projetos/` — só os csv, todos juntos, sem subpastas. O `projetos/`
fica intacto.

> tags: cp, glob
> dica: o asterisco funciona em qualquer parte do caminho, inclusive no nome da pasta
> dica: um caminho com dois asteriscos pega os csv de todas as subpastas de uma vez; falta criar a pasta antes
> solucao: mkdir entrega
> solucao: cp projetos/*/*.csv entrega/

```setup
mkdir -p projetos/robo projetos/site projetos/app
for c in robo site app; do
  printf 'item,valor\npeca,10\n' > projetos/$c/custos_$c.csv
  echo foto > projetos/$c/foto_$c.jpg
done
printf 'data,visitas\n' > projetos/site/visitas_site.csv
```

```check
[ -d entrega ] || falha "falta a pasta entrega/"
for f in "$ORIG"/projetos/*/*.csv; do
  b=$(basename "$f"); cmp -s "$f" "entrega/$b" || falha "falta entrega/$b"
done
[ "$(ls -A entrega | wc -l)" = "$(ls "$ORIG"/projetos/*/*.csv | wc -l)" ] || falha "entrega/ tem coisa que não é csv"
intacto projetos
```

## n2-p8 · 800 · Sem gastar espaço
> etapa: 2

A `apostila.pdf` (grande) também precisa estar em `entrega/apostila.pdf`. Mas sem
ocupar o dobro do disco, e de um jeito que, **se alguém apagar a `apostila.pdf`
original, a de `entrega/` continue funcionando**.

> tags: ln
> dica: cópia ocupa o dobro; symlink quebra se o original sumir. Sobra um tipo de link
> dica: o ln sem a flag -s dá outro nome pro mesmo arquivo
> solucao: ln apostila.pdf entrega/apostila.pdf

```setup
bytes apostila.pdf 2000000
mkdir -p entrega
```

```check
existe entrega/apostila.pdf
[ -L entrega/apostila.pdf ] && falha "é symlink: se a apostila.pdf original sumir, ele quebra"
[ entrega/apostila.pdf -ef apostila.pdf ] || falha "é uma cópia: ocupa o dobro do espaço"
```

## n2-p9 · 850 · Sem perder o antigo
> etapa: 2

Mova **tudo** de `novos/` para `arquivo/`. Só que `arquivo/` já tem um
`relatorio.txt` que não pode ser perdido: o de `novos/` tem que entrar como
`relatorio_novo.txt`.

> tags: mv
> dica: o mv sobrescreve sem perguntar — resolva primeiro o arquivo que tem o nome repetido
> dica: dois passos: o relatório com nome novo, depois o resto com asterisco
> solucao: mv novos/relatorio.txt arquivo/relatorio_novo.txt
> solucao: mv novos/* arquivo/

```setup
mkdir -p novos arquivo
echo "relatório 2024 — NÃO APAGAR" > arquivo/relatorio.txt
echo "planilha velha" > arquivo/custos_2024.csv
echo "relatório 2025" > novos/relatorio.txt
echo "fotos" > novos/fotos.txt
echo "custos" > novos/custos_2025.csv
```

```check
cmp -s "$ORIG/arquivo/relatorio.txt" arquivo/relatorio.txt || falha "o relatorio.txt antigo foi sobrescrito"
cmp -s "$ORIG/novos/relatorio.txt" arquivo/relatorio_novo.txt || falha "falta arquivo/relatorio_novo.txt com o relatório novo"
for f in fotos.txt custos_2025.csv; do cmp -s "$ORIG/novos/$f" "arquivo/$f" || falha "arquivo/$f não chegou"; done
nenhum 'novos/*'
```

## n3-a · Começo e fim
> etapa: 3
> fichas: head, tail

  $ head arquivo          as 10 primeiras linhas
  $ head -n 3 arquivo     as 3 primeiras
  $ tail -n 3 arquivo     as 3 últimas
  $ tail -n +2 arquivo    da linha 2 até o fim (pula o cabeçalho)
  $ tail -f log.txt       fica olhando o fim enquanto o arquivo cresce (Ctrl+C sai)

Arquivo de dados costuma ser grande demais pra `cat`. Olhe as pontas primeiro.

MISSÃO: `estacao.csv` tem uma leitura por dia. Em que **data** foi a última
leitura? (a data é a primeira coluna; responda do jeito que está escrita)

> dica: a última leitura é a última linha
> dica: o irmão do head mostra o fim; diga quantas linhas você quer
> solucao: tail -n 1 estacao.csv
> solucao: responder 2025-07-19

```setup
gera_estacao estacao.csv 2025 200 7
```

```check
resp "$(tail -n 1 "$ORIG/estacao.csv" | cut -d, -f1)"
```

## n3-b · Contar e encaixar
> etapa: 3
> fichas: wc, pipe

  $ wc -l arquivo               linhas
  $ wc -w arquivo               palavras
  $ wc -c arquivo               bytes
  $ wc -l < arquivo             só o número, sem o nome do arquivo do lado
  $ tail -n +2 a.csv | wc -l    o | liga a saída de um na entrada do outro

O `|` (pipe) é do shell, como o `>`: existe em qualquer lugar. É a ideia central
do Unix — programas pequenos que se encaixam (`ficha pipe`).

MISSÃO: quantos **gastos** tem `gastos.csv`? Cada linha é um gasto,
menos a primeira, que é o cabeçalho.

> dica: o wc conta todas as linhas, inclusive o cabeçalho
> dica: dá pra descontar 1 de cabeça, ou cortar o cabeçalho antes e mandar pro wc pelo pipe
> solucao: tail -n +2 gastos.csv | wc -l
> solucao: responder 87

```setup
gera_gastos gastos.csv 87 3
```

```check
resp "$(($(wc -l < "$ORIG/gastos.csv") - 1))"
```

## n3-c · Ler sem se afogar
> etapa: 3
> fichas: less

O `cat` despeja tudo de uma vez. Pra ler com calma, use um paginador:

  $ less arquivo      espaço desce · b sobe · /texto busca · n próxima · g início · G fim · q sai
  $ less -N arquivo   com número de linha
  $ less -S a.csv     sem quebrar linha comprida (bom pra csv)
  $ more arquivo      o avô do less: só vai pra frente. É o único que o POSIX garante.

MISSÃO: o `sistema.log` tem milhares de linhas. Abra com o less, busque por
`ERRO` e responda o **horário** (HH:MM:SS) do **primeiro** erro.

> dica: dentro do less, a barra começa uma busca; Enter confirma
> dica: a busca para na primeira ocorrência a partir de onde você está; o horário é a segunda coisa da linha
> solucao: # less sistema.log  →  /ERRO  Enter
> solucao: responder 12:06:47

```setup
awk 'BEGIN{ t=6*3600
  for(i=1;i<=3000;i++){ t+=7+(i*13)%11; h=int(t/3600); m=int(t%3600/60); s=t%60
    if(i==1834) msg="ERRO sensor de temperatura sem resposta"
    else if(i==2411) msg="ERRO falha ao gravar leitura"
    else msg="INFO leitura ok sala " (1+i%8)
    printf "2025-10-17 %02d:%02d:%02d %s\n", h,m,s,msg }}' > sistema.log
```

```check
resp "$(grep -m1 ERRO "$ORIG/sistema.log" | cut -d' ' -f2)"
```

## n3-p1 · 550 · As colunas
> etapa: 3

Qual é o nome da **quarta coluna** de `gastos.csv`?

> tags: head
> dica: os nomes das colunas ficam na primeira linha
> dica: o head mostra o começo; diga a ele quantas linhas quer
> solucao: head -n 1 gastos.csv
> solucao: responder valor

```setup
gera_gastos gastos.csv 300 5
```

```check
resp "$(head -n 1 "$ORIG/gastos.csv" | cut -d, -f4)"
```

## n3-p2 · 600 · Chuva do primeiro dia
> etapa: 3

Quanto choveu (última coluna, em mm) no **primeiro dia** registrado em `estacao.csv`?

> tags: head
> dica: a primeira linha é o cabeçalho; o primeiro dia vem logo depois
> dica: pegue as primeiras linhas com o head e leia a coluna do fim
> solucao: head -n 2 estacao.csv
> solucao: responder 7.3

```setup
gera_estacao estacao.csv 2025 150 9
```

```check
resp_num "$(sed -n 2p "$ORIG/estacao.csv" | cut -d, -f4)"
```

## n3-p3 · 650 · Tamanho do resumo
> etapa: 3

Quantas **palavras** tem o `resumo.txt`?

> tags: wc
> dica: o wc conta mais coisa além de linhas
> dica: tem flag pra palavras (a inicial em inglês)
> solucao: wc -w resumo.txt
> solucao: responder 58

```setup
arq resumo.txt <<'EOF'
O consumo de energia elétrica em moradias estudantis cresce no verão,
quando ventiladores e chuveiros ficam ligados por mais tempo. Este
trabalho mediu o consumo de doze repúblicas de uma cidade do interior
entre 2023 e 2025. A troca de lâmpadas e o uso de timer no chuveiro
reduziram a conta de luz em 18% no segundo ano.
EOF
```

```check
resp "$(wc -w < "$ORIG/resumo.txt")"
```

## n3-p4 · 700 · A linha 42
> etapa: 3

O que está escrito na **linha 42** de `diario.txt`? Responda a linha inteira.

> tags: head, tail, pipe
> dica: o head pega até a linha 42; dessas, você só quer a última
> dica: encaixe os dois com um pipe
> solucao: head -n 42 diario.txt | tail -n 1
> solucao: responder dia 39: garoa de manhã no bloco 4

```setup
{ echo "# diário — 2025"; echo "# república da rua 7"; echo "# um registro por dia"
  awk 'BEGIN{ split("chuva fraca|sol forte|vento sul|garoa de manhã|nublado|calor seco|chuva forte|neblina",c,"|")
    split("bloco 1|bloco 2|bloco 3|bloco 4|biblioteca|bandejão",l,"|")
    for(d=1;d<=90;d++) printf "dia %d: %s no %s\n", d, c[1+(d*5)%8], l[1+(d*7)%6] }'; } > diario.txt
```

```check
resp "$(sed -n 42p "$ORIG/diario.txt")"
```

## n3-p5 · 750 · As últimas do log
> etapa: 3

Salve as **5 últimas linhas** de `registro.log` num arquivo `ultimas.log`.
O `registro.log` fica intacto.

> tags: tail, redirect
> dica: o tail pega o fim; diga quantas linhas
> dica: a saída vai pro arquivo novo com o redirecionamento simples
> solucao: tail -n 5 registro.log > ultimas.log

```setup
awk 'BEGIN{ for(i=1;i<=120;i++) printf "2025-10-%02d 0%d:00 leitura %d ok\n", 1+int(i/8), i%8, i }' > registro.log
```

```check
existe ultimas.log
tail -n 5 "$ORIG/registro.log" | cmp -s - ultimas.log || falha "ultimas.log não tem exatamente as 5 últimas linhas"
intacto registro.log
```

## n3-p6 · 800 · Sem o cabeçalho
> etapa: 3

Crie `dados.csv`: igual a `estacao.csv`, mas **sem a linha de cabeçalho**.

> tags: tail, redirect
> dica: você quer da segunda linha até o fim
> dica: o tail aceita um + antes do número: aí ele conta a partir do começo
> solucao: tail -n +2 estacao.csv > dados.csv

```setup
gera_estacao estacao.csv 2025 60 9
```

```check
existe dados.csv
tail -n +2 "$ORIG/estacao.csv" | cmp -s - dados.csv || falha "dados.csv devia ser o estacao.csv sem a primeira linha, e mais nada"
intacto estacao.csv
```

## n3-p7 · 850 · O campeão de linhas
> etapa: 3

Dos arquivos em `relatorios/`, qual tem **mais linhas**?

> tags: wc, glob
> dica: o wc aceita vários arquivos de uma vez e mostra um número pra cada
> dica: wc -l com o asterisco; ignore a linha do total
> solucao: wc -l relatorios/*
> solucao: responder calculo.txt

```setup
mkdir -p relatorios
awk 'BEGIN{ for(i=1;i<=40;i++) print "linha " i }' > relatorios/fisica.txt
awk 'BEGIN{ for(i=1;i<=73;i++) print "linha " i }' > relatorios/calculo.txt
awk 'BEGIN{ for(i=1;i<=12;i++) print "linha muito comprida com bastante texto pra parecer o maior arquivo " i }' > relatorios/quimica.txt
awk 'BEGIN{ for(i=1;i<=55;i++) print "linha " i }' > relatorios/historia.txt
```

```check
resp_arquivo calculo.txt
```

## n3-p8 · 900 · Uma semana de janeiro
> etapa: 3

Crie `semana.csv` com o **cabeçalho** de `estacao.csv` seguido das leituras de
**10 a 16 de janeiro** (7 dias). O arquivo começa em 1º de janeiro.

> tags: head, tail, pipe, redirect
> dica: são dois pedaços: o cabeçalho, e depois um recorte do meio. O segundo entra com >>
> dica: com o cabeçalho na linha 1, o dia 10 está na linha 11. Pegue até a linha do dia 16 e, dessas, as últimas 7
> solucao: head -n 1 estacao.csv > semana.csv
> solucao: head -n 17 estacao.csv | tail -n 7 >> semana.csv

```setup
gera_estacao estacao.csv 2025 90 12
```

```check
existe semana.csv
{ sed -n 1p "$ORIG/estacao.csv"; sed -n 11,17p "$ORIG/estacao.csv"; } | cmp -s - semana.csv \
  || falha "semana.csv devia ter o cabeçalho e as linhas de 2025-01-10 a 2025-01-16, e mais nada"
```

## n3-p9 · 950 · A leitura fantasma
> etapa: 3

O `leituras.txt` tem **uma leitura por linha**. Quantas leituras tem?

> tags: wc, cat
> dica: confira o número do wc com o que você vê no fim do arquivo
> dica: o wc -l conta quebras de linha, não linhas — e a última linha pode não ter quebra
> solucao: wc -l leituras.txt
> solucao: tail -n 3 leituras.txt
> solucao: responder 12

```setup
printf '23.1\n22.8\n24.0\n25.3\n24.9\n23.7\n22.2\n21.9\n23.4\n24.6\n25.0\n24.4' > leituras.txt
```

```check
resp 12
```
