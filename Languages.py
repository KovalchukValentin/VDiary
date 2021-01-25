class Language:
    def __init__(self):
        self.months = ()

    def set_en(self):
        self.months = ("January", 'February', "March",
                       "April", "May", "June",
                       "July", "August", "September",
                       "October", "November", "December")
        self.week = ("Mo", "Tu", "We", "Th", "Fr", "Sa", "Su")
        self.day = "Day"
        self.month = "Month"
        self.language = "Language"
        self.next = "Next"
        self.prev = "Prev"

    def set_ru(self):
        pass

    def get_label_month(self, numb):
        return self.months[int(numb)-1]