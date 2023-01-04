from coffee_break import build
from coffee_break.cache import use_cache
from coffee_break.node import File  
from coffee_break.task import Task
import logging

logging.basicConfig(level=logging.DEBUG)

class MyTask(Task):
    def run(self):
        with open(self.input_nodes[0].path, 'r') as f:
            data = f.read()

        with open(self.output_nodes[0].path, 'w') as f:
            f.write(data)
            f.write(data)

source_file = File('input.dat')
dest_file = File('output.dat')

task = MyTask([source_file], [dest_file])

with use_cache('cache.db') as cache:
    build(task, cache)
