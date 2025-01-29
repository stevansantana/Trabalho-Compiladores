all:
	flex combo.l
	bison -d combo.y
	gcc -o combo combo.tab.c lex.yy.c main.c -lfl

clean:
	rm -f combo combo.tab.c combo.tab.h lex.yy.c
