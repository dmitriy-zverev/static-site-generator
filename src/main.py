import os
import shutil

from consts import COPY_TO_DIR, COPY_FROM_DIR


def main():
    copy_from_public_to_static(COPY_FROM_DIR, COPY_TO_DIR)

def copy_from_public_to_static(from_dir, to_dir):
    static_dir = os.path.abspath(from_dir)

    if os.path.exists(os.path.abspath(to_dir)):
        shutil.rmtree(os.path.abspath(to_dir))

    os.mkdir(os.path.abspath(to_dir))

    public_dir = os.path.abspath(to_dir)
    static_content = os.listdir(static_dir)

    for content in static_content:
        static_file_path = os.path.join(static_dir, content)
        if os.path.isfile(static_file_path):
            public_file_path = os.path.join(public_dir, content)
            shutil.copy(static_file_path, public_file_path)
        else:
            copy_from_public_to_static(
                static_file_path,
                os.path.join(public_dir, content)
            )
    


if __name__ == "__main__":
    main()
