# Usa a imagem oficial do Python
FROM python:3.12-slim

# Define diretório de trabalho no container
WORKDIR /app

# Copia o arquivo de dependências
COPY requirements.txt .

# Instala dependências no sistema e no Python
RUN apt-get update && apt-get install -y \
    gcc libffi-dev libssl-dev python3-dev firebird-dev \
 && pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt \
 && apt-get remove -y gcc \
 && apt-get autoremove -y \
 && rm -rf /var/lib/apt/lists/*

# Copia o restante do projeto para o container
COPY . .

# Expõe a porta padrão do Uvicorn/FastAPI
EXPOSE 8000

# Comando para iniciar o servidor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
