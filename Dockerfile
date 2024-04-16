# 

FROM python:3.12

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 3100

CMD sh -c 'prisma db push && gunicorn --pythonpath src main:app --bind "0.0.0.0:3100" --worker-class "uvicorn.workers.UvicornWorker"'