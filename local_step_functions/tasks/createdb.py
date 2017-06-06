from local_step_functions.app import create_app
from local_step_functions.models.db import db


def run_state_executor():
    while True:
        to_run = get_next_machine_to_run()
        if to_run is None:
            time.sleep(2)
            continue

        machine, execution = to_run
        output = run_state_machine(machine, execution, None)


if __name__ == '__main__':
    app = create_app()
    with app.test_request_context():
        db.create_all()
