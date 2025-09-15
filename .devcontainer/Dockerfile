# Use a Python 3.10 image as the base.
# The 'slim' image does not contain all necessary libraries.
FROM python:3.10

# Install system dependencies needed for building packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container.
COPY requirements.txt .

# Install all the packages from the requirements.txt file.
RUN pip3 install --no-cache-dir -r requirements.txt
