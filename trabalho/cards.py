# cards.py - Baralho dinâmico de Magic: The Gathering

def obter_carta(jogador, nome):
    """ Retorna os atributos de uma carta pelo nome. """
    return jogador.cartas_dinamicas.get(nome, None)

def adicionar_carta_dinamica(jogador, nome, atributos):
    """ Adiciona uma carta criada dinamicamente ao dicionário. """
    jogador.cartas_dinamicas[nome] = atributos