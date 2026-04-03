PYTHONPATH := .:components/sdk-core/src:systems/operator/operator_component/src:systems/operator/gateway/src:systems/operator/src

.PHONY: run test

run:
	PYTHONPATH=$(PYTHONPATH) python -m operator_system

test:
	PYTHONPATH=$(PYTHONPATH) pytest systems/operator/tests -q
