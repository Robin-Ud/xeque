# Trilha sistema

Formato igual ao de `nativo.md` (`> etapa: N`; sem rating = lição, com rating =
puzzle), mais três campos:

- `> tipo: investigar | fazer | arrumar` — aparece no cabeçalho. Investigar é
  detetive na máquina real (o check calcula a resposta na hora); fazer e arrumar
  mexem só na arena.
- `> requer: systemd, rpm|dpkg` — cada termo precisa de uma das alternativas
  (comando, caminho que existe, ou `systemd` = PID 1 é o systemd). Sem isso, o
  item some nessa máquina e o `validar` pula.
- `> sem: ss` — o comando vira um impostor que recusa; o check usa `nao_usou`.

O shell vê a máquina inteira, mas só escreve na arena (landlock). Resposta ao
vivo só de fato **estável**: nada de memória livre, uptime ou PID que muda.
Check portátil: Fedora (gawk, bash como sh) e Mint (mawk, dash) — `$DISTRO`
diz qual família, `resp_um_de` aceita mais de uma resposta.

## s1-a · O que é Linux
> etapa: 1
> tipo: investigar
> fichas: kernel, distro, systemd

Linux, a rigor, é **um programa só: o kernel**. Ele liga primeiro e fica no
meio entre o hardware e todo o resto. Nenhum programa seu encosta no hardware:
o navegador não fala com a placa de Wi-Fi, o editor não escreve direto no disco.
Eles **pedem** ao kernel ("abre esse arquivo", "manda esses bytes pela rede"),
e o kernel decide se deixa. "Permission denied" é o kernel dizendo não.

O resto vem de outros projetos, empilhado em cima dele:

  apps              navegador, editor, o próprio xeque
  gráfico           quem desenha as janelas (lição c)
  base              bash, ls, cp, a glibc: quase tudo do projeto GNU (lição b)
  systemd           o primeiro programa que o kernel liga; ele sobe todo o resto
  kernel (Linux)    processos, memória, drivers, arquivos, permissões
  hardware

**Distribuição** é quem escolhe essas peças, configura, empacota e mantém tudo
atualizado: Fedora, Mint, Ubuntu, Arch. O kernel é o mesmo em todas.

  $ uname -r              a versão do kernel rodando agora
  $ cat /etc/os-release   quem é a distribuição
  $ ps -p 1               o processo número 1: o primeiro que o kernel ligou

Nesta trilha você enxerga a máquina inteira, de verdade, mas só consegue
escrever dentro da arena (`~`). Pode fuçar sem medo: quem garante isso é o
próprio kernel (você vai ver como na etapa de segurança).

MISSÃO: descubra a versão do kernel que está rodando e responda.

> dica: o comando que imprime o nome do sistema tem uma flag que mostra só a versão (em inglês, release)
> solucao: uname -r
> solucao: responder "$(uname -r)"

```setup
mkdir -p notas
```

```check
resp "$(uname -r)"
```

## s1-b · Quem escreveu o quê
> etapa: 1
> tipo: investigar
> fichas: gnu, glibc

O kernel sozinho não te dá nem um `ls`. Quase tudo que você digita no terminal
veio do **GNU**, o projeto que o Richard Stallman começou em 1983 pra fazer um
Unix livre. Em 1991 eles tinham quase tudo, menos o kernel — e o Linux encaixou
no buraco. Por isso tem gente que fala "GNU/Linux".

  $ ls --version | head -1     ls (GNU coreutils): o pacote dos comandos básicos
  $ bash --version | head -1   o shell, também do GNU
  $ ldd --version | head -1    a glibc: a biblioteca por onde os programas falam com o kernel

O caminho de um `cat arquivo`:

  cat → glibc (open, read) → kernel → driver → disco

O programa chama uma função da glibc; ela faz a **chamada de sistema** (syscall)
pro kernel; o kernel fala com o hardware e devolve os bytes.

Nem todo Linux tem GNU: o Android usa o kernel Linux com outra base, e o Alpine
(o Linux dos containers) usa busybox e outra biblioteca C. Mesmo kernel, outra
camada em cima.

MISSÃO: de qual projeto vem o seu `ls`? Responda o que aparece **entre
parênteses** na primeira linha da versão dele.

> dica: quase todo programa responde a uma flag que mostra a versão e quem fez
> dica: a resposta toda costuma vir na primeira linha; o head corta o resto
> solucao: ls --version | head -1
> solucao: responder "$(ls --version | head -1 | sed 's/.*(//; s/).*//')"

```setup
mkdir -p notas
```

