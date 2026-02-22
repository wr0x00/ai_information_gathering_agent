# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=django_ai_agent.ai_agent_project.settings

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        nodejs \
        npm \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Node.js dependencies
COPY package.json package-lock.json* ./
RUN npm install

# Copy project
COPY . .

# Build React frontend
RUN npm run build

# Expose port
EXPOSE 8000

# Collect static files
RUN python django_ai_agent/manage.py collectstatic --noinput

# Run migrations and start server
CMD ["sh", "-c", "python django_ai_agent/manage.py migrate && python django_ai_agent/manage.py runserver 0.0.0.0:8000"]
