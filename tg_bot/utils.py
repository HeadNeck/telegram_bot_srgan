

import os, shutil




def create_dir(paths):
    for path in paths:
        if not os.path.exists(path):
            os.mkdir(path)

def clean_folders(folder_names):
    for folder_name in folder_names:
        for filename in os.listdir(folder_name):
            file_path = os.path.join(folder_name, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