```check
v=$(ls --version 2>/dev/null | head -1 | sed -n 's/.*(\(.*\)).*/\1/p')
resp_um_de "${v:-desconhecido}" "${v,,}" "${v#GNU }"
```

## s1-c · Terminal, shell e a parte gráfica
> etapa: 1
> tipo: investigar
> fichas: terminal, shell, wayland

Três coisas que parecem uma só:

  terminal   o programa gráfico que desenha a janela e as letras (kitty, GNOME Terminal)
  shell      o programa dentro dele que lê o que você digita e roda comandos (bash)
  sessão     o compositor que desenha TODAS as janelas, inclusive a do terminal

Dá pra trocar de shell sem fechar a janela: digite `sh`, veja o prompt mudar,
e `exit` volta. E dá pra ter shell sem janela nenhuma: Ctrl+Alt+F3 abre um
console de texto do próprio kernel (volta com Ctrl+Alt+F1, F2 ou F7 — depende
da distro).

  $ echo $0                    qual shell está rodando
  $ echo $XDG_SESSION_TYPE     wayland ou x11 (vazio = sem sessão gráfica, ex.: por ssh)
  $ echo $XDG_CURRENT_DESKTOP  qual ambiente gráfico (GNOME, X-Cinnamon, niri...)

Wayland e X11 são dois jeitos de os programas pedirem pra aparecer na tela.
O X11 é de 1987; o Wayland nasceu em 2008 pra substituir. O Fedora já é só
Wayland; o Mint ainda vem com X11.

MISSÃO: qual é o **tipo** da sua sessão gráfica? (se vier vazio, responda tty)

> dica: o tipo da sessão fica guardado numa variável de ambiente que começa com XDG
> solucao: echo $XDG_SESSION_TYPE
> solucao: responder "${XDG_SESSION_TYPE:-tty}"

```setup
mkdir -p notas
```

```check
resp "${XDG_SESSION_TYPE:-tty}"
```

## s1-p1 · 350 · A versão da distro
> etapa: 1
> tipo: investigar

Qual é o **número da versão** da sua distribuição? (no Ubuntu 24.04, seria 24.04)

> tags: os-release
> dica: toda distro moderna se apresenta num arquivo de texto dentro de /etc
> dica: nesse arquivo, a versão aparece em mais de uma linha; procure a que é só o número (o ID da versão)
> solucao: grep VERSION /etc/os-release
> solucao: responder "$(grep '^VERSION_ID=' /etc/os-release | cut -d= -f2 | tr -d '"')"

```setup
mkdir -p notas
```

```check
resp "$(. /etc/os-release; echo "$VERSION_ID")"
```

## s1-p2 · 400 · Quem nasceu primeiro
> etapa: 1
> tipo: investigar

Todo programa rodando ganha um número. Qual é o **nome** do processo número 1?

> tags: pid1, ps
> dica: o kernel dá o número 1 pro primeiro programa que ele liga
> dica: o ps mostra um processo específico se você passar o número dele com -p
> solucao: ps -p 1
> solucao: responder "$(ps -o comm= -p 1)"

```setup
mkdir -p notas
```

```check
resp "$(ps -o comm= -p 1)"
```

## s1-p3 · 450 · Pra qual processador
> etapa: 1
> tipo: investigar

O kernel é compilado pra um tipo de processador (uma **arquitetura**): um kernel
de PC não roda num celular. Pra qual arquitetura foi compilado o seu?

> tags: kernel, uname
> dica: o mesmo comando que mostra a versão do kernel tem uma flag pra máquina (em inglês, machine)
> dica: uname --help lista as flags; a resposta é uma palavra só
> solucao: uname -m
> solucao: responder "$(uname -m)"

```setup
mkdir -p notas
```

```check
resp "$(uname -m)"
```

## s1-p4 · 550 · O shell por dentro
> etapa: 1
> tipo: investigar

Qual é a versão do **bash**? Basta o começo (ex.: 4.4).

> tags: gnu, bash
> dica: todo programa do GNU responde a uma flag que mostra a versão
> dica: o próprio bash também guarda a versão numa variável com o nome dele
> solucao: bash --version | head -1
> solucao: responder "$BASH_VERSION"

```setup
mkdir -p notas
```

```check
v="${BASH_VERSINFO[0]}.${BASH_VERSINFO[1]}"
resp_um_de "$v" "$v.${BASH_VERSINFO[2]}" "$BASH_VERSION" "${BASH_VERSION%%(*}"
```

## s1-p5 · 600 · A ponte pro kernel
> etapa: 1
> tipo: investigar
> requer: ldd

