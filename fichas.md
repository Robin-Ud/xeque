# Fichas

Formato: `## nome · ano (ou época)`, `> etapa: N` (na trilha, aparece quando a
etapa abre), `> resumo:` (uma linha: ano + por quê + camada; vai no topo das
lições que apontam pra ela com `> fichas:`) e o texto: a história curta, as
camadas e o `cuidado` (quando NÃO usar, ou o que morde). Linhas que começam com
`  POSIX`, `  GNU`, `  Mac/BSD`, `  busybox` ou `  cuidado` ganham cor.
Dentro da arena: `ficha NOME`. No livre, todas valem; na trilha, só as da etapa.

## posix · 1988–1992
> etapa: 1
> resumo: o mínimo que todo Unix garante — o resto muda de máquina pra máquina

Nos anos 80 cada empresa tinha o seu Unix: System V (AT&T), BSD (Berkeley),
SunOS, AIX, HP-UX... Um script que rodava num quebrava no outro. O IEEE juntou
todo mundo e escreveu um padrão: em 1988 a parte do sistema, em 1992 a parte dos
**comandos e do shell**. O nome POSIX foi sugestão do Richard Stallman.

POSIX é o **mínimo garantido**: quem segue o padrão tem esses comandos, com essas
flags, funcionando desse jeito. Linux, Mac, os BSD e o busybox seguem — e cada um
soma seus extras por cima. Os extras é que mudam de máquina pra máquina.

  POSIX     o que roda em qualquer lugar. É o que a trilha te ensina primeiro.
  GNU       extras do Linux comum (Ubuntu, Fedora, Debian). Etapa gnu, no fim.
  Mac/BSD   extras do Mac — DIFERENTES dos GNU. O mesmo -i do sed muda de sintaxe.
  cuidado   "funciona no meu Linux" não quer dizer POSIX. Script que vai viajar:
            teste num sh enxuto (busybox sh, dash) antes.

## busybox · 1995
> etapa: 1
> resumo: 1995, um binário só fazendo papel de dezenas de comandos enxutos

Em 1995 o Bruce Perens precisava que o disquete de instalação do Debian (1,44 MB)
coubesse um Linux de emergência inteiro. Escreveu um único programa que faz o
papel de dezenas de comandos, cada um na versão mais enxuta possível. Virou o
"canivete suíço do Linux embarcado": está no seu roteador, na smart TV, no
recovery do Android, no Alpine (o Linux dos containers Docker).

O truque: um binário só, com vários nomes. Ele olha **com que nome foi chamado**
e age como aquele comando. Confira: `ls -l $PATH` — todos apontam pro mesmo arquivo.

  busybox   tem alguns extras do GNU (sed -i, sort -h, grep -r). Não confie nele
            pra dizer o que é POSIX: confie na ficha.
  sem man   aqui não tem manual. Todo comando responde a --help.
  cuidado   é enxuto de propósito: flag rara do GNU pode não existir, ou existir
            com outro comportamento. Deu erro estranho? --help antes de culpar você.

## cd · builtin
> etapa: 1
> resumo: embutido no shell: um programa filho não consegue mudar a pasta do pai

Por que o `cd` não é um programa como o `ls`? Todo programa roda num **processo
filho** do shell. O filho pode mudar a pasta dele, mas não a do pai — então um
programa `cd` mudaria de pasta e morreria, e você continuaria onde estava. Por
isso ele é embutido no próprio shell. Nos primeiros Unix ele se chamava `chdir`.

  POSIX     cd pasta · cd .. · cd (vai pro $HOME) · cd - (volta pra anterior)
  POSIX     $OLDPWD guarda a pasta anterior; $PWD a atual
  type cd   mostra "cd é um comando interno do shell"
  cuidado   cd pasta; rm -rf * — se o cd falhar (erro de digitação), o rm roda
            ONDE VOCÊ ESTÁ. Sempre cd pasta && rm ..., ou o caminho no próprio rm.

## pwd · builtin
> etapa: 1
> resumo: "onde estou?"; o -P mostra o caminho real, sem atalhos

