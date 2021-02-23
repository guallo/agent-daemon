# agent-daemon

## Using agent.sh to run the agent into a docker container

```bash
./agent.sh --jobs-server-cert-file -Mlocalhost.pem --jobs-endpoint https://localhost:8443/api/jobs/ --api-key-file -Mapi-key --job-pids-file job-pids --pull-every-secs 5
```

notice how we prepended an `-M` to the file path `localhost.pem`; that is to bind-mount that local file into the docker container.
