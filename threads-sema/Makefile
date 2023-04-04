ALL=barrier rendezvous


CFLAGS=-g -pthread -Wall -O

all: $(ALL)


rendezvous: rendezvous.c
	$(CC) -o $@ $< $(CFLAGS)

barrier: barrier.c
	$(CC) -o $@ $< $(CFLAGS)

clean:
	rm -f $(ALL)
