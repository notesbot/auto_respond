FROM python:3.10 

WORKDIR /app

COPY requirements.txt .

RUN pip install --user -r requirements.txt

COPY auto_respond.py .

CMD ["python", "auto_respond.py"]