import random
from typing import Any, Dict

try:
    import docker
    from docker import errors as docker_errors
except ModuleNotFoundError:
    docker = None
    docker_errors = None


def _get_client() -> Any:
    if docker is None:
        raise RuntimeError("Python docker SDK is not installed. Install with 'pip install docker'.")

    client = docker.from_env()

    try:
        client.ping()
    except docker_errors.DockerException as exc:
        raise RuntimeError(
            "Unable to connect to Docker engine. Ensure Docker Desktop is running and Docker daemon is available."
        ) from exc

    return client


def get_docker_status() -> Dict[str, Any]:
    try:
        client = _get_client()
        version = client.version() or {}
        return {
            "available": True,
            "server_version": version.get("Version", "unknown"),
            "docker_info": version,
        }
    except RuntimeError as exc:
        return {
            "available": False,
            "error": str(exc),
        }


def create_workspace_container(name: str) -> Dict[str, Any]:
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Workspace name must be a non-empty string.")

    client = _get_client()

    max_retries = 6
    last_error = None

    for _ in range(max_retries):
        port = random.randint(6000, 7000)

        try:
            container = client.containers.run(
                "lscr.io/linuxserver/webtop:latest",
                detach=True,
                ports={"3000/tcp": port},
                environment={"TITLE": name},
            )

            return {
                "id": container.id,
                "port": port,
                "url": f"http://localhost:{port}",
            }

        except docker_errors.ImageNotFound as exc:
            raise RuntimeError(
                "Webtop image not found. Try pulling the image manually: docker pull lscr.io/linuxserver/webtop:latest"
            ) from exc

        except docker_errors.APIError as exc:
            last_error = exc
            # port conflicts or transient API errors: retry with new port
            continue

        except docker_errors.DockerException as exc:
            raise RuntimeError(f"Unable to create container: {exc}") from exc

    raise RuntimeError(
        "Unable to allocate a free host port for the workspace container after multiple attempts." +
        (f" Last error: {last_error}" if last_error else "")
    )
