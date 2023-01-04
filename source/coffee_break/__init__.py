__version__ = "0.0.0"
__version_info__ = tuple(__version__.split("."))


import logging

from .task import Task

logger = logging.getLogger(__name__)


def build(task, value_db):
    logging.info(f"Building {task!r}")

    # Do DFS to find input task ordering
    build_tasks = depth_first_search(task)

    # For each input task, see if it needs to be run, running it if so.
    for build_task in build_tasks:
        if _task_should_run(build_task, value_db):
            logging.info(f"Running task {build_task!r}")
            build_task.run()
            value_db.set(
                build_task.cache_id,
                {"inputs": _gather_input_cache_values(build_task), "outputs": _gather_output_cache_values(build_task)},
            )


def _task_should_run(task, value_db):
    current_cache_value = task.cache_value

    # If any outputs nodes can't provide a cache-value, then the task needs to run
    output_cache_values = current_cache_value["outputs"]
    if any(cache_value is None for cache_value in output_cache_values):
        return True

    # If we can't find cached values for the task, then the task needs to run
    try:
        previous_cache_ids = value_db.get(task.cache_id)
    except KeyError:
        return True

    previous_input_cache_ids = previous_cache_ids['inputs']
    previous_output_cache_ids = previous_cache_ids['outputs']

    input_cache_values = current_cache_value["inputs"]
    assert not any(cache_value is None for cache_value in input_cache_values)

    # If the cached input values don't match the current values, then the task needs to run
    if input_cache_values != previous_input_cache_ids:
        return True

    # If the cached output values don't match the current values, then the task needs to run
    if output_cache_values != previous_output_cache_ids:
        return True

    return False


def _gather_input_cache_values(task: Task):
    cache_values = []
    for input_node in task.input_nodes:
        cache_value = input_node.cache_value
        if cache_value is None:
            raise ValueError(f"Input node with no cache value. {input_node!r}")
        cache_values.append(cache_value)
    return cache_values


def _gather_output_cache_values(task: Task):
    return [node.cache_value for node in task.output_nodes]


def depth_first_search(task):
    tasks = []
    _depth_first_search(task, tasks, set())
    return tasks


def _depth_first_search(task, tasks, seen):
    for input_node in task.input_nodes:
        input_task = input_node.producer_task
        if input_task is not None:
            if input_task not in seen:
                _depth_first_search(input_task, tasks, seen)
    tasks.append(task)
    seen.add(task)
