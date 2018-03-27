import os


def create_directories_to_path(path):
    """Create directories to a path if they don't exist."""

    try:
        os.makedirs(os.path.dirname(path))
    except Exception:
        # directory already exists
        pass
