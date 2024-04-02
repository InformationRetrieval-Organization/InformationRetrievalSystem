# InformationRetrievalEvaluation

## python Unix
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install --upgrade pip
```
## python Windows
```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
pip install --upgrade pip
```
## database 

```bash
docker compose -f docker.compose.yml up -d
prisma db push
```