Todo `ls`, `cat` e `firefox` passa pela biblioteca C pra falar com o kernel.
Qual é a **versão da glibc** dessa máquina? (só o número, ex.: 2.31)

> tags: glibc, gnu
> dica: tem um comando que lista as bibliotecas de um programa; ele vem junto com a glibc e diz a versão dela
> dica: a versão é o último pedaço da primeira linha
> solucao: ldd --version | head -1
> solucao: responder "$(ldd --version | head -1 | awk '{print $NF}')"

```setup
mkdir -p notas
```

```check
resp "$(ldd --version 2>&1 | head -1 | awk '{print $NF}')"
```

## s1-p6 · 650 · Quem desenha as janelas
> etapa: 1
> tipo: investigar

Qual **ambiente gráfico** (o compositor) está desenhando a sua tela agora?
Responda o nome como o sistema diz. Se não tiver nenhum (ex.: por ssh), responda nenhum.

> tags: grafico, wayland
> dica: o nome do ambiente fica numa variável de ambiente, prima da que diz o tipo da sessão
> dica: as variáveis da sessão gráfica começam com XDG_; o env lista todas
> solucao: env | grep XDG
> solucao: responder "${XDG_CURRENT_DESKTOP:-nenhum}"

```setup
mkdir -p notas
```

```check
d="${XDG_CURRENT_DESKTOP:-nenhum}"
IFS=: read -ra ds <<< "$d"
resp_um_de "$d" "${d,,}" "${ds[@]}" "${ds[@],,}" "${d#X-}"
```

## s1-p7 · 750 · Cada peça na sua camada
> etapa: 1
> tipo: arrumar

Em `pecas/` tem um arquivo pra cada peça de um sistema Linux. Mova cada um pra
pasta da camada certa, dentro de `camadas/`. No fim, `pecas/` fica vazia.

  kernel    o que roda no próprio kernel (drivers e sistemas de arquivos moram lá)
  base      a base do GNU: biblioteca C, comandos, shell
  systemd   o PID 1 e os pedaços dele
  grafico   o que desenha a tela
  distro    o que só existe porque alguém empacotou e identificou a distribuição
  apps      programas que você abre

`cat pecas/NOME` explica cada peça.

> tags: camadas
> dica: leia cada peça com cat antes; ela conta o que faz, e o que ela faz diz a camada
> dica: dá pra mover várias de uma vez pra mesma pasta: mv a b c camadas/base/
> solucao: mv pecas/linux pecas/ext4 pecas/iwlwifi camadas/kernel/
> solucao: mv pecas/glibc pecas/coreutils pecas/bash camadas/base/
> solucao: mv pecas/systemd pecas/journald camadas/systemd/
> solucao: mv pecas/wayland pecas/xorg pecas/cinnamon pecas/gnome-shell camadas/grafico/
> solucao: mv pecas/dnf pecas/apt pecas/os-release camadas/distro/
> solucao: mv pecas/firefox pecas/libreoffice camadas/apps/

```setup
mkdir -p pecas camadas/kernel camadas/base camadas/systemd camadas/grafico camadas/distro camadas/apps
peca() { printf '%s\n' "$2" > "pecas/$1"; }
peca linux       "o núcleo: reparte CPU e memória entre os processos"
peca ext4        "o jeito de organizar os arquivos dentro de uma partição do disco"
peca iwlwifi     "o driver da placa de Wi-Fi da Intel"
peca glibc       "a biblioteca C: os programas chamam ela pra fazer chamadas de sistema"
peca coreutils   "ls, cp, mv, cat e companhia"
peca bash        "lê o que você digita e roda os programas"
peca systemd     "o primeiro processo; sobe e vigia os serviços"
peca journald    "o serviço que guarda os logs do sistema"
peca wayland     "o protocolo que os programas usam pra pedir lugar na tela"
peca xorg        "o servidor gráfico antigo, do X11"
peca cinnamon    "o ambiente gráfico do Mint"
peca gnome-shell "o ambiente gráfico padrão do Fedora"
peca dnf         "instala e atualiza os pacotes do Fedora"
peca apt         "instala e atualiza os pacotes do Debian, Ubuntu e Mint"
peca os-release  "o arquivo em /etc que diz o nome e a versão da distribuição"
peca firefox     "o navegador"
peca libreoffice "planilha, texto e apresentação"
```

