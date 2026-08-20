"""Permite `python -m curso ...` além do comando `curso ...`."""

import sys

from curso.cli import main

if __name__ == "__main__":
    sys.exit(main())
