class Character:
    def __init__(self,  name, ascension_stat, quality, element, role, scale) -> None:
        self.name = name
        self.ascension_stat = ascension_stat
        self.quality = quality
        self.element = element
        self.role = role
        self.scale = scale

    def __str__(self) -> str:
        return self.name