```check
nenhum 'pecas/*'
certas=0; total=0
while read -r camada pecas_dela; do
  for p in $pecas_dela; do
    total=$((total + 1)); [ -f "camadas/$camada/$p" ] && certas=$((certas + 1))
  done
done <<'EOF'
kernel linux ext4 iwlwifi
base glibc coreutils bash
systemd systemd journald
grafico wayland xorg cinnamon gnome-shell
distro dnf apt os-release
apps firefox libreoffice
EOF
[ "$certas" = "$total" ] || falha "$certas de $total peças estão na camada certa — releia com cat as que sobraram em dúvida"
```

## s2-a · Programa × processo
> etapa: 2
> tipo: investigar
> fichas: processo

**Programa** é um arquivo parado no disco (`/usr/bin/sleep`). **Processo** é um
programa rodando: o kernel carregou ele na memória, deu um número (o **PID**) e
está repartindo a CPU com ele. O mesmo programa pode virar dez processos ao mesmo
tempo — dez abas do terminal são dez `bash`.

Todo processo nasce de outro: o pai faz uma cópia de si mesmo (fork) e a cópia
troca de programa (exec). Por isso todo processo tem um **PPID**, o PID do pai,
e tudo vira uma árvore com o PID 1 no topo.

  $ echo $$               o PID deste shell
  $ echo $PPID            o PID de quem abriu este shell
  $ ps -f                 os processos deste terminal, com pai (PPID) e dono (UID)
  $ ps -ef --forest       todos da máquina, desenhados como árvore (less pra rolar)
  $ ps -o comm= -p 1234   só o nome do processo 1234

MISSÃO: este shell foi aberto por outro processo. Qual é o **nome** do pai dele?

> dica: o shell guarda o PID do pai numa variável de três letras
> dica: com o número do pai, o ps mostra o nome dele se você pedir só a coluna comm
> solucao: ps -o comm= -p $PPID
> solucao: responder "$(ps -o comm= -p $PPID)"

```setup
mkdir -p notas
```

```check
pai=$(ps -o ppid= -p "$SHELL_PID" | tr -d ' ')
resp "$(ps -o comm= -p "$pai")"
```

## s2-b · Cada processo leva uma cópia
> etapa: 2
> tipo: fazer
> fichas: ambiente

Todo processo carrega três coisas suas: um **dono** (o usuário), uma **pasta
atual** e um **ambiente** (variáveis como HOME, PATH, LANG). Quando o pai cria
um filho, o filho ganha uma **cópia** delas. Mexer na cópia não muda o original.

  $ X=1; bash -c 'echo $X'          vazio: X ficou só neste shell
  $ export X=1; bash -c 'echo $X'   1: export põe X no ambiente, e o filho herda
  $ Y=2 bash -c 'echo $Y'           2: só pra esse filho, sem mexer no seu shell
  $ env                             o ambiente inteiro deste processo

Por isso o `cd` é embutido no shell (`ficha cd` na trilha nativa): um programa
`cd` mudaria a pasta dele mesmo e morreria, e a sua continuaria onde estava.

Repare: aqui `echo $HOME` mostra a arena, não a sua casa. O xeque abriu este
shell com outra cópia do ambiente — é só uma variável. A casa de verdade está
em `$XEQUE_CASA` (aqui, só leitura).

MISSÃO: faça um **shell filho** escrever o valor de `CAFE` (que tem que ser
`forte`) no arquivo `visto.txt`.

> dica: o filho só vê a variável se ela estiver no ambiente — não basta existir no seu shell
> dica: dois jeitos: export antes, ou a variável grudada na frente do comando do filho
> solucao: export CAFE=forte
> solucao: bash -c 'echo $CAFE' > visto.txt

```setup
mkdir -p notas
```

```check
existe visto.txt
[ "$(cat visto.txt)" = forte ] || falha "visto.txt tem \"$(cat visto.txt)\" — o filho não viu CAFE=forte"
```

## s2-c · Sinais: como se fala com um processo
> etapa: 2
> tipo: fazer
> fichas: sinal, jobs

O kernel deixa um processo mandar **sinais** pra outro: avisos curtos com um
número e um nome. Os que importam:

  Ctrl+C     INT    "para, por favor" (o programa pode tratar)
  Ctrl+Z     TSTP   pausa; fg volta, bg continua em segundo plano
  kill PID   TERM   "termina" — o padrão; o programa pode arrumar a casa antes
  kill -9    KILL   o kernel mata na hora; o programa nem fica sabendo
  kill -l           a lista toda

Um `&` no fim roda o comando em **segundo plano**: o shell devolve o prompt e o
processo segue. `jobs` lista os seus, `%1` é o primeiro deles, `$!` é o PID do último.

  $ sleep 300 &
  $ jobs
  $ kill %1

