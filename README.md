# agent-daemon

To run the `agent` into a docker container:

```bash
./agent.sh [AGENT_ARG]...
```

In case you want to bind-mount a local file into the docker container
just prepend an `-M` to the file path, for example:

```bash
./agent.sh --jobs-server-cert-file "-Mcerts/server.pem" [AGENT_ARG]...
```
