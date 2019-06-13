import os
import multiprocessing


class Job(multiprocessing.Process):
    def __init__(self, cmd, dir_, env=os.environ):
        super().__init__()
        self._cmd = cmd
        self._dir = dir_
        self._env = env
    
    def run(self):
        os.chdir(self._dir)
        os.execlpe('bash', 'bash', '-c', self._cmd, self._env)