MISSÃO: rode `sleep 1000` em segundo plano, confira com `jobs` que ele está lá,
e mate ele. No fim, nenhum `sleep 1000` seu pode estar rodando.

> dica: o & no fim do comando devolve o prompt na hora
> dica: o kill aceita o PID ou o número do job com % na frente
> solucao: sleep 1000 &
> solucao: kill $!

```setup
mkdir -p notas
```

```check
usou '&'
usou kill
pgrep -u "$(id -u)" -f '^sleep 1000$' >/dev/null && falha "ainda tem sleep 1000 rodando (jobs mostra?)"
true
```

## s2-p1 · 450 · Seu número
> etapa: 2
> tipo: investigar

Qual é o **PID** do shell em que você está digitando?

> tags: processo, pid
> dica: o próprio shell guarda o número dele numa variável
> dica: é uma variável de nome curto, feita só de símbolos
> solucao: echo $$
> solucao: responder $$

```setup
mkdir -p notas
```

```check
resp "$SHELL_PID"
```

## s2-p2 · 500 · O dono do primeiro
> etapa: 2
> tipo: investigar

Todo processo tem dono. De qual **usuário** é o processo número 1?

> tags: processo, ps
> dica: o ps mostra colunas que você escolhe com -o; uma delas é o usuário
> dica: o nome da coluna é a palavra em inglês pra usuário
> solucao: ps -o user= -p 1
> solucao: responder "$(ps -o user= -p 1)"

```setup
mkdir -p notas
```

```check
resp "$(ps -o user= -p 1)"
```

## s2-p3 · 600 · O filho não muda o pai
> etapa: 2
> tipo: fazer

O `entra.sh` tem um `cd` pra pasta das fotos. Rode ele e veja: você continua
onde estava. Faça o **seu shell** terminar em `projeto/fotos` **usando o
entra.sh** (sem digitar o cd você mesmo).

> tags: processo, source
> dica: rodar ./entra.sh cria um filho; o cd acontece nele e morre com ele
> dica: o shell tem um embutido que lê um arquivo e roda as linhas no próprio shell, sem filho
> solucao: . ./entra.sh

```setup
mkdir -p projeto/fotos projeto/textos
printf '#!/bin/sh\ncd "$HOME/projeto/fotos"\necho "entrei em $PWD"\n' > entra.sh
chmod +x entra.sh
```

```check
usou entra.sh
em projeto/fotos
```

## s2-p4 · 700 · Só pra esse filho
> etapa: 2
> tipo: fazer

O `mostra.sh` imprime a variável `MODO`. Faça ele imprimir `teste` e guarde a
saída em `saida.txt` — **sem export**: `MODO` não pode passar a existir no
ambiente do seu shell.

> tags: ambiente
> dica: dá pra dar uma variável só pra um comando, sem ela ficar no seu shell
> dica: o formato é NOME=valor logo antes do comando, na mesma linha
> solucao: MODO=teste ./mostra.sh > saida.txt

```setup
printf '#!/bin/sh\necho "modo: ${MODO:-nenhum}"\n' > mostra.sh
chmod +x mostra.sh
```

```check
existe saida.txt
[ "$(cat saida.txt)" = "modo: teste" ] || falha "saida.txt tem \"$(cat saida.txt)\""
nao_usou export
```

## s2-p5 · 750 · Até o topo
> etapa: 2
> tipo: investigar

Subindo de pai em pai a partir do seu shell, quantos processos existem **entre**
ele e o PID 1? (não conte o seu shell nem o PID 1)

> tags: processo, pid
> dica: cada processo tem um pai; vá subindo pelo PPID até chegar no 1
> dica: o ps -ef --forest desenha a árvore; ou pergunte o ppid de cada um com ps -o ppid= -p NÚMERO
> solucao: ps -o pid,ppid,comm -p $PPID
> solucao: responder "$(n=0; p=$PPID; while [ $p -gt 1 ]; do n=$((n+1)); p=$(ps -o ppid= -p $p); done; echo $n)"

```setup
mkdir -p notas
```

```check
n=0; p=$(ps -o ppid= -p "$SHELL_PID" | tr -d ' ')
while [ "${p:-0}" -gt 1 ]; do n=$((n + 1)); p=$(ps -o ppid= -p "$p" | tr -d ' '); done
resp "$n"
```

## s2-p6 · 850 · O seu systemd
> etapa: 2
> tipo: investigar
> requer: systemd, pgrep

O systemd não roda uma vez só. Além do PID 1, existe um **só seu**, que cuida
das coisas da sua sessão. Qual é o **PID** dele?

