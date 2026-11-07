# Fichas do sistema

Mesmo formato do `fichas.md`: `## nome · ano (ou época)`, `> etapa: N`, `> resumo:`
(uma linha; vai no topo das lições e no `xeque mapa`) e o texto. Aqui a ficha é de
**pasta** (`## /etc`), de **arquivo** (`## /etc/os-release`) ou de **conceito**
(`## kernel`). Linhas que começam com `  FHS`, `  Fedora`, `  Mint`, `  olhe` ou
`  cuidado` ganham cor: o padrão, o que muda em cada distro, um comando pra ver
com os próprios olhos e quando morde. Na arena: `ficha /etc`; fora: `xeque ficha /etc`.

## kernel · 1991
> etapa: 1
> resumo: o Linux de verdade: o programa que manda no hardware e atende os pedidos dos outros

Em agosto de 1991 o Linus Torvalds, estudante em Helsinque, avisou num fórum que
estava fazendo "um sistema operacional (só um hobby, não vai ser grande e
profissional como o GNU)". Hoje são dezenas de milhões de linhas, escritas por
milhares de pessoas, rodando de relógio a supercomputador.

O kernel faz quatro coisas: reparte a CPU entre os processos, dá a cada um a sua
memória (e não deixa um invadir o outro), fala com o hardware pelos **drivers**
e controla arquivos e permissões. Nenhum programa toca no hardware: todos pedem
ao kernel, por chamadas de sistema (syscalls).

  olhe      uname -r (versão) · uname -m (processador) · cat /proc/version
  Fedora    segue o kernel novo de perto: chega versão nova a cada poucas semanas
  Mint      fica numa versão por mais tempo (a do Ubuntu LTS), com correções por cima
  cuidado   "Linux" no dia a dia quer dizer o sistema inteiro. Quando a diferença
            importa (um bug, um driver), pergunte: é o kernel ou é a distro?

## gnu · 1983
> etapa: 1
> resumo: o projeto que escreveu quase tudo que você digita: bash, ls, cp, a glibc

Em 1983 o Richard Stallman anunciou o GNU ("GNU's Not Unix"): um sistema
parecido com o Unix, mas livre, que qualquer um pudesse estudar, mudar e
distribuir. Em 1991 o GNU tinha compilador, shell, comandos e biblioteca — só
faltava o kernel (o deles, o Hurd, nunca ficou pronto). O Linux encaixou no buraco.

Por isso o nome "GNU/Linux": no terminal, o que você mais toca é GNU.

  olhe      ls --version · bash --version · ldd --version (a glibc)
  Fedora    GNU de ponta a ponta (coreutils, bash, glibc)
  Mint      igual. O Ubuntu 25.10 começou a trocar o coreutils por uma versão
            em Rust (uutils) — o Mint 22 ainda é o GNU de sempre
  cuidado   nem todo Linux é GNU: Android, Alpine e roteadores têm kernel Linux
            com outra base. Script que vai pra eles não pode contar com flag GNU.

## glibc · 1987
> etapa: 1
> resumo: a biblioteca no meio do caminho: os programas chamam ela, ela chama o kernel

