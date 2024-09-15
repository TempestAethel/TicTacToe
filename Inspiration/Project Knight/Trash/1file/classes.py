class Task:
    def __init__(self, base_data):
        self.base_data = base_data
        self.name = base_data["name"]
        self.level = 0
        self.max_level = 0
        self.xp = 0
        self.xp_multipliers = []

    def get_max_xp(self):
        max_xp = round(self.base_data["maxXp"] * (self.level + 1) * (1.01 ** self.level))
        return max_xp

    def get_xp_left(self):
        return round(self.get_max_xp() - self.xp)

    def get_max_level_multiplier(self):
        max_level_multiplier = 1 + self.max_level / 10
        return max_level_multiplier

    def get_xp_gain(self):
        return apply_multipliers(10, self.xp_multipliers)

    def increase_xp(self):
        self.xp += apply_speed(self.get_xp_gain())
        if self.xp >= self.get_max_xp():
            excess = self.xp - self.get_max_xp()
            while excess >= 0:
                self.level += 1
                excess -= self.get_max_xp()
            self.xp = self.get_max_xp() + excess


class Job(Task):
    def __init__(self, base_data):
        super().__init__(base_data)
        self.income_multipliers = []

    def get_level_multiplier(self):
        level_multiplier = 1 + (self.level + 1).bit_length() / 3.32  # Similar to log10 in JS
        return level_multiplier

    def get_income(self):
        return apply_multipliers(self.base_data["income"], self.income_multipliers)


class Skill(Task):
    def __init__(self, base_data):
        super().__init__(base_data)

    def get_effect(self):
        effect = 1 + self.base_data["effect"] * self.level
        return effect

    def get_effect_description(self):
        description = self.base_data["description"]
        text = "x" + str(round(self.get_effect(), 2)) + " " + description
        return text


class Item:
    def __init__(self, base_data):
        self.base_data = base_data
        self.name = base_data["name"]
        self.expense_multipliers = []

    def get_effect(self):
        if game_data.current_property != self and self not in game_data.current_misc:
            return 1
        return self.base_data["effect"]

    def get_effect_description(self):
        description = self.base_data["description"]
        if self.name in item_categories["Properties"]:
            description = "Happiness"
        return "x" + str(round(self.base_data["effect"], 1)) + " " + description

    def get_expense(self):
        return apply_multipliers(self.base_data["expense"], self.expense_multipliers)


class Requirement:
    def __init__(self, elements, requirements):
        self.elements = elements
        self.requirements = requirements
        self.completed = False

    def is_completed(self):
        if self.completed:
            return True
        for requirement in self.requirements:
            if not self.get_condition(requirement):
                return False
        self.completed = True
        return True


class TaskRequirement(Requirement):
    def __init__(self, elements, requirements):
        super().__init__(elements, requirements)
        self.type = "task"

    def get_condition(self, requirement):
        return game_data.task_data[requirement["task"]].level >= requirement["requirement"]


class CoinRequirement(Requirement):
    def __init__(self, elements, requirements):
        super().__init__(elements, requirements)
        self.type = "coins"

    def get_condition(self, requirement):
        return game_data.coins >= requirement["requirement"]


class AgeRequirement(Requirement):
    def __init__(self, elements, requirements):
        super().__init__(elements, requirements)
        self.type = "age"

    def get_condition(self, requirement):
        return days_to_years(game_data.days) >= requirement["requirement"]


class EvilRequirement(Requirement):
    def __init__(self, elements, requirements):
        super().__init__(elements, requirements)
        self.type = "evil"

    def get_condition(self, requirement):
        return game_data.evil >= requirement["requirement"]