> tags: systemd, processo
> dica: procure entre os processos que são seus (não do root) um que tenha o mesmo nome do PID 1
> dica: o pgrep acha PID pelo nome; com -u ele olha só os de um usuário
> solucao: pgrep -u "$USER" -x systemd
> solucao: responder "$(pgrep -u "$(id -u)" -x systemd)"

```setup
mkdir -p notas
```

```check
resp "$(pgrep -u "$(id -u)" -x systemd | head -1)"
```

## s2-p7 · 900 · O teimoso
> etapa: 2
> tipo: fazer
> requer: pgrep

O `teimoso.sh` ignora o pedido educado de terminar. Rode ele em segundo plano e
acabe com ele. No fim, nenhum `teimoso.sh` seu pode estar rodando.

> tags: sinal, kill
> dica: o kill padrão manda um sinal que o programa pode ignorar — leia o teimoso.sh
> dica: tem um sinal que nem chega no programa: o kernel encerra direto
> solucao: ./teimoso.sh &
> solucao: kill -9 $!

```setup
printf '#!/bin/bash\ntrap "echo \\"TERM? não vou não.\\"" TERM\nwhile :; do sleep 1; done\n' > teimoso.sh
chmod +x teimoso.sh
```

```check
usou teimoso
usou kill
sleep 0.3
pgrep -u "$(id -u)" -f 'teimoso\.sh$' >/dev/null && falha "o teimoso.sh ainda está rodando"
true
```

## s3-a · Um / só
> etapa: 3
> tipo: investigar
> fichas: /, montagem

No Windows cada disco é uma letra: C:, D:, E:. No Linux existe **uma árvore só**,
que começa em `/` (a raiz). Disco, partição e pendrive não viram letra: são
**montados** numa pasta, e a partir dali o conteúdo deles aparece ali dentro.

  $ findmnt              tudo que está montado, desenhado em árvore
  $ findmnt /            o que está montado na raiz
  $ df -h                quanto espaço tem cada sistema de arquivos
  $ lsblk -f             os discos, as partições e o tipo de cada uma

Pendrive espetado aparece em `/run/media/SEU_USUARIO/` no Fedora e em
`/media/SEU_USUARIO/` no Mint. E tem coisa montada que nem disco tem: o `/proc`
e o `/sys` são o kernel fingindo ser pasta (etapa 4), e o `tmpfs` guarda
arquivos na memória RAM.

MISSÃO: qual é o **tipo** do sistema de arquivos montado em `/`? (ext4, btrfs, xfs...)

> dica: o comando que desenha a árvore de montagens aceita uma pasta e mostra só ela
> dica: ele tem colunas; a que você quer é o tipo (em inglês, filesystem type)
> solucao: findmnt /
> solucao: responder "$(findmnt -no FSTYPE /)"

```setup
mkdir -p notas
```

```check
resp "$(findmnt -no FSTYPE /)"
```

## s3-b · O primeiro nível
> etapa: 3
> tipo: investigar
> fichas: fhs, /usr, /etc, /var, /bin

Desde 1994 as distros seguem um combinado de onde cada coisa mora: o **FHS**.
O primeiro nível do `/`, numa linha cada (`xeque mapa` mostra todos, com ficha):

  /usr          os programas e tudo que vem com eles (ícones, manuais, bibliotecas)
  /etc          a configuração da máquina inteira
  /var          o que muda com o uso: logs, cache, filas, bancos de dados
  /home         as casas dos usuários       /root   a casa do root
  /boot         o kernel e o que ele precisa pra ligar
  /dev          os dispositivos, como arquivos       /proc /sys   o kernel (etapa 4)
  /run          o que só vale até desligar          /tmp         temporário de todos
  /opt          programa de fora, inteiro numa pasta só
  /media /mnt   onde montar pendrive e disco extra   /srv        o que a máquina serve
  /bin /sbin /lib /lib64   hoje são só atalhos pro /usr

A regra de bolso:
**/usr é o que veio no pacote, /etc é o que o admin muda, /var é o que muda sozinho.**

  $ ls -l /            o primeiro nível, com os atalhos marcados com ->

MISSÃO: o `/bin` de hoje é um atalho. **Pra onde** ele aponta? (se na sua
máquina for uma pasta de verdade, responda nenhum)

> dica: no ls -l, atalho aparece com uma seta no fim da linha
> dica: tem um comando que só lê pra onde um atalho aponta
> solucao: ls -l /
> solucao: responder "$(readlink /bin)"

```setup
mkdir -p notas
```

```check
t=$(readlink /bin)
resp_um_de "${t:-nenhum}" "/${t#/}" "${t%/}/" "/${t#/}/"
```

