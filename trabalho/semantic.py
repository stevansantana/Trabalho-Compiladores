import os

# semantic.py - Analisador Semântico para Magic: The Gathering

# Lista de símbolos de mana válidos
MANA_SYMBOLS = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "W", "U", "B", "R", "G", "X"}

def validar_carta(carta):
    """ Verifica se a carta é válida conforme as regras semânticas. """

    # Verifica se o custo de mana é válido
    for custo in carta["Custo de Mana"]:
        if not (custo.startswith("{") and custo.endswith("}")):
            print(f"Erro semântico: O custo de mana '{custo}' da carta '{carta['Nome']}' está mal formatado.")
            return False

        simbolo = custo[1:-1]  # Remove as chaves { }
        if simbolo not in MANA_SYMBOLS:
            print(f"Erro semântico: O símbolo de mana '{simbolo}' da carta '{carta['Nome']}' não é válido.")
            return False

    # Se a carta for uma criatura, ela deve ter Poder e Resistência
    if carta["Tipo"] == "Criatura":
        if "Poder" not in carta or "Resistência" not in carta:
            print(f"❌ Erro semântico: A criatura '{carta['Nome']}' deve ter Poder e Resistência.")
            return False
        if int(carta["Poder"]) < 0 or int(carta["Resistência"]) < 0:
            print(f"❌ Erro semântico: A criatura '{carta['Nome']}' tem valores negativos de Poder ou Resistência.")
            return False

    limpar_tela()
    print(f"Carta '{carta['Nome']}' validada com sucesso!")
    return True

def validar_combo(carta1, carta2):
    """ Verifica se as duas cartas formam um combo válido. """
    # Combo Maldição da Morte + Peste
    if (carta1["Nome"] == "Maldição da Morte" and carta2["Nome"] == "Peste") or \
       (carta1["Nome"] == "Peste" and carta2["Nome"] == "Maldição da Morte"):
        return "Maldição da Morte + Peste"
    
    # Combo City on Fire + Peste
    if (carta1["Nome"] == "City on Fire" and carta2["Nome"] == "Peste") or \
       (carta1["Nome"] == "Peste" and carta2["Nome"] == "City on Fire"):
        return "City on Fire + Peste"
    
    return None


def limpar_tela():
        """Limpa a tela do terminal."""
        os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    """Pausa o programa até o usuário pressionar Enter."""
    input("\nPressione Enter para continuar...")