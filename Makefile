## The Makefile includes instructions on environment setup and lint tests
# Each "command" runs exactly in different shell, so chain commands using &&
# setup: Create and activate a virtual environment
# Install: install dependencies in requirements.txt
# Lint: Dockerfile should pass hadolint, any code.py should pass pylint
 
# Targets
  
setup:
	# Create python virtualenv using  python builtin 'venv' module
	# install pylint for python linting
	python3 -m venv ./venv &&\
	pip install pylint &&\
	sudo wget -O /bin/hadolint https://github.com/hadolint/hadolint/releases/download/v2.12.0/hadolint-Linux-x86_64 &&\
	sudo chmod +x /bin/hadolint
install:
	# This should be run from inside a virtualenv
	. ./venv/bin/activate &&\
	pip install --upgrade pip &&\
	pip install -r requirements.txt
	sleep 3
lint:
	# See local hadolint install instructions:   https://github.com/hadolint/hadolint
	# linter for Dockerfiles
	# linter for Python source code linter: https://www.pylint.org/
	. ./venv/bin/activate &&\
	hadolint Dockerfile &&\
	pylint --disable=R,C,W0611,E0401,E0402,E0611 --fail-under=7 ./**/*.py 
	# Pylint fails only if the score under 7
	sleep 2

test:
	# Run Unit tests on Job application
	. ./venv/bin/activate &&\
	python3 src/backend/manage.py test job/
	sleep 2
run:
	# Run django server
	. ./venv/bin/activate &&\
	python src/backend/manage.py runserver 0.0.0.0:8080 &
docker:
	. ./venv/bin/activate &&\
	docker images &&\
	docker build -t django-job-board . &&\
	docker run -d --name django-job-board -p 8000:8000 django-job-board 

local-runtime: install lint test run
docker-runtime: install lint test docker