"print working directory". Existe embutido no shell e também como programa
(`/bin/pwd`) — o embutido é o que você usa.

  POSIX     pwd -P mostra o caminho real, resolvendo atalhos (symlinks)
  POSIX     pwd -L (o padrão) mostra o caminho por onde você chegou
  cuidado   entrou por um atalho? o pwd mostra o atalho, não onde os arquivos
            moram. Antes de apagar algo "aqui", pwd -P.

## echo · o menos portável
> etapa: 1
> resumo: o comando que mais muda entre shells; com \n ou -n, use printf

Um dos comandos mais antigos e o que mais muda de máquina pra máquina. No
System V ele interpretava `\n` sozinho; no BSD não, mas aceitava `-n` pra não
pular linha. O POSIX não conseguiu padronizar os dois jeitos e recomenda usar
`printf` sempre que tiver `\n`, `-n`, ou texto que começa com `-`.

  bash      echo "a\nb" imprime a\nb literal; echo -e interpreta
  dash      o sh do Debian/Ubuntu: echo "a\nb" JÁ pula linha, -e nem existe
  POSIX     printf 'a\nb\n' — igual em todo lugar
  regra     echo pra texto simples; printf pro resto
  cuidado   não use echo pra imprimir variável que você não controla (nome de
            arquivo, linha de csv): se ela começar com - ou tiver \, sai torto.
            printf '%s\n' "$x".

## ls · 1971
> etapa: 1
> resumo: Unix V1, 1971. -R é o tree nativo; --color é só do GNU

Já estava no Unix V1, em 1971, nos Bell Labs. O nome é "list", encurtado — no
Unix os comandos mais usados ganharam nomes de duas letras pra digitar menos
num teletipo que imprimia em papel.

  POSIX     -a ocultos · -A sem . e .. · -l detalhes · -R recursivo (o "tree" nativo)
  POSIX     -t por data · -S por tamanho · -r inverte · -1 um por linha · -F marca pasta com /
  GNU       --color · -h tamanhos legíveis (o -h também existe no Mac e no busybox)
  Mac/BSD   cor é -G; --color não existe no ls antigo do Mac
  cuidado   ls é pra olhos, não pra script: for f in $(ls) quebra em nome com
            espaço, e o formato do -l muda de sistema pra sistema. Em script: for f in *.

## mkdir · 1971
> etapa: 1
> resumo: Unix V1. -p cria as mães que faltam (POSIX); -v é extra

Antes de 1983 não existia uma chamada de sistema pra criar pasta. O `/bin/mkdir`
rodava como root e montava a pasta na mão: criava o diretório e depois os dois
nomes especiais dentro dele, o `.` (ela mesma) e o `..` (a mãe). É por isso que
toda pasta tem esses dois. O BSD 4.2 criou a chamada `mkdir()` e acabou com a gambiarra.

  POSIX     -p cria os pais que faltam e não reclama se já existe · -m define permissão
  GNU       -v avisa cada pasta criada (o Mac também tem)
  cuidado   o -p é calado: mkdir -p safar/2025 cria uma árvore nova com o erro
            de digitação, sem reclamar. Confira com ls depois.

## touch · 1979
> etapa: 1
> resumo: Unix V7, 1979: feito pra mudar data e enganar o make; criar é efeito colateral

Apareceu no Unix V7. Foi feito pra **mudar a data** de um arquivo, não pra criar:
o `make` decide o que recompilar comparando datas, e o `touch` servia pra
"enganar" o make. Criar o arquivo vazio quando ele não existe é efeito colateral
— que virou o uso mais comum.

  POSIX     -c não cria se não existir · -m só a data de modificação · -r copia a data de outro arquivo
  POSIX     -t 202510171230 data no formato fixo AAAAMMDDhhmm
  GNU       -d 'yesterday' ou -d '2025-10-17 12:30' entende data por extenso
  cuidado   num arquivo que já existe, touch não apaga nada, mas muda a data — e
            backup, make e find -mtime decidem pela data. Pra criar vazio de
            propósito (ou zerar), : > arq deixa a intenção clara.

## cat · 1971
> etapa: 1
> resumo: Unix V1: concatenar. O POSIX só tem -u; -n e -A são extras

