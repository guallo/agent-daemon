#!/usr/bin/env python3

import os
import time
import base64
import argparse
import requests
import multiprocessing


class Job(multiprocessing.Process):
    def __init__(self, uuid, cmd, directory=None, user=None, b64payload=None, extra_env=None):
        super().__init__()
        self._uuid = uuid
        self._cmd = cmd
        self._directory = directory
        self._user = user
        self._b64payload = b64payload
        self._extra_env = extra_env
    
    def run(self):
        if self._extra_env is not None:
            os.environ.update(self._extra_env)
        
        if self._directory is not None:
            os.chdir(self._directory)
        
        if self._b64payload is not None:
            payload = base64.b64decode(self._b64payload)
            open(f'payload_{self._uuid}', 'wb').write(payload)
        
        if self._user is not None:
            os.execlp('gosu', 'gosu', self._user, 'bash', '-c', self._cmd)
        else:
            os.execlp('bash', 'bash', '-c', self._cmd)


class Agent:
    def __init__(self, jobs_server_cert_file, jobs_endpoint, api_key_file,
                        job_pids_file, pull_every_secs):
        assert jobs_endpoint.startswith('https://')
        self._jobs_server_cert_file = jobs_server_cert_file
        self._jobs_endpoint = jobs_endpoint
        self._api_key_file = api_key_file
        self._job_pids_file = job_pids_file
        self._pull_every_secs = pull_every_secs
    
    def run(self):
        api_key = open(self._api_key_file, 'rb').read().strip()
        open(self._job_pids_file, 'wb')
        
        while True:
            r = requests.get(self._jobs_endpoint, headers={'X-API-Key': api_key},
                            verify=self._jobs_server_cert_file)
            jobs_data = r.json()
            
            for job_data in jobs_data:
                extra_env = {
                    'JOB_UUID': job_data['uuid'],
                    'AGENT_PID': str(multiprocessing.current_process().pid),
                    'JOB_PIDS_FILE': self._job_pids_file,
                }
                if job_data['extra_env'] is not None:
                    extra_env.update(job_data['extra_env'])
                
                job = Job(job_data['uuid'], job_data['cmd'], job_data['directory'], 
                            job_data['user'], job_data['b64payload'], extra_env)
                job.start()
                
                open(self._job_pids_file, 'ab').write(f'{job.pid}{os.linesep}'.encode('utf-8'))
            time.sleep(self._pull_every_secs)


def main():
    import daemon
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--jobs-server-cert-file', type=str, required=True)
    parser.add_argument('--jobs-endpoint', type=str, required=True)
    parser.add_argument('--api-key-file', type=str, required=True)
    parser.add_argument('--job-pids-file', type=str, required=True)
    parser.add_argument('--pull-every-secs', type=float, required=True)
    parser.add_argument('--daemonize', action='store_true')
    args = parser.parse_args()
    
    agent = Agent(args.jobs_server_cert_file, args.jobs_endpoint, args.api_key_file,
                    args.job_pids_file, args.pull_every_secs)
    
    if args.daemonize:
        with daemon.DaemonContext():
            agent.run()
    else:
        agent.run()


if __name__ == '__main__':
    main()
