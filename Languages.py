class Language:
    def __init__(self, language):
        self.set_en()

        if language == "ru":
            self.set_ru()

    def set_en(self):
        self.months = ("January", 'February', "March",
                       "April", "May", "June",
                       "July", "August", "September",
                       "October", "November", "December")
        self.week = ("Mo", "Tu", "We", "Th", "Fr", "Sa", "Su")
        self.day = "Day"
        self.month = "Month"
        self.language = "Language"
        self.next = "->"
        self.prev = "<-"
        self.theme = "Theme"

    def set_ru(self):
        self.months = ("Январь", 'Февраль', "Март",
                       "Апрель", "Май", "Июнь",
                       "Июль", "Август", "Сентябрь",
                       "Октябрь", "Ноябрь", "Декабрь")
        self.week = ("Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд")
        self.day = "День"
        self.month = "Месяц"
        self.language = "Язык"
        self.next = "->"
        self.prev = "<-"
        self.theme = "Тема"

    def get_label_month(self, numb):
        return self.months[int(numb)-1]