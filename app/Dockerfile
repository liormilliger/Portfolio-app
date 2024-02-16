FROM python:3.9-slim

#Copying and installing dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Copying relevant folders
COPY ./static /app/static
COPY ./templates /app/templates
COPY main.py .
EXPOSE 5000

# Run main.py when the container launches
CMD ["python", "main.py"]
