# Curiosidades

Atalhos e truques que quase ninguém descobre sozinho. Sem puzzle e sem rating: o
`xeque curiosidade` mostra uma que você ainda não viu (a mesma o dia todo, até
você ver) e o menu deixa a próxima à vista.

Formato: `## id · onde · título`. `> tente:` (obrigatório) é o que fazer agora pra
sentir na mão; `> requer:` esconde a curiosidade na máquina que não tem a
ferramenta (comando no PATH ou caminho, igual à trilha sistema). Bash: vale no
bash puro (readline) e no ble.sh, salvo quando o texto diz o contrário.

## alt-ponto · bash · Alt+. cola o último argumento do comando anterior
Fez `ls ~/Downloads/relatorio-final.pdf` e agora quer abrir? Digite `xdg-open `
e aperte **Alt+.**: o caminho inteiro aparece. Apertou de novo, vem o último
argumento do comando de antes, e assim por diante.
> tente: rode `ls /etc/hostname`, depois digite `cat ` e aperte Alt+.

## ctrl-r · bash · Ctrl+R procura no histórico enquanto você digita
**Ctrl+R** e um pedaço do comando: aparece o mais recente que bate. Ctrl+R de
novo vai pro anterior; Enter roda; seta pro lado deixa editar antes.
No bash puro, Ctrl+S (ir pro mais novo) costuma congelar o terminal: Ctrl+Q destrava.
> tente: aperte Ctrl+R e digite `ssh` (ou `git`)

## ctrl-x-e · bash · Ctrl+X Ctrl+E abre a linha no editor
Comando ficou comprido demais pra editar na linha? **Ctrl+X** e depois **Ctrl+E**
abre ele no seu `$EDITOR`. Salvou e saiu, o shell roda o que ficou no arquivo:
serve pra montar um for de várias linhas com calma.
> tente: digite `echo oi`, aperte Ctrl+X Ctrl+E, troque por `echo tchau`, salve e saia

## alt-hash · bash · Alt+# guarda o comando no histórico sem rodar
Meio caminho de um comando e lembrou que precisa fazer outra coisa antes?
**Alt+#** põe um `#` na frente e dá Enter: vira comentário, não roda, mas fica no
histórico. Depois é só ↑, apagar o `#` e seguir.
> tente: digite `rm -r algo-importante`, aperte Alt+#, e veja que nada aconteceu (↑ traz de volta)

## ctrl-u-y · bash · Ctrl+U recorta a linha, Ctrl+Y cola de volta
**Ctrl+U** recorta do cursor até o começo; **Ctrl+K**, do cursor até o fim;
**Ctrl+Y** cola o último recorte. O uso clássico: digitou um comando enorme,
lembrou que precisa de um `cd` antes. Ctrl+U, faz o cd, Ctrl+Y, Enter.
> tente: digite `ls -la`, aperte Ctrl+U, rode `cd /tmp`, e aperte Ctrl+Y

## ctrl-w · bash · Ctrl+W apaga a palavra de trás, Alt+D a da frente
Backspace letra por letra é lento. **Ctrl+W** apaga a palavra antes do cursor
(o que ela apagou dá pra colar com Ctrl+Y); **Alt+D** apaga a palavra seguinte.
> tente: digite `echo um dois tres` e apague o `tres` com um Ctrl+W

## alt-b-f · bash · Alt+B e Alt+F pulam de palavra em palavra
Seta pro lado anda uma letra. **Alt+B** volta uma palavra, **Alt+F** avança uma;
**Ctrl+A** vai pro começo da linha e **Ctrl+E** pro fim (no ble.sh, Ctrl+E no fim
da linha também aceita a sugestão cinza).
> tente: digite `cp arquivo-um arquivo-dois destino` e vá até o `arquivo-dois` com Alt+B

## ctrl-x-u · bash · Ctrl+X Ctrl+U desfaz a edição da linha
Apagou o que não devia? **Ctrl+X** e depois **Ctrl+U** desfaz a última mudança
na linha, e repete pra desfazer mais. É o Ctrl+Z da linha de comando.
> tente: digite `echo teste`, apague com Ctrl+W, e traga de volta com Ctrl+X Ctrl+U

## alt-u-l-c · bash · Alt+U, Alt+L e Alt+C mudam a caixa da palavra
Do cursor até o fim da palavra: **Alt+U** põe em MAIÚSCULA, **Alt+L** em
minúscula, **Alt+C** capitaliza. Bom pra variável que você digitou minúscula.
> tente: digite `echo $home`, ponha o cursor no `h` e aperte Alt+U

## alt-t · bash · Alt+T troca duas palavras de lugar
**Alt+T** troca a palavra do cursor com a anterior. Inverteu origem e destino
num `cp` ou `mv`? Cursor na segunda, Alt+T. (Ctrl+T faz o mesmo com duas letras.)
> tente: digite `mv destino origem`, cursor no fim, e aperte Alt+T

