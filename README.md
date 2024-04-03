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
