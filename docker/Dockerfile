# Slim build of python
FROM python:3.8-slim

# Metadata
LABEL maintainer="Me" \ description="Python program in 3.8"

# Get tree utility for visualizing folder structure
RUN apt-get update && apt-get install tree

# Copy repository root to the app directory
COPY . / /app/

# Make a new working directory called app
WORKDIR /app/

# Install requirements 
RUN pip install -r requirements.txt

# Expose Port 8050
EXPOSE 8050

# Run python test script
ENTRYPOINT ["python3"]
CMD ["main.py"]