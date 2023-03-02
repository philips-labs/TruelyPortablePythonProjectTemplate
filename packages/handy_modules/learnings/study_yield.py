
import logging

FORMAT = '%(filename)s:%(funcName)s:%(lineno)d: %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)


def counter():

    print("Now in Coutner")
    yield 10
    for i in range(3):
        yield i


    yield "First"

    yield "stop"

    #if the following statement is reached, an exception will be thrown
    return "stop"

def strange_counter(nr):
    """
    This shows that python transforms a method into a generator object
    if it contains a yield statement, even if that yield statement isn't triggered

    :param nr:
    :return:
    """

    if nr < 0:
        return -1
    else:
        yield nr


class StartingWithin:

    def __init__(self):
        self.busy=True

        logging.info("starting within")
        self.gom1 = self.m1()
        self.gom1.send(None)
        for i in range(10):
            logging.info(f"withing {i}")
            self.gom1.send(i)



    def m1(self):
        yield
        self.add = True
        while self.busy:
            logging.info("m1")
            yield
            if self.add:
                logging.info("m1 adding")
                self.m2loop=self.m2()
                self.m2loop.send(None)
                self.add = False
            else:
                logging.info("m1 using")
                yield
                self.m2loop.send(1)
            yield
            logging.info("m1 second")
            yield



    def m2(self):
        while self.busy:
            yield
            logging.info("m2")
            yield
            logging.info("m2 second")

def interactive_counter(start):

    while True:
        override = yield start
        logging.info(f"interactive {str(override)}, start={str(start)}")
        if override is None:
            start += 1
        else:
            start = override

class Replacement:


    def  __init__(self):
        self.busy = True

        self.placeholder = self.placeholder_loop()
        self.placeholder.send(None)
        self.replacement = self.toadd()
        self.replacement.send(None)

        self.main = self.basicloop()
        self.main.send(None)

    def replacewith(self, generator):

        self.placeholder = generator


    def basicloop(self):

        i=0
        while self.busy:
            logging.info("before placeholder")
            self.placeholder.send(i)
            logging.info("after placeholder")
            i+=1
            yield



    def toadd(self):

        logging.info(f"base to add dynamically")
        n=0
        while self.busy:
            r = yield n
            logging.info(f"Dynamic base r={r}, n={n}")
            yield
            logging.info("This one takes more time ")
            yield
            logging.info("and has many more yields")


    def placeholder_loop(self):
        logging.info(f"placeholder d dynamically")
        n = 0
        while self.busy:
            r = yield n
            logging.info(f"placeholder base r={r}, n={n}")


def study_replacement():

    sr = Replacement()
    sr.main.send(0)
    sr.replacewith(sr.replacement)
    sr.main.send(1)
    sr.main.send(1)
    sr.main.send(1)

    count = interactive_counter(0)
    count.send(None)
    sr.replacewith(count)
    sr.main.send(1)





class NestedYields:

    def __init__(self):
        self.busy = True

        logging.info("initializing")
        self.makefirst = self.firstbase()
        logging.info("created makefirst")
        self.makefirst.send(None)
        logging.info("sent none to make first")
        self.mainloop = self.secondbase()
        logging.info("created mainloop")
        self.mainloop.send(None)
        logging.info("sent none to mainloop")
        self.addedbase = self.basetoadd()
        self.addedbase.send(None)
        self.placeholderbase = self.placeholder()
        logging.info("finished initializing")


    def firstbase(self):
        n = 0
        while self.busy:
            logging.info(f" going to yield {n}")
            r = yield n
            n += r
            logging.info(f" received r={r} now will yield n={n}")
            n = yield n

    def secondbase(self):
        s=1
        while self.busy:
            logging.info(f"going to send {s}")
            n = self.makefirst.send(s)
            s+=n
            logging.info(f"incremented s by received {n} and going to yield {s}")
            r = yield s
            logging.info(f"s={s}, n = {n} received r = {r}, going to yield r={r}")
            s = yield r
            logging.info(f"sent {r} received {s}")




def study_nesting():

    logging.info(" starting study")
    ny = NestedYields()
    logging.info("ny initialized")


    for i in range(10):

        r = ny.mainloop.send(i)
        logging.info(f"main sent {i} received {r}")





def study_counter_case():

    #you must work with the instance of the method and not with the method itself.
    #a method that returns a yield behaves as a class
    generator_object = counter()
    busy = True
    while busy:

        ret = next(generator_object)
        print("Now received {:s}".format(str(ret)))
        if ret == "stop":
            busy = False


    print("Now look how a function changes")
    print(str(strange_counter(-1)))
    print(str(strange_counter(1)))

    gen_counter = strange_counter(1)
    print(str(next(gen_counter)))

    print(" Interactive counter")
    gen_interactive = interactive_counter(-1)
    for i in range(4):
        print(str(next(gen_interactive)))

    print("jump to 10")
    print(str(gen_interactive.send(10)))

    for i in range(4):
        print(str(next(gen_interactive)))


def study_launchingwithin():
    st = StartingWithin()


if __name__ == "__main__":
    logging.info("starting")
    study_launchingwithin()
