PYTHONPATH := .:components/sdk-core/src:systems/operator/gateway/src

.PHONY: test run

test:
	PYTHONPATH=$(PYTHONPATH) pytest systems/operator/gateway/tests -q

run:
	PYTHONPATH=$(PYTHONPATH) python -m operator_gateway