Quase todo programa é escrito em C ou usa algo escrito em C. Pra abrir um
arquivo, o programa não fala direto com o kernel: chama a função `open()` da
**biblioteca C**, e ela faz a chamada de sistema. No Linux comum essa biblioteca
é a glibc, do GNU (começou no fim dos anos 80).

  cat a.txt → glibc: open(), read() → kernel → driver do disco → bytes de volta

  olhe      ldd --version · ldd /usr/bin/ls (as bibliotecas que o ls carrega)
  Fedora    glibc nova a cada versão do Fedora
  Mint      a do Ubuntu LTS, mais antiga
  cuidado   programa compilado num glibc novo pode não rodar num velho ("GLIBC_2.38
            not found"). É por isso que flatpak e AppImage levam a própria base junto.

## systemd · 2010
> etapa: 1
> resumo: o processo número 1: o primeiro que o kernel liga, e que liga todo o resto

Quando o kernel termina de acordar, ele roda **um** programa — e para por aí.
Esse programa (o init, PID 1) tem que subir todo o resto: rede, login, som,
interface gráfica. Por décadas foi o init do System V (1983), um monte de
scripts rodados em fila. Em 2010 o Lennart Poettering e o Kay Sievers lançaram
o systemd, que sobe tudo em paralelo e vigia cada serviço. O Fedora foi o
primeiro grande a adotar (2011); Debian e Ubuntu vieram em 2015.

  olhe      ps -p 1 · systemctl status (a árvore de tudo que ele cuida)
  Fedora    systemd
  Mint      systemd também (herdado do Ubuntu)
  cuidado   o systemd é muitos programas: journald (logs), logind (sessões),
            resolved (DNS)... Quando alguém fala "o systemd", pergunte qual pedaço.

## shell · 1971
> etapa: 1
> resumo: o programa que lê o que você digita e roda os outros programas

O primeiro shell do Unix foi escrito pelo Ken Thompson em 1971. Em 1979 veio o
Bourne shell (`sh`), do Stephen Bourne, que virou o padrão. Em 1989 o GNU fez o
**bash** ("Bourne-Again SHell"), compatível com ele e com extras. Zsh e fish são
outros shells; o `sh` de hoje é um padrão (POSIX) que vários programas cumprem.

O shell é só um programa: você pode rodar um dentro do outro (`bash`, `sh`,
`exit`) sem fechar janela nenhuma.

  olhe      echo $0 · echo $SHELL (o shell de login, que vem do /etc/passwd)
  Fedora    bash; o /bin/sh também é o bash
  Mint      bash pra você; o /bin/sh é o dash, mais enxuto e mais rápido
  cuidado   script com #!/bin/sh no Fedora aceita coisa de bash que no Mint quebra.
            Usou recurso de bash? Escreva #!/bin/bash.

## terminal · 1978
> etapa: 1
> resumo: a janela que desenha as letras — não é o shell, é onde o shell mora

Antes das telas, o "terminal" era uma máquina de escrever ligada ao computador:
o **teletipo** (TTY). Depois vieram terminais de vídeo, como o VT100 da DEC (1978).
Hoje o terminal é um programa gráfico que **imita** um VT100: kitty, GNOME
Terminal, o do Cinnamon. Ele só desenha letras e repassa o teclado; quem entende
os comandos é o shell que roda dentro dele.

O nome antigo ficou: `/dev/tty`, `tty`, `pts` (pseudo-terminal) — etapa 4.

  olhe      tty (qual terminal é o seu) · echo $TERM (qual terminal ele finge ser)
  olhe      Ctrl+Alt+F3: um console de texto do próprio kernel, sem janela nenhuma
            (volta com Ctrl+Alt+F1, F2 ou F7, depende da distro)
  cuidado   cor, atalho e copiar/colar são do terminal; variável, alias e histórico
            são do shell. Antes de mexer em config, descubra de qual dos dois é.

## wayland · 2008
> etapa: 1
> resumo: o jeito novo de os programas pedirem pra aparecer na tela (o velho é o X11)

O X Window System nasceu no MIT em 1984; a versão 11 (X11) é de 1987 e durou
décadas. Nele, um servidor central (o Xorg) desenha tudo e qualquer programa
pode ler o teclado e a tela dos outros. Em 2008 o Kristian Høgsberg começou o
Wayland: cada programa desenha a própria janela e o **compositor** junta tudo.
Mais simples e mais seguro.

No Wayland o compositor é o próprio ambiente gráfico: GNOME (mutter), KDE
(kwin), niri, Hyprland.

  olhe      echo $XDG_SESSION_TYPE · echo $XDG_CURRENT_DESKTOP
  Fedora    só Wayland: o GNOME do Fedora 43 nem tem mais sessão X11
  Mint      Cinnamon em X11 por padrão; Wayland ainda experimental
  cuidado   programa antigo no Wayland roda pelo XWayland, um X11 de mentirinha.
            Captura de tela, atalho global e "colar" entre apps podem mudar de jeito.

## distro · 1993
> etapa: 1
> resumo: quem escolhe, configura, empacota e mantém as peças: Fedora, Mint, Debian...

Em 1992 instalar Linux era juntar kernel, GNU e o resto na mão. Logo apareceram
as **distribuições**, que fazem isso por você: Slackware e Debian (1993), Red Hat
(1994). O Fedora nasceu do Red Hat em 2003; o Ubuntu do Debian em 2004; o Mint
do Ubuntu em 2006. Toda distro usa o mesmo kernel e quase as mesmas peças — o
que muda são as escolhas, o empacotamento e o ritmo.

  olhe      cat /etc/os-release
  Fedora    Red Hat → Fedora: rpm/dnf, SELinux, firewalld, versão nova a cada 6 meses
  Mint      Debian → Ubuntu → Mint: deb/apt, AppArmor, ufw, base LTS por anos
  cuidado   tutorial da internet é de uma distro. Antes de copiar, veja de qual:
            apt × dnf é o sinal mais óbvio, mas pasta de config e grupo também mudam.

## /etc/os-release · 2012
> etapa: 1
> resumo: a carteira de identidade da distro: nome, versão e de quem ela descende

Cada distro tinha o seu arquivo: `/etc/redhat-release`, `/etc/debian_version`,
`/etc/lsb-release`... Script que queria saber "onde estou?" tinha que testar
todos. Em 2012 o systemd propôs um só, com formato `CHAVE=valor`, e hoje todo
mundo usa.

  olhe      cat /etc/os-release · . /etc/os-release; echo $ID $VERSION_ID
  ID        o nome curto: fedora, linuxmint, ubuntu
  ID_LIKE   de quem descende: no Mint, "ubuntu debian". O Fedora não tem (é a raiz)
  Fedora    é um link pro /usr/lib/os-release: quem manda é o pacote, não você
  Mint      no Ubuntu também é link; confira com ls -l /etc/os-release
  cuidado   pra script decidir "apt ou dnf", olhe o ID_LIKE (ou se o comando
            existe), não o NAME — o NAME é pra gente ler, muda à toa.

## processo · 1969
> etapa: 2
> resumo: um programa rodando: tem número (PID), pai (PPID), dono, pasta e ambiente

O Unix trouxe uma ideia simples: pra rodar um programa, um processo faz uma
**cópia de si mesmo** (`fork`) e a cópia **troca de programa** (`exec`). Seu
shell faz isso a cada comando que você digita. Por isso todo processo tem pai,
e a máquina inteira é uma árvore com o PID 1 no topo.

O kernel guarda pra cada processo: o PID, o PPID, o dono (uid), a pasta atual,
o ambiente, os arquivos abertos e quanta memória e CPU ele usa.

  olhe      ps -f · ps -ef --forest · echo $$ $PPID
  olhe      top (ao vivo; q sai) · /proc/PID (etapa 4: o processo visto como pasta)
  Fedora    igual
  Mint      igual
  cuidado   PID é reciclado: o 4321 de agora pode ser outro programa daqui a uma
            hora. Nunca guarde PID pra matar depois sem conferir o nome antes.

## ambiente · 1979
> etapa: 2
> resumo: as variáveis que cada processo herda do pai como cópia: HOME, PATH, LANG...

O ambiente apareceu no Unix V7 (1979): uma lista de `NOME=valor` que o pai
passa pro filho no `exec`. O filho recebe uma **cópia**: o que ele mudar morre
com ele. Variável de shell comum fica só no shell; `export` põe ela no
ambiente, e aí os filhos herdam.

  olhe      env · echo $PATH · printenv HOME
  olhe      X=1 bash -c 'echo $X' (só pra esse filho) · export X=1 (pra todos daqui pra frente)
  Fedora    igual
  Mint      igual
  cuidado   mudar o .bashrc não muda os shells que já estão abertos: cada um leu o
            arquivo quando nasceu. Abra um novo (ou `. ~/.bashrc`) — etapa 7.

## source · 1979
> etapa: 2
> resumo: roda um arquivo dentro do SEU shell, sem criar filho — por isso ele muda você

`./script.sh` cria um processo filho: o `cd` e as variáveis dele morrem quando
ele acaba. `. script.sh` (ou `source script.sh`, no bash) lê o arquivo e roda
linha por linha no **próprio shell**. É assim que o `.bashrc` funciona: o bash
faz um `.` nele quando abre.

O `.` vem do Bourne shell (1979); o nome `source` é do csh e o bash aceita os dois.

  olhe      type . source (os dois são embutidos)
  POSIX     . arquivo — funciona em qualquer sh (dash, busybox)
  GNU       source arquivo — bash e zsh; no dash do Mint (/bin/sh) não existe
  cuidado   source roda TUDO no seu shell: um `exit` lá dentro fecha o seu
            terminal. Só dê source em arquivo que você leu.

## sinal · 1971
> etapa: 2
> resumo: o recado curto que o kernel entrega a um processo: termina, para, pausa, continua

Sinais existem desde o primeiro Unix. Cada um é um número com nome; o processo
pode tratar a maioria (fazer algo antes de sair) ou ignorar — menos o KILL e o
STOP, que o kernel aplica direto.

  INT  (2)  Ctrl+C: "para, por favor"
  TERM (15) o padrão do kill: "termine" — dá tempo de salvar e fechar arquivos
  KILL (9)  morte imediata, sem aviso; arquivos podem ficar pela metade
  HUP  (1)  "o terminal fechou" — por isso o programa morre quando você fecha a janela
  STOP/CONT pausa e continua (Ctrl+Z manda o TSTP, primo educado do STOP)

  olhe      kill -l · trap -p (o que o seu shell está tratando)
  cuidado   kill -9 é o último recurso, não o primeiro: TERM antes, espere uns
            segundos, aí KILL. Banco de dados e gerenciador de pacotes odeiam -9.

## jobs · anos 80
> etapa: 2
> resumo: o controle do shell sobre o que está em primeiro e segundo plano (&, fg, bg)

O controle de jobs nasceu no csh do BSD, no começo dos anos 80, e o bash copiou. `&` roda
em segundo plano; Ctrl+Z pausa o que está na frente; `bg` faz ele continuar
atrás; `fg` traz pra frente. `%1`, `%2` são os jobs deste shell.

  olhe      jobs · fg %1 · bg · kill %1 · echo $! (PID do último &)
  POSIX     &, jobs, fg, bg, kill %N
  cuidado   job é coisa do shell: fechou o terminal, o HUP leva todos junto.
            Pra algo sobreviver, nohup comando & — ou um serviço (etapa 10).

## fhs · 1994
> etapa: 3
> resumo: o combinado entre as distros sobre o que mora em cada pasta

No começo dos anos 90 cada distro arrumava as pastas do seu jeito. Em 1994 saiu
o FSSTND, que virou o **FHS** (Filesystem Hierarchy Standard) em 1997; a versão
3.0, de 2015, é mantida pela Linux Foundation. Ele diz o que vai em `/etc`,
`/usr`, `/var`... e por isso você acha as coisas no mesmo lugar em qualquer distro.

A regra de bolso:
**/usr é o que veio no pacote, /etc é o que o admin muda, /var é o que muda sozinho.**

  olhe      man hier (o FHS explicado pasta por pasta) · xeque mapa
  Fedora    segue o FHS, com o usrmerge completo (até o /usr/sbin virou atalho)
  Mint      segue o FHS; as bibliotecas ficam em /usr/lib/x86_64-linux-gnu (multiarch do Debian)
  cuidado   o FHS é um combinado, não uma lei. Programa de fora às vezes inventa
            pasta própria; distro às vezes atrasa ou adianta o padrão.

## montagem · 1971
> etapa: 3
> resumo: pendurar um sistema de arquivos numa pasta: é assim que disco vira caminho

No Unix não existe C: nem D:. Cada sistema de arquivos (uma partição, um
pendrive, um pedaço da RAM) é **montado** numa pasta, e o conteúdo dele aparece
ali. O `mount` existe desde o primeiro Unix. O que montar no boot fica no
`/etc/fstab` (e hoje o systemd transforma cada linha dele numa unit `.mount`).

  olhe      findmnt · df -h · lsblk -f · cat /etc/fstab
  Fedora    btrfs: / e /home são subvolumes do mesmo sistema de arquivos;
            pendrive vai pra /run/media/SEU_USUARIO
  Mint      ext4 em / (e /home na mesma partição, se você não separou);
            pendrive vai pra /media/SEU_USUARIO
  cuidado   montar por cima de uma pasta esconde o que tinha nela (não apaga).
            Arquivo "sumido" depois de montar algo? Desmonte e ele volta.

## / · 1969
> etapa: 3
> resumo: a raiz: o começo da única árvore, onde todo caminho absoluto começa

Todo caminho que começa com `/` parte daqui. É o primeiro sistema de arquivos
que o boot monta; os outros se penduram nele.

  olhe      ls -l / · findmnt /
  cuidado   o perigo de verdade não é alguém digitar a raiz: é caminho montado com
            variável vazia. Num script, "$PASTA/lixo" com PASTA vazia vira "/lixo".
            Escreva "${PASTA:?}/lixo": se ela estiver vazia, o shell para com erro.

## /bin · 1971
> etapa: 3
> resumo: os comandos básicos — hoje só um atalho pro /usr/bin (o usrmerge)

No começo dos anos 70, o disco do PDP-11 do Ken Thompson e do Dennis Ritchie
encheu. Montaram um segundo disco em `/usr` (de *user*: era onde ficavam as
casas) e os programas que não cabiam foram pra `/usr/bin`. Ficou combinado: o
que precisa pro boot em `/bin`, o resto em `/usr/bin`. O motivo sumiu (hoje o
initramfs resolve), mas a divisão durou 40 anos. O **usrmerge** juntou tudo de
volta: `/bin` virou atalho pro `/usr/bin`.

  olhe      ls -ld /bin · readlink /bin
  Fedora    juntou em 2012 (Fedora 17)
  Mint      juntado também (veio do Ubuntu; o Debian fechou em 2023)
  cuidado   script antigo com #!/usr/bin/bash ou #!/bin/bash funciona nos dois
            jeitos agora. Mas não conte com isso em sistema velho ou fora do Linux.

## /sbin · 1971
> etapa: 3
> resumo: os comandos de administrador — também virou atalho, e no Fedora sumiu dentro do bin

O `s` é de *system*: programas que só o admin usa (formatar disco, configurar
rede). Mesma história do `/bin`: virou atalho pro `/usr/sbin`.

  olhe      ls -ld /sbin /usr/sbin
  Fedora    desde o Fedora 42 até o /usr/sbin é atalho pro /usr/bin: tudo num lugar só
  Mint      /sbin → /usr/sbin, que ainda é uma pasta de verdade
  cuidado   comando de admin "não encontrado" como usuário comum? Antigamente o
            /sbin nem estava no PATH de quem não era root. Tente o caminho inteiro.

## /lib · 1971
> etapa: 3
> resumo: as bibliotecas que os programas carregam — atalho pro /usr/lib

Biblioteca é código que vários programas usam junto (a glibc é a principal).
Também passou pelo usrmerge: `/lib` aponta pro `/usr/lib`.

  olhe      ls -ld /lib · ldd /usr/bin/ls (o que o ls puxa daqui)
  Fedora    as bibliotecas de 64 bits ficam em /usr/lib64
  Mint      ficam em /usr/lib/x86_64-linux-gnu (o "multiarch" do Debian)
  cuidado   nunca apague nada aqui "pra liberar espaço": metade dos programas
            para de abrir. Quem limpa biblioteca é o gerenciador de pacotes.

## /lib64 · 2003
> etapa: 3
> resumo: as bibliotecas de 64 bits — existe porque todo programa procura o carregador ali

Quando os PCs ganharam 64 bits, as bibliotecas de 64 foram pra uma pasta
própria. E tem um detalhe que segura essa pasta pra sempre: todo programa traz
**gravado** o caminho do carregador `/lib64/ld-linux-x86-64.so.2`, que é quem
liga as bibliotecas antes do programa rodar.

  olhe      ls -l /lib64/ld-linux* · file /usr/bin/ls (aparece o "interpreter")
  Fedora    atalho pro /usr/lib64, cheia de bibliotecas
  Mint      atalho pro /usr/lib64, quase vazia: só o carregador mora lá
  cuidado   esse é o único arquivo sem o qual NENHUM programa abre. Não mexa.

## /boot · anos 90
> etapa: 3
> resumo: o kernel, o initramfs e o carregador: o que a máquina precisa pra ligar

Aqui ficam o kernel (`vmlinuz-VERSÃO`), o **initramfs** (um mini-sistema que
ajuda o kernel a achar o disco de verdade) e a config do GRUB. O `/boot/efi` é
a partição que o firmware da placa-mãe (UEFI) lê. Etapa 12 conta o boot todo.

  olhe      ls /boot · findmnt /boot /boot/efi
  Fedora    partição ext4 separada (o / é btrfs) + /boot/efi em vfat
  Mint      dentro do / (ext4), + /boot/efi em vfat
  cuidado   /boot cheio trava atualização de kernel. O gerenciador de pacotes
            guarda só os últimos kernels; nunca apague vmlinuz na mão.

## /dev · 1971
> etapa: 3
> resumo: os dispositivos como arquivos: disco, terminal, mouse, o buraco negro /dev/null

"Tudo é arquivo": o disco é `/dev/sda` ou `/dev/nvme0n1`, o seu terminal é
`/dev/pts/N`, e `/dev/null` engole tudo que você mandar. Quem cria esses
arquivos é o kernel (e o udev dá nome bonito). Etapa 4 abre ele por dentro.

  olhe      ls /dev · tty · ls -l /dev/null
  cuidado   escrever em /dev/sda é escrever no disco cru, por cima de tudo. É
            assim que se perde um disco com um `dd` trocado. Confira a letra duas vezes.

## /etc · 1971
> etapa: 3
> resumo: a configuração da máquina inteira, em texto — o que o administrador muda

O nome vem de "et cetera": no começo era a pasta do "resto". Virou a casa da
configuração do sistema todo: usuários (`passwd`, `group`), o que montar
(`fstab`), o nome da máquina (`hostname`), a rede, os serviços. Quase tudo é
texto puro. A config de UM usuário fica na casa dele (`~/.config`, etapa 7).

  olhe      ls /etc · cat /etc/hostname · cat /etc/fstab
  Fedora    usa /etc/sysconfig pra opções de serviço
  Mint      usa /etc/default pro mesmo papel (herança do Debian)
  cuidado   antes de editar algo daqui, copie: sudo cp arquivo arquivo.bak. Um
            erro no fstab ou no sudoers pode não deixar a máquina ligar ou te dar root.

## /home · anos 80
> etapa: 3
> resumo: as casas dos usuários: tudo que é seu, inclusive a sua configuração

Cada usuário ganha `/home/NOME`, que é o `~`. Lá ficam seus arquivos e os
ponto-arquivos (`.config`, `.local`, `.bashrc`). O `/home` separado do `/`
permite reinstalar o sistema sem perder nada seu.

  olhe      echo $XEQUE_CASA · ls -ld /home/* · findmnt -T /home
  Fedora    subvolume btrfs próprio; sua casa nasce fechada pros outros (700)
  Mint      na mesma partição do / por padrão; a casa costuma nascer 750 ou 755
            (o grupo, ou todo mundo, lista) — confira com ls -ld ~
  cuidado   "é meu porque está na minha casa" é falso: cada arquivo tem dono
            próprio (etapa 5). Um sudo descuidado deixa arquivo do root aqui dentro.

## /root · 1971
> etapa: 3
> resumo: a casa do administrador — fora do /home pra existir mesmo se ele falhar

O root não mora no `/home`: se o disco do `/home` não montar, o administrador
ainda precisa de uma casa pra consertar. Por isso `/root` fica na raiz.

  olhe      ls -ld /root (fechada: você nem lista)
  Fedora    o instalador pergunta se quer liberar o login do root
  Mint      o root vem bloqueado; tudo de admin passa pelo sudo
  cuidado   ls /root dar "Permission denied" é o normal. Não é bug, é o kernel
            protegendo a casa de outro usuário.

## /run · 2011
> etapa: 3
> resumo: o que só vale enquanto a máquina está ligada: PIDs, sockets, montagens do usuário

Até 2011 isso ficava espalhado em `/var/run` e `/var/lock`, num disco que nem
estava pronto no começo do boot. O `/run` é um tmpfs (RAM) montado logo cedo,
e some no desligar. O Fedora 15 foi um dos primeiros a ter.

  olhe      ls /run · ls /run/user/$(id -u) (a sua parte) · findmnt /run
  Fedora    pendrive aparece em /run/media/SEU_USUARIO
  Mint      igual; nos dois, o velho /var/run virou atalho pra cá
  cuidado   nada aqui sobrevive a um reboot. Programa que guarda estado em /run
            perde tudo ao desligar — de propósito.

## /tmp · 1971
> etapa: 3
> resumo: temporário de todo mundo: qualquer um escreve, só o dono apaga o que é seu

Qualquer usuário pode criar arquivo aqui, mas o **sticky bit** (o `t` em
`drwxrwxrwt`) impede um de apagar o do outro. A arena do xeque mora aqui.

  olhe      ls -ld /tmp · findmnt -T /tmp
  Fedora    tmpfs desde 2013: vive na RAM, some no desligar
  Mint      no disco, limpo a cada boot
  cuidado   arquivo grande no /tmp do Fedora come memória. Pra temporário grande
            ou que precisa sobreviver ao reboot, use /var/tmp.

## /usr · 1971
> etapa: 3
> resumo: os programas e tudo que vem com eles — o que o gerenciador de pacotes instala

Começou como a casa dos usuários (*user*) e virou o lugar dos programas (história
na ficha do /bin). Hoje é "o que veio no pacote": `bin` (programas), `lib`
(bibliotecas), `share` (ícones, manuais, traduções), `local` (o que VOCÊ
compilou ou instalou fora do gerenciador). Etapa 8 abre ele por dentro.

  olhe      ls /usr · du -sh /usr 2>/dev/null
  cuidado   não edite nada em /usr: a próxima atualização sobrescreve. Pra mudar
            config que veio do pacote, o lugar é o /etc (etapa 7).

## /var · anos 80
> etapa: 3
> resumo: o que muda sozinho com o uso: logs, cache, filas, bancos de dados

"Variável": tudo que cresce e muda enquanto a máquina roda. `/var/log` (os
registros), `/var/cache` (dá pra apagar e refazer), `/var/lib` (o estado dos
programas, como a lista de pacotes instalados), `/var/tmp` (temporário que
sobrevive ao reboot). Etapa 9 abre ele por dentro.

  olhe      ls /var · du -sh /var/* 2>/dev/null | sort -h
  cuidado   disco enchendo do nada? Quase sempre é log ou cache em /var.
            Apague com a ferramenta certa (journalctl --vacuum-size, dnf/apt clean),
            não na mão.

## /opt · anos 90
> etapa: 3
> resumo: programa que veio de fora da distro, inteiro numa pasta só

O `/opt` é pra pacote "opcional" de terceiros que não quer se espalhar pelo
`/usr`: tudo dele fica em `/opt/NOME`. O Google Chrome, por exemplo, se instala
em `/opt/google/chrome`.

  olhe      ls /opt
  cuidado   o que está aqui geralmente não é atualizado pelo dnf/apt da distro,
            a não ser que o programa tenha posto o repositório dele.

## /media · 2004
> etapa: 3
> resumo: onde o sistema monta sozinho o que você espeta (pendrive, HD externo)

Entrou no FHS em 2004 pra separar o removível do `/mnt`.

  olhe      ls /media
  Fedora    fica vazio: o Fedora usa /run/media/SEU_USUARIO
  Mint      é aqui: /media/SEU_USUARIO/NOME_DO_PENDRIVE
  cuidado   tirar o pendrive sem ejetar pode perder o que ainda estava indo pro
            disco. Ejete (ou umount) antes de puxar.

## /mnt · 1971
> etapa: 3
> resumo: o lugar do administrador montar algo na mão, por um tempo

Vazio por padrão. É onde se monta à mão um disco pra consertar, uma imagem, um
compartilhamento de rede.

  olhe      ls /mnt
  cuidado   montar algo aqui não sobrevive ao reboot: o que é pra ficar vai pro /etc/fstab.

## /srv · 2004
> etapa: 3
> resumo: os dados que a máquina serve pros outros (site, arquivos) — num note, vazio

Servidor web e de arquivos guardariam o que servem em `/srv/www`, `/srv/ftp`.
Na prática, cada programa ainda usa seu canto (`/var/www`).

  olhe      ls /srv
  cuidado   pasta vazia na raiz não é lixo: faz parte do padrão. Não apague.

## /proc · 1984
> etapa: 3
> resumo: o kernel fingindo ser pasta: cada processo vira uma pasta com o número dele

Não tem disco nenhum por trás: cada vez que você lê um arquivo daqui, o kernel
**inventa** o conteúdo na hora. A ideia veio do Unix 8ª edição (1984); o Linux
foi muito além. Etapa 4.

  olhe      ls /proc · cat /proc/uptime · ls /proc/$$
  cuidado   os arquivos mostram tamanho 0 e mesmo assim têm conteúdo. Não é bug:
            é que o conteúdo não existe até alguém ler.

## /sys · 2003
> etapa: 3
> resumo: o hardware visto pelo kernel, como pastas: bateria, telas, discos, drivers

Veio no Linux 2.6 pra organizar o que o `/proc` misturava: aqui cada aparelho e
cada driver tem sua pasta. Etapa 4 e 11.

  olhe      ls /sys/class · cat /sys/class/power_supply/BAT*/capacity
  cuidado   alguns arquivos daqui, quando escritos (como root), mudam o hardware
            na hora: brilho, ventoinha, CPU. Leia à vontade; escreva sabendo o que faz.

## /afs · anos 80
> etapa: 3
> resumo: só no Fedora: um lugar reservado pro AFS, um sistema de arquivos de rede das universidades

O AFS (Andrew File System) nasceu na Carnegie Mellon nos anos 80: um disco de
rede compartilhado por um campus inteiro. O pacote `filesystem` do Fedora cria
`/afs` vazio pra quem usar.

  olhe      ls -ld /afs · rpm -qf /afs
  Fedora    existe, vazio
  Mint      não existe
  cuidado   não é seu nem de nenhum programa seu. Deixe quieto.

## /lost+found · anos 70
> etapa: 3
> resumo: só em ext4: onde o conserto do disco (fsck) põe os pedaços que perderam o nome

Quando o disco desliga no meio de uma escrita, o `fsck` pode achar dados sem
nome nenhum apontando pra eles. Ele salva esses pedaços aqui, numerados.

  olhe      ls -ld /lost+found (só o root lista)
  Fedora    não tem no /: o btrfs se conserta de outro jeito
  Mint      tem (ext4)
  cuidado   pasta vazia e esquisita na raiz, mas é do sistema de arquivos. Não apague.
