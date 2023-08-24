FROM python:latest
RUN apt-get update && apt-get install -y libgl1-mesa-glx
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY ./ ./
EXPOSE 8001
CMD ["python", "app.py"]