Unix V1. O nome vem de con**cat**enate: o trabalho dele é **juntar** arquivos,
um atrás do outro. Mostrar um arquivo só é o uso pequeno. Em 1983 o Rob Pike
reclamou que estavam enchendo o cat de opções ("cat -v considered harmful"):
programa bom faz uma coisa só. E nos anos 90 a Usenet criou o prêmio "useless
use of cat" pra quem escreve `cat arq | grep x` em vez de `grep x arq`.

  POSIX     cat a b c > tudo · cat -u (sem buffer) — é a ÚNICA flag do POSIX
  GNU       -n numera linhas · -A mostra caracteres invisíveis (tab, \r, fim de linha)
  Mac/BSD   -n e -v existem; -A não
  cuidado   arquivo grande inunda a tela (less, head); binário (foto, pdf) suja o
            terminal — se acontecer, digite reset. E cat arq | grep x → grep x arq.

## redir · 1971 / 1979
> etapa: 1
> resumo: > e < desde 1971, 2> desde 1979; quem faz é o shell, não o comando

Não é programa: é o **shell** que abre o arquivo antes de rodar o comando, e o
comando nem sabe que está escrevendo num arquivo. O `>` e o `<` já estavam no
shell do Unix V1. O `2>` (separar os erros) veio com o shell do Stephen Bourne,
em 1979: todo programa tem três canais — 0 entrada, 1 saída, 2 erros.

  POSIX     > cria/zera · >> acrescenta · < lê de arquivo · 2> erros · 2>&1 erros junto da saída
  POSIX     : > arq zera um arquivo (o : é o comando que não faz nada)
  bash      &> arq (saída e erros juntos) · |& — atalhos que o sh puro não tem
  cuidado   sort arq > arq deixa arq VAZIO: o shell zera o arquivo antes do sort
            ler. Escreva em outro nome e depois mv.

## cp · 1971
> etapa: 2
> resumo: Unix V1. -R é POSIX; -a é GNU; a barra no fim muda tudo no Mac

Unix V1. Copiar é ler um arquivo e escrever outro: a cópia é independente, ganha
data nova e (sem -p) dono e permissão de quem copiou.

  POSIX     -R recursivo (pasta inteira) · -i pergunta antes de sobrescrever · -p preserva data e permissão
  POSIX     -r é o jeito antigo do -R; quase todo mundo aceita
  GNU       -a (= -R preservando tudo) · -v mostra cada arquivo · -u só se for mais novo
  Mac/BSD   CUIDADO: cp -R pasta/ destino (com a barra no fim) copia o CONTEÚDO,
            não a pasta. No GNU a barra não faz diferença.
  cuidado   sobrescreve o destino calado, sem lixeira. Copiar por cima de algo
            importante: cp -i, ou ls no destino antes.

## mv · 1971
> etapa: 2
> resumo: Unix V1. No mesmo disco só troca o nome — por isso 10 GB move na hora

Unix V1. No mesmo disco, `mv` não copia nada: só troca o nome do arquivo na
pasta. Por isso mover um vídeo de 10 GB é instantâneo. Entre discos diferentes
ele copia tudo e depois apaga o original. "Renomear" não existe à parte: é mover
pro mesmo lugar com outro nome.

  POSIX     -i pergunta antes de sobrescrever · -f nunca pergunta
  extras    -v (GNU, Mac, busybox) mostra o que fez · -n não sobrescreve nunca
  cuidado   mv a destino: se destino é pasta, a entra nela; se não existe, a vira
            "destino". Errou o nome da pasta? Você acabou de renomear o arquivo.
            Pra mover pra pasta, termine com barra: mv a papers/ (falha se não existir).

## rm · 1971
> etapa: 2
> resumo: Unix V1. Tira o nome do arquivo (unlink) — não existe lixeira

Não existe lixeira. Por dentro, o `rm` chama `unlink`: tira o **nome** do arquivo
da pasta. Quando nenhum nome aponta mais pros dados (e nenhum programa está com
ele aberto), o espaço é liberado. É por isso que a chamada se chama unlink — e é
por isso que hard link (ln) funciona.

  POSIX     -r recursivo · -f sem perguntar e sem erro se não existir · -i pergunta cada um
  GNU       --preserve-root (padrão): recusa rm -rf / · -I pergunta uma vez só · -v
  hábito    echo rm *.tmp antes — o * vira os nomes ANTES do rm rodar, e o echo mostra quais
  fora      trash-put (lixeira de verdade) é do pacote trash-cli: não conte com ele
            em máquina alheia.
  cuidado   rm -rf "$PASTA/" com a variável vazia vira rm -rf / . Em script,
            "${PASTA:?}" aborta se ela estiver vazia.

