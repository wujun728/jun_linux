all:server client
server:server.c
	gcc -o server server.c
client:client.c
	gcc -o client client.c

.PHONY:clean run
clean:
	rm server
	rm client
	rm *.o
run:
	./server &
	./client
