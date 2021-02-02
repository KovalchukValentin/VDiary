class Style:
    def __init__(self):
        self.themes = {1: "dark", 2: "light"}
        self.current_theme = self.themes[1]
        self.update_theme()

    def update_theme(self):
        if self.current_theme == self.themes[1]:
            self.main_bg = [.15, .15, .15]
        elif self.current_theme == self.themes[2]:
            self.main_bg = []
        return None