pyhton version used  python3.13

create virtualenv - python3.13 -m venv venv 

install requirements - pip install -r requirements.txt

Build vecotr db  -  python3.13 -m rag.vector_store

run application -  python -m uvicorn main:app --reload