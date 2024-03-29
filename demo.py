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


def display_output(kingdom):
    print("Kingdom Name:", kingdom.name)
    print("Skills:")
    for int_class_id, strength in kingdom.skills.items():
        print(f"Int_Class_ID: {int_class_id}, Strength: {strength}")

    print("Clans:")
    for i, clan in enumerate(kingdom.clans):
        print(f"Clan {i+1}:")
        print(f"Name: {clan.name}, Max Cloning Power: {clan.max_cloning_power}, Cloning Var: {clan.cloning_var}, Base Deploy Cost: {clan.base_deploy_cost}")
        print("Soldiers:")
        for soldier in clan.soldiers:
            print(f"Name: {soldier.name}, Active Condition: {soldier.active_condition}, Skill Reference: {soldier.skill_ref}, Strength: {soldier.strength}, Postfix to Infix: {soldier.postfix_to_infix}")

def main():
    if len(sys.argv) < 2:
        print("XML file path not provided.")
        return

    xml_file_path = sys.argv[1]
    kingdom = parse_xml(xml_file_path)
    
    # Use the kingdom object for further processing
    if kingdom:
        display_output(kingdom)

if __name__ == "__main__":
    main()