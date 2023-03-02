
import platform
import os
from command_run import command_run, commandlist_run

CURDIR = os.path.dirname(os.path.abspath(__file__))
print("currentdir = {:s}".format(CURDIR))

ONEHIGHER =os.path.dirname(CURDIR)
print("ONEHIGHER={:s}".format(ONEHIGHER))

def find_pycharm_windows():
    """

    :return: string contains link to pycharm
    """
    assumed_base = r"C:\Program Files\JetBrains"
    for dir in os.listdir(assumed_base):
        totname = os.path.join(assumed_base, dir)
        if dir.startswith("PyCharm"):
            print("Using PyCharm version {:s}".format(dir))
            seek = os.listdir(os.path.join(totname,"bin"))
            if "pycharm.exe" in seek:
                res = os.path.join(totname, "bin", "pycharm.exe")
                if os.path.isfile(res):
                    return res
            elif "pycharm64.exe" in seek:
                res = os.path.join(totname, "bin", "pycharm64.exe")
                if os.path.isfile(res):
                    return res

            err = Exception("ERROR: Cannot file {}".format(res))
            raise(err)


def find_pycharm_mac():
    """

    """
    def lookfor(app):
        for i in listofapps:
            if i.startswith(app):
                name, exto = os.path.splitext(i)
                return name
        return None

    listofapps = os.listdir("/Applications")
    res = lookfor("PyCharm")
    if not res:
        return ["echo Can't find PyCharm"]

    cmd = ["open", "-a", res,  ONEHIGHER]
    return cmd

def get_command():

    print(platform.system())
    if platform.system() == "Windows":
        res= find_pycharm_windows()
        cmd =[res, ONEHIGHER]
        return cmd

    elif platform.system() == "Darwin":
        cmd = find_pycharm_mac()
        return cmd

    return "python"


if __name__ == "__main__":

   cmd = get_command()
   print(cmd)
   commandlist_run(cmd)
   



