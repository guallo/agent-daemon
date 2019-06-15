import os
import multiprocessing


class Job(multiprocessing.Process):
    def __init__(self, cmd, dir_=None, user=None):
        super().__init__()
        self._cmd = cmd
        self._dir = dir_
        self._user = user
    
    def run(self):
        if self._dir is not None:
            os.chdir(self._dir)
        
        if self._user is not None:
            os.execlp('gosu', 'gosu', self._user, 'bash', '-c', self._cmd)
        else:
            os.execlp('bash', 'bash', '-c', self._cmd)
