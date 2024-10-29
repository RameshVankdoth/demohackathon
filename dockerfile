# Use the official Python image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for pyodbc and ODBC drivers
RUN apt-get update && apt-get install -y \
    unixodbc \
    unixodbc-dev \
    build-essential \
    libssl-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Microsoft ODBC driver for SQL Server (optional: include only if you need it)
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Copy application files to the container
COPY app.py /app/
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 5000

# Define the command to run the app
CMD ["python", "app.py"]
