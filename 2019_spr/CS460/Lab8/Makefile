
all:	magic8d magic8

magic8d:	magic8d.c
	gcc -g -m32 -fno-stack-protector -z execstack -o magic8d magic8d.c

magic8:	magic8.c
	gcc -m32 -fno-stack-protector -z execstack -o magic8 magic8.c

clean:
	rm -f *.o magic8d magic8 testsc eggshell
