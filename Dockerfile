FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

RUN apt-get update && \
    apt-get install -y --no-install-recommends netcat && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /app

COPY . ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 80
EXPOSE 443

ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