## rmdir · anos 70
> etapa: 2
> resumo: só apaga pasta vazia: o jeito seguro de limpar pastas

O irmão medroso do `rm -r`: só apaga pasta **vazia**. Se tiver qualquer coisa
dentro, recusa e avisa. Por isso é o jeito seguro de limpar pastas: dá pra mandar
todas de uma vez que só as vazias somem.

  POSIX     -p apaga a pasta e as mães que ficarem vazias (rmdir -p a/b/c)
  GNU       --ignore-fail-on-non-empty: não reclama das cheias
  cuidado   "parece vazia mas não apaga": tem oculto lá dentro. ls -A mostra.

## glob · 1971
> etapa: 2
> resumo: * e ? eram um programa à parte (/etc/glob); hoje o shell expande antes

Nos primeiros Unix, quem trocava `*.txt` pelos nomes era um programa separado,
o `/etc/glob` ("global"), que o shell chamava. O Bourne shell (1979) trouxe isso
pra dentro. O ponto é o mesmo até hoje: o **shell** expande, e o comando recebe
a lista pronta. O `rm *.tmp` nunca vê o asterisco.

  POSIX     * qualquer coisa · ? um caractere · [abc] um desses · [!abc] nenhum desses
  bash      ** com shopt -s globstar (desce em subpastas) · extglob
  não-glob  {a,b} e {1..5} são das chaves do bash: geram texto, existindo ou não
  cuidado   nada casou? o padrão vai LITERAL pro comando (rm: *.tmp não existe).
            O * não pega ocultos. Com milhares de arquivos: "argument list too
            long" — aí é find.

## ln · 1971 / 1983
> etapa: 2
> resumo: hard link do Unix V1; symlink do BSD, 1983. -s é POSIX

O hard link é do Unix V1: um arquivo pode ter **vários nomes**, todos iguais, todos
"o original". O `ls -l` mostra quantos nomes cada arquivo tem (o número depois
das permissões). O symlink veio do BSD 4.2, em 1983: um arquivinho que só guarda
um **caminho**, como um bilhete dizendo "o que você quer está ali".

  hard      ln alvo nome — mesmo arquivo, outro nome. Apagar um não afeta o outro.
            Não funciona com pasta nem entre discos.
  symlink   ln -s alvo nome — aponta pro caminho. Funciona com pasta e entre discos,
            mas quebra se o alvo mudar de lugar ou sumir.
  POSIX     -s · -f substitui se já existir
  GNU       -r cria o symlink com caminho relativo automático · -v
  cuidado   o caminho do symlink relativo é lido a partir da pasta do LINK, não
            de onde você está: ln -s dados/a.csv atalhos/a cria um link quebrado.
            Confira com ls -l (link quebrado costuma aparecer em vermelho).

## head · Berkeley, anos 70
> etapa: 3
> resumo: nasceu em Berkeley; head -n N é POSIX, head -n -N é GNU

O Unix V7, da AT&T, não tinha `head`: quem queria as 10 primeiras linhas escrevia
`sed 10q`. Ele nasceu no BSD, em Berkeley, e se espalhou porque fazia falta.

  POSIX     head -n 5 arq
  antigo    head -5 arq — sintaxe velha, ainda aceita quase sempre
  GNU       head -n -5: tudo MENOS as 5 últimas (o busybox também aceita)
  Mac/BSD   não aceita número negativo; -c conta bytes
  cuidado   head -n -5 num script que vai pro Mac quebra. Linha do meio
            (a 42) é sed -n 42p ou head | tail, não dois heads.

## tail · anos 70
> etapa: 3
> resumo: -n +2 pula cabeçalho, -f assiste log ao vivo — tudo POSIX

