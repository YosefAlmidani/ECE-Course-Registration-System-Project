import sqlite3
from data_classes import Section

class DatabaseHandler:
    def __init__(self, db_path="kau_engineering.db"):
        self.db_path = db_path

    def validate_login(self, user_id, password):
        """
        Checks credentials against both Students and Faculty tables.
        Returns: ('student', name, program) or ('admin', name, dept)
        """
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            
            # Check Student
            c.execute("SELECT name, program FROM students WHERE student_id=? AND password=?", (user_id, password))
            student = c.fetchone()
            if student:
                return 'student', student[0], student[1]

            # Check Faculty
            c.execute("SELECT name, department FROM faculty WHERE faculty_id=? AND password=?", (user_id, password))
            faculty = c.fetchone()
            if faculty:
                return 'admin', faculty[0], faculty[1]

        return None, None, None

    def get_student_schedule(self, student_id, semester="2025"):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            query = """
                SELECT s.section_id, s.course_code, s.days, s.start_time, s.end_time, s.semester
                FROM registrations r
                JOIN sections s ON r.section_id = s.section_id
                WHERE r.student_id = ? AND r.semester = ?
            """
            c.execute(query, (student_id, semester))
            rows = c.fetchall()
            return [Section(*row) for row in rows]

    def get_available_sections(self, course_code):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("""
                SELECT section_id, course_code, days, start_time, end_time, semester
                FROM sections WHERE course_code = ?
            """, (course_code,))
            rows = c.fetchall()
            return [Section(*row) for row in rows]

    def register_student(self, student_id, section_obj):
        try:
            with sqlite3.connect(self.db_path) as conn:
                c = conn.cursor()
                c.execute("""
                    INSERT INTO registrations (student_id, course_code, section_id, semester)
                    VALUES (?, ?, ?, ?)
                """, (student_id, section_obj.course_code, section_obj.section_id, section_obj.semester))
                conn.commit()
            return True, "Registration Successful"
        except sqlite3.IntegrityError:
            return False, "Already registered for this course/section."
        except Exception as e:
            return False, f"Database Error: {e}"

    def get_student_info(self, student_id):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("SELECT name, level, program, email FROM students WHERE student_id=?", (student_id,))
            return c.fetchone()

    def change_student_password(self, student_id, new_password):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("UPDATE students SET password=? WHERE student_id=?", (new_password, student_id))
            conn.commit()

    def get_student_level(self, student_id):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("SELECT level FROM students WHERE student_id=?", (student_id,))
            row = c.fetchone()
            return row[0] if row else None

    def get_courses_by_level(self, level, student_id):
        """
        Gets courses based on level AND the student's specific program plan.
        """
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            # 1. Get Program first
            c.execute("SELECT program FROM students WHERE student_id=?", (student_id,))
            res = c.fetchone()
            if not res: return []
            program = res[0]

            # 2. Get Courses for that program and level
            c.execute("""
                SELECT courses.course_code, courses.name, courses.credits
                FROM program_plans
                JOIN courses ON program_plans.course_code = courses.course_code
                WHERE program_plans.program=? AND program_plans.level=?
            """, (program, level))
            return c.fetchall()
    
    def get_program_plan(self, student_id):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("SELECT program, level FROM students WHERE student_id=?", (student_id,))
            student_data = c.fetchone()
            if not student_data: return None
            
            program, student_level = student_data
            
            c.execute("""
                SELECT program_plans.level, program_plans.course_code, courses.name
                FROM program_plans
                JOIN courses ON program_plans.course_code = courses.course_code
                WHERE program_plans.program=?
                ORDER BY program_plans.level, program_plans.course_code
            """, (program,))
            
            data = c.fetchall()
            
            plan = {}
            for lvl, code, name in data:
                if lvl not in plan: plan[lvl] = []
                plan[lvl].append({"course_code": code, "name": name})

            return {"program": program, "student_level": student_level, "plan": plan}