## alt-star · bash · Alt+* escreve na linha todas as opções do Tab
Tab mostra as opções; **Alt+*** escreve todas elas na linha, pra você conferir
ou apagar uma ou outra antes de rodar.
> tente: digite `ls /etc/host` e aperte Alt+*

## bang-bang · bash · sudo !! repete o último comando com sudo
`!!` é o último comando inteiro; `!$` o último argumento dele. Esqueceu o sudo:
`sudo !!`. O bash mostra o comando expandido antes de rodar.
> tente: rode `echo primeiro segundo`, depois `echo !$`

## circunflexo · bash · ^errado^certo corrige o último comando e roda
Digitou `gti status`? `^gti^git` troca a primeira ocorrência no comando anterior
e roda de novo. Só a primeira: pra mais que isso, ↑ e edite.
> tente: rode `echo bom dai`, depois `^dai^dia`

## cd-menos · shell · cd - volta pra pasta de antes
`cd -` vai pra pasta onde você estava antes do último cd (e mostra qual é). Dois
`cd -` seguidos te deixam alternando entre duas pastas.
> tente: `cd /etc`, `cd ~`, e depois `cd -` duas vezes

## chaves · bash · arq{,.bak} vira arq arq.bak
O bash expande `{a,b}` antes de rodar: `cp config.txt{,.bak}` vira
`cp config.txt config.txt.bak`. Também serve pra `mkdir -p projeto/{dados,fig,texto}`
e sequências como `{1..5}`.
> tente: rode `echo foto{1..3}.jpg` e `echo arq{,.bak}`

## underscore · bash · $_ é o último argumento (pra script e pra pressa)
`mkdir -p fotos/2026/viagem && cd $_` cria e já entra. `$_` é o último argumento
do comando anterior, mas como variável: funciona dentro de script, onde o Alt+. não existe.
> tente: rode `mkdir -p /tmp/teste/xeque && cd $_` e depois `pwd`

## ctrl-z · shell · Ctrl+Z pausa o programa, fg volta pra ele
Tá no meio de um `less` ou do vi e precisa de um comando rápido? **Ctrl+Z**
suspende o programa e te devolve o shell; `fg` volta exatamente onde estava.
`jobs` lista o que ficou pausado; `bg` deixa continuar rodando no fundo.
> tente: abra `less /etc/os-release`, aperte Ctrl+Z, rode `ls`, depois `fg`

## reset · terminal · reset conserta o terminal bagunçado
Deu `cat` num arquivo binário e agora o terminal só mostra símbolo estranho,
ou o que você digita não aparece? Digite `reset` (mesmo sem ver) e Enter.
> tente: só guarde o nome. Quando acontecer, `reset` e Enter, mesmo às cegas

## ctrl-l · shell · Ctrl+L limpa a tela sem perder o que você digitou
Igual ao `clear`, mas sem precisar apagar a linha que você já começou: limpa a
tela e mantém o comando pela metade lá em cima.
> tente: digite `echo meio comando` sem dar Enter e aperte Ctrl+L

## type-a · bash · type -a diz o que um comando é de verdade
`ls` é o programa `/usr/bin/ls` ou um alias com cor? `type -a ls` mostra todos:
alias, função, builtin e cada arquivo no PATH, na ordem em que o shell procura.
> tente: rode `type -a ls`, `type -a cd` e `type -a echo`

## less-f · less · Shift+F transforma o less num tail -f
Dentro do less, **Shift+F** vai pro fim e fica esperando linha nova, como
`tail -f`. **Ctrl+C** para de seguir e você volta a rolar e buscar normalmente.
> tente: `less +F /var/log/dnf.log` (ou qualquer log) e depois Ctrl+C
> requer: less

## less-filtro · less · &palavra mostra só as linhas que batem
Dentro do less, `&erro` e Enter esconde todas as linhas que não têm "erro". É um
grep sem sair do less; `&` e Enter vazio mostra tudo de novo.
> tente: `less /etc/services`, digite `&ssh` e Enter
> requer: less

## less-v · less · v abre no editor o arquivo que você está lendo
Achou o erro lendo no less? **v** abre o mesmo arquivo no seu `$EDITOR`; saiu
do editor, volta pro less.
> tente: `less ~/.bashrc` e aperte v (saia sem salvar)
> requer: less

## less-s · less · -S dentro do less corta as linhas longas
Tabela larga quebrando em várias linhas? Dentro do less, digite `-S` e Enter:
as linhas passam a ser cortadas e a seta pro lado rola na horizontal. `-S` de novo desfaz.
Qualquer opção do less dá pra ligar assim, com ele aberto.
> tente: `ps aux | less`, digite `-S` e Enter, role com →
> requer: less

