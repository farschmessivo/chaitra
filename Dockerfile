FROM python:3.7
ADD web /web
WORKDIR /web
RUN pip install -r requirements.txt
CMD ["python", "app.py"]