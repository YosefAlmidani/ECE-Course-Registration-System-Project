import sqlite3

class Validator:
    @staticmethod
    def check_time_conflict(new_section, current_schedule_sections):
        #Checks if the new_section overlaps with any section in the current schedule.
        for registered_section in current_schedule_sections:
            # 1. Check Semester Match
            if new_section.semester != registered_section.semester:
                continue 

            # 2. Check Day Overlap
            days_new = set(new_section.get_days_list())
            days_current = set(registered_section.get_days_list())
            
            # If no common days, there is no conflict
            if not days_new.intersection(days_current):
                continue 

            # 3. Check Time Overlap (Only if days overlap)
            start1 = new_section.get_start_integer()
            end1 = new_section.get_end_integer()
            start2 = registered_section.get_start_integer()
            end2 = registered_section.get_end_integer()

            # Logic: (Start1 < End2) and (Start2 < End1)
            if start1 < end2 and start2 < end1:
                conflict_days = days_new.intersection(days_current)
                return True, f"Time Conflict: {new_section.course_code} overlaps with {registered_section.course_code} on {conflict_days}"
        
        return False, "No Conflict"

    @staticmethod
    def validate_prerequisites(db_path, student_id, course_code):
        #Checks if the student has passed all prerequisites for a course.
        try:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()

            # 1. Get required prerequisites for this course
            c.execute("SELECT prereq_code FROM prerequisites WHERE course_code=?", (course_code,))
            required_prereqs = [row[0] for row in c.fetchall()] 

            if not required_prereqs:
                conn.close()
                return True, "No prerequisites required"

            # 2. Get student's passed courses
            c.execute("SELECT course_code FROM transcript WHERE student_id=?", (student_id,))
            completed_courses = [row[0] for row in c.fetchall()]

            conn.close()

            # 3. Compare lists
            missing = [req for req in required_prereqs if req not in completed_courses]

            if missing:
                return False, f"Missing Prerequisites: {', '.join(missing)}"
            
            return True, "All prerequisites met"

        except Exception as e:
            return False, f"System Error checking prerequisites: {str(e)}"