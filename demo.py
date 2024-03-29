import sys
import xml.etree.ElementTree as ET

class Soldier:
    def __init__(self, name, active_condition, skill_ref, strength):
        self.name = name
        self.active_condition = active_condition
        self.skill_ref = skill_ref
        self.strength = strength
        self.postfix_to_infix = self.postfix_to_infix()

    def postfix_to_infix(self):
        postfix_exp = self.active_condition.split()
        s = []
        for token in postfix_exp:
            if token not in {'gt', 'lt', 'eq', 'and', 'or'}:
                s.append(token)
            else:
                operand2 = s.pop()
                operand1 = s.pop()
                temp = f"({operand1} {token} {operand2})"
                s.append(temp)
        return s.pop()

class Clan:
    def __init__(self, name, max_cloning_power, cloning_var, base_deploy_cost, soldiers):
        self.name = name
        self.max_cloning_power = max_cloning_power
        self.cloning_var = cloning_var
        self.base_deploy_cost = base_deploy_cost
        self.soldiers = soldiers
        self.total_strength = sum(soldier.strength for soldier in soldiers)
        self.total_deploy_cost = len(soldiers) * base_deploy_cost

class Kingdom:
    def __init__(self, name, skills, clans):
        self.name = name
        self.skills = skills
        self.clans = clans

def parse_xml(xml_file_path):
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        kingdom_name = root.find("Name").text  # Changed variable name to kingdom_name
        skills = {}
        for skill_node in root.findall("Skill"):
            int_class_id = int(skill_node.find("Int_Class_ID").text)
            strength = int(skill_node.find("Strength").text)
            skills[int_class_id] = strength
        clans = []
        for clan_node in root.findall("Clan"):
            clan_name = clan_node.find("Name").text  # Use a different variable name for clan name
            max_cloning_power = int(clan_node.find("MaxCloningPower").text)
            cloning_var = clan_node.find("CloningVar").text
            base_deploy_cost = int(clan_node.find("BaseDeployCost").text)
            soldiers = []
            for soldier_node in clan_node.findall("Soldier"):
                soldier_name = soldier_node.find("Name").text
                active_condition = soldier_node.find("Active").text
                skill_ref = int(soldier_node.find("SkillRef").text)
                strength = skills.get(skill_ref, "Skill not found")
                soldiers.append(Soldier(soldier_name, active_condition, skill_ref, strength))
            clans.append(Clan(clan_name, max_cloning_power, cloning_var, base_deploy_cost, soldiers))
        return Kingdom(kingdom_name, skills, clans)
       
    except Exception as e:
        print("Failed to parse XML file:", e)
        
def display_output(kingdom, budget):
    print("Kingdom Name:", kingdom.name)
    print("Skills:")
    for int_class_id, strength in kingdom.skills.items():
        print(f"Int_Class_ID: {int_class_id}, Strength: {strength}")

    sorted_clans = sorted(kingdom.clans, key=lambda x: x.total_deploy_cost)
    total_kingdom_strength = 0
    total_deploy_cost = 0
    for clan in sorted_clans:
        if total_deploy_cost + clan.total_deploy_cost <= budget:
            total_kingdom_strength += clan.total_strength
            total_deploy_cost += clan.total_deploy_cost
        else:
            break

    print("Maximum Kingdom Strength within the budget:", total_kingdom_strength)
    print("Total Deployment Cost of Selected Clans:", total_deploy_cost)

def main():
    if len(sys.argv) < 3:
        print("Usage: python demo.py <XML_file> <budget>")
        return

    xml_file_path = sys.argv[1]
    budget = int(sys.argv[2])
    kingdom = parse_xml(xml_file_path)
    
    # Use the kingdom object for further processing
    if kingdom:
        display_output(kingdom, budget)

if __name__ == "__main__":
    main()
