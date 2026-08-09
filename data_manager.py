import sqlite3
import os
from user import User


class DataManager:

    def __init__(self, db_file="data/techpath.db"):

        self.db_file = db_file

        # Make sure the directory exists
        directory = os.path.dirname(self.db_file)

        if directory:
            os.makedirs(directory, exist_ok=True)

        self.create_database()

    # =====================================================
    # DATABASE CONNECTION
    # =====================================================

    def get_connection(self):

        connection = sqlite3.connect(
            self.db_file
        )

        connection.row_factory = sqlite3.Row

        return connection

    # =====================================================
    # CREATE DATABASE
    # =====================================================

    def create_database(self):

        connection = self.get_connection()

        cursor = connection.cursor()

        # -------------------------------------------------
        # USERS TABLE
        # -------------------------------------------------

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (

                user_id TEXT PRIMARY KEY,

                name TEXT NOT NULL,

                age INTEGER NOT NULL,

                education TEXT NOT NULL,

                career_goal TEXT NOT NULL,

                study_hours REAL NOT NULL,

                password TEXT NOT NULL,

                current_level TEXT,

                programming_experience TEXT,

                interests TEXT,

                learning_style TEXT,

                email TEXT UNIQUE NOT NULL,

                verified INTEGER DEFAULT 0,

                verification_code INTEGER

            )
        """)

        # -------------------------------------------------
        # PROGRESS TABLE
        # -------------------------------------------------

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS progress (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id TEXT NOT NULL,

                skill_name TEXT NOT NULL,

                completed INTEGER DEFAULT 0,

                UNIQUE(user_id, skill_name),

                FOREIGN KEY(user_id)
                REFERENCES users(user_id)
                ON DELETE CASCADE

            )
        """)

        connection.commit()

        connection.close()

    # =====================================================
    # USER HELPER
    # =====================================================

    def _row_to_user(self, row):

        if row is None:
            return None

        return User(
            row["user_id"],
            row["name"],
            int(row["age"]),
            row["education"],
            row["career_goal"],
            float(row["study_hours"]),
            row["password"],
            row["current_level"],
            row["programming_experience"],
            row["interests"],
            row["learning_style"],
            row["email"],
            bool(row["verified"]),
            (
                int(row["verification_code"])
                if row["verification_code"] is not None
                else None
            )
        )

    # =====================================================
    # SAVE USER
    # =====================================================

    def save_user(self, user):

        connection = self.get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO users (

                user_id,
                name,
                age,
                education,
                career_goal,
                study_hours,
                password,
                current_level,
                programming_experience,
                interests,
                learning_style,
                email,
                verified,
                verification_code

            )

            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?
            )
        """, (

            user.user_id,
            user.name,
            user.age,
            user.education,
            user.career_goal,
            user.study_hours,
            user.password,
            user.current_level,
            user.programming_experience,
            user.interests,
            user.learning_style,
            user.email,
            int(user.verified),
            user.verification_code

        ))

        connection.commit()

        connection.close()

    # =====================================================
    # LOAD ALL USERS
    # =====================================================

    def load_users(self):

        connection = self.get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM users
        """)

        rows = cursor.fetchall()

        connection.close()

        return [
            self._row_to_user(row)
            for row in rows
        ]

    # =====================================================
    # GENERATE USER ID
    # =====================================================

    def get_next_id(self):

        connection = self.get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            SELECT user_id
            FROM users
            WHERE user_id LIKE 'AI%'
        """)

        rows = cursor.fetchall()

        connection.close()

        numbers = []

        for row in rows:

            user_id = row["user_id"]

            try:

                numbers.append(
                    int(user_id[2:])
                )

            except (ValueError, TypeError):

                pass

        next_number = (
            max(numbers) + 1
            if numbers
            else 1
        )

        new_id = f"AI{next_number:03d}"

        print(
            "🆕 GENERATED USER ID:",
            new_id
        )

        return new_id

    # =====================================================
    # LOAD USER BY ID
    # =====================================================

    def load_user_by_id(self, user_id):

        connection = self.get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM users
            WHERE user_id = ?
        """, (
            str(user_id).strip(),
        ))

        row = cursor.fetchone()

        connection.close()

        return self._row_to_user(row)

    # =====================================================
    # LOAD USER BY EMAIL
    # =====================================================

    def load_user_by_email(self, email):

        connection = self.get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM users
            WHERE LOWER(email) = LOWER(?)
        """, (
            email.strip(),
        ))

        row = cursor.fetchone()

        connection.close()

        return self._row_to_user(row)

    # =====================================================
    # LOAD USER BY NAME
    # =====================================================

    def load_user_by_name(self, name):

        connection = self.get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM users
            WHERE name = ?
        """, (
            name,
        ))

        row = cursor.fetchone()

        connection.close()

        return self._row_to_user(row)

    # =====================================================
    # UPDATE USER
    # =====================================================

    def update_user(self, user):

        connection = self.get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            UPDATE users

            SET

                name = ?,
                age = ?,
                education = ?,
                career_goal = ?,
                study_hours = ?,
                password = ?,
                current_level = ?,
                programming_experience = ?,
                interests = ?,
                learning_style = ?,
                email = ?,
                verified = ?,
                verification_code = ?

            WHERE user_id = ?

        """, (

            user.name,
            user.age,
            user.education,
            user.career_goal,
            user.study_hours,
            user.password,
            user.current_level,
            user.programming_experience,
            user.interests,
            user.learning_style,
            user.email,
            int(user.verified),
            user.verification_code,
            user.user_id

        ))

        connection.commit()

        connection.close()

    # =====================================================
    # DELETE USER
    # =====================================================

    def delete_user(self, user_id):

        connection = self.get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM progress
            WHERE user_id = ?
        """, (
            str(user_id),
        ))

        cursor.execute("""
            DELETE FROM users
            WHERE user_id = ?
        """, (
            str(user_id),
        ))

        connection.commit()

        connection.close()

    # =====================================================
    # SAVE PROGRESS
    # =====================================================

    def save_progress(self, user_id, roadmap):

        connection = self.get_connection()

        cursor = connection.cursor()

        for skill in roadmap:

            cursor.execute("""
                INSERT INTO progress (

                    user_id,
                    skill_name,
                    completed

                )

                VALUES (?, ?, ?)

                ON CONFLICT(user_id, skill_name)

                DO UPDATE SET

                    completed =
                    excluded.completed

            """, (

                str(user_id),
                skill.name,
                int(skill.completed)

            ))

        connection.commit()

        connection.close()

    # =====================================================
    # LOAD PROGRESS
    # =====================================================

    def load_progress(self, user_id):

        progress = {}

        connection = self.get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                skill_name,
                completed

            FROM progress

            WHERE user_id = ?

        """, (
            str(user_id),
        ))

        rows = cursor.fetchall()

        connection.close()

        for row in rows:

            progress[
                row["skill_name"]
            ] = bool(
                row["completed"]
            )

        return progress

    # =====================================================
    # DELETE PROGRESS
    # =====================================================

    def delete_progress(self, user_id):

        connection = self.get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM progress
            WHERE user_id = ?
        """, (
            str(user_id),
        ))

        connection.commit()

        connection.close()