FROM python:3.10

WORKDIR /app

COPY requirements.txt .

# STEP 1: Fix pip + setuptools version issue
RUN pip install --upgrade pip setuptools

# STEP 2: Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# STEP 3: Copy your code
COPY . .

# STEP 4: Run FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
