
import subprocess
import shlex


def command_call(command):
    print(f"passing {command}: {shlex.split(command)}")
    subprocess.call([shlex.split(command)], shell=True)




def command_Popen(command):
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, shell = True)
    while True:
        output = process.stdout.readline().decode("utf-8")
        print(f"poll={process.poll()}")
        print(f'output = {output}')
        if output == '' and process.poll() is not None:
            break
    rc = process.poll()
    return rc


def command_run(command):
    process = subprocess.run(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell = True)
    rc = process.stdout.decode('utf-8')
    return rc


def __example1():
    print("starting")
    rc = command_run("python -m willcrash")
    print("\nnow for rc:\n---BEGIN-----")
    print(rc)
    print("-----END----")



def __example2():
    print("starting")
    rc = command_run("dir")
    print("\nnow for rc:\n---BEGIN-----")
    print(rc)
    print("-----END----")


if "__main__" == __name__:

    __example2()
    __example1()