## s3-c · Onde a arena mora
> etapa: 3
> tipo: investigar
> fichas: /tmp, /home

A sua pasta atual não é "um lugar da máquina": é um **atributo do processo**
(etapa 2). Cada processo tem a dele, e ela pode cair em qualquer sistema de
arquivos da árvore.

Aqui o `~` é a arena, que mora no `/tmp`. Já a sua casa de verdade está em
`$XEQUE_CASA`. Elas podem estar em sistemas de arquivos diferentes:

  $ findmnt -T PASTA      em qual montagem essa pasta cai
  $ df -h PASTA           o espaço do sistema de arquivos dela
  $ pwd                   o caminho por onde você entrou
  $ pwd -P                o caminho físico, sem atalhos no meio

No Fedora o `/tmp` é **tmpfs**: vive na memória RAM e some quando desliga. No
Mint ele fica no disco e é limpo no boot. Por isso arquivo grande no `/tmp` do
Fedora come memória.

MISSÃO: qual é o **tipo** do sistema de arquivos onde está a arena (`~`)?

> dica: o findmnt aceita uma flag que diz "em qual montagem cai essa pasta" (em inglês, target)
> solucao: findmnt -T ~
> solucao: responder "$(findmnt -no FSTYPE -T ~)"

```setup
mkdir -p notas
```

```check
resp "$(findmnt -no FSTYPE -T "$XEQUE_ARENA")"
```

## s3-p1 · 450 · Onde mora a sua casa
> etapa: 3
> tipo: investigar

Qual é o **tipo** do sistema de arquivos onde está a sua casa **de verdade**
(`$XEQUE_CASA`, não a arena)?

> tags: montagem, findmnt
> dica: o mesmo comando que mostra as montagens diz em qual delas uma pasta cai
> dica: use a variável no lugar do ~ — o ~ daqui é a arena
> solucao: findmnt -T "$XEQUE_CASA"
> solucao: responder "$(findmnt -no FSTYPE -T "$XEQUE_CASA")"

```setup
mkdir -p notas
```

```check
resp "$(findmnt -no FSTYPE -T "$XEQUE_CASA")"
```

## s3-p2 · 500 · Quantos no primeiro andar
> etapa: 3
> tipo: investigar

Quantos itens (pastas e atalhos, **sem os ocultos**) tem no primeiro nível do `/`?

> tags: fhs, ls
> dica: liste a raiz e conte
> dica: um por linha, e o wc conta as linhas
> solucao: ls / | wc -l
> solucao: responder "$(ls / | wc -l)"

```setup
mkdir -p notas
```

```check
resp "$(ls / | wc -l)"
```

## s3-p3 · 600 · Quanto cabe na casa
> etapa: 3
> tipo: investigar

Qual é o **tamanho total** do sistema de arquivos da sua casa de verdade
(`$XEQUE_CASA`)? Responda como o `df -h` escreve (ex.: 98G).

> tags: montagem, df
> dica: o df mostra o espaço de um sistema de arquivos se você passar uma pasta dele
> dica: o total é a coluna Tam. (Size); o ~ daqui é a arena, não a casa
> solucao: df -h "$XEQUE_CASA"
> solucao: responder "$(df -h --output=size "$XEQUE_CASA" | tail -1)"

```setup
mkdir -p notas
```

```check
resp "$(df -h --output=size "$XEQUE_CASA" | tail -1 | tr -d ' ')"
```

## s3-p4 · 700 · Pastas que vivem na memória
> etapa: 3
> tipo: investigar
> requer: findmnt

Quantos sistemas de arquivos do tipo **tmpfs** estão montados agora?

> tags: montagem, tmpfs
> dica: o findmnt filtra por tipo (em inglês, type) e pode tirar o cabeçalho
> dica: uma montagem por linha; conte as linhas
> solucao: findmnt -t tmpfs
> solucao: responder "$(findmnt -n -t tmpfs | wc -l)"

```setup
mkdir -p notas
```

```check
resp "$(findmnt -n -t tmpfs | wc -l)"
```

## s3-p5 · 750 · Mudança chegando
> etapa: 3
> tipo: arrumar

Chegou uma caixa (`chegou/`) com coisas de uma máquina. Coloque cada uma na
pasta certa da raiz falsa `raiz/`. Leia cada uma com `cat` — ela diz o que é.
No fim, `chegou/` fica vazia.

