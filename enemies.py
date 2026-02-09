import random

class Loot:
    def __init__(self, name, effect_desc, passive=True):
        self.name = name
        self.effect_desc = effect_desc
        self.passive = passive

class Enemy:
    def __init__(self, name, weapon_type, attack_power, req_type, req_val, req_desc, loot):
        self.name = name
        self.weapon_type = weapon_type # 'bow', 'spear', 'sword', 'boss'
        self.attack_power = attack_power
        self.req_type = req_type 
        self.req_val = req_val
        self.req_desc = req_desc 
        self.loot = loot 

    @property
    def range_type(self):
        # Converte arma para alcance
        if self.weapon_type == 'bow': return 'far'    # Ataca de 0, 1, 2
        if self.weapon_type == 'spear': return 'mid'  # Ataca de 1, 2
        if self.weapon_type == 'sword': return 'near' # Ataca de 2
        if self.weapon_type == 'boss': return 'all'
        return 'near'

def create_deck():
    deck = []
    
    # --- INIMIGOS COMUNS ---
    deck.append(Enemy("Besteiro Real", "bow", 2, "sum", 20, "Soma >= 20", 
                      Loot("Aljava Sem Fim", "Custo de Glória para rerrolar reduzido em 1")))
    
    deck.append(Enemy("Carrasco", "sword", 4, "full_house", 0, "Full House (AA-BBB)", 
                      Loot("Machado de Verdugo", "+1 no valor de um dado (Custa 1 Vida)")))
                      
    deck.append(Enemy("Caçador Élfico", "bow", 2, "kind", 4, "Quadra (AAAA)", 
                      Loot("Capa de Esquiva", "Chance de esquivar ataque (Rerrolar defesa)")))
                      
    deck.append(Enemy("Guarda do Portão", "spear", 3, "straight", 0, "Sequência (1-2-3-4-5)", 
                      Loot("Escudo de Torre", "Bloqueia totalmente 1 Ataque (Quebra ao usar)")))
                      
    deck.append(Enemy("Bárbaro do Norte", "sword", 4, "mixed_pairs", 2, "Dois Pares (AA-BB)", 
                      Loot("Talismã da Fênix", "Renasce c/ 1 Vida ao morrer (Quebra ao usar)")))
                      
    deck.append(Enemy("Cavaleiro Negro", "spear", 3, "kind", 3, "Trinca (AAA)", 
                      Loot("Armadura de Placas", "Reduz dano de Lanças em 1")))
                      
    deck.append(Enemy("Ninja das Sombras", "sword", 2, "sum", 28, "Soma >= 28", 
                      Loot("Bomba de Fumaça", "Troca Posição de Inimigos (Grátis)")))
                      
    deck.append(Enemy("General de Guerra", "bow", 3, "mixed_pairs", 3, "3 Pares (AA-BB-CC)", 
                      Loot("Estandarte de Guerra", "Começa turno com +1 Foco (Rerrolar 1)")))

    deck.append(Enemy("Monge Renegado", "sword", 3, "all_odd", 0, "Todos Ímpares", 
                      Loot("Ervas Medicinais", "Cura custa 5 dados (invés de 6)")))
                      
    deck.append(Enemy("Mestre de Cerco", "spear", 3, "all_even", 0, "Todos Pares", 
                      Loot("Engrenagem Mestra", "Altera dado +/- 1 (Custa 1 Vida)")))
                      
    deck.append(Enemy("Feiticeiro", "bow", 2, "exact_sum", 21, "Soma Exata 21", 
                      Loot("Amuleto de Proteção", "Imune a ataques de Longe se tiver Glória")))
                      
    deck.append(Enemy("Gigante da Montanha", "sword", 5, "kind", 5, "Quina (AAAAA)", 
                      Loot("Manopla de Força", "Pares geram +1 Fúria extra")))
    
    # Embaralha os inimigos comuns PRIMEIRO
    random.shuffle(deck)

    # --- BOSS (Sempre por último) ---
    boss = Enemy("O SENHOR DA GUERRA", "boss", 6, "boss_special", 0, "Trinca(6) + Trinca(1)", 
                 Loot("A Coroa do Rei", "Troféu Final"))
    
    deck.append(boss)

    return deck
