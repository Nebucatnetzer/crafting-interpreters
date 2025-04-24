HAD_ERROR = False


def error(line: int, message: str) -> None:
    report(line, "", message)


def report(line: int, where: str, message: str) -> None:
    """Report an eror and it's location."""
    global HAD_ERROR  # noqa: PLW0603
    print("[line " + str(line) + "] Error" + where + ": " + message)
    HAD_ERROR = True
