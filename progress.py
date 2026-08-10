from data_manager import DataManager


class ProgressTracker:

    def __init__(self, roadmap):

        self.roadmap = roadmap

        # Uses DATABASE_URL from the environment (Postgres),
        # same as the rest of TechPath AI
        self.data_manager = DataManager()

    # =========================================================
    # COMPLETE SKILL
    # =========================================================

    def complete_skill(self, skill_name):

        for skill in self.roadmap:

            if skill.name.lower() == skill_name.lower():

                skill.set_completed(True)

                return True

        return False

    # =========================================================
    # COMPLETED SKILLS
    # =========================================================

    def completed_skills(self):

        count = 0

        for skill in self.roadmap:

            if skill.completed:
                count += 1

        return count

    # =========================================================
    # REMAINING SKILLS
    # =========================================================

    def remaining_skills(self):

        return (
            len(self.roadmap)
            - self.completed_skills()
        )

    # =========================================================
    # PROGRESS PERCENTAGE
    # =========================================================

    def progress_percentage(self):

        total = len(self.roadmap)

        if total == 0:
            return 0

        completed = self.completed_skills()

        percentage = (
            completed / total
        ) * 100

        return round(
            percentage,
            2
        )

    # =========================================================
    # DISPLAY PROGRESS
    # =========================================================

    def display_progress(self):

        print(
            "\n========== Progress =========="
        )

        print(
            f"Completed : {self.completed_skills()}"
        )

        print(
            f"Remaining : {self.remaining_skills()}"
        )

        print(
            f"Progress  : {self.progress_percentage():.2f}%"
        )

    # =========================================================
    # SEARCH SKILL
    # =========================================================

    def search_skill(self, keyword):

        results = []

        keyword = keyword.lower()

        for skill in self.roadmap:

            if keyword in skill.name.lower():

                results.append(skill)

        return results

    # =========================================================
    # SAVE PROGRESS
    # =========================================================

    def save_progress(self, user_id):

        self.data_manager.save_progress(
            user_id,
            self.roadmap
        )

    # =========================================================
    # LOAD PROGRESS
    # =========================================================

    def load_progress(self, user_id):

        saved_progress = (
            self.data_manager.load_progress(
                user_id
            )
        )

        for skill in self.roadmap:

            if skill.name in saved_progress:

                skill.completed = (
                    saved_progress[skill.name]
                )