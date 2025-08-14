import sys

from consts import (
    COPY_TO_DIR, 
    COPY_FROM_DIR,
)
from functions import (
    copy_from_public_to_static,
    generate_pages_recursively,
)


def main():
    basepath = sys.argv[0]

    if not basepath:
        basepath = "/"

    copy_from_public_to_static(COPY_FROM_DIR, COPY_TO_DIR)
    generate_pages_recursively("content", "template.html", "docs", basepath)


if __name__ == "__main__":
    main()