O par do head, mas com um superpoder: `tail -f` fica olhando o fim do arquivo e
mostra cada linha nova assim que ela é escrita. É como todo administrador de
sistema assiste um log ao vivo.

  POSIX     tail -n 5 · tail -n +2 (da linha 2 até o fim: pula cabeçalho) · tail -f
  antigo    tail -5 e tail +2 — sintaxe velha, evite em script
  GNU       -F: segue o arquivo pelo nome, mesmo se for apagado e recriado (log rotacionado). O Mac também tem.
  cuidado   tail -f num log que é rotacionado (renomeado e recriado) fica olhando
            o arquivo velho e para de mostrar linha nova: aí é -F.

## less · 1985
> etapa: 3
> resumo: 1985, "less is more": volta e busca. O POSIX só garante o more

O `more` (Berkeley, 1978) mostrava um arquivo uma tela por vez, mas só ia pra
frente. O Mark Nudelman escreveu um que também voltava e buscava, e
chamou de `less` — porque "less is more". Quase todo Linux tem; mas o POSIX só
garante o `more`, e em container mínimo às vezes é só o que existe.

  teclas    espaço desce · b sobe · /texto busca · n próxima · N anterior · g início · G fim · q sai
  less      -N numera linhas · -S não quebra linha comprida (ótimo pra csv) · -i busca sem maiúscula
  POSIX     more arq — espaço desce, q sai, /texto busca
  cuidado   less é pra olhos: no meio de um cano (| less | wc) ou num script não
            faz sentido. Pra extrair um pedaço, head/tail/grep.

## wc · 1971
> etapa: 3
> resumo: Unix V1. O -l conta quebras de linha, não linhas

Unix V1, "word count". Pegadinha clássica: o `-l` conta **quebras de linha** (o
caractere \n), não linhas. Se a última linha do arquivo não termina com \n, ela
não entra na conta.

  POSIX     -l linhas · -w palavras · -c bytes · -m caracteres (num terminal UTF-8, acento conta 1, não 2)
  POSIX     wc -l < arq — só o número, sem o nome do arquivo do lado
  Mac/BSD   o número sai com espaços na frente ("      42"): cuidado ao comparar texto
  cuidado   csv com cabeçalho: wc -l conta o cabeçalho junto. Arquivo salvo sem
            \n no fim: a última linha não conta. -c é byte, não letra.

## pipe · 1973
> etapa: 3
> resumo: 1973, Thompson implementou numa noite: aqui nasceu a filosofia Unix

Não é comando, é do shell — como o `>`. O Doug McIlroy defendia desde os anos 60
que programas deviam se encaixar "como mangueiras de jardim". Em 1973 o Ken
Thompson implementou o `|` numa noite, e no dia seguinte o pessoal dos Bell Labs
estava reescrevendo os programas pra ler da entrada e escrever na saída. Daí veio
a filosofia Unix: programas pequenos, que fazem uma coisa bem feita, e se ligam.

  POSIX     a | b — a saída de a vira a entrada de b. Funciona em todo shell.
  POSIX     só a saída (canal 1) entra no cano; erros (2) vão pra tela: 2>&1 | junta
  cuidado   o resultado ($?) é o do ÚLTIMO comando: grep x sumiu.csv | wc -l
            "dá certo" e imprime 0, mesmo com o arquivo inexistente. No bash,
            set -o pipefail faz o cano falhar se qualquer pedaço falhar.

## grep · 1973
> etapa: 4
> resumo: 1973, o g/re/p do editor ed. -c -i -l -v -E -F são POSIX; -r e -o, extras

No editor `ed`, o comando `g/re/p` queria dizer "em todas as linhas (global) que
casam a expressão (regular expression), imprima (print)". Conta a história que o
Doug McIlroy pediu um jeito de buscar em vários arquivos e o Ken Thompson
tirou esse pedaço do ed e fez um programa — numa noite, de novo. Unix V4, 1973.

  POSIX     -i ignora caixa · -v inverte · -c conta · -l só nomes · -n número da linha
  POSIX     -q quieto (só o código de saída, pra if) · -x linha inteira · -E estendida · -F texto literal
  extras    -r recursivo · -o só o pedaço que casou · -w palavra inteira — GNU, Mac e busybox têm
  GNU       -P (regex do Perl) · --color · -z — o grep do Mac não tem -P
  antigo    egrep e fgrep = grep -E e grep -F; evite, estão sendo aposentados
  cuidado   padrão sem aspas: o shell expande o * antes. O . casa QUALQUER
            caractere (1.5 casa 125): texto literal é grep -F. Sem arquivo, o
            grep fica esperando o teclado — Ctrl+C.

