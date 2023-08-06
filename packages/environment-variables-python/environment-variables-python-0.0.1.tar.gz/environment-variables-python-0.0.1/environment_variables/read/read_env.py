from dotenv import dotenv_values


def read_env(file_path: str) -> dict:
    values = dotenv_values(dotenv_path=file_path)
    return values
