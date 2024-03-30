import ast
import sys
import xml.etree.ElementTree as ET

class Soldier:
    def __init__(self, name, active_condition, skill_ref, strength):
        self.name = name
        self.active_condition = active_condition
        self.skill_ref = skill_ref
        self.strength = strength

    def postfix_to_infix(self, var_value, cloning_var):
        postfix_exp = self.active_condition.split()
        print(f"Postfix expression list: {postfix_exp}")  # Added for debugging
        s = []
        for token in postfix_exp:
            if token not in {'gt', 'lt', 'eq', 'and', 'or'}:
                # If token is a variable placeholder, replace it with actual value
                token = str(var_value) if token == cloning_var else token
                s.append(token)
            else:
                # Replace symbolic operators with Python equivalents
                if token == 'eq':
                    token = '=='
                elif token == 'lt':
                    token = '<'
                elif token == 'gt':
                    token = '>'
                s.append(token)

        # Convert postfix expression to infix
        stack = []
        for token in s:
            if token not in {'+', '-', '*', '/', '^', '==', '<', '>', 'and', 'or'}:
                stack.append(token)
            else:
                operand2 = stack.pop()
                operand1 = stack.pop()
                infix_exp = f"({operand1} {token} {operand2})"
                print(f"Infix expression: {infix_exp}")  # Added for debugging
                stack.append(infix_exp)
        
        infix_exp = stack.pop()
        print(f"Final infix expression: {infix_exp}")  # Added for debugging
        return infix_exp



    def is_active(self, clone_count, cloning_var):
        infix_exp = self.postfix_to_infix(clone_count, cloning_var)
        try:
            result = ast.literal_eval(infix_exp)
            return result
        except Exception as e:
            print("Error evaluating infix expression:", e)
            return False

class Clan:
    def __init__(self, name, max_cloning_power, cloning_var, base_deploy_cost, soldiers):
        self.name = name
        self.max_cloning_power = max_cloning_power
        self.cloning_var = cloning_var
        self.base_deploy_cost = base_deploy_cost
        self.soldiers = soldiers

class Kingdom:
    def __init__(self, name, clans):
        self.name = name
        self.clans = clans

def parse_xml(xml_file_path):
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        name = root.find("Name").text
        clans = []
        for clan_node in root.findall("Clan"):
            name = clan_node.find("Name").text
            max_cloning_power = int(clan_node.find("MaxCloningPower").text)
            print(f"Clan: {name}, Max Cloning Power: {max_cloning_power}")  # Added for debugging
            cloning_var = clan_node.find("CloningVar").text
            base_deploy_cost = int(clan_node.find("BaseDeployCost").text)
            soldiers = []
            for soldier_node in clan_node.findall("Soldier"):
                soldier_name = soldier_node.find("Name").text
                active_condition = soldier_node.find("Active").text
                print(f"Soldier: {soldier_name}, Active Condition: {active_condition}")  # Added for debugging
                skill_ref = int(soldier_node.find("SkillRef").text)
                strength = skill_ref  # Assuming strength is based on skill reference
                soldiers.append(Soldier(soldier_name, active_condition, skill_ref, strength))
            clans.append(Clan(name, max_cloning_power, cloning_var, base_deploy_cost, soldiers))
        return Kingdom(name, clans)
    except Exception as e:
        print("Failed to parse XML file:", e)



def calculate_strength_within_budget(kingdom, budget):
    max_strength = 0

    num_clans = len(kingdom.clans)
    max_clone_powers = [clan.max_cloning_power for clan in kingdom.clans]
    
    def calculate_total_strength(clone_counts):
        total_strength = 0
        for i, clan in enumerate(kingdom.clans):
            for soldier in clan.soldiers:
                if soldier.is_active(clone_counts[i], clan.cloning_var):
                    total_strength += soldier.strength * clone_counts[i]
        return total_strength

    def generate_clone_combinations(clone_counts, clan_index):
        if clan_index == num_clans:
            nonlocal max_strength
            total_strength = calculate_total_strength(clone_counts)
            max_strength = max(max_strength, total_strength)
            return

        for clone_count in range(max_clone_powers[clan_index] + 1):
            clone_counts[clan_index] = clone_count
            generate_clone_combinations(clone_counts, clan_index + 1)

    generate_clone_combinations([0] * num_clans, 0)
    
    return max_strength, max_clone_powers


def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py input.xml budget")
        return

    xml_file_path = sys.argv[1]
    budget = int(sys.argv[2])

    kingdom = parse_xml(xml_file_path)
    if kingdom:
        max_strength, max_clone_power = calculate_strength_within_budget(kingdom, budget)
        print("Maximum Strength within Budget:", max_strength)
        print("Maximum Clone Power per Clan:", max_clone_power)

if __name__ == "__main__":
    main()