## sort · 1971
> etapa: 4
> resumo: Unix V1. -n -r -k -t -u são POSIX; -h e -V, GNU

Unix V1. Ordenar é tão central que o sort é um dos programas mais otimizados
do sistema: arquivo maior que a memória, ele divide em pedaços, ordena cada um
em disco e junta no fim.

  POSIX     -n numérico · -r inverte · -k2 pela coluna 2 · -t, separador · -u sem repetidos
  POSIX     -f ignora caixa · -o arq escreve no arquivo (pode ser o mesmo da entrada!)
  GNU       -h entende 4K, 2M (o busybox também) · -V versões (1.10 depois de 1.9) · -R embaralha
  cuidado   sem -n, 10 vem antes de 9 (ordem de texto). A ordem muda com o idioma
            do sistema: LC_ALL=C sort pra ordem por byte, igual em toda máquina.
            sort arq > arq zera o arquivo: use sort -o arq arq.

## uniq · anos 70
> etapa: 4
> resumo: só junta repetições VIZINHAS: quase sempre vem depois de um sort

Anos 70, Bell Labs. Ele lê linha por linha e compara cada uma só com a de cima —
por isso não precisa guardar nada na memória, e por isso só enxerga repetição
vizinha. A dupla `sort | uniq -c | sort -rn` é a receita mais famosa do terminal.

  POSIX     -c conta · -d só as repetidas · -u só as únicas · -f N pula N campos
  extras    -i ignora caixa (GNU, Mac, busybox)
  cuidado   sem sort antes, "milho soja milho" conta milho duas vezes, separado.
            Só quer tirar repetidos, sem contar? sort -u faz em um passo.

## cut · anos 80
> etapa: 4
> resumo: AT&T, início dos anos 80. -d -f -c são POSIX; separador de 1 caractere só

Veio da AT&T no começo dos anos 80, junto com o irmão `paste` (que faz o
contrário: cola colunas). Corta cada linha em pedaços e fica com os que você pedir.

  POSIX     -d, separador · -f2 campo 2 · -f1,3 · -f2- do 2 em diante · -c1-5 caracteres
  POSIX     -s pula linha que não tem o separador
  GNU       --complement (tudo menos) · --output-delimiter
  cuidado   o separador é UM caractere: "a  b" (dois espaços) vira 3 campos, um
            vazio — pra colunas separadas por espaço, awk. CSV com vírgula dentro
            de aspas ("Silva, J.") também quebra o cut.

## tr · anos 70
> etapa: 4
> resumo: troca caractere por caractere; só lê da entrada, nunca de arquivo

Unix dos anos 70, "translate". Faz uma coisa só: troca (ou apaga) caracteres
um a um, numa passada. Ótimo pra planilha: vírgula decimal, ; por , e \r de Windows.

  POSIX     tr ';' ',' · tr -d '\r' apaga · tr -s ' ' espreme repetidos · tr -c complemento
  POSIX     classes: '[:lower:]' '[:upper:]' '[:digit:]' '[:space:]'
  cuidado   não troca palavra: tr milho soja troca m→s, i→o, l→j... letra por letra.
            Não abre arquivo: tr a b < arq. O GNU tr vê letra acentuada como 2 bytes
            e estraga acento — palavra e acento é com sed.

## find · 1974
> etapa: 5
> resumo: 1974, PWB/UNIX. -name -type -exec são POSIX; -delete e -printf, extras

