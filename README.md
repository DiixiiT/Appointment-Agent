## pyhton version used  python3.13

### Create virtualenv:
```
python3.13 -m venv venv 
```

### Install requirements:
```
pip install -r requirements.txt
```

### Build vecotr db:
``` 
python3.13 -m rag.vector_store
```
### run application:
```
 python -m uvicorn main:app --reload
```