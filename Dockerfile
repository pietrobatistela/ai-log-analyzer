# 1. Imagem base leve do Python
FROM python:3.11-slim

# 2. Define o diretório de trabalho dentro do container
WORKDIR /app

# 3. Copia o arquivo de dependências e instala os pacotes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copia o código da aplicação para o container
COPY app ./app

# 5. Expõe a porta que a aplicação vai utilizar
EXPOSE 8000

# 6. Comando para iniciar o servidor Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]