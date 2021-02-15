FROM python:3.8
WORKDIR .
COPY src/ ./src
COPY samples/ ./samples
COPY tests/ ./tests
COPY requirements.txt .
COPY interface.py .
RUN pip install -r requirements.txt
ENTRYPOINT ["python","./interface.py"]
