FROM python:3.8

# Working Directory
WORKDIR /app

# Copy source code to working directory
COPY . app.py /app/

# Install packages from requirements.txt
RUN pip install --upgrade pip &&\
    pip install -v -r requirements.txt

EXPOSE 5000

CMD ["python", "./app.py"]
