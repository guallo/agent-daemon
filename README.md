# agent-daemon

## Using agent.sh to run the agent into a docker container

```bash
./agent.sh --jobs-server-cert-file -Mlocalhost.pem --jobs-endpoint https://localhost:8443/api/jobs/ --api-key-file -Mapi-key --job-pids-file job-pids --pull-every-secs 5
```

Notice how we prepended an `-M` to the file paths `localhost.pem` and `api-key`; that is used to reference local files that we want to bind-mount into the container. Conversely the `job-pids` file path, makes only reference to that file into the container.
