class Language:
    def __init__(self):
        self.months = ()

    def set_en(self):
        self.months = ("January", 'February', "March",
                       "April", "May", "June",
                       "July", "August", "September",
                       "October", "November", "December")
        self.day = "Day"
        self.month = "Month"
        self.language = "Language"

    def set_ru(self):
        pass

    def get_label_month(self, numb):
        return self.months[int(numb)-1]