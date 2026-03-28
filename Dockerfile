# 1. Use a lightweight Python base
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy only requirements first (this speeds up builds)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy your app code and the trained model
# Make sure your folder names match exactly!
COPY ./app ./app
COPY ./models ./models

# 5. Expose the port FastAPI runs on
EXPOSE 8000

# 6. Command to start the API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]