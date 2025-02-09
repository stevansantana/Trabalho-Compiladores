# game.py - Sistema básico de jogo para Magic: The Gathering com turnos

import cards
import os
from lexer import lexer
from parser import parser
from cards import adicionar_carta_dinamica, obter_carta
import semantic  

class Jogador:
    def __init__(self, nome):
        self.nome = nome
        self.vida = 20
        self.mana = 100
        self.baralho = [] 
        self.mao = []
        self.campo = []
        self.cartas_dinamicas = {}
    
    def comprar_carta(jogador):
        """ Compra uma carta do baralho e coloca na mão """
        if jogador.baralho:
            carta = jogador.baralho.pop()
            jogador.mao.append(carta)
            limpar_tela()
            print(f"{jogador.nome} comprou a carta: {carta}")
            pausar()
            limpar_tela()
        else:
            print(f"{jogador.nome} não tem mais cartas no baralho!")

    def jogar_carta(jogador, oponente):
        if not jogador.mao:
            print(f"{jogador.nome} não tem cartas na mão para jogar!")
            return

        print(f"\n{jogador.nome}, escolha uma carta para jogar no campo:\n")
        for i, carta in enumerate(jogador.mao):
            detalhes = obter_carta(jogador, carta)  # Busca no contexto do jogador
            if detalhes:
                custo_mana = detalhes.get("Custo de Mana", [])
                print(f"{i + 1} - {carta} (Custo: {', '.join(custo_mana)})")

        escolha = int(input("Digite o número da carta: ")) - 1

        if 0 <= escolha < len(jogador.mao):
            carta_escolhida = jogador.mao[escolha]
            detalhes = obter_carta(jogador, carta_escolhida)  # Busca no contexto do jogador

            if not detalhes:
                print("Erro: Detalhes da carta não encontrados!")
                return

            custo_mana = detalhes.get("Custo de Mana", [])

            # Verifica se o jogador tem mana suficiente
            if len(custo_mana) <= jogador.mana:
                jogador.mana -= len(custo_mana)  # Gasta a mana
                jogador.mao.pop(escolha)
                jogador.campo.append(carta_escolhida)
                limpar_tela()
                print(f"{jogador.nome} jogou {carta_escolhida} no campo!")

                # Verifica se há combos ativos
                if len(jogador.campo) >= 2:
                    carta1 = obter_carta(jogador, jogador.campo[-1])
                    carta2 = obter_carta(jogador, jogador.campo[-2])
                    combo = semantic.validar_combo(carta1, carta2)

                    if combo == "Maldição da Morte + Peste":
                        print("Combo 'Maldição da Morte + Peste' ativado! O dano de Peste é amplificado.")
                        dano = 4  # Dano amplificado (2 de Peste + 2 de Maldição da Morte)
                        oponente.vida -= dano
                        print(f"{oponente.nome} perdeu {dano} pontos de vida! Vida restante: {oponente.vida}")

                    elif combo == "City on Fire + Peste":
                        print("Combo 'City on Fire + Peste' ativado! O dano de Peste é triplicado.")
                        dano = 6  # Dano triplicado (2 de Peste * 3)
                        oponente.vida -= dano
                        print(f"{oponente.nome} perdeu {dano} pontos de vida! Vida restante: {oponente.vida}")
            else:
                print("Mana insuficiente para jogar esta carta.")
        else:
            print("Escolha inválida.")



    def atacar(jogador, oponente):
        if not jogador.campo:
            print(f"{jogador.nome} não tem criaturas no campo para atacar!")
            return

        print(f"{jogador.nome} está atacando {oponente.nome}!\n")
        print("Escolha as criaturas que vão atacar:")
        for i, carta in enumerate(jogador.campo):
            detalhes = cards.obter_carta(jogador, carta)
            if detalhes["Tipo"] == "Criatura":
                print(f"{i + 1} - {carta} (Poder: {detalhes['Poder']})")

        atacantes = input("\nDigite os números das criaturas (separados por vírgula): ").split(",")
        atacantes = [int(a) - 1 for a in atacantes]
        limpar_tela()

        dano_total = 0
        for i in atacantes:
            if 0 <= i < len(jogador.campo):
                carta = jogador.campo[i]
                detalhes = cards.obter_carta(jogador, carta)
                if detalhes["Tipo"] == "Criatura":
                    dano_total += int(detalhes["Poder"])

        oponente.vida -= dano_total
        print(f"{oponente.nome} recebeu {dano_total} de dano! Vida restante: {oponente.vida}")

    def mostrar_estado(self):
        """ Mostra o estado atual do jogador """
        print(f"\n--- {self.nome} ---")
        print(f"Vida: {self.vida}")
        print(f"Mão: {self.mao}")
        print(f"Campo: {self.campo}")
        print("-------------------\n")

