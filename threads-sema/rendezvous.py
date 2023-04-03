# The goal of this assignment is to ensure that BOTH
# of the start messages appear before EITHER of the
# end messages, no matter the ordering of the statements.
# Valid orderings are:
#   A-start, B-start, A-end, B-end
#   A-start, B-start, B-end, A-end
#   B-start, A-start, A-end, B-end
#   B-start, A-start, B-end, A-end

# The testcases ensure different scheduling at key
# points within each thread (don't modify)
#
# Success means passing all of the testcases (8).

import threading
import time
import queue

# Right about here create your locking mechanism


def init_locking_mechanism():
    """This function is called right before a test case is run"""

    # Note, it's fine by me if you use global variables to handle the
    # locking. Python's global stuff is weird though. TL;DR to be
    # able to see and modify values like maxthreads above, you need
    # to include a line like: "global maxthreads" at the top of the
    # function where you use it.
    pass


def thread_a(testcase, q):
    if testcase == 1:
        time.sleep(1)

    print("thread A start")
    q.put(0)

    if testcase == 2:
        time.sleep(1)

    # XXX This is the rendezvous point

    if testcase == 3:
        time.sleep(1)

    print("thread A end")
    q.put(1)

    if testcase == 4:
        time.sleep(1)


def thread_b(testcase, q):
    if testcase == 5:
        time.sleep(1)

    print("thread B start")
    q.put(2)

    if testcase == 6:
        time.sleep(1)

    ## XXX This is the rendezvous point

    if testcase == 7:
        time.sleep(1)

    print("thread B end")
    q.put(3)

    if testcase == 8:
        time.sleep(1)


def main():
    for testcase in range(1, 9):
        init_locking_mechanism()
        q = queue.Queue(4)

        # Create and start the threads
        ta = threading.Thread(target=thread_a, daemon=True, args=(testcase, q))
        tb = threading.Thread(target=thread_b, daemon=True, args=(testcase, q))
        [t.start() for t in [ta, tb]]

        # Wait for them to finish
        [t.join() for t in [ta, tb]]

        # Check the results...
        assert q.full(), f"testcase{testcase}: Queue is not full"

        lst = []
        for i in range(4):
            lst.append(q.get())

        assert (lst[0] == 0 and lst[1] == 2) or (
            lst[0] == 2 or lst[1] == 0
        ), f"testcase{testcase} start messages out of order: {lst}"
        assert (lst[2] == 1 and lst[3] == 3) or (
            lst[2] == 3 or lst[3] == 1
        ), f"testcase{testcase} end messages out of order: {lst}"


if __name__ == "__main__":
    main()
