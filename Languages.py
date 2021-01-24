class Language:
    def __init__(self):
        self.months = ()

    def set_en(self):
        self.months = ("January", 'February', "March",
                       "April", "May", "June",
                       "July", "August", "September",
                       "October", "November", "December")

    def set_ru(self):
        pass

    def get_label_month(self, numb):
        return self.months[int(numb)-1]