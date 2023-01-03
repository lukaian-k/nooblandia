import os


def clear_dir(directory:str):
    for root, dirs, files in os.walk(directory):
        
        for file in files:
            os.unlink(os.path.join(root, file))

        for dir in dirs:
            os.rmtree(os.path.join(root, dir))