%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "combo.h"

void yyerror(const char *s);
int yylex();
%}

%union {
  char* string;
}

%token COMBO NAME COLORS CARDS STRATEGY WIN_CONDITION
%token <string> STRING
%token LBRACE RBRACE COLON SEMICOLON COMMA MANA_SYMBOL

%%

program:
  combos
;

combos:
  combo
  | combos combo
;

combo:
  COMBO LBRACE combo_body RBRACE { printf("Combo válido!\\n\n"); }
;

combo_body:
  NAME COLON STRING SEMICOLON {
    printf("Nome do Combo: %s\n", $3);
  }
  COLORS COLON LBRACE color_list RBRACE SEMICOLON {
    printf("Cores do Combo: ");
  }
  CARDS COLON LBRACE card_list RBRACE SEMICOLON {
    printf("Cartas do Combo: ");
  }
  STRATEGY COLON STRING SEMICOLON {
    printf("Estratégia: %s\n", $3);
  }
  WIN_CONDITION COLON STRING SEMICOLON {
    printf("Condição de Vitória: %s\n", $3);
  }
;


color_list:
  MANA_SYMBOL
  | color_list COMMA MANA_SYMBOL
;

card_list:
  STRING
  | card_list COMMA STRING
;

%%

void yyerror(const char *s) {
  fprintf(stderr, "Erro: %s\\n", s);
}
