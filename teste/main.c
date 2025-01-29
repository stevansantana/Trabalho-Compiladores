#include <stdio.h>
#include "combo.h"

extern int yyparse();
extern FILE *yyin;

int main(int argc, char **argv) {
  if (argc > 1) {
    yyin = fopen(argv[1], "r");
    if (!yyin) {
      perror("Erro ao abrir arquivo");
      return 1;
    }
  }

  yyparse();
  return 0;
}
