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
                stack.append(f"({operand1} {token} {operand2})")
        
        return stack.pop()

    def is_active(self, clone_count, cloning_var):
        infix_exp = self.postfix_to_infix(clone_count, cloning_var)
        result = eval(infix_exp)
        return result

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
            cloning_var = clan_node.find("CloningVar").text
            base_deploy_cost = int(clan_node.find("BaseDeployCost").text)
            soldiers = []
            for soldier_node in clan_node.findall("Soldier"):
                soldier_name = soldier_node.find("Name").text
                active_condition = soldier_node.find("Active").text
                skill_ref = int(soldier_node.find("SkillRef").text)
                strength = skill_ref  # Assuming strength is based on skill reference
                soldiers.append(Soldier(soldier_name, active_condition, skill_ref, strength))
            clans.append(Clan(name, max_cloning_power, cloning_var, base_deploy_cost, soldiers))
        return Kingdom(name, clans)
    except Exception as e:
        print("Failed to parse XML file:", e)

def calculate_strength_within_budget(kingdom, budget):
    max_strength = 0

    for clone_count_a in range(min(kingdom.clans[0].max_cloning_power + 1, budget // kingdom.clans[0].base_deploy_cost + 1)):
        for clone_count_b in range(min(kingdom.clans[1].max_cloning_power + 1, (budget - clone_count_a * kingdom.clans[0].base_deploy_cost) // kingdom.clans[1].base_deploy_cost + 1)):
            
            total_deploy_cost = clone_count_a * kingdom.clans[0].base_deploy_cost + clone_count_b * kingdom.clans[1].base_deploy_cost

            if total_deploy_cost > budget:
                break

            # Calculate the total strength for this combination
            total_strength = 0
            for soldier in kingdom.clans[0].soldiers:
                if soldier.is_active(clone_count_a, kingdom.clans[0].cloning_var):
                    total_strength += soldier.strength * clone_count_a

            for soldier in kingdom.clans[1].soldiers:
                if soldier.is_active(clone_count_b, kingdom.clans[1].cloning_var):
                    total_strength += soldier.strength * clone_count_b

            print(f"Clone Count A: {clone_count_a}, Clone Count B: {clone_count_b}, Total Strength: {total_strength}")

            max_strength = max(max_strength, total_strength)

    return max_strength



def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py input.xml budget")
        return

    xml_file_path = sys.argv[1]
    budget = int(sys.argv[2])

    kingdom = parse_xml(xml_file_path)
    if kingdom:
        max_strength = calculate_strength_within_budget(kingdom, budget)
        print("Maximum Strength within Budget:", max_strength)

if __name__ == "__main__":
    main()
