import ply.yacc as yacc
from lexer import tokens  # Importando os tokens do lexer.py
import semantic
import os

# Regra principal: define uma carta
def p_card(p):
    '''card : CARD_NAME mana_cost CARD_TYPE CARD_TEXT
            | CARD_NAME mana_cost CARD_TYPE CARD_TEXT creature_stats'''  # Apenas criaturas têm poder e resistência

    if p[3] == "Criatura" and len(p) == 6:
        p[0] = {
            "Nome": p[1],
            "Custo de Mana": p[2],
            "Tipo": p[3],
            "Texto": p[4],
            "Poder": p[5]["Poder"],
            "Resistência": p[5]["Resistência"]
        }
    else:
        p[0] = {
            "Nome": p[1],
            "Custo de Mana": p[2],
            "Tipo": p[3],
            "Texto": p[4]
        }

# Regra para capturar múltiplos custos de mana
def p_mana_cost(p):
    '''mana_cost : MANA_COST
                 | mana_cost MANA_COST'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

# Regra para Criaturas (POWER e TOUGHNESS)
def p_creature_stats(p):
    '''creature_stats : POWER TOUGHNESS'''
    p[0] = {"Poder": p[1], "Resistência": p[2]}

# Regra de erro para detectar problemas de sintaxe
def p_error(p):
    if p:
        limpar_tela()
        print(f"Erro de sintaxe próximo a '{p.value}' na posição {p.lexpos}")
        pausar()
    else:
        print("Erro de sintaxe: fim inesperado")
        pausar()
        limpar_tela()

# Criando o parser
parser = yacc.yacc()

def limpar_tela():
        """Limpa a tela do terminal."""
        os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    """Pausa o programa até o usuário pressionar Enter."""
    input("\nPressione Enter para continuar...")