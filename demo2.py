import sys
import xml.etree.ElementTree as ET
import itertools

import itertools

class Skill:
    def __init__(self, int_class_id, strength):
        self.int_class_id = int_class_id
        self.strength = strength

class Soldier:
    def __init__(self, int_class_id, name, active_condition, skill_ref):
        self.int_class_id = int_class_id
        self.name = name
        self.active_condition = active_condition
        self.skill_ref = skill_ref

class Clan:
    def __init__(self, name, max_cloning_power, base_deploy_cost, soldiers):
        self.name = name
        self.max_cloning_power = max_cloning_power
        self.base_deploy_cost = base_deploy_cost
        self.soldiers = soldiers

class Kingdom:
    def __init__(self, name, skills, clans):
        self.name = name
        self.skills = skills
        self.clans = clans

# Function to calculate the total strength of a clan
def calculate_clan_strength(clan, skills):
    return sum(calculate_soldier_strength(soldier, skills) for soldier in clan.soldiers)

# Function to calculate the strength of a soldier
def calculate_soldier_strength(soldier, skills):
    return sum(skills[skill_ref] for skill_ref in soldier.skill_ref)

# Function to calculate the total deploy cost of a clan
def calculate_clan_deploy_cost(clan, selected_cloning_power):
    return clan.base_deploy_cost * selected_cloning_power

# Function to generate all possible combinations of clans and cloning powers
def generate_combinations(kingdom):
    all_combinations = []
    for r in range(1, len(kingdom.clans) + 1):
        for combination in itertools.product(kingdom.clans, repeat=r):
            all_combinations.append(combination)
    return all_combinations

# Function to find the optimal kingdom configuration
def find_optimal_kingdom(kingdom):
    optimal_strength = 0
    optimal_cost = float('inf')
    optimal_configuration = None

    all_combinations = generate_combinations(kingdom)
    for combination in all_combinations:
        for cloning_powers in itertools.product(*(range(1, clan.max_cloning_power + 1) for clan in combination)):
            total_strength = sum(calculate_clan_strength(clan, kingdom.skills) for clan in combination)
            total_cost = sum(calculate_clan_deploy_cost(clan, power) for clan, power in zip(combination, cloning_powers))
            if total_strength > optimal_strength or (total_strength == optimal_strength and total_cost < optimal_cost):
                optimal_strength = total_strength
                optimal_cost = total_cost
                optimal_configuration = (combination, cloning_powers)

    return optimal_configuration, optimal_strength, optimal_cost

# Example usage:
def main():
    # Input data
    skills_data = {1: 3, 2: 4, 3: 1, 4: 5}
    soldiers_clan_a = [
        Soldier(5, 'p_a', 'x == 2', [1]),
        Soldier(6, 'q_a', 'x == 1', [2])
    ]
    soldiers_clan_b = [
        Soldier(7, 'p_b', 'y == 1', [3]),
        Soldier(8, 'q_b', 'y == 2', [4])
    ]
    clan_a = Clan('clan_a', 2, 5, soldiers_clan_a)
    clan_b = Clan('clan_b', 3, 7, soldiers_clan_b)
    kingdom = Kingdom('base_kingdom', skills_data, [clan_a, clan_b])

    # Find the optimal kingdom configuration
    optimal_configuration, optimal_strength, optimal_cost = find_optimal_kingdom(kingdom)

    # Print the optimal configuration
    print("Optimal Kingdom Configuration:")
    for i, (clan, cloning_power) in enumerate(zip(*optimal_configuration)):
        print(f"Clan {i+1}: {clan.name}, Cloning Power: {cloning_power}")
    print("Total Produced Strength:", optimal_strength)
    print("Total Deploy Cost:", optimal_cost)

if __name__ == "__main__":
    main()
