import os
def file_exists(folder_path, filename):
    file_path = os.path.join(folder_path, filename)
    return os.path.exists(file_path)