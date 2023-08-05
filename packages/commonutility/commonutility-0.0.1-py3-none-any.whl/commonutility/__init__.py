import socket

import os
import zipfile


def get_machine_ip():
    """
    Retrieve the current machine IP address

    :return: IP address
    """
    s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))

    return s.getsockname()[0]


def decompress_file(file_path, destination_dir):
    """
    Decompress zip/tar file at file_path to destination_dir

    :param file_path: Zip file path
    :param destination_dir: The directory to extract file
    """
    if not os.path.isfile(file_path):
        raise Exception('No file exists at location [{}]'.format(file_path))

    with zipfile.ZipFile(file_path, 'r') as zip_file:
        zip_file.extractall(destination_dir)


def search_recursive(directory, file_names):
    """
    Search file in given directory which is matched file_names, and return the absolute path of file

    :param directory: Directory to search file
    :param file_names: File names to match

    :return: A tuple,
              first value is bool, success or failure
              second value is absolute path of file, if found else None
    """
    if not os.path.exists(directory):
        return False, None

    index_files = [file.lower() for file in file_names]

    for directory_path, directory_names, files in os.walk(directory):
        for file in files:
            if file.lower() in index_files:
                return True, os.path.join(directory_path, file)

    return False, None
