# Use the official Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install gunicorn
RUN pip install gunicorn

# Copy project
COPY . /app/

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "invoice_project.wsgi:application"]
