#!/usr/bin/env bash
# Sobe o JF Treino do zero, sem Docker.
#
#     ./comecar.sh              instala, monta a demonstração e serve
#     ./comecar.sh --limpo      apaga o banco antes (recomeça do zero)
#
# Requisitos: Python 3.11+ e Node 20+.

set -euo pipefail
cd "$(dirname "$0")"

if [[ "${1:-}" == "--limpo" ]]; then
  echo "Apagando o banco local…"
  rm -f jf.db
fi

# Sem chave fixa a sessão cai a cada reinício do servidor, o que durante o
# desenvolvimento parece um bug de login.
if [[ -z "${JF_CHAVE_SECRETA:-}" ]]; then
  export JF_CHAVE_SECRETA="desenvolvimento-local-nao-usar-em-producao"
fi

echo "→ Instalando o pacote Python…"
pip install -e . --quiet

echo "→ Compilando o PWA…"
(cd web && npm install --silent && npm run build)

if [[ ! -f jf.db ]]; then
  echo "→ Montando a demonstração…"
  jf demonstracao
else
  echo "→ Banco já existe; mantendo os dados. Use --limpo para recomeçar."
  jf preparar >/dev/null
fi

echo
echo "→ http://127.0.0.1:8770"
echo
exec jf servir
