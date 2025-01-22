from enum import Enum


class Faction(Enum):
    Federation = "United Federation of Planets"
    Klingon = "Klingon Empire"
    Romulan = "Romulan Star Empire"
    Cardassian = "Cardassian Union"
    Borg = "Borg Collective"
    Dominion = "Dominion"
    Ferengi = "Ferengi Alliance"
    Vulcan = "Vulcan High Command"
    Bajoran = "Bajoran Provisional Government"
    Andorian = "Andorian Empire"
    Tholian = "Tholian Assembly"
    Breen = "Breen Confederacy"
    Species_8472 = "Species 8472"
    Xindi = "Xindi Council"
    Orion = "Orion Syndicate"

    def __str__(self):
        """Returns a human-readable name for the faction."""
        return self.value


if __name__ == "__main__":
    # Example usage
    faction = Faction.Klingon
    print(faction)  # Output: Klingon Empire
