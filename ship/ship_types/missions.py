from enum import Enum


class Mission(Enum):
    Exploration = "Deep space exploration and discovery"
    Combat = "Offensive and defensive military operations"
    Diplomatic = "Facilitation of negotiations and peace treaties"
    Scientific = "Research and scientific study missions"
    Colonization = "Establishment of colonies on new worlds"
    Patrol = "Routine security and border patrol"
    Rescue = "Search and rescue operations"
    Espionage = "Covert intelligence and reconnaissance"
    Trade = "Facilitation of trade and resource transport"
    Humanitarian = "Disaster relief and medical aid"
    Maintenance = "Shipyard and repair support missions"
    Training = "Crew training and field exercises"

    def __str__(self):
        """Returns a human-readable description of the mission type."""
        return self.value


if __name__ == "__main__":
    # Example usage
    mission = Mission.Exploration
    print(mission)  # Output: Deep space exploration and discovery
