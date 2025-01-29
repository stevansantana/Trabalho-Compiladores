%{
#include <stdio.h>
#include "combo.tab.h"
%}

%%

COMBO           { return COMBO; }
name            { return NAME; }
colors          { return COLORS; }
cards           { return CARDS; }
strategy        { return STRATEGY; }
win_condition   { return WIN_CONDITION; }

"{"             { return LBRACE; }
"}"             { return RBRACE; }
":"             { return COLON; }
";"             { return SEMICOLON; }
","             { return COMMA; }

\"[^\"]+\"      { yylval.string = strdup(yytext); return STRING; }
[RUBGW]         { return MANA_SYMBOL; }

[ \t\n]         { /* Ignorar espaços e quebras de linha */ }
.               { printf("Token inválido: %s\\n", yytext); exit(1); }

%%
