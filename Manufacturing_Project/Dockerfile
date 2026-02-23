# Step 1: Use Python as the base
FROM python:3.9-slim

# Step 2: Set the working folder inside the container
WORKDIR /app

# Step 3: Copy your requirements list and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 4: Copy everything else (your code, the model folder, and the CSV)
COPY . .

# Step 5: Tell Docker to open port 8000 (FastAPI's default)
EXPOSE 8000

# Step 6: Start the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]