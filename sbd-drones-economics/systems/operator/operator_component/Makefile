PYTHONPATH := .:components/sdk-core/src:systems/operator/operator_component/src

.PHONY: test run

test:
	PYTHONPATH=$(PYTHONPATH) pytest systems/operator/operator_component/tests -q

run:
	PYTHONPATH=$(PYTHONPATH) python -m operator_component
