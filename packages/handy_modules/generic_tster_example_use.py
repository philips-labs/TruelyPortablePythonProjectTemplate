
import os
import logging
from datetime import datetime
from handy_modules.generic_tster import tst_runner



#defining logfile
NOW = datetime.now()
DATE_TIME = NOW.strftime("%Y_%m_%d_%H_%M_%S_")
LOGFILENAME ="example_logging" + DATE_TIME + ".log"

FORMAT = '%(asctime)s:%(levelname)-8s:%(filename)s:%(funcName)s:%(lineno)d: %(message)s'

""""
As an example of how to store the output of the logging to a file and how 
to just keep it to the output stream of the program
"""
STORE_IN_FILE=False
if STORE_IN_FILE:
  handlers = [logging.FileHandler(LOGFILENAME), logging.StreamHandler()]
else:
  handlers = [logging.StreamHandler()]


logging.basicConfig(format=FORMAT, handlers=handlers, level=logging.DEBUG)


def example_successful_tst():
    logging.info("Example Success")
    assert True, "This shall not result in an error"


def example_fail():
    logging.info("Failure via exception")

    msg="Showing how Failing looks like"
    assert msg == "Not True", msg


""""
Avoid the name "test" to avoid interference with pytest
"""
def tstmain():
    tests = [example_successful_tst, example_fail]

    return tst_runner(tests)




if __name__ == "__main__":

    tstmain()