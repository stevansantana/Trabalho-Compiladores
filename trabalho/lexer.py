import ply.lex as lex

tokens = (
    'CARD_NAME',    # Nome da carta
    'MANA_COST',    # Custo de mana da carta
    'CARD_TYPE',    # Tipo da carta (Criatura, Feitiço, etc.)
    'CARD_TEXT',    # Texto da carta (habilidades ou efeitos)
    'POWER',        # Poder da criatura
    'TOUGHNESS',    # Resistência da criatura
)

# Variável de estado para controlar se o próximo número é POWER ou TOUGHNESS
next_number_is_power = True

def t_CARD_TYPE(t):
    r'(Criatura|Feitiço|Encantamento|Artefato|Planeswalker)'  # Tipos de carta
    return t

def t_CARD_NAME(t):
    r'[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ0-9\- ]*'  # Aceita letras acentuadas, números, hífens e espaços
    t.value = t.value.strip()  # Remove espaços extras, se houver
    return t

def t_MANA_COST(t):
    r'\{[0-9A-Za-z]+\}'  # Custo de mana no formato {1}, {U}, {G}{G}, etc.
    return t

def t_CARD_TEXT(t):
    r'"[^"]*"'  # Texto entre aspas
    return t

def t_NUMBER(t):
    r'-?\b[0-9]+\b'  # Agora aceita números negativos, como -1, -2, etc.
    global next_number_is_power

    if next_number_is_power:
        t.type = 'POWER'  # O primeiro número é POWER
        next_number_is_power = False  # O próximo número será TOUGHNESS
    else:
        t.type = 'TOUGHNESS'  # O segundo número é TOUGHNESS
        next_number_is_power = True  # Reseta para o próximo par POWER/TOUGHNESS

    return t

# Ignorar espaços e tabulações
t_ignore = ' \t\n'

# Tratamento de erro (se houver caractere inválido)
def t_error(t):
    print(f"Caractere inválido '{t.value[0]}' na posição {t.lexpos}")
    t.lexer.skip(1)

lexer = lex.lex()


