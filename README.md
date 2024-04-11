# Information Retrieval Evaluation

## documents

[preparation sheet](https://docs.google.com/document/d/1CyZr6BCO7HAJkWeOlmOVO5_PjgciXi6qZNcJ2JwUiyE/edit?usp=sharing)

[evaluation sheet](https://docs.google.com/document/d/1RlGlw1xzIZ5iDCYKw6M5eYVcVZCS67_rZi2n-odH48c/edit?usp=sharing)

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

## production deployment

```bash
gunicorn -c gunicorn_config.py main:app
```