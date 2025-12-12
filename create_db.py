import sqlite3

def create_database():
    print("--- Creating KAU Engineering Database (Updated for Specific Programs) ---")
    
    conn = sqlite3.connect("kau_engineering.db")
    c = conn.cursor()

    # --- 1. Create Tables ---

    # Table: Students
    c.execute("""CREATE TABLE IF NOT EXISTS students(
        student_id TEXT PRIMARY KEY,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT,
        program TEXT, -- Now stores: 'Computer', 'Biomedical', 'Power', 'Comm'
        level INTEGER
    )""")

    # Table: Courses
    c.execute("""CREATE TABLE IF NOT EXISTS courses(
        course_code TEXT PRIMARY KEY,
        name TEXT,
        credits INTEGER,
        level INTEGER
    )""")

    # Table: Prerequisites
    c.execute("""CREATE TABLE IF NOT EXISTS prerequisites(
        course_code TEXT,
        prereq_code TEXT,
        FOREIGN KEY (course_code) REFERENCES courses(course_code),
        FOREIGN KEY (prereq_code) REFERENCES courses(course_code)
    )""")

    # Table: Program Plans (The Mapping Table)
    c.execute("""CREATE TABLE IF NOT EXISTS program_plans(
        program TEXT,    -- e.g., 'Computer', 'Biomedical'
        level INTEGER,   -- e.g., 3, 4
        course_code TEXT,
        PRIMARY KEY (program, course_code),
        FOREIGN KEY (course_code) REFERENCES courses(course_code)
    )""")
    # Table: Faculty
    c.execute("""CREATE TABLE IF NOT EXISTS faculty(
        faculty_id TEXT PRIMARY KEY,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT,
        department TEXT
    )""")

    # Table: Sections
    c.execute("""CREATE TABLE IF NOT EXISTS sections(
        section_id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_code TEXT,
        section_number INTEGER,
        days TEXT,
        start_time TEXT,
        end_time TEXT,
        faculty_id TEXT,
        semester TEXT,
        FOREIGN KEY (course_code) REFERENCES courses(course_code),
        FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id)
    )""")

    # Table: Transcript
    c.execute("""CREATE TABLE IF NOT EXISTS transcript(
        student_id TEXT,
        course_code TEXT,
        grade TEXT,
        FOREIGN KEY (student_id) REFERENCES students(student_id),
        FOREIGN KEY (course_code) REFERENCES courses(course_code)
    )""")

    # Table: Registrations
    c.execute("""CREATE TABLE IF NOT EXISTS registrations(
        student_id TEXT,
        course_code TEXT,
        section_id INTEGER,
        semester TEXT,
        FOREIGN KEY (student_id) REFERENCES students(student_id),
        FOREIGN KEY (course_code) REFERENCES courses(course_code),
        FOREIGN KEY (section_id) REFERENCES sections(section_id)
    )""")

    # Table: Faculty Teaching
    c.execute("""CREATE TABLE IF NOT EXISTS faculty_teaching(
        faculty_id TEXT,
        section_id INTEGER,
        FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id),
        FOREIGN KEY (section_id) REFERENCES sections(section_id)
    )""")

    print("Tables structure updated.")

    # -- Students --
    students = [
        ('2344442','Ahmed Al-Qahtani','ahmed1@stu.kau.edu.sa','AShkej2#','Computer',4),
        ('2466991','Fahad Al-Harbi','fahad2@stu.kau.edu.sa','dnbdj2356','Biomedical',3),
        ('2435550','Saud Al-Zahrani','saud3@stu.kau.edu.sa','djood123','Power',3),
        ('2433381','Nawaf Al-Omari','nawaf4@stu.kau.edu.sa','poldf2#kr','Comm',3),
        ('2435066','Mansour Al-Juhani','mans5@stu.kau.edu.sa','flkk909@','Computer',3),
        ('2367667','Turki Al-Mutairi','turki6@stu.kau.edu.sa','lklk556##','Computer',4),
        ('2499565','Omar Al-Shamrani','omar7@stu.kau.edu.sa','tt2kee5@','Biomedical',3),
        ('2400098','Khalid Al-Dosari','khalid8@stu.kau.edu.sa','uuin123%','Power',3),
        ('2499098','Rayan Al-Shehri','rayan9@stu.kau.edu.sa','enfp111$','Comm',3),
        ('2457893','Majed Al-Ghamdi','majed10@stu.kau.edu.sa','poerf$1112$','Computer',3)
    ]
    c.execute("DELETE FROM students")
    c.executemany("INSERT INTO students VALUES (?,?,?,?,?,?)", students)

    # -- Courses --
    courses = [
        ('PHYS202','Physics',4,3),
        ('MATH206','Calculus',4,3),
        ('IE200','Intro to Engineering',3,3),
        ('EE201','Matlab Programming',3,3),
        ('MATH207','Diff Equations',4,4),
        ('MENG102','Engineering Drawing',4,4),
        ('EE301', 'Signals and Systems', 3, 5),     
        ('BME200', 'Intro to Biomedical', 3, 3)     
    ]
    c.execute("DELETE FROM courses")
    c.executemany("INSERT INTO courses VALUES (?,?,?,?)", courses)

    # -- Prerequisites --
    prereq = [
        ('PHYS202','PHYS110'),
        ('MATH206','MATH110'),
        ('MATH207','MATH206'),
        ('EE301', 'MATH207')
    ]
    c.execute("DELETE FROM prerequisites")
    c.executemany("INSERT INTO prerequisites VALUES (?,?)", prereq)

    # -- Program Plans --
    plans = [
        # Computer Engineering Plan
        ('Computer',3,'MATH206'),
        ('Computer',3,'EE201'),
        ('Computer',3,'IE200'),
        ('Computer',4,'MATH207'),
        ('Computer',4,'PHYS202'),

        # Biomedical Engineering Plan (Different focus)
        ('Biomedical',3,'BME200'),
        ('Biomedical',3,'PHYS202'),
        ('Biomedical',3,'MATH206'),
        ('Biomedical',4,'MATH207'),

        # Power Engineering Plan
        ('Power',3,'MATH206'),
        ('Power',3,'PHYS202'),
        ('Power',3,'MENG102'),
        ('Power',4,'MATH207'),
        ('Power',4,'EE201'),

        # Communications Engineering Plan
        ('Comm',3,'MATH206'),
        ('Comm',3,'EE201'),
        ('Comm',4,'MATH207'),
        ('Comm',5,'EE301')
    ]
    c.execute("DELETE FROM program_plans")
    c.executemany("INSERT INTO program_plans VALUES (?,?,?)", plans)

    # -- Faculty --
    faculty = [
        ('F001','Dr. Abdullah Al-Malki','malki@kau.edu.sa','hgvfg22','Physics'),
        ('F002','Dr. Hamad Al-Fifi','fifi@kau.edu.sa','jdkfhv447','Mathematics'),
        ('F003','Dr. Saleh Al-Harthy','harthy@kau.edu.sa','ooeukl2234','Industrial Engineering'),
        ('F004','Dr. Yousef Al-Saadi','saadi@kau.edu.sa','#kfvhv99','Electrical Eng'),
        ('F005','Dr. Majed Al-Jahdali','jahdali@kau.edu.sa','pkrjj23@','Mathematics'),
        ('F006','Dr. Adel Al-Mutairi','adel@kau.edu.sa','kfj89uie','Mechanical Eng'),
        ('F007','Dr. Sami Al-Ghamdi','sami@kau.edu.sa','ldkk113%','Physics'),
        ('F008','Dr. Hazza Al-Qahtani','hazza@kau.edu.sa','lkekroro90&','Industrial Engineering'),
        ('F009','Dr. Mohammed Al-Dosari','mdosari@kau.edu.sa','jfhkjfh@','Electrical Eng'),
        ('F010','Dr. Rashed Al-Shamrani','rashed@kau.edu.sa','jdhgjh223','Mechanical Eng')
    ]
    c.execute("DELETE FROM faculty")
    c.executemany("INSERT INTO faculty VALUES (?,?,?,?,?)", faculty)

    # -- Sections --
    sections = [
        ('PHYS202',1,'Sun Tue Thu','08:00','08:50','F001','2025'),
        ('PHYS202',2,'Mon Wed','10:00','11:15','F007','2025'),
        ('PHYS202',3,'Sun Tue Thu','12:00','12:50','F001','2025'),
        ('MATH206',1,'Sun Tue Thu','09:00','09:50','F002','2025'),
        ('MATH206',2,'Mon Wed','12:00','13:15','F005','2025'),
        ('MATH206',3,'Sun Tue Thu','14:00','14:50','F002','2025'),
        ('IE200',1,'Sun Tue','11:00','12:15','F003','2025'),
        ('IE200',2,'Mon Wed','08:00','09:15','F008','2025'),
        ('IE200',3,'Tue Thu','13:00','14:15','F003','2025'),
        ('EE201',1,'Sun Tue Thu','10:00','10:50','F004','2025'),
        ('EE201',2,'Mon Wed','14:00','15:15','F009','2025'),
        ('EE201',3,'Sun Tue Thu','15:00','15:50','F004','2025'),
        ('MATH207',1,'Sun Tue Thu','08:00','08:50','F002','2025'),
        ('MATH207',2,'Mon Wed','11:00','12:15','F005','2025'),
        ('MATH207',3,'Sun Tue Thu','13:00','13:50','F002','2025'),
        ('MENG102',1,'Sun Tue','09:00','10:15','F006','2025'),
        ('MENG102',2,'Mon Wed','12:00','13:15','F010','2025'),
        ('MENG102',3,'Tue Thu','14:00','15:15','F006','2025'),
        ('EE301',1,'Sun Tue Thu','09:00','09:50','F004','2025'), 
        ('BME200',1,'Mon Wed','08:00','09:15','F001','2025')     
    ]
    c.execute("DELETE FROM sections")
    c.execute("DELETE FROM sqlite_sequence WHERE name='sections'")
    c.executemany("INSERT INTO sections(course_code,section_number,days,start_time,end_time,faculty_id,semester) VALUES (?,?,?,?,?,?,?)", sections)

    # -- Faculty Teaching --
    faculty_teaching = []
    for i in range(1,21):
        faculty_teaching.append(('F001', i)) 

    c.execute("DELETE FROM faculty_teaching")
    # Cleanups
    c.execute("DELETE FROM transcript")
    c.execute("DELETE FROM registrations")

    conn.commit()
    conn.close()
    print("Database populated with SPECIFIC Program Plans (Computer, Biomedical, etc).")

if __name__ == "__main__":
    create_database()