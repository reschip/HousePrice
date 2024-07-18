FROM python:3.9

WORKDIR /app

COPY ./app/main.py ./app/main.py
COPY ./app/modelo_entrenado.json ./app/modelo_entrenado.json
COPY ./app/preprocessor.pkl ./app/preprocessor.pkl
COPY ./app/requirements.txt ./app/requirements.txt
RUN pip install --no-cache-dir -r ./app/requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
