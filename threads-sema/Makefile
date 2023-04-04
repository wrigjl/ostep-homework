ALL=barrier rendezvous fork-join mutex-nostarve reader-writer reader-writer-nostarve


CFLAGS=-g -pthread -Wall -O

all: $(ALL)

rendezvous: rendezvous.c common_threads.h
	$(CC) -o $@ $< $(CFLAGS)

barrier: barrier.c common_threads.h
	$(CC) -o $@ $< $(CFLAGS)

fork-join: fork-join.c
	$(CC) -o $@ $< $(CFLAGS)

mutex-nostarve: mutex-nostarve.c common_threads.h
	$(CC) -o $@ $< $(CFLAGS)

reader-writer: reader-writer.c common_threads.h
	$(CC) -o $@ $< $(CFLAGS)

reader-writer-nostarve: reader-writer-nostarve.c common_threads.h
	$(CC) -o $@ $< $(CFLAGS)

clean:
	rm -f $(ALL)
