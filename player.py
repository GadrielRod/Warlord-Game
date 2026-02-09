class Player:
    def __init__(self, name="Guerreiro Desconhecido"):
        self.name = name
        self.max_health = 10
        self.health = 8 # Padrão (Dificuldade Normal) 
        self.glory = 0 # Ouro (Rerrolar tudo)
        self.focus = 0  # Prata (Rerrolar um)
        self.fury = 0   # Dados Pretos (Overclock)
        
        # Inventário: Máximo 3 itens
        self.inventory = [] 

    def equip_loot(self, loot, ui_handler):
        ui_handler.print_message(f"Você obteve: [{loot.name}]")
        ui_handler.print_message(f"Efeito: {loot.effect_desc}")
        
        if len(self.inventory) < 3:
            self.inventory.append(loot)
            ui_handler.print_message("Item adicionado ao inventário.")
        else:
            ui_handler.print_message("Inventário CHEIO (Máx 3).")
            ui_handler.print_message("Itens atuais:")
            for i, item in enumerate(self.inventory):
                print(f"   {i+1}. {item.name}")
            
            choice = ui_handler.get_input("Deseja substituir algum? (Digite 1-3 ou 'N' para descartar o novo): ")
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < 3:
                    removed = self.inventory[idx]
                    self.inventory[idx] = loot
                    ui_handler.print_message(f"Você descartou {removed.name} e pegou {loot.name}.")
                else:
                    ui_handler.print_message("O novo item foi deixado no campo de batalha.")
            else:
                ui_handler.print_message("O novo item foi deixado no campo de batalha.")

    def has_item(self, name_part):
        """Verifica se tem item pelo nome parcial"""
        for item in self.inventory:
            if item and name_part in item.name:
                return item
        return None

    def heal(self, amount):
        cost_per_hp = 6
        if self.has_item("Ervas"):
            cost_per_hp = 5
        
        real_heal = amount // cost_per_hp
        if real_heal > 0:
            self.health = min(self.max_health, self.health + real_heal)
            return real_heal
        return 0

    def take_damage(self, amount):
        if amount <= 0: return
        
        # Item: Escudo de Torre (Bloqueia e quebra)
        shield = self.has_item("Escudo de Torre")
        if shield:
            print(f">> {shield.name} bloqueou o impacto e se estilhaçou!")
            self.inventory.remove(shield)
            return

        self.health -= amount
        
        if self.health <= 0:
            # Item: Talismã (Renasce e quebra)
            talisman = self.has_item("Talismã")
            if talisman:
                print(f">> {talisman.name} brilhou e reviveu você com 1 HP!")
                self.health = 1
                self.inventory.remove(talisman)
            else:
                self.health = 0