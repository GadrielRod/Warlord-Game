import os
import time

class UI:
    def __init__(self):
        self.DICE_MAP = {
            1: "⚀", 2: "⚁", 3: "⚂", 4: "⚃", 5: "⚄", 6: "⚅"
        }

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self):
        print("\n" + " – " * 20)
        print("   W A R L O R D :  A  T R I L H A  D O  G U E R R E I R O")
        print(" – " * 20)

    def choose_character(self):
        self.clear_screen()
        self.print_header()
        print("\n:: ESCOLHA SEU GUERREIRO ::")
        print("-" * 60)
        print("1. [Bartolomeu, Mão de Alface]")
        print("   > Vantagem Inicial: +1 DADO DE FÚRIA ")
        print("   > Lema: 'Eu vim aqui pra bater e comer pudim. E acabou o pudim.'")
        print("-" * 60)
        print("2. [Jaiminho, Corpo Mole]")
        print("   > Vantagem Inicial: +2 VIDA ")
        print("   > Lema: 'É que eu quero evitar a fadiga.'")
        print("-" * 60)
        print("3. [Gertrudes, Cobradora de Dívidas]")
        print("   > Vantagem Inicial: +2 GLÓRIA ")
        print("   > Lema: 'Ninguém escapa do vencimento do boleto.'")
        print("-" * 60)
        return input(">> Digite 1, 2 ou 3 para selecionar: ")

    def print_dice(self, dice_list):
        symbols = [f"[{self.DICE_MAP[d]}]" for d in dice_list]
        print(f"DADOS: {' '.join(symbols)}  >>> {dice_list}")

    def display_menu(self):
        self.print_header()
        print("\n:: MENU PRINCIPAL ::")
        print("1. [INICIAR BATALHA] (Jogar)")
        print("2. [PERGAMINHOS ANTIGOS] (Regras)")
        print("3. [BESTIÁRIO] (Inimigos & Itens)")
        print("4. [ABANDONAR] (Sair)")
        print("-" * 60)
        return input(">> Escolha uma opção: ")

    def display_rules(self):
        print(":: REGRAS DO GUERREIRO ::\n")
        rules = [
            "[OBJETIVO]: Derrotar o Senhor da Guerra. Se sua Vida cair a 0, você perde.",
            "",
            "[1. PREPARAR]: Role 5 dados.",
            "   - ⚅ (6): Cura Vida.",
            "   - ⚄ (5): Ganha 'Glória' para rerrolar todos os dados.",
            "   - Pares: Geram 'Fúria' (Dados extras de ataque).",
            "   - Converta dados em 'Foco' para rerrolar 1 dado específico.",
            "",
            "[2. DEFENDER]: Inimigos atacam baseados na distância da arma.",
            "   - 🏹 Arqueiros: Atacam de qualquer lugar.",
            "   - 🔱 Lanceiros: Atacam do meio ou perto.",
            "   - 🗡️ Espadachins: Só atacam de perto.",
            "",
            "[3. ATACAR]: Use dados + Fúria para cumprir o requisito da carta.",
            "   - Matar inimigo concede um ITEM (Max 3 no inventário)."
        ]
        for line in rules:
            print(line)
        input("\n[ENTER PARA VOLTAR]")
        self.clear_screen()

    def display_bestiary(self, deck):
        print(f"{'NOME':<20} | {'ARMA':<6} | {'REQUISITO':<20} | {'LOOT':<20}")
        print("-" * 80)
        for enemy in deck:
            icon = "🏹" if enemy.weapon_type == 'bow' else "🔱" if enemy.weapon_type == 'spear' else "🗡️"
            print(f"{enemy.name:<20} | {icon:<6} | {enemy.req_desc:<20} | {enemy.loot.name:<20}")
            print(f"   > Efeito: {enemy.loot.effect_desc}")
            print("-" * 80)
        input("\n[ENTER PARA VOLTAR]")
        self.clear_screen()

    def print_status(self, player):
        print(f"\nGUERREIRO: {player.name.upper()}")
        print(f"[❤️ VIDA: {player.health}/{player.max_health}]")
        print(f"[🏆 GLÓRIA: {player.glory}] [🧿 FOCO: {player.focus}] [🔥 FÚRIA: {player.fury}]")
        print("-" * 60)
        print("INVENTÁRIO:")
        if not player.inventory:
            print("  (Vazio)")
        else:
            for item in player.inventory:
                print(f"  > [{item.name}]: {item.effect_desc}")
        print("-" * 60)

    def print_enemies(self, active_enemies):
        print("\nCAMPO DE BATALHA:")
        positions = ["LONGE (0)", "MÉDIO (1)", "PERTO (2)"]
        
        for i, enemy in enumerate(active_enemies):
            will_attack = False
            if enemy.range_type == 'all': will_attack = True 
            elif enemy.range_type == 'far': will_attack = True 
            elif enemy.range_type == 'mid' and i >= 1: will_attack = True 
            elif enemy.range_type == 'near' and i == 2: will_attack = True 
            
            status_icon = " [⚔️ ATACANDO]" if will_attack else " [💤 ESPERA]"
            pos_label = positions[i] if i < 3 else "???"
            
            w_icon = "🏹" if enemy.weapon_type == 'bow' else "🔱" if enemy.weapon_type == 'spear' else "🗡️"
            
            print(f"  {i+1}. [{pos_label}] {w_icon} {enemy.name}{status_icon}")
            print(f"     ATK: {enemy.attack_power} | REQ: {enemy.req_desc}")

    def print_message(self, msg):
        print(f">> {msg}")

    def get_input(self, prompt):
        return input(f"{prompt} ")
