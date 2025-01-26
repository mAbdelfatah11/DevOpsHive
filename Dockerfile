# Base image: uses the same py3.12 version tested locally, note: it uses apk package manager
FROM python:3.12-slim-bullseye

# Ste ENV: increase logs verbosity exposed by django runtime
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy deps file
COPY requirements.txt . /app/

# Install deps: prevent pip from caching downloaded packages  reduce the size of the Docker image  "--no-cache-dir"
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest app src
COPY . /app/

# All time Eexecutable set as ENTRYPOINT
ENTRYPOINT [ "python", "src/backend/manage.py", "runserver", "0.0.0.0:8000" ]

# More likely changed Params set as CMD
# CMD [ "0.0.0.0:8000" ]

# Port metadata
EXPOSE 8000

