all:server.o client.o common.o
	gcc -o server server.o common.o
	gcc -o client client.o common.o
server.o:server.c
	gcc -c server.c
client.o:client.c
	gcc -c client.c
common.o:common.c
	gcc -c common.c
clean:
	rm *.o
	rm server
	rm client
