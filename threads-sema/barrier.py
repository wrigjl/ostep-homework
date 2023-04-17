# This is a generalization of the rendezvous problem.
# The problem with the relatively easy solution to
# rendezvous is that if there are n threads, it
# doesn't work.
#
# What we're looking for here is that all N threads
# reach the rendezvous point before continuing on.
# The code will be tested up to 4 threads.

import threading
import time
import queue

# Right about here create your locking mechanism

maxthreads = 4


def init_locking_mechanism():
    """This function is called right before a test case is run"""

    # Note, it's fine by me if you use global variables to handle the
    # locking. Python's global stuff is weird though. TL;DR to be
    # able to see and modify values like maxthreads above, you need
    # to include a line like: "global maxthreads" at the top of the
    # function where you use it.
    pass


def thread_N(n, testcase, q, expecting):
    """The real workhorse. You need to modify this to include rendezvous support"""

    # n is the current thread's number (0-based)
    # testcase is the testcase number (determines where/if we sleep)
    # q - a queue used for reporting results
    # expecting: the number of threads we're expecting to rendezvous here.
    if testcase == 1:
        time.sleep(1)

    print(f"thread {n} start")
    q.put((n, "start", expecting))

    if testcase == 2:
        time.sleep(1)

    # XXX This is the rendezvous point

    if testcase == 3:
        time.sleep(1)

    print(f"thread {n} end")
    q.put((n, "end", expecting))

    if testcase == 4:
        time.sleep(1)


def main():
    # This creates some threads and expects for them to rendezvous.
    for nthreads in range(2, maxthreads + 1):
        for tc in range(maxthreads * 4):
            print(f"Test: threads={nthreads} case={tc}")
            q = queue.Queue(nthreads * 2)
            thds = []

            targetthd = tc // 4
            init_locking_mechanism()
            for i in range(nthreads):
                if i == targetthd:
                    testcase = tc % 4
                else:
                    testcase = -1

                t = threading.Thread(
                    target=thread_N, daemon=True, args=(i, testcase, q, nthreads)
                )
                thds.append(t)

            [t.start() for t in thds]

            # Wait for them to finish
            [t.join() for t in thds]
            assert q.full(), "Queue is not full"

            lst = []
            for i in range(nthreads * 2):
                lst.append(q.get())
                q.task_done()

            q.join()
            i = 0
            for l in lst:
                if i < nthreads:
                    assert l[1] == "start", f"bad ordering {lst}"
                else:
                    assert l[1] == "end", f"bad ordering {lst}"
                i += 1


if __name__ == "__main__":
    main()
