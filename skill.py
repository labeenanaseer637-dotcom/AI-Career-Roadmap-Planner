class Skill:

    def __init__(self, name, category, difficulty, completed=False):
        self.name = name
        self.category = category
        self.difficulty = difficulty
        self.completed = completed

    def display_skill(self):

        status = "Completed" if self.completed else "Not Completed"

        print(f"Skill: {self.name}")
        print(f"Category: {self.category}")
        print(f"Difficulty: {self.difficulty}")
        print(f"Status: {status}")

    def set_completed(self, completed):
      self.completed = completed

    def to_dict(self):
        return {
            "name": self.name,
            "category": self.category,
            "difficulty": self.difficulty,
            "completed": self.completed
        }