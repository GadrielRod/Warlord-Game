import random
from dice import DiceSystem
from collections import Counter

class GameEngine:
    def __init__(self, player, deck, ui):
        self.player = player
        self.deck = deck
        self.ui = ui
        self.active_enemies = []
        # O deck já vem embaralhado do enemies.py com o boss no final

    def start(self):
        self.ui.clear_screen()
        self.ui.print_header()
        
        while self.player.health > 0:
            # Vitória: Só ganha se deck vazio E sem inimigos ativos
            if not self.deck and not self.active_enemies:
                self.ui.print_message("\n=== VITÓRIA LENDÁRIA! VOCÊ SE TORNOU O SENHOR DA GUERRA ===")
                break 
            
            # Spawn de inimigos
            while len(self.active_enemies) < 3 and self.deck:
                self.active_enemies.append(self.deck.pop(0))

            self.ui.print_status(self.player)
            self.ui.print_enemies(self.active_enemies)

            # --- LÓGICA DE MORTE SÚBITA ---
            # Se não tem mais cartas no baralho e só resta 1 inimigo (o Boss ou o último),
            # Pula a fase de preparação.
            is_sudden_death = (not self.deck and len(self.active_enemies) == 1)

            if not is_sudden_death:
                self.phase_prepare()
            else:
                self.ui.print_message("\n!!! MORTE SÚBITA: SEM FASE DE PREPARAÇÃO !!!")
                self.ui.print_message("Recursos esgotados. É matar ou morrer.")
            
            if self.player.health > 0:
                self.phase_defend()
            
            if self.player.health > 0:
                self.phase_attack()

            if self.player.health <= 0:
                self.ui.print_message("\n=== VOCÊ CAIU EM COMBATE. FIM DE JOGO. ===")
                break 

    def phase_prepare(self):
        self.ui.print_message("\n--- FASE 1: PREPARAR (Recursos) ---")
        input("[ENTER] Para rolar dados...")
        
        # Item: Estandarte
        if self.player.has_item("Estandarte"):
             self.player.focus += 1
             self.ui.print_message("Estandarte de Guerra gerou +1 Foco.")

        dice = DiceSystem.roll(5)
        self.ui.print_dice(dice)
        
        # Lógica de conversão de FOCO (mantida igual)
        self.ui.print_message("Digite índices dos dados para virar FOCO (ex: '1 3') ou ENTER para pular.")
        
        chosen_indices = []
        valid_input = False
        while not valid_input:
            sel = self.ui.get_input("Escolha: ")
            if not sel.strip():
                valid_input = True
            else:
                try:
                    chosen_indices = [int(x)-1 for x in sel.split()]
                    valid_input = True
                except ValueError:
                    self.ui.print_message("Entrada inválida.")

        remaining_dice = []
        focus_gain = 0
        
        for i, val in enumerate(dice):
            if i in chosen_indices:
                self.player.focus += 1
                focus_gain += 1
            else:
                remaining_dice.append(val)
                
        if focus_gain > 0:
            self.ui.print_message(f"Gerou {focus_gain} de Foco.")
        
        # --- CÁLCULOS ATUALIZADOS ---
        
        # 1. VIDA (Dados 6)
        sixes = [d for d in remaining_dice if d == 6]
        heal_amount = len(sixes) # 1 de vida por dado 6
        
        # [NOVO] Item: Ervas Medicinais (+1 vida por dado 6)
        if self.player.has_item("Ervas") and heal_amount > 0:
            heal_amount += len(sixes) # Dobra a cura basicamente (1 base + 1 extra)
            self.ui.print_message("Ervas Medicinais potencilizaram a cura!")

        if heal_amount > 0:
            self.player.health = min(self.player.max_health, self.player.health + heal_amount)
            self.ui.print_message(f"Recuperou {heal_amount} Vida.")
        
        # 2. GLÓRIA (Dados 5)
        fives = [d for d in remaining_dice if d == 5]
        glory_gain = len(fives)
        
        # [NOVO] Item: Engrenagem Mestra (+1 Glória por dado 5)
        if self.player.has_item("Engrenagem") and glory_gain > 0:
            glory_gain += len(fives)
            self.ui.print_message("Engrenagem Mestra gerou Glória extra!")

        self.player.glory += glory_gain
        if glory_gain > 0: self.ui.print_message(f"Ganhou {glory_gain} Glória.")
        
        # 3. FÚRIA (Pares de 1, 2, 3, 4)
        others = [d for d in remaining_dice if d < 5]
        counts = Counter(others)
        fury_gain = 0
        for k, v in counts.items():
            fury_gain += v // 2
        
        # Item: Manopla de Força
        if fury_gain > 0 and self.player.has_item("Manopla"):
            fury_gain += 1
            self.ui.print_message("Manopla aumentou sua Fúria.")

        # [NOVO] Item: Machado de Verdugo (+1 Fúria fixo)
        if self.player.has_item("Machado"):
            fury_gain += 1
            self.ui.print_message("Machado de Verdugo gerou +1 Fúria extra.")

        self.player.fury += fury_gain
        if fury_gain > 0: self.ui.print_message(f"Gerou {fury_gain} de Fúria.")

    def phase_defend(self):
        self.ui.print_message("\n--- FASE 2: DEFENDER ---")
        
        # [NOVO] Item: Bomba de Fumaça (Consumível)
        smoke_bomb = self.player.has_item("Bomba de Fumaça")
        if smoke_bomb:
            if self.ui.get_input("Usar Bomba de Fumaça para evitar TODOS ataques? (s/n): ").lower() == 's':
                self.ui.print_message("PUFF! Você desapareceu na fumaça. Nenhum dano sofrido.")
                self.player.inventory.remove(smoke_bomb)
                return # Pula a fase de defesa inteira

        for i, enemy in enumerate(self.active_enemies):
            can_hit = False
            if enemy.range_type == 'all': can_hit = True
            elif enemy.range_type == 'far': can_hit = True 
            elif enemy.range_type == 'mid' and i >= 1: can_hit = True
            elif enemy.range_type == 'near' and i == 2: can_hit = True
            
            # Item: Amuleto (Bloqueia Longe se tiver Glória)
            if enemy.range_type == 'far' and self.player.has_item("Amuleto") and self.player.glory > 0:
                self.ui.print_message("Amuleto protegeu contra ataque à distância.")
                can_hit = False

            if can_hit:
                self.ui.print_message(f"{enemy.name} ataca!")
                atk_dice = DiceSystem.roll(enemy.attack_power)
                
                # Item: Capa de Esquiva
                if self.player.has_item("Capa"):
                    self.ui.print_dice(atk_dice)
                    if self.ui.get_input("Usar Capa de Esquiva para rerrolar 1 dado? (s/n): ").lower() == 's':
                        atk_dice[0] = random.randint(1, 6)
                
                # Item: Armadura (Reduz dano de Lanças)
                if enemy.weapon_type == 'spear' and self.player.has_item("Armadura"):
                    if atk_dice: atk_dice.pop() # Remove um dado do ataque
                    self.ui.print_message("Armadura de Placas absorveu impacto.")
                
                self.ui.print_dice(atk_dice)
                
                damage = sum(atk_dice) // 4
                
                # [NOVO] Item: Aljava Sem Fim (Reduz dano de Arqueiros)
                if enemy.weapon_type == 'bow' and self.player.has_item("Aljava"):
                    if damage > 0:
                        damage = max(0, damage - 1)
                        self.ui.print_message("Aljava Sem Fim permitiu cobertura: -1 de Dano.")

                if damage > 0:
                    self.ui.print_message(f"Sofreu {damage} de dano!")
                    self.player.take_damage(damage)
                else:
                    self.ui.print_message("O ataque errou ou foi bloqueado.")
                
                if self.player.health <= 0: return

    def phase_attack(self):
        self.ui.print_message("\n--- FASE 3: ATACAR ---")

        # 1. Decisão de uso de Fúria
        use_fury = 0
        if self.player.fury > 0:
            q = self.ui.get_input(f"Usar quantos de Fúria? (Max {self.player.fury}): ")
            if q.isdigit():
                use_fury = min(int(q), self.player.fury)
        
        total_dice = 5 + use_fury
        current_dice = DiceSystem.roll(total_dice)
        
        rerolling = True
        while rerolling:
            self.ui.print_dice(current_dice)
            print(f"Glória: {self.player.glory} | Foco: {self.player.focus} | Fúria: {self.player.fury} | Vida: {self.player.health}")
            
            # Removida opção [M]anipular pois os itens mudaram de função
            action = self.ui.get_input("[A]tacar, [G]lória (Rerrolar Tudo - Custo 1), [F]oco (Rerrolar 1): ")
            
            # --- RERROLAR TUDO (GLÓRIA) ---
            if action.lower() == 'g':
                if self.player.glory >= 1:
                    self.player.glory -= 1
                    current_dice = DiceSystem.roll(total_dice)
                    self.ui.print_message("Glória usada! Todos os dados foram rerrolados.")
                else:
                    self.ui.print_message("Glória insuficiente!")

            # --- RERROLAR UM (FOCO) ---
            elif action.lower() == 'f':
                if self.player.focus >= 1:
                    try:
                        idx_str = self.ui.get_input("Qual dado rerrolar? (1-N): ")
                        if idx_str.isdigit():
                            idx = int(idx_str) - 1
                            if 0 <= idx < len(current_dice):
                                self.player.focus -= 1
                                current_dice[idx] = random.randint(1, 6)
                                self.ui.print_message("Foco usado! Dado rerrolado.")
                            else:
                                self.ui.print_message("Dado inválido.")
                    except ValueError:
                         self.ui.print_message("Entrada inválida.")
                else:
                    self.ui.print_message("Foco insuficiente!")

            # --- ATACAR ---
            elif action.lower() == 'a':
                rerolling = False
            
            else:
                self.ui.print_message("Opção inválida.")

        # 2. Escolher alvo e verificar sucesso
        target_idx = self.ui.get_input("Atacar qual inimigo? (1-3 ou 0 cancelar): ")
        if target_idx.isdigit() and int(target_idx) > 0:
            t_idx = int(target_idx) - 1
            if t_idx < len(self.active_enemies):
                target = self.active_enemies[t_idx]
                
                success = DiceSystem.check_requirement(current_dice, target.req_type, target.req_val)
                
                if success:
                    self.ui.print_message(f"INIMIGO DERROTADO: {target.name}")
                    self.player.equip_loot(target.loot, self.ui)
                    self.active_enemies.pop(t_idx)
                    
                    # Consome a fúria usada apenas se atacar (seja sucesso ou falha na vdd, mas aqui manteve a logica)
                    self.player.fury -= use_fury 
                    
                    if target.loot.name == "A Coroa do Rei":
                        self.deck = [] 
                        self.active_enemies = []
                else:
                    self.ui.print_message("Ataque falhou! Requisitos não atendidos.")
                    self.player.fury -= use_fury # Perde a fúria usada mesmo se falhar
