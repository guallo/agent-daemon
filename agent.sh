#!/usr/bin/env bash

DOCKER_IMAGE="agent-daemon:latest"
DOCKER_ARGS=()
AGENT_ARGS=()

while (($#)); do
    case $1 in
        --jobs-server-cert-file|--api-key-file|--job-pids-file)
            AGENT_ARGS+=("$1")
            if [[ "$2" == -M* ]]; then
                source="$(realpath -m "${2:2}")"
                target="/mnt/$source"
                DOCKER_ARGS+=("--mount" "type=bind,source=$source,target=$target")
            else
                target="$2"
            fi
            AGENT_ARGS+=("$target")
            shift 2
            ;;
        *)
            AGENT_ARGS+=("$1")
            shift
            ;;
    esac
done

format="{{.Repository}}"
if [[ "$DOCKER_IMAGE" == *:* ]]; then
    format="$format:{{.Tag}}"
fi

if ! docker images --format "$format" | grep -P "^.{${#DOCKER_IMAGE}}$" \
    | grep -qF "$DOCKER_IMAGE"; then
    pushd "$(dirname "$(realpath "$BASH_SOURCE")")"
    docker build -t "$DOCKER_IMAGE" .
    popd
fi

container="$(echo "$DOCKER_IMAGE" | tr -d -c "[:alpha:][:digit:]")-container"
exec docker run --name "$container" --rm -it --network=host \
    "${DOCKER_ARGS[@]}" "$DOCKER_IMAGE" "${AGENT_ARGS[@]}"
