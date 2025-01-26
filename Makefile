## The Makefile includes instructions on environment setup and lint tests
# Each "command" runs exactly in different shell, so chain commands using &&
# setup: Create and activate a virtual environment
# Install: install dependencies in requirements.txt
# Lint: Dockerfile should pass hadolint, any code.py should pass pylint
 
# Target

# Global commands
#
## add support for Bash shell to allow bash only compatible commands like source
SHELL := /bin/bash
  
setup:
	# Create python virtualenv using  python builtin 'venv' module
	# install pylint for python linting
	python3 -m venv venv &&\
	source venv/bin/activate &&\
	pip3 install pylint &&\
	sudo wget -O /bin/hadolint https://github.com/hadolint/hadolint/releases/download/v2.12.0/hadolint-Linux-x86_64 &&\
	sudo chmod +x /bin/hadolint
install:
	# This should be run from inside a virtualenv
	source venv/bin/activate &&\
	pip3 install --upgrade pip &&\
	pip3 install -r requirements.txt
	sleep 3
lint:
	# See local hadolint install instructions:   https://github.com/hadolint/hadolint
	# linter for Dockerfiles
	# linter for Python source code linter: https://www.pylint.org/
	source venv/bin/activate &&\
	hadolint Dockerfile &&\
	pylint --disable=R,C,W0611,E0401,E0402,E0611 --fail-under=7 src/**/*.py 
	# Pylint fails only if the score under 7
	sleep 2

test:
	# Run Unit tests on Job application
	source venv/bin/activate &&\
	python3 src/backend/manage.py test src/backend/job/
	sleep 2
run:
	# Run django server
	source venv/bin/activate &&\
	python3 src/backend/manage.py runserver 0.0.0.0:8080 &
docker:
	# Stop and remove any existing container with the same name
	# Build the Docker image
	# Remove dangling images
	# Run the Docker container
	source venv/bin/activate &&\
	(docker rm -f django-job-board || true) &&\
	docker build -t django-job-board . &&\
	(docker image prune -f || true) &&\
	docker run -d --name django-job-board -p 8000:8000 django-job-board

local-runtime: install lint test run
docker-runtime: install lint test docker