Escrito pelo Dick Haight no PWB/UNIX, a versão da AT&T pros programadores, e
lançado no Unix V5 (1974). A sintaxe é estranha porque não são flags: é uma
**expressão** avaliada pra cada arquivo, da esquerda pra direita:
`-name '*.pdf' -size +1M` quer dizer "é pdf E é maior que 1 MB".

  POSIX     find PASTA -name '*.pdf' · -type f/d · -size +10M · -mtime -7 · -newer arq
  POSIX     ! nega · -o "ou" · -exec cmd {} \; (um por vez) · -exec cmd {} + (todos juntos)
  extras    -iname · -maxdepth · -mindepth · -delete · -empty — GNU, Mac e busybox têm
  GNU       -printf '%s %p\n' (tamanho, caminho...) · -not (= !) — o Mac não tem -printf
  cuidado   a ordem importa: find . -delete -name '*.tmp' apaga TUDO (o -delete
            vem antes do teste). Rode com -print primeiro e troque por -delete no
            fim. Padrão sem aspas: o shell expande antes do find ver.

## xargs · fim dos anos 70
> etapa: 5
> resumo: PWB/UNIX: transforma uma lista (linhas) em argumentos de um comando

Também do PWB/UNIX. Resolve um problema: o cano entrega **texto** na entrada,
mas o `rm` quer **argumentos**. O xargs lê a entrada e monta o comando — em lotes,
pra nunca estourar o "argument list too long".

  POSIX     -n 1 um argumento por vez · -I {} põe o item onde estiver o {} · -t mostra o comando
  extras    -0 junto com find -print0 (nomes com espaço) · -r não roda se vier vazio
            · -P 4 em paralelo — GNU, Mac e busybox têm
  cuidado   sem -0, nome com espaço vira dois argumentos e o comando age no
            arquivo errado. Com find, -exec cmd {} + faz o mesmo sem esse risco.

## vi · 1976
> etapa: 6
> resumo: 1976, Bill Joy. É POSIX: está em toda máquina, até no busybox

O Bill Joy, em Berkeley, criou o modo **visual** do editor `ex` — daí "vi". O
terminal dele, um ADM-3A, tinha as setas desenhadas nas teclas h j k l e o Esc
onde hoje fica o Tab: por isso o vi é assim. O vim (1991, Bram Moolenaar) é o
"vi melhorado"; o nvim (2014) é um fork do vim. O vi puro é o que sobra numa VM.

  modos     normal (comandos) · i insere · Esc volta pro normal · : comando de linha
  POSIX     :w salva · :q sai · :q! sai sem salvar · :wq · dd apaga linha · u desfaz · /texto busca
  busybox   vi enxuto: o básico do POSIX funciona; plugin e config do vim, não
  cuidado   travou? Esc, Esc, :q! e Enter. Pra trocar a mesma coisa em 50 arquivos,
            não abra um por um: sed.

## sed · 1974
> etapa: 6
> resumo: Bell Labs, 1974: o ed em fluxo. -n s///g são POSIX; -i é extra e muda no Mac

O Lee McMahon, nos Bell Labs, pegou os comandos do editor `ed` e fez um editor de
**fluxo** (stream editor): ele não abre o arquivo pra você mexer, passa o texto
por uma receita, linha por linha. Entrou no Unix V7, em 1979.

  POSIX     s/velho/novo/ (1ª da linha) · s/a/b/g (todas) · -n com p (só imprime o que pedir)
  POSIX     sed -n 42p (linha 42) · sed '1d' (apaga a 1ª) · sed 10q · $ é a última linha
  extras    -E regex estendida (GNU, Mac, busybox; entrou no POSIX bem depois)
  GNU       sed -i 's/a/b/' arq edita o arquivo no lugar (o busybox também)
  Mac/BSD   sed -i '' 's/a/b/' arq — o -i do Mac EXIGE um argumento (o sufixo do backup)
  cuidado   sed -i sem testar: rode sem o -i primeiro e olhe a saída. Caminho com
            barras? troque o separador: s|/home/a|/home/b|.

## awk · 1977
> etapa: 7
> resumo: 1977, Aho, Weinberger e Kernighan: colunas, condições e contas. POSIX

