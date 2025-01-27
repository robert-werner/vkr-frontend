import nox


@nox.session(python=["3.12"], reuse_venv=False)
def lint(session: nox.Session):
    """Lint environment.

    :param session: nox session
    """
    session.install(".[lint]")
    session.run("flake8", ".")
    session.run("black", "--check", ".")
