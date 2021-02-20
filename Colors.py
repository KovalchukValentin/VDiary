class Style:
    def __init__(self):
        self.themes = {1: "dark", 2: "light"}
        self.current_theme = self.themes[2]
        self.update_theme()
        self.gray_for_text_in_btn = (.5, .5, .5, 1)

    def update_theme(self):
        if self.current_theme == self.themes[1]:
            # self.main_bg = [.15, .15, .15]
            self.main_bg = [.15, .15, .15]
            self.text_color = [.95, .95, .95]
            self.arrow_left = "images\\arrow_left_dark.png"
            self.arrow_right = "images\\arrow_right_dark.png"
            self.text_weekend_color = "#ff5a00"
            self.bg_n_current_btn = "images\current_btn.png"
            self.bg_n_active_btn = "images\\active_day_dark.png"
            self.mark_color = "#ffffff"
            self.bg_empty = "images\empty.png"
            self.menu = "images\menu_dark.png"
        elif self.current_theme == self.themes[2]:
            self.main_bg = [.95, .95, .95]
            self.text_color = [.15, .15, .15]
            self.arrow_left = "images\\arrow_left_light.png"
            self.arrow_right = "images\\arrow_right_light.png"
            self.text_weekend_color = "#ff5a00"
            self.bg_n_current_btn = "images\current_btn.png"
            self.bg_n_active_btn = "images\\active_day_dark.png"
            self.mark_color = "#ff5a00"
            self.bg_empty = "images\empty.png"
            self.menu = "images\menu_light.png"
        return None