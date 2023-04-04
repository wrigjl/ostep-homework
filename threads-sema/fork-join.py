# The goal of this assignment is to ensure that
# "child finish" always prints before "parent finish"


import threading
import time
import queue

# Right about here create your locking mechanism

# replace with semaphore creation/init
sem = None


def init_locking_mechanism():
    """This function is called right before a test case is run"""

    # Note, it's fine by me if you use global variables to handle the
    # locking. Python's global stuff is weird though. TL;DR to be
    # able to see and modify values like maxthreads above, you need
    # to include a line like: "global maxthreads" at the top of the
    # function where you use it.
    pass


def parent_thread(testcase, q):

    print("parent start")
    q.put(("parent", "start"))
    t = threading.Thread(target=child_thread, args=(testcase, q))

    if testcase == 1:
        time.sleep(1)

    t.start()

    if testcase == 2:
        time.sleep(1)

    # Use semphore here

    ### Leave these two lines alone, please
    q.put(("parent", "end"))
    t.join()


def child_thread(testcase, q):
    if testcase == 3:
        time.sleep(1)

    print("child start")
    q.put(("child", "start"))

    if testcase == 4:
        time.sleep(1)

    print("child end")
    q.put(("child", "end"))

    # use semaphore here

    if testcase == 5:
        time.sleep(1)


def main():
    for testcase in range(1, 5):
        init_locking_mechanism()
        q = queue.Queue(4)

        # Create and start the thread
        t = threading.Thread(target=parent_thread, daemon=True, args=(testcase, q))
        t.start()

        # Wait for it to finish
        t.join()

        # Check the results...
        assert q.full(), f"testcase{testcase}: Queue is not full"

        lst = []
        for i in range(4):
            lst.append(q.get())

        assert lst[0] == ("parent", "start"), f"bad order {lst}"
        assert lst[1] == ("child", "start"), f"bad order {lst}"
        assert lst[2] == ("child", "end"), f"bad order {lst}"
        assert lst[3] == ("parent", "end"), f"bad order {lst}"


if __name__ == "__main__":
    main()
