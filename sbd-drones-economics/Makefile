PYTHONPATH := .:components/sdk-core/src:systems/operator/operator_component/src:systems/operator/gateway/src:systems/operator/src

.PHONY: setup build-all build-docker run-all run-all-docker tests-all tests-all-docker

setup:
	python -m venv .venv
	. .venv/bin/activate && pip install --upgrade pip pytest

build-all:
	@echo "Python services do not require native compilation."

build-docker:
	docker compose build

run-all:
	PYTHONPATH=$(PYTHONPATH) python -m operator_system

run-all-docker:
	docker compose up --build operator_system

tests-all:
	PYTHONPATH=$(PYTHONPATH) pytest

tests-all-docker:
	docker compose run --rm operator_system pytest
