import random
from collections import Counter

class DiceSystem:
    @staticmethod
    def roll(qty):
        """Rola uma quantidade de dados d6."""
        return [random.randint(1, 6) for _ in range(qty)]

    @staticmethod
    def check_requirement(dice, req_type, req_val=0):
        """
        Verifica se os dados atendem ao requisito do inimigo.
        """
        if not dice:
            return False
            
        counts = Counter(dice)
        values = sorted(dice)
        total = sum(dice)

        if req_type == 'sum':
            return total >= req_val
            
        elif req_type == 'exact_sum':
            return total == req_val

        elif req_type == 'kind': 
            # Ex: AAAA (4 iguais). req_val = 4
            return any(c >= req_val for c in counts.values())
            
        elif req_type == 'full_house': 
            # AA-BBB (Um par e uma trinca, ou 5 iguais)
            has_3 = any(c >= 3 for c in counts.values())
            has_2 = any(c >= 2 for c in counts.values())
            # Se tem 5 iguais, tecnicamente satisfaz
            five_kind = any(c >= 5 for c in counts.values())
            # Se tem 3 e 2, precisa verificar se são números diferentes
            valid_full = (has_3 and has_2 and len(counts) >= 2)
            return valid_full or five_kind

        elif req_type == 'mixed_pairs': 
            # AA-BB-C (2 pares distintos). req_val = 2
            pairs = 0
            for k, v in counts.items():
                pairs += v // 2
            return pairs >= req_val
            
        elif req_type == 'straight': 
            # Sequência de 5 (ex: 1-2-3-4-5 ou 2-3-4-5-6)
            unique_vals = sorted(list(set(values)))
            if len(unique_vals) < 5: return False
            for i in range(len(unique_vals) - 1):
                if unique_vals[i+1] != unique_vals[i] + 1:
                    return False
            return True
            
        elif req_type == 'all_odd':
            return all(d % 2 != 0 for d in dice)
            
        elif req_type == 'all_even':
            return all(d % 2 == 0 for d in dice)

        # --- NOVA REGRA DO BOSS ---
        elif req_type == 'boss_special':
            # Duas trincas somando 21 exatos (Implica 6,6,6 + 1,1,1)
            # Requer ter pelo menos três 6 e três 1
            has_three_6 = counts[6] >= 3
            has_three_1 = counts[1] >= 3
            return has_three_6 and has_three_1

        return False

