from consts import (
    COPY_TO_DIR, 
    COPY_FROM_DIR,
)
from functions import (
    copy_from_public_to_static,
    generate_page,
)


def main():
    copy_from_public_to_static(COPY_FROM_DIR, COPY_TO_DIR)
    generate_page("content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
    main()

