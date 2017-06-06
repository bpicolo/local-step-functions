.PHONY: app
app: virtualenv_run
	./virtualenv_run/bin/python -m local_step_functions.app

.PHONY: daemon
daemon: virtualenv_run
	./virtualenv_run/bin/python -m local_step_functions.daemon.state_executor


virtualenv_run:
	virtualenv -ppython3.6 virtualenv_run
	pip install -r requirements.txt