def criar_carta(jogador):
    print(f"\n🔹 {jogador.nome}, crie uma carta! 🔹\n")
    print("Siga este formato ao descrever sua carta:\n")
    print("1. Nome da Carta: O nome da carta (ex.: Dragão Azul)")
    print("2. Custo de Mana: Insira o custo de mana entre chaves, ex.: {2}{U}")
    print("3. Tipo da Carta: Escolha entre Criatura, Feitiço, Encantamento, etc.")
    print('4. Texto da Carta: Insira as habilidades ou efeitos entre aspas (ex.: "Voar").')
    print("5. Poder e Resistência: Para criaturas, insira os valores de poder e resistência.\n")
    print("Exemplos de entrada:\n")
    print("Para criaturas: Dragão Azul {2}{U} Criatura \"Voar\" 4 4")
    print("Para encantamentos: Peste {1}{B} Feitiço \"Causa 2 pontos de dano ao oponente\".\n")

    descricao = input("Digite a descrição da carta: ")

    # Análise léxica
    lexer.input(descricao)
    tokens = list(lexer)
    if not tokens:
        print("Erro: Descrição inválida. Não foi possível criar a carta.")
        return

    # Análise sintática
    carta = parser.parse(descricao, lexer=lexer)
    if not carta:
        print("Erro: Descrição inválida. Não foi possível criar a carta.")
        return

    # Análise semântica
    if not semantic.validar_carta(carta):
        limpar_tela()
        print("Erro: A carta não é válida semanticamente.")
        pausar()
        return

    pausar()
    limpar_tela()    
    jogador.baralho.append(carta["Nome"])
    adicionar_carta_dinamica(jogador, carta["Nome"], carta)  # Adiciona ao dicionário do jogador
    print(f"Carta '{carta['Nome']}' criada e adicionada ao baralho de {jogador.nome}!")
    pausar()
    limpar_tela()
    
def iniciar_turno(jogador):
        jogador.mana += 1  # Ganha 1 mana por turno
        print(f"{jogador.nome} ganhou 1 mana. Mana total: {jogador.mana}")    

def limpar_tela():
        """Limpa a tela do terminal."""
        os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    """Pausa o programa até o usuário pressionar Enter."""
    input("\nPressione Enter para continuar...")

def inicializar_jogo(jogador1, jogador2):
    print("🔹 Bem-vindo ao jogo simplficado de Magic The Gathering! 🔹\n")
    print("Cada jogador deve criar 3 cartas para começar.")
    pausar()
    limpar_tela()

    for jogador in [jogador1, jogador2]:
        print(f"{jogador.nome}, crie suas cartas:")
        for _ in range(3):  # Cada jogador cria um número cartas
            criar_carta(jogador)


# Função principal do jogo
def jogo():
    jogador1 = Jogador("Jogador 1")
    jogador2 = Jogador("Jogador 2")
    jogadores = [jogador1, jogador2]

    # Inicializa o jogo com cartas criadas pelos jogadores
    inicializar_jogo(jogador1, jogador2)

    turno = 0

    while jogador1.vida > 0 and jogador2.vida > 0:
        jogador_atual = jogadores[turno % 2]
        oponente = jogadores[(turno + 1) % 2]

        limpar_tela()
        print(f"\n🔹 {jogador_atual.nome}, faça sua jogada:\n")
        print("1 - Comprar uma carta")
        print("2 - Jogar uma carta no campo")
        print("3 - Atacar")
        print("4 - Criar uma carta")  
        escolha = input("\nEscolha uma ação: ")

        limpar_tela()

        if escolha == "1":
            jogador_atual.comprar_carta()
        elif escolha == "2":
            jogador_atual.jogar_carta(oponente)
        elif escolha == "3":
            jogador_atual.atacar(oponente)
        elif escolha == "4": 
            criar_carta(jogador_atual)
        else:
            print("Escolha inválida. Perdeu a vez!")
            pausar()
            limpar_tela()

        print(f"\nFim do turno de {jogador_atual.nome}.")
        pausar()

        turno += 1

    vencedor = jogador1 if jogador1.vida > 0 else jogador2
    limpar_tela()
    print(f"\n🎉 {vencedor.nome} venceu o jogo!")

if __name__ == "__main__":
    jogo()
