FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000


# docker run -p 8000:8000 <image_name>
docker run -p 8000:8000 robustapi
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
