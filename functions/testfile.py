import os

def create_testfile(static_folder):
    path = os.path.join(static_folder, "testfile_1MB.bin")
    if not os.path.exists(path):
        with open(path, "wb") as f:
            f.write(os.urandom(1024 * 1024))
    return path