## man-k · man · man -k acha o comando quando você não lembra o nome
`man -k palavra` (o mesmo que `apropos`) procura nas descrições de todas as
páginas. Os números entre parênteses são seções: `man 5 passwd` é o arquivo,
`man 1 passwd` o comando.
> tente: `man -k compress` e depois `man 5 passwd`
> requer: man

## vi-ponto · vim · . repete a última mudança
No vi, **.** refaz a última edição inteira. Apagou uma linha com `dd`? `.` apaga
a próxima. Trocou uma palavra com `cw`? Vá na outra e `.`.
> tente: abra um arquivo de teste, `dd` numa linha e `.` três vezes
> requer: vi

## vi-ci · vim · ci" troca o que está entre aspas
`ci"` apaga tudo entre as aspas (o cursor pode estar em qualquer lugar da linha
antes delas) e entra no modo de inserção. Vale com `(`, `{`, `[`, `'` e `w`
(palavra): `ciw`, `ci(`, `di{`. É do vim, não do vi original nem do busybox.
> tente: numa linha com `nome = "antigo"`, digite `ci"` e escreva o novo valor
> requer: vi

## vi-estrela · vim · * busca a palavra que está embaixo do cursor
Sem digitar nada: **\*** pula pra próxima ocorrência da palavra do cursor,
**#** pra anterior, e `n` continua. Bom pra achar onde uma variável aparece de novo.
> tente: abra um script, cursor no nome de uma variável, e aperte *
> requer: vi

## column-t · gnu · column -t alinha qualquer saída em colunas
Saída separada por espaços toda torta? Joga num `| column -t` e vira tabela.
Com `-s,` vale pra CSV.
> tente: `mount | column -t | less -S`
> requer: column

## watch-d · gnu · watch -d roda de novo e pinta o que mudou
`watch -d -n1 comando` roda o comando a cada segundo em tela cheia e destaca o
que mudou desde a última vez. Bom pra ver arquivo crescendo ou disco enchendo.
> tente: `watch -d -n1 date` (Ctrl+C sai)
> requer: watch

## kitty-h · kitty · Ctrl+Shift+H abre todo o histórico do terminal no pager
O kitty manda tudo que passou na janela pro less: **Ctrl+Shift+H**. Lá dentro
vale `/` pra buscar, `&` pra filtrar, tudo que o less faz.
> tente: aperte Ctrl+Shift+H e digite `/` mais alguma palavra que passou
> requer: kitty

## kitty-g · kitty · Ctrl+Shift+G abre só a saída do último comando
O comando cuspiu 500 linhas? **Ctrl+Shift+G** abre só a saída dele no pager,
sem o resto. Precisa da integração de shell do kitty (vem ligada no bash).
> tente: rode `ls -R /etc 2>/dev/null` e aperte Ctrl+Shift+G
> requer: kitty

## kitty-z-x · kitty · Ctrl+Shift+Z e X pulam de prompt em prompt
Rolando pra cima atrás de onde começou um comando? **Ctrl+Shift+Z** pula pro
prompt anterior e **Ctrl+Shift+X** pro próximo. Também usa a integração de shell.
> tente: rode três comandos com saída longa e volte com Ctrl+Shift+Z
> requer: kitty

## kitty-e · kitty · Ctrl+Shift+E abre um link sem mouse
**Ctrl+Shift+E** marca cada URL na tela com uma letra: aperte a letra e o link
abre no navegador. **Ctrl+Shift+P** e depois **F** faz o mesmo com caminhos de
arquivo, escrevendo o caminho escolhido na linha de comando.
> tente: rode `echo https://example.com` e aperte Ctrl+Shift+E
> requer: kitty

## kitty-u · kitty · Ctrl+Shift+U escreve qualquer caractere ou emoji
**Ctrl+Shift+U** abre um seletor: busque pelo nome em inglês ("check", "arrow",
"degree") ou digite o código, e o caractere entra na linha. Acaba com o
copia-e-cola de símbolo.
> tente: aperte Ctrl+Shift+U, digite `degree` e escolha o °
> requer: kitty

## kitten-icat · kitty · kitten icat mostra imagem dentro do terminal
O kitty desenha imagem de verdade: `kitten icat foto.png` mostra a foto ali no
terminal, sem abrir visualizador. Bom pra conferir um gráfico que um script gerou.
> tente: `kitten icat` com qualquer .png ou .jpg que você tenha
> requer: kitty

## kitten-diff · kitty · kitten diff compara dois arquivos lado a lado
`kitten diff velho.txt novo.txt` mostra os dois lado a lado, colorido, com a
sintaxe destacada. Também compara duas pastas inteiras.
> tente: `cp ~/.bashrc /tmp/b && echo '# mudou' >> /tmp/b && kitten diff ~/.bashrc /tmp/b`
> requer: kitty
