#include <chrono>
#include <iostream>
#include <semaphore>
#include <thread>
#include <cassert>
#include <sstream>

#define assertm(exp, msg) assert(((void)msg, exp))

// If done correctly, each child should print their "before" message
// before either prints their "after" message. Test by adding sleep(1)
// calls in various locations.

// You likely need two semaphores to do this correctly, and some
// other integers to track things.

class Barrier {
private:
    // add semaphores and other information here
public:
    Barrier(int n);

    // no default constructor, no copy constructor
    Barrier() = delete;
    Barrier(const Barrier&) = delete;

    void wait();
};


// the single barrier we are using for this program
Barrier *b;

// Initialization stuff goes here
Barrier::Barrier(int num_threads) {
}

void Barrier::wait() {
    // barrier code goes here
}

//
// XXX: don't change below here (just run it!)
//

void child(int id) {
    std::stringstream ss;

    ss << "child " << id << ": before" << std::endl;
    std::cout << ss.str();
    using namespace std::literals;
    if (id != 0)
        std::this_thread::sleep_for(std::chrono::milliseconds(10 + id));
    b->wait();
    ss << "child " << id << ": after" << std::endl;
    std::cout << ss.str();
}


// run with a single argument indicating the number of 
// threads you wish to create (1 or more)
int main(int argc, char *argv[]) {
    assertm(argc == 2, "requires exactly one argument: number of theads");
    int num_threads = atoi(argv[1]);
    assertm(num_threads > 0, "nthreads must be > 0");

    std::thread *p[num_threads];

    printf("parent: begin\n");
    b = new Barrier(num_threads);
    
    int i;
    for (i = 0; i < num_threads; i++) {
        p[i] = new std::thread(child, i);
    }

    for (i = 0; i < num_threads; i++) {
        p[i]->join();
        delete p[i];
        p[i] = nullptr;
    }

    printf("parent: end\n");
    return 0;
}

