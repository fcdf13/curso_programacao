# Duas etapas: o Node só compila o PWA, e a imagem final leva apenas o
# resultado. Assim nem o node_modules nem o toolchain de build sobram no
# que vai para produção.

FROM node:22-slim AS web
WORKDIR /web
# package.json antes do resto: o npm ci só refaz quando as dependências mudam,
# não a cada alteração de código.
COPY web/package.json web/package-lock.json ./
RUN npm ci
COPY web/ ./
RUN npm run build


FROM python:3.11-slim AS app
WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    JF_BANCO=sqlite:////dados/jf.db

COPY pyproject.toml ./
COPY jf/ ./jf/
RUN pip install --no-cache-dir .

COPY --from=web /web/dist ./web/dist

# O banco vive num volume: sem isso o histórico de treino do aluno some a cada
# `docker compose up --build`.
RUN mkdir -p /dados
VOLUME /dados

EXPOSE 8770

# `0.0.0.0` e não `127.0.0.1`: dentro do contêiner, ouvir só o loopback deixaria
# a porta publicada inacessível de fora.
CMD ["sh", "-c", "jf preparar && jf servir --host 0.0.0.0 --porta 8770"]
