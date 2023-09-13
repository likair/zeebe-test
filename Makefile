.PHONY: all install_poetry setup test robot deploy_zeebe depose_zeebe export_requirements clean

all: setup deploy_zeebe test depose_zeebe

install_zbctl:
	command -v zbctl >/dev/null 2>&1 || npm i -g zbctl

install_poetry:
	command -v poetry >/dev/null 2>&1 || curl -sSL https://install.python-poetry.org | python3 -
	poetry config virtualenvs.in-project true

setup: install_poetry install_zbctl
	poetry install
	poetry run pre-commit install

test: robot

robot:
	poetry run robot -L TRACE -V test_data.yaml -d results tests

deploy_zeebe:
	# docker inspect zeebe >/dev/null 2>&1 || docker run -d -p 9600:9600 -e ZEEBE_STANDALONE_GATEWAY=true --name zeebe camunda/zeebe:latest
	docker inspect zeebe >/dev/null 2>&1 || docker compose up -d

depose_zeebe:
	# docker rm -f zeebe
	docker compose down

export_requirements:
	poetry export -f requirements.txt --output requirements.txt

clean:
	find . -name "*.pyc" -delete
	rm -rf .venv
	rm -rf .pytest_cache
	rm -f poetry.lock
