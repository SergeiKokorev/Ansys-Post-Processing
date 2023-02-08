import os


def get_files(ext: str, directory: str) -> list:
    
    files = []
    try:
        for file in os.listdir(directory):
            if file.endswith(f'.{ext}'):
                files.append(os.path.join(directory, file))
    except FileNotFoundError:
        raise FileNotFoundError(f'The system could not find the specified path {directory}')
    
    return files