class CareerAdvisor:

    def generate_advice(self, user, progress):

        advice = []

        # Greeting
        advice.append(f"Hello {user.name}! 👋")

        # Current level
        if user.current_level == "Beginner":
            advice.append(
                "You are at the beginning of your AI journey. Build a strong foundation before moving to advanced topics."
            )

        elif user.current_level == "Intermediate":
            advice.append(
                "You already have a solid foundation. It is a good time to focus on real-world projects."
            )

        else:
            advice.append(
                "You have advanced skills. Focus on specialization and portfolio development."
            )

        # Study hours
        if user.study_hours < 2:
            advice.append(
                "Increasing your study time to at least 2 hours per day could help you progress faster."
            )

        elif user.study_hours <= 4:
            advice.append(
                "Your study routine is consistent. Keep practicing regularly."
            )

        else:
            advice.append(
                "Excellent dedication! Your study schedule should help you reach your goal quickly."
            )

        # Progress
        percentage = progress.progress_percentage()

        if percentage < 30:
            advice.append(
                "Complete the easy skills first before attempting harder topics."
            )

        elif percentage < 70:
            advice.append(
                "Great progress! Keep building projects while learning."
            )

        else:
            advice.append(
                "You're close to your career goal. Start preparing your portfolio and resume."
            )

        return advice