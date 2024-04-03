
#include <iostream>
#include <thread>
#include <semaphore>
#include <chrono>
#include <vector>
#include <mutex>
#include <cassert>

class MyBlock {
    private:    
        // a pointer to your semaphore. Note: it has to be a pointer
        // because you cannot move- or copy-construct a semaphore.
        std::counting_semaphore<1> *sem;
    public:

        MyBlock(const MyBlock &) = delete; // no copies allowed

        // These are the functions you need to implement
        MyBlock();
        ~MyBlock();
        void block();
        void unblock();
};

// create a new "block" (you need to "new" a counting semaphone)
MyBlock::MyBlock() {
}

// destroy a block (you need to delete anything you new'd)
MyBlock::~MyBlock() {
}

// Block this thread until "unblock" is called using your
// semaphore
void MyBlock::block() {
}

// Make it so that a thread can move forward using your
// semaphore
void MyBlock::unblock() {
}

//========================================================================

// everything below this line is test code. Correct implementation of
// MyBlock will produce no assertion errors. It takes about 6 seconds to
// run to completion.

std::mutex eventQueueLock;
std::vector<std::string> eventQueue;

// initialize semaphore

void insertEvent(std::string event) {
    // This is kinda neat. Construction of this object locks the mutex, and
    // destruction unlocks it. Therefore it's impossible to forget one of the
    // operations.
    const std::lock_guard<std::mutex> lock(eventQueueLock);

    eventQueue.push_back(event);
}

void child(MyBlock *b, int testnumber) {
    using namespace std::chrono_literals;

    if (testnumber == 3)
        std::this_thread::sleep_for(1s);

    insertEvent("child start");

    if (testnumber == 4)
        std::this_thread::sleep_for(1s);

    insertEvent("child end");

    b->unblock();

    if (testnumber == 5)
        std::this_thread::sleep_for(1s);
}

void parent(int testnumber) {
    MyBlock b;

    insertEvent("parent start");

    auto t = std::thread(child, &b, testnumber);

    using namespace std::chrono_literals;
    std::this_thread::sleep_for(1s);

    b.block();

    insertEvent("parent end");
    t.join();
}

int main(int argc, char *argv[]) {
    for (int testcase = 0; testcase < 6; testcase++) {
        std::cout << "Test case: " << testcase << std::endl;
        eventQueue.clear();
        auto t = std::thread(parent, testcase);
        t.join();
        assert(eventQueue.size() == 4);
        assert(eventQueue[0] == "parent start");
        assert(eventQueue[1] == "child start");
        assert(eventQueue[2] == "child end");
        assert(eventQueue[3] == "parent end");
    }
    return 0;
}

