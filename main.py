from player import Player
from ui import UI
from enemies import create_deck
from engine import GameEngine

def main():
    ui = UI()
    
    while True:
        option = ui.display_menu()
        
        if option == '1':
            # --- SELEÇÃO DE PERSONAGEM ---
            char_choice = ui.choose_character()
            
            player_name = "Guerreiro Anônimo"
            start_fury = 0
            start_glory = 0
            start_health = 0
            
            if char_choice == '1':
                player_name = "Bartolomeu, o 'Mão de Alface'"
                start_fury = 1 # Bônus da Isabelle (Mutineer)
                ui.print_message("Você escolheu BARTOLOMEU! Começa com +1 Fúria.")
            elif char_choice == '2':
                player_name = "Jaiminho, 'Corpo Mole'"
                start_health = 10
                ui.print_message("Você escolheu JAIMINHO! Começa com +2 de vida.")
            else:
                player_name = "Gertrudes, a 'Cobradora de Dívidas'"
                start_glory = 2 # Bônus do Toussaint (Mutineer)
                ui.print_message("Você escolheu GERTRUDES! Começa com +2 Glória.")
            
            input("[ENTER] Para iniciar a jornada...")

            # Inicializa jogador com os bônus
            player = Player(name=player_name)
            player.fury += start_fury
            player.glory += start_glory
            player.health += start_health
            
            deck = create_deck()
            engine = GameEngine(player, deck, ui)
            engine.start()
            
            input("\n>> Pressione ENTER para voltar ao menu...")
            
        elif option == '2':
            ui.display_rules()
            
        elif option == '3':
            temp_deck = create_deck()
            ui.display_bestiary(temp_deck)
            
        elif option == '4':
            ui.print_message("Saindo do campo de batalha...")
            break
            
        else:
            ui.print_message("Opção inválida.")
            input(">> [ENTER]")

if __name__ == "__main__":
    main()
