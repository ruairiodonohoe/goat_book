"""Container commangs."""

import subprocess

USER = "elspeth"


def create_session_on_server(host: str, email: str) -> str:
    """Create session on server."""
    return _exec_in_container(host, ["/venv/bin/python", "manage.py", "create_session", email])


def _exec_in_container(host: str, commands: list) -> str:
    """Exec in container."""
    if "localhost" in host:
        return _exec_in_container_locally(commands)
    return _exec_in_container_on_server(host, commands)


def _exec_in_container_locally(commands: list) -> str:
    """Exec in container locally."""
    print(f"Running {commands} on inside local docker container")  # noqa : T201
    return _run_commands(["docker", "exec", _get_container_id(), *commands])


def _exec_in_container_on_server(host: str, commands: list) -> str:
    """Exec in container on server."""
    print(f"Running {commands!r} on {host} inside docker container")  # noqa : T201
    return _run_commands(["ssh", f"{USER}@{host}", "docker", "exec", "superlists", *commands])


def _get_container_id() -> str:
    """Get container id."""
    return (
        subprocess.check_output(
            ["docker", "ps", "-q", "--filter", "ancestor=superlists"]  # noqa: S607
        )
        .decode("utf-8")
        .strip()
    )


class CommandError(Exception):
    """Custom exception raised when a shell or container command fails."""


def _run_commands(commands: list) -> str:
    """Run commands."""
    process = subprocess.run(  # noqa: S603
        commands, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False
    )
    result = process.stdout.decode()
    if process.returncode != 0:
        raise CommandError(result)
    print(f"Result: {result!r}")  # noqa : T201
    return result.strip()


def reset_database(host: str) -> str:
    """Reset database."""
    return _exec_in_container(host, ["/venv/bin/python", "manage.py", "flush", "--noinput"])