> tags: fhs
> dica: a regra de bolso: veio no pacote → /usr; o admin muda → /etc; muda sozinho → /var
> dica: o que some no desligar vai pro /run; o que é de alguém, pra casa dele; o que é do boot, pro /boot
> solucao: mv chegou/vmlinuz raiz/boot/
> solucao: mv chegou/hostname chegou/fstab raiz/etc/
> solucao: mv chegou/tcc.odt raiz/home/ana/
> solucao: mv chegou/jogo raiz/opt/
> solucao: mv chegou/sshd.pid raiz/run/
> solucao: mv chegou/rascunho raiz/tmp/
> solucao: mv chegou/htop raiz/usr/bin/
> solucao: mv chegou/firefox.png raiz/usr/share/icons/
> solucao: mv chegou/boot.log raiz/var/log/
> solucao: mv chegou/pacotes-baixados raiz/var/cache/

```setup
mkdir -p chegou/jogo raiz/boot raiz/etc raiz/home/ana raiz/opt raiz/run raiz/tmp \
  raiz/usr/bin raiz/usr/share/icons raiz/var/log raiz/var/cache
c() { printf '%s\n' "$2" > "chegou/$1"; }
c vmlinuz           "o kernel, comprimido: o carregador do boot lê ele pra ligar a máquina"
c hostname          "o nome da máquina; o administrador escolhe e muda quando quiser"
c fstab             "a lista do que montar onde quando a máquina liga; o administrador edita"
c tcc.odt           "o trabalho de conclusão de curso da Ana"
c jogo/LEIAME       "um jogo inteiro, com tudo dentro, que veio de fora da distro"
c sshd.pid          "o número do processo do servidor ssh; não faz sentido depois de desligar"
c rascunho          "alguém rascunhou isso; pode sumir a qualquer hora"
c htop              "um programa que veio num pacote da distro"
c firefox.png       "o ícone que um pacote instalou pro menu"
c boot.log          "o registro do que aconteceu no último boot; cresce sozinho"
c pacotes-baixados  "pacotes que o gerenciador baixou; dá pra apagar e baixar de novo"
```

```check
nenhum 'chegou/*'
certas=0; total=0
while read -r alvo item; do
  total=$((total + 1)); [ -e "raiz/$alvo/$item" ] && certas=$((certas + 1))
done <<'EOF'
boot vmlinuz
etc hostname
etc fstab
home/ana tcc.odt
opt jogo
run sshd.pid
tmp rascunho
usr/bin htop
usr/share/icons firefox.png
var/log boot.log
var/cache pacotes-baixados
EOF
[ "$certas" = "$total" ] || falha "$certas de $total no lugar certo — releia com cat as que ficaram em dúvida"
```

## s3-p6 · 800 · Pelo atalho
> etapa: 3
> tipo: investigar

Entre em `fotos/praia`. Onde você está **de verdade**? Responda o caminho
físico, sem atalho nenhum no meio, a partir da arena (no formato a/b/c).

> tags: caminho, symlink
> dica: o pwd mostra o caminho por onde você entrou; os atalhos ficam no meio dele
> dica: o pwd tem uma flag que resolve os atalhos (em inglês, physical)
> solucao: cd fotos/praia
> solucao: pwd -P
> solucao: responder albuns/2024/praia

```setup
mkdir -p albuns/2023/serra albuns/2024/praia albuns/2024/sitio
ln -s albuns/2024 fotos
echo "pôr do sol" > albuns/2024/praia/legenda.txt
```

```check
resp_um_de albuns/2024/praia "~/albuns/2024/praia" "$XEQUE_ARENA/albuns/2024/praia" "$(cd "$XEQUE_ARENA/albuns/2024/praia" && pwd -P)"
```

## s3-p7 · 900 · O disco de verdade
> etapa: 3
> tipo: investigar
> requer: systemd, lsblk, findmnt

Qual é o nome do **disco** (o aparelho inteiro, não a partição) que guarda o `/`?
(ex.: sda, nvme0n1, vda)

> tags: montagem, lsblk
> dica: comece descobrindo qual partição está montada em /; depois descubra de qual disco ela é
> dica: o lsblk desenha discos com as partições penduradas embaixo; a coluna TYPE diz quem é disk
> solucao: findmnt -no SOURCE /
> solucao: lsblk
> solucao: responder "$(lsblk -rsno NAME,TYPE "$(findmnt -no SOURCE / | sed 's/\[.*//')" | awk '$2=="disk"{print $1}')"

```setup
mkdir -p notas
```

```check
dev=$(findmnt -no SOURCE / | sed 's/\[.*//')
resp "$(lsblk -rsno NAME,TYPE "$dev" | awk '$2=="disk"{print $1; exit}')"
```
