from user import User
from data_manager import DataManager
from career_path import CareerPath
from progress import ProgressTracker
from analytics import Analytics
from visualization import Visualization


# -----------------------------
# Create Managers
# -----------------------------
data_manager = DataManager("data/users.csv")
career_manager = CareerPath("data/careers.csv")

current_user = None
roadmap = []
tracker = None


while True:

    print("\n" + "=" * 50)
    print("        AI CAREER ROADMAP PLANNER")
    print("=" * 50)

    print("1. Create User Profile")
    print("2. View Profile")
    print("3. Generate Roadmap")
    print("4. View Roadmap")
    print("5. Mark Skill Completed")
    print("6. View Progress")
    print("7. Analytics")
    print("8. Visualize")
    print("9. Search Skill")
    print("10. Filter Skills")
    print("11. Save Progress")
    print("12. Load Progress")
    print("13. Exit")

    choice = input("\nEnter your choice: ")

    # ==================================================
    # CREATE USER
    # ==================================================
    if choice == "1":

        name = input("Enter Name: ")

        while True:
            try:
                age = int(input("Enter Age: "))
                break
            except ValueError:
                print("Please enter a valid age.")

        education = input("Enter Education: ")

        while True:
            try:
                study_hours = float(input("Study Hours Per Day: "))
                break
            except ValueError:
                print("Please enter a valid number.")

        careers = career_manager.get_careers()

        print("\nAvailable Careers\n")

        for index, career in enumerate(careers, start=1):
            print(f"{index}. {career}")

        while True:

            try:

                career_choice = int(input("\nSelect Career: "))

                if 1 <= career_choice <= len(careers):
                    career_goal = careers[career_choice - 1]
                    break

                print("Invalid Choice!")

            except ValueError:
                print("Please enter a number.")

        user_id = data_manager.get_next_id()

        current_user = User(
            user_id,
            name,
            age,
            education,
            career_goal,
            study_hours
        )

        data_manager.save_user(current_user)

        print("\nProfile Created Successfully!")
      
        print(f"Your User ID is: {current_user.user_id}")

    # ==================================================
    # VIEW PROFILE
    # ==================================================
    elif choice == "2":

       try:

         user_id = int(input("Enter User ID: "))

         user = data_manager.load_user_by_id(user_id)

         if user:

            current_user = user
            current_user.display_profile()

         else:
 
            print("User not found.")

       except ValueError:

        print("Please enter a valid User ID.")

    # ==================================================
    # GENERATE ROADMAP
    # ==================================================
    elif choice == "3":

        if current_user:

            roadmap = career_manager.generate_roadmap(
                current_user.career_goal
            )

            progress = data_manager.load_progress(
                current_user.user_id
            )

            for skill in roadmap:

                if skill.name in progress:
                    skill.set_completed(progress[skill.name])

            tracker = ProgressTracker(roadmap)

            print("\nRoadmap Generated Successfully!")

        else:

            print("Please create a profile first.")

    # ==================================================
    # VIEW ROADMAP
    # ==================================================
    elif choice == "4":

        if roadmap:

            print("\nYour Roadmap\n")

            for skill in roadmap:

                skill.display_skill()
                print("-" * 40)

        else:

            print("Generate roadmap first.")

    # ==================================================
    # COMPLETE SKILL
    # ==================================================
    elif choice == "5":

        if tracker:

            skill_name = input("Enter Skill Name: ")

            if tracker.complete_skill(skill_name):

                data_manager.save_progress(
                    current_user.user_id,
                    roadmap
                )

                print("Skill marked as completed!")

            else:

                print("Skill not found!")

        else:

            print("Generate roadmap first.")

    # ==================================================
    # VIEW PROGRESS
    # ==================================================
    elif choice == "6":

        if tracker:
            tracker.display_progress()
        else:
            print("Generate roadmap first.")

    # ==================================================
    # ANALYTICS
    # ==================================================
    elif choice == "7":

        if roadmap:

            analytics = Analytics(roadmap)

            analytics.summary()
            analytics.category_summary()
            analytics.difficulty_summary()

        else:

            print("Generate roadmap first.")

    # ==================================================
    # VISUALIZATION
    # ==================================================
    elif choice == "8":

        if roadmap:

            visual = Visualization(roadmap)

            visual.progress_pie_chart()
            visual.category_bar_chart()
            visual.difficulty_chart()

        else:

            print("Generate roadmap first.")

    # ==================================================
    # SEARCH SKILL
    # ==================================================
    elif choice == "9":

        if tracker:

            keyword = input("Enter Skill Name: ")

            results = tracker.search_skill(keyword)

            if results:

                for skill in results:
                    skill.display_skill()
                    print("-" * 40)

            else:

                print("No matching skill found.")

        else:

            print("Generate roadmap first.")

    # ==================================================
    # FILTER SKILLS
    # ==================================================
    elif choice == "10":

        if tracker:

            print("\n1. Completed Skills")
            print("2. Remaining Skills")
            print("3. Easy")
            print("4. Medium")
            print("5. Hard")

            option = input("Choose Filter: ")

            if option == "1":
                skills = tracker.completed_list()

            elif option == "2":
                skills = tracker.remaining_list()

            elif option == "3":
                skills = tracker.filter_difficulty("Easy")

            elif option == "4":
                skills = tracker.filter_difficulty("Medium")

            elif option == "5":
                skills = tracker.filter_difficulty("Hard")

            else:
                print("Invalid Choice!")
                continue

            if skills:

                for skill in skills:

                    skill.display_skill()
                    print("-" * 40)

            else:

                print("No skills found.")

        else:

            print("Generate roadmap first.")

    # ==================================================
    # SAVE PROGRESS
    # ==================================================
    elif choice == "11":

        if current_user and roadmap:

            data_manager.save_progress(
                current_user.user_id,
                roadmap
            )

            print("Progress Saved Successfully!")

        else:

            print("Nothing to save.")

    # ==================================================
    # LOAD PROGRESS
    # ==================================================
    elif choice == "12":

        if current_user and roadmap:

            progress = data_manager.load_progress(
                current_user.user_id
            )

            for skill in roadmap:

                if skill.name in progress:
                    skill.set_completed(progress[skill.name])

            print("Progress Loaded Successfully!")

        else:

            print("Generate roadmap first.")

    # ==================================================
    # EXIT
    # ==================================================
    elif choice == "13":

        print("\nThank you for using AI Career Roadmap Planner!")
        break

    else:

        print("Invalid Menu Choice!")