class Language:
    def __init__(self, language):
        self.set_en()
        self.languages = {"en": "English", "ru": "Русский"}
        if language == "ru":
            self.set_ru()

    def set_en(self):
        self.current_lang = "en"
        self.months = ("January", 'February', "March",
                       "April", "May", "June",
                       "July", "August", "September",
                       "October", "November", "December")
        self.week = ("Mo", "Tu", "We", "Th", "Fr", "Sa", "Su")
        self.day = "Day"
        self.month = "Month"
        self.language = "Language"
        self.theme = "Theme"
        self.current_day = "Current day"
        self.day_is_empty = "Day is empty"
        self.choose_language = "Choose language"
        self.choose_theme = "Choose theme"
        self.confirm = "Confirm"
        self.themes = {"light": "Light", "dark": "Dark"}

    def set_ru(self):
        self.current_lang = "ru"
        self.months = ("Январь", 'Февраль', "Март",
                       "Апрель", "Май", "Июнь",
                       "Июль", "Август", "Сентябрь",
                       "Октябрь", "Ноябрь", "Декабрь")
        self.week = ("Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд")
        self.day = "День"
        self.month = "Месяц"
        self.language = "Язык"
        self.theme = "Тема"
        self.day_is_empty = "Нет записей"
        self.current_day = "Текущий день"
        self.choose_language = "Смена языка"
        self.confirm = "Подтвердить"
        self.choose_theme = "Смена темы"
        self.themes = {"light": "Светлая", "dark": "Тёмная"}

    def get_label_month(self, numb):
        return self.months[int(numb)-1]

    def update(self, language):
        if language == "ru":
            self.set_ru()
        else:
            self.set_en()