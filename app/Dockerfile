# FROM python:3.11 AS Builder
# WORKDIR /app
# COPY requirements.txt .
# RUN pip install -r requirements.txt

# # FROM python:3.11-slim
# # COPY --from=Builder /usr/local/lib/python3.11/dist-packages /usr/local/lib/python3.11/dist-packages/
# # WORKDIR /app
# COPY . .
# EXPOSE 5000

# CMD ["python3", "main.py"]

FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run main.py when the container launches
CMD ["python", "main.py"]
# CMD ["flask", "run"]
