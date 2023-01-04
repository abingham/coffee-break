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
                build_task.id, (_gather_input_cache_values(build_task), _gather_output_cache_values(build_task))
            )


def _task_should_run(task, value_db):
    input_tracking_ids = _gather_input_cache_values(task)
    assert not any(tracking_id is None for tracking_id in input_tracking_ids)

    output_tracking_ids = _gather_output_cache_values(task)
    if any(tracking_id is None for tracking_id in output_tracking_ids):
        return True

    try:
        previous_input_tracking_ids, previous_output_tracking_ids = value_db.get(task.id)
    except KeyError:
        return True

    if input_tracking_ids != previous_input_tracking_ids:
        return True

    if output_tracking_ids != previous_output_tracking_ids:
        return True

    return False


def _gather_input_cache_values(task: Task):
    tracking_ids = []
    for input_node in task.input_nodes:
        tracking_id = input_node.cache_value()
        if tracking_id is None:
            raise ValueError(f"Input node with no cache value. {input_node!r}")
        tracking_ids.append(tracking_id)
    return tracking_ids


def _gather_output_cache_values(task: Task):
    return [node.cache_value() for node in task.output_nodes]



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
