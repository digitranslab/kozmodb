def start_http(*args, **kwargs):
    from kozmodb.utilities.log import initialize_logging

    initialize_logging("http")

    from kozmodb.api.http.start import start

    start(*args, **kwargs)


def start_mysql(*args, **kwargs):
    from kozmodb.utilities.log import initialize_logging

    initialize_logging("mysql")

    from kozmodb.api.mysql.start import start

    start(*args, **kwargs)


def start_postgres(*args, **kwargs):
    from kozmodb.utilities.log import initialize_logging

    initialize_logging("postgres")

    from kozmodb.api.postgres.start import start

    start(*args, **kwargs)


def start_tasks(*args, **kwargs):
    from kozmodb.utilities.log import initialize_logging

    initialize_logging("tasks")

    from kozmodb.interfaces.tasks.task_monitor import start

    start(*args, **kwargs)


def start_ml_task_queue(*args, **kwargs):
    from kozmodb.utilities.log import initialize_logging

    initialize_logging("ml_task_queue")

    from kozmodb.utilities.ml_task_queue.consumer import start

    start(*args, **kwargs)


def start_scheduler(*args, **kwargs):
    from kozmodb.utilities.log import initialize_logging

    initialize_logging("scheduler")

    from kozmodb.interfaces.jobs.scheduler import start

    start(*args, **kwargs)


def start_litellm(*args, **kwargs):
    """Start the LiteLLM server"""
    from kozmodb.utilities.log import initialize_logging

    initialize_logging("litellm")

    from kozmodb.api.litellm.start import start

    start(*args, **kwargs)
