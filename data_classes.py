class Section:
    #Matches the 'sections' table in the KAU database.
    def __init__(self, section_id, course_code, days, start_time, end_time, semester):
        self.section_id = section_id
        self.course_code = course_code
        self.days = days             
        self.start_time = start_time 
        self.end_time = end_time     
        self.semester = semester

    def get_days_list(self):
        #Input: "Sun Tue Thu" -> Output: ['Sun', 'Tue', 'Thu']

        return self.days.split()

    def get_start_integer(self):
        #Input: "08:30" -> Output: 830

        return int(self.start_time.replace(':', ''))

    def get_end_integer(self):
        #Input: "09:20" -> Output: 920

        return int(self.end_time.replace(':', ''))

    def __str__(self):
        return f"{self.course_code} (Sec {self.section_id}): {self.days} {self.start_time}-{self.end_time}"