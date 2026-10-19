#!/bin/bash
DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"
python3 "$DIR/xeque.py" "$@"
