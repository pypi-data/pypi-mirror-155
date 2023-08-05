import os
import sys
from subprocess import Popen
from contextlib import contextmanager
import time

from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile
import uuid

web_path = os.path.dirname(os.path.realpath(__file__))  # cyc-next
server_path = os.path.join(web_path, 'server')
FILE_NAME = 'workspace.yaml'
CHANGE_LINE_NUMBER = 4
FIELD_LENGTH = 6
WITHOUT_PROJECT = 0
HAVE_PROJECT = 1
DOWNLOAD_PATH = 'https://bitbucket.org/robotdreamers/cnext_sample_projects/get/9ee7cba2573c.zip'


def change_path(path):
    os.chdir(server_path)
    my_file = open(FILE_NAME)

    string_list = my_file.readlines()
    my_file.close()

    project_id = str(uuid.uuid1())
    string_list[0] = 'active_project: ' + '"' + project_id + '"' + '\n'
    content_2 = string_list[2];
    string_list[2] = content_2[:FIELD_LENGTH] + 'id: ' + '"' + project_id + '"' + '\n'

    content = string_list[CHANGE_LINE_NUMBER]
    print(string_list[CHANGE_LINE_NUMBER])
    string_list[CHANGE_LINE_NUMBER] = content[:FIELD_LENGTH] + \
        'path: ' + '\'' + path + '\'' + '\n'
    print(string_list[CHANGE_LINE_NUMBER])
    my_file = open(FILE_NAME, 'w')
    new_file_contents = ''.join(string_list)
    # Convert `string_list` to a single string
    my_file.write(new_file_contents)
    my_file.close()
    print('map path for sample project done!')


def ask():
    answer = input('Would you like to start with a sample project? (Y/N) :')
    if(answer == 'y' or answer == 'Y'):
        return HAVE_PROJECT
    elif (answer == 'n' or answer == 'N'):
        return WITHOUT_PROJECT
    else:
        ask()


def build():
    os.chdir(web_path)
    os.system('npm i --force')
    os.system('npm run build')
    os.chdir(server_path)
    os.system('npm i')


def download_and_unzip(url, extract_to='.'):
    http_response = urlopen(url)
    zipfile = ZipFile(BytesIO(http_response.read()))
    zipfile.extractall(path=extract_to)
    skywaler_path = os.path.join(
        extract_to, zipfile.namelist()[0], 'Skywalker')
    change_path(os.path.normpath(skywaler_path).replace(os.sep,'/'))


def build_path():
    path = input(
        'Please enter the directory\'s path to store the sample project in: ')
    print('Checking your path: ' + path)
    if os.path.isdir(path):
        os.chdir(path)
        folder_name = os.path.basename(path)
        print('Your sample project will download in', folder_name)
        download_and_unzip(DOWNLOAD_PATH, path)
    else:
        print('Your path isn\'t correct, Please try again')
        build_path()

def clear_content():
    os.chdir(server_path)
    my_file = open(FILE_NAME, 'w')
    new_file_contents = ''
    # Convert `string_list` to a single string
    my_file.write(new_file_contents)
    my_file.close()


def main():
    status = ask()
    if(status == WITHOUT_PROJECT):
        # remove all in workspace.yaml
        clear_content()
        build()
    else:
        build_path()
        build()


@contextmanager
def run_and_terminate_process():
    try:
        print("cnext starting !")

        os.chdir(web_path)
        web_proc = Popen('npm start', shell=True)

        os.chdir(server_path)
        my_env = os.environ.copy()
        my_env["PATH"] = os.path.dirname(
            sys.executable) + os.path.pathsep + my_env["PATH"]

        ser_proc = Popen('npm run start-prod', shell=True, env=my_env)
        yield

    finally:
        web_proc.terminate()  # send sigterm, or ...
        web_proc.kill()      # send sigkill

        ser_proc.terminate()  # send sigterm, or ...
        ser_proc.kill()      # send sigkill


def start():
    with run_and_terminate_process() as running_proc:
        while True:
            time.sleep(1000)


if __name__ == '__main__':
    main()
