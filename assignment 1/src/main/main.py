from src.chasing.chasing_simulator import ChasingSimulator
from src.creature.creature_characteristics_logger import (
    CreatureCharacteristicsDescriptor,
    CreatureCharacteristicsDescriptorImpl,
)
from src.fighting.damage_calculator import BasicDamageCalculator, DamageCalculator
from src.fighting.fighting_simulator import FightingSimulator
from src.creature.random_creature_generator import random_creature
from src.static.characteristics import STATUS_PREDATOR, STATUS_PREY
from src.static.simulation_constants import (
    PREDATOR_MAX_LOCATION,
    PREDATOR_MIN_LOCATION,
    PREY_MAX_LOCATION,
    PREY_MIN_LOCATION,
    SIMULATION_COUNT,
)


def simulate(
    logger: CreatureCharacteristicsDescriptor, damage_calculator: DamageCalculator
):
    predator = random_creature(
        (PREDATOR_MIN_LOCATION, PREDATOR_MAX_LOCATION), STATUS_PREDATOR
    )
    print(logger.description(predator) + "\n")

    prey = random_creature((PREY_MIN_LOCATION, PREY_MAX_LOCATION), STATUS_PREY)
    print(logger.description(prey) + "\n")

    chasing_simulator = ChasingSimulator(predator, prey)
    chase_winner_status = chasing_simulator.simulate_chase()

    if chase_winner_status == STATUS_PREDATOR:
        fighting_simulator = FightingSimulator(predator, prey, damage_calculator)
        fight_winner_status = fighting_simulator.simulate_fight()
        if fight_winner_status == STATUS_PREDATOR:
            print("Some R-rated things have happened\n")
        else:
            print("Pray ran into infinity\n")
    else:
        print("Pray ran into infinity\n")


def main():
    logger = CreatureCharacteristicsDescriptorImpl()
    damage_calculator = BasicDamageCalculator()
    for i in range(SIMULATION_COUNT):
        print("------------------------------------")
        print(f"Starting simulation #{i+1}\n")
        simulate(logger, damage_calculator)
        print(f"Simulation #{i+1} has been finished")
        print("------------------------------------\n")


if __name__ == "__main__":
    main()
