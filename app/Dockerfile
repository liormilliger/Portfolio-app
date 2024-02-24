FROM python:3.9-alpine

#Copying and installing dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Copying relevant folders
COPY ./templates /app/templates
COPY main.py .
EXPOSE 5000

# Run main.py when the container launches
CMD ["python", "main.py"]
