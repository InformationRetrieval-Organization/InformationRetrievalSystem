# InformationRetrievalEvaluation

## python

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
* add your `NYT_API_KEY` API key

## database 

```bash
docker compose -f docker.compose.yml up -d
prisma db push
```

### pgadmin
Open `http://localhost:5050/`
1) Email: root@root.com
2) Password: root

Click with the right mouse button on Servers and select Register -> Server.

Connection tab requires to type:
1) Host name/address: db
2) Port: 5432
3) Username: postgres
4) Password: postgres