O nome são as iniciais dos três autores, nos Bell Labs. É uma linguagem inteira
feita pra uma coisa: ler linha por linha, partir em campos ($1, $2... e $NF, o
último) e fazer algo com eles. Cada sistema traz um: gawk (GNU, Fedora), mawk
(Debian/Ubuntu), o "one true awk" do Kernighan (Mac), o do busybox.

  POSIX     awk '{print $2}' · -F, separador · $NF último campo · NR número da linha
  POSIX     awk '$3 > 10' (condição) · '{s += $3} END {print s}' (soma)
  GNU       gawk: gensub(), -i inplace, FPAT — não conte com eles fora do Linux
  recente   --csv (2023, gawk e o awk do Kernighan) entende vírgula entre aspas
  cuidado   CSV com "Silva, J." quebra o -F, comum. Passou de umas 5 linhas de
            awk? Provavelmente é um script de verdade (sh ou Python).

## chmod · 1971
> etapa: 8
> resumo: Unix V1. u+x e 755 são POSIX, -R também; --reference é GNU

Unix V1. Cada arquivo tem três trios de permissão — dono, grupo, outros — e cada
trio é r (ler), w (escrever), x (executar; numa pasta, "entrar"). O número é a
soma: r=4, w=2, x=1. 755 = rwx r-x r-x.

  POSIX     chmod +x script · u+x só o dono · go-w tira escrita dos outros · 644 · 755 · -R
  GNU       --reference=arq copia a permissão de outro · -v · -c
  Mac/BSD   +a e -a pra ACL (permissões extras, coisa de Mac)
  cuidado   chmod 777 (ou -R 777) "pra funcionar" abre tudo pra todos: nunca.
            chmod -R +x põe x em todo arquivo, não só nas pastas.

## sh · 1971 / 1979 / 1989
> etapa: 8
> resumo: Thompson 1971, Bourne 1979, bash 1989. #!/bin/sh = só POSIX

O primeiro shell foi o do Ken Thompson (1971). O do Stephen Bourne (1979, Unix
V7) é o pai de todos: variáveis, if, for, case. O bash (1989, Brian Fox, projeto
GNU) é o "Bourne Again SHell". O POSIX padronizou um sh mínimo, e cada sistema
aponta o /bin/sh pra um: dash no Debian/Ubuntu, ash no busybox, bash nos outros.

  POSIX     #!/bin/sh no topo · if/case/for/while · $(cmd) · ${x%.txt} · [ teste ]
  bash      [[ ]] · arrays · {1..5} · ${x//a/b} · source — só com #!/bin/bash
  Mac/BSD   bash antigo (3.2, por causa da licença GPLv3) e zsh como padrão desde 2019
  cuidado   script com #!/bin/sh e [[ ]] ou {1..5} funciona no Fedora (sh = bash)
            e quebra no Ubuntu, no Alpine e no busybox. Usou bash? Diga #!/bin/bash.

## encadear · 1979
> etapa: 8
> resumo: Bourne 1979: && e || decidem pelo código de saída (0 = deu certo)

Todo comando termina com um número, o código de saída: 0 deu certo, qualquer
outro falhou (`echo $?` mostra o último). O `;` vem do primeiro shell; o `&&` e
o `||` vieram com o Bourne shell e transformaram esse número em decisão.

  POSIX     a && b (b só se a deu certo) · a || b (b só se a falhou) · a ; b (os dois)
  POSIX     true e false: comandos que só devolvem 0 e 1
  cuidado   a && b || c NÃO é if/else: se b falhar, c roda também. Decisão de
            verdade é if a; then b; else c; fi.

## for · 1979
> etapa: 8
> resumo: Bourne 1979; o done e o fi vêm do ALGOL 68. ${f%.x} POSIX, ${f//a/b} bash

O Stephen Bourne gostava do ALGOL 68 e trouxe de lá o jeito de fechar bloco com
a palavra ao contrário: if/fi, case/esac. O do...od não deu: `od` já era um
comando (octal dump) — virou do...done.

  POSIX     for f in *.txt; do ...; done · "$f" sempre com aspas
  POSIX     ${f%.txt} tira do fim · ${f#IMG_} tira do começo (vieram do ksh, 1983)
  bash      ${f//a/b} troca tudo · {1..10} · for ((i=0; i<5; i++))
  fora      seq 1 10 não é POSIX (GNU, Mac e busybox têm)
  cuidado   for f in $(ls) quebra em nome com espaço: use o glob. Se nada casar,
            o laço roda UMA vez com "*.txt" literal — teste [ -e "$f" ] || continue.
