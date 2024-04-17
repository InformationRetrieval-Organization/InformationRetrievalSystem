# Information Retrieval Evaluation

## documents

[preparation doc](https://docs.google.com/document/d/1CyZr6BCO7HAJkWeOlmOVO5_PjgciXi6qZNcJ2JwUiyE/edit?usp=sharing)

[evaluation doc](https://docs.google.com/document/d/1RlGlw1xzIZ5iDCYKw6M5eYVcVZCS67_rZi2n-odH48c/edit?usp=sharing)

[ground truth sheet](https://docs.google.com/spreadsheets/d/1wl72UrtBVSqMwfYwsJgIb21gftcBTYMtiB67N0tCS7A/edit?usp=sharing)

## requirements

* Python >=3.7
* Visual Studio Code

## Python

### unix/mac
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install --upgrade pip
```

### windows
```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
pip install --upgrade pip
```

## environment variables
* copy and rename the `.env.sample` file to `.env`
* when you want to crawl data, you have to set the API keys

## database 
```bash
docker compose -f docker.compose.yml up -d
prisma db push
```

### optional: pgadmin
Open `http://localhost:5050/`
1) Email: root@root.com
2) Password: root

Click with the right mouse button on Servers and select Register -> Server.

Connection tab requires to type:
1) Host name/address: db
2) Port: 5432
3) Username: postgres
4) Password: postgres

## optional: swagger
Open `http://localhost:8000/docs` to see the swagger UI

## optional: Docker
building
```bash
docker build --tag tonylukeregistry.azurecr.io/tonylukeregistry/information-retrieval/api:latest .
```

running container locally
```bash
docker run --detach --publish 3100:3100 tonylukeregistry.azurecr.io/tonylukeregistry/information-retrieval/api:latest
```


## optional: azure deployment
change connection string;
```bash
postgresql://<dbuser>:<dbpassword>@<dbservername>.postgres.database.azure.com:<port>/<bdname>?schema=public&sslmode=require
```

startup command (azure needs gunicorn)
```bash
prisma db push && gunicorn --pythonpath src main:app --bind "0.0.0.0:3100" --worker-class "uvicorn.workers.UvicornWorker"
```



