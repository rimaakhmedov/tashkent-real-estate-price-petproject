FROM tiangolo/uvicorn-gunicorn:python3.11

RUN mkdir /fastapi

COPY requirements.txt /fastapi

WORKDIR /fastapi

RUN pip install -r requirements.txt -f https://download.pytorch.org/whl/torch_stable.html

COPY . /fastapi

EXPOSE 8001

CMD ["uvicorn", "fastapi_app:app", "--host", "0.0.0.0", "--port", "8001"]