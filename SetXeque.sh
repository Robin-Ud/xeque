#!/bin/bash
# SetXeque — instala o xeque (puzzles de terminal com rating) e, se você quiser,
# libera acesso por ssh pro Matheus te ajudar de longe (via Tailscale).
# Pode rodar de novo quando quiser: ele só faz o que falta.
set -euo pipefail

REPO=${XEQUE_REPO:-https://github.com/Robin-Ud/xeque.git}
DIR=${XEQUE_DIR:-$HOME/xeque}
DROPIN=/etc/ssh/sshd_config.d/10-xeque.conf

uso() {
  cat <<'EOF'
uso:
  curl -fsSL https://raw.githubusercontent.com/Robin-Ud/xeque/main/SetXeque.sh | bash
  curl -fsSL .../SetXeque.sh | bash -s -- --chave tskey-auth-...   # + acesso remoto
  ~/xeque/SetXeque.sh --remover-acesso                             # desfaz o acesso
EOF
}

ok()    { printf '\e[32m✓\e[0m %s\n' "$*"; }
aviso() { printf '\e[33m!\e[0m %s\n' "$*"; }
erro()  { printf '\e[31m✗\e[0m %s\n' "$*" >&2; exit 1; }
# rodando via `curl | bash`, a entrada é o próprio script: pergunta lê do terminal
pergunta() { local r; read -r -p "$1 [s/N] " r < /dev/tty; [[ $r =~ ^[sS] ]]; }

gerente() {
  for g in apt-get dnf pacman; do command -v $g >/dev/null && { echo $g; return; }; done
  erro "não reconheci o gerenciador de pacotes (apt, dnf ou pacman)"
}

instalar() {  # nomes do Debian/Ubuntu/Mint; o pacman chama dois deles diferente
  local g; g=$(gerente)
  case $g in
    apt-get) sudo apt-get update -qq && sudo apt-get install -y -qq "$@" ;;
    dnf)     sudo dnf install -y -q "$@" ;;
    pacman)  sudo pacman -S --needed --noconfirm $(printf '%s\n' "$@" | sed 's/^python3$/python/; s/^openssh-server$/openssh/') ;;
  esac
}

recarregar_ssh() { sudo systemctl reload ssh 2>/dev/null || sudo systemctl reload sshd; }

instalar_xeque() {
  local falta=()
  for c in git python3 bash busybox; do command -v $c >/dev/null || falta+=("$c"); done
  if [ ${#falta[@]} -gt 0 ]; then
    echo "instalando: ${falta[*]} (o sudo vai pedir sua senha)"
    instalar "${falta[@]}"
  fi
  python3 -c 'import sys; sys.exit(sys.version_info < (3, 10))' \
    || erro "o xeque precisa do Python 3.10 ou mais novo (você tem $(python3 -V)). Atualize o sistema e rode de novo."
  ok "dependências: git, python3, bash, busybox"

  if [ -d "$DIR/.git" ]; then
    git -C "$DIR" pull --ff-only -q && ok "xeque atualizado em $DIR"
  elif [ -e "$DIR" ]; then
    erro "$DIR já existe e não é o xeque. Rode com XEQUE_DIR=outra/pasta"
  else
    git clone -q "$REPO" "$DIR" && ok "xeque baixado em $DIR"
  fi

  mkdir -p "$HOME/.local/bin"
  ln -sf "$DIR/xeque.sh" "$HOME/.local/bin/xeque"
  if command -v fish >/dev/null; then
    fish -c 'fish_add_path -U ~/.local/bin' && ok "~/.local/bin no PATH do fish"
  fi
  case ":$PATH:" in
    *":$HOME/.local/bin:"*) ok "comando xeque no PATH" ;;
    *) aviso "abra um terminal novo pro comando xeque aparecer (o ~/.profile põe ~/.local/bin no PATH)" ;;
  esac

  echo "testando nesta máquina (uns 2 minutos)..."
  if bash "$DIR/xeque_test.sh" > /tmp/xeque_setup_teste.log 2>&1; then
    ok "teste passou"
  else
    aviso "o teste falhou — manda o /tmp/xeque_setup_teste.log pro Matheus"
  fi
}

liberar_acesso() {
  local chave=$1 pub="$DIR/chaves/matheus.pub"
  cat <<EOF

Acesso remoto: isso vai
  • instalar o servidor ssh e o Tailscale (uma rede privada entre você e o Matheus)
  • deixar a chave do Matheus ($pub) entrar como $USER
  • desligar o login por senha no ssh (só entra quem tem chave)
Dá pra desfazer quando quiser:  $DIR/SetXeque.sh --remover-acesso
EOF
  pergunta "Liberar o acesso?" || { aviso "acesso não liberado"; return; }

  command -v sshd >/dev/null || [ -x /usr/sbin/sshd ] || instalar openssh-server
  sudo systemctl enable --now ssh 2>/dev/null || sudo systemctl enable --now sshd
  mkdir -p "$HOME/.ssh" && chmod 700 "$HOME/.ssh"
  touch "$HOME/.ssh/authorized_keys" && chmod 600 "$HOME/.ssh/authorized_keys"
  grep -qxF "$(cat "$pub")" "$HOME/.ssh/authorized_keys" || cat "$pub" >> "$HOME/.ssh/authorized_keys"
  ok "chave do Matheus autorizada"

  grep -q 'sshd_config.d' /etc/ssh/sshd_config \
    || aviso "seu sshd_config não lê $DROPIN; o login por senha continua ligado"
  printf 'PasswordAuthentication no\nKbdInteractiveAuthentication no\nPermitRootLogin no\n' \
    | sudo tee "$DROPIN" >/dev/null
  sudo sshd -t && recarregar_ssh && ok "ssh só com chave"

  command -v tailscale >/dev/null || curl -fsSL https://tailscale.com/install.sh | sh
  sudo systemctl enable --now tailscaled
  sudo tailscale up --authkey "$chave" --hostname "xeque-$USER"
  ok "na rede do Tailscale. Manda isso pro Matheus:  $USER@xeque-$USER  ($(tailscale ip -4 | head -1))"
}

remover_acesso() {
  local pub="$DIR/chaves/matheus.pub" ak="$HOME/.ssh/authorized_keys"
  if [ -f "$ak" ] && [ -f "$pub" ]; then
    grep -vxF "$(cat "$pub")" "$ak" > "$ak.tmp" || true
    mv "$ak.tmp" "$ak" && chmod 600 "$ak" && ok "chave do Matheus removida"
  fi
  if [ -f "$DROPIN" ]; then
    sudo rm -f "$DROPIN" && recarregar_ssh && ok "ssh voltou à configuração de antes"
  fi
  if command -v tailscale >/dev/null; then
    sudo tailscale logout && ok "fora da rede do Tailscale (sudo apt remove tailscale tira o programa)"
  fi
}

chave='' remover=''
while [ $# -gt 0 ]; do
  case $1 in
    --chave) chave=${2:-}; [ -n "$chave" ] || erro "--chave precisa da chave do Tailscale"; shift 2 ;;
    --remover-acesso) remover=1; shift ;;
    -h|--help) uso; exit 0 ;;
    *) uso; erro "opção desconhecida: $1" ;;
  esac
done

if [ -n "$remover" ]; then
  remover_acesso
  exit 0
fi
instalar_xeque
[ -n "$chave" ] && liberar_acesso "$chave"
echo
ok "tudo pronto. Abra um terminal e digite:  xeque"
