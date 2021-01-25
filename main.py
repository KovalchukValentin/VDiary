from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button

from kivy.graphics import Rectangle, Color

from kivy.lang import Builder

from kivy.garden.navigationdrawer import NavigationDrawer

import DataBase
import Languages


class Week_layout(BoxLayout):
    def __init__(self):
        super(Week_layout, self).__init__()
        for numb, day in enumerate(language.week):
            if numb <= 4:
                self.add_widget(Label(text=day))
            else:
                self.add_widget(Label(text=day, color="red"))


class Top_menu_layout(BoxLayout):
    def __init__(self):
        super(Top_menu_layout, self).__init__()
        self.add_widget(Button())


class Month_layout(GridLayout):
    def __init__(self):
        super(Month_layout, self).__init__()
        self.cols = 7
        self.active_day = int(date.current_date.day)
        self.active_month = int(date.current_date.month)
        self.active_year = int(date.current_date.year)
        self.add_day_btns(self.active_month, self.active_year)

    def add_day_btns(self, month: int, year: int):
        self.days = [0] * 42
        first_weekday = date.get_weekday(1, month, year)
        days_in_month = date.days_in_months[month - 1]
        last_weekday = date.get_weekday(days_in_month, month, year)

        if first_weekday != 0:
            if month - 2 == -1:
                days_in_prev_month = date.days_in_months[11]
            else:
                days_in_prev_month = date.days_in_months[month - 2]

            for i in range(first_weekday):
                self.add_widget(Button(text=str(days_in_prev_month - first_weekday + i + 1), disabled=True))

        for i in range(days_in_month):
            if i+1 == date.current_date.day and date.current_date.month == month:
                self.days[i] = Button(text=str(i+1), on_release=self.day_btn)
            elif i+1 == self.active_day:
                self.days[i] = Button(text=str(i + 1), on_release=self.day_btn)
            else:
                self.days[i] = Button(text=str(i+1), on_release=self.day_btn)
            self.add_widget(self.days[i])

        if last_weekday != 6:
            for i in range(7 - last_weekday):
                self.add_widget(Button(text=str(i + 1), disabled=True))

    def get_count_buttons(self):
        pass

    def day_btn(self, args):
        app.window.transition.direction = "left"
        app.window.current = "day"


class SideBar(NavigationDrawer):
    def __init__(self):
        super(SideBar, self).__init__()
        side_Layout = BoxLayout(orientation="vertical")

        title_name = Label(text="CalendarApp", size_hint=(1, .5), halign="left")
        side_Layout.add_widget(title_name)

        self.open_day_btn = Button(text=language.day, on_press=self.open_day)
        side_Layout.add_widget(self.open_day_btn)

        self.open_month_btn = Button(text=language.month, on_press=self.open_month,  disabled=True)
        side_Layout.add_widget(self.open_month_btn)
        # self.open_month_btn.disabled = True

        self.language_btn = Button(text=language.language, on_press=self.show_language_setting)
        side_Layout.add_widget(self.language_btn)

        self.add_widget(side_Layout)

    def open_day(self, args):
        args.disabled = True
        self.toggle_state()
        self.open_month_btn.disabled = False

    def open_month(self, args):
        args.disabled = True
        self.toggle_state()
        self.open_day_btn.disabled = False

    def show_language_setting(self, args):
        pass


class MainWindow(Screen):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.sidebar = SideBar()
        # self.sidebar.add_widget(self.draw_top_menu_bar())
        self.sidebar.add_widget(self.draw_month(date.current_date.month))
        self.add_widget(self.sidebar)

    def view_month(self):
        pass

    def draw_top_menu_bar(self):
        top_layout = BoxLayout()
        return top_layout


    def draw_month(self, month):
        month_grid = BoxLayout(orientation="vertical")
        month_grid.add_widget(Top_menu_layout())
        month_grid.add_widget(Week_layout())
        month_grid.add_widget(Month_layout())
        return month_grid

    def open_day(self, args):
        app.window.transition.direction = "left"
        app.window.current = "data"


class DayWindow(Screen):
    def __init__(self):
        super(DayWindow, self).__init__()
        self.add_widget(Button(text="Back", on_press=self.change_window))

    def change_window(self, args):
        app.window.transition.direction = "right"
        app.window.current = "month"


class WindowManager(ScreenManager):
    def __init__(self):
        super(WindowManager, self).__init__()
        month = MainWindow()
        self.add_widget(month)
        data = DayWindow()
        self.add_widget(data)


class CalendarApp(App):
    def build(self):
        self.window = WindowManager()
        return self.window


if __name__ == "__main__":
    db = DataBase.DB()
    date = DataBase.Date()
    language = Languages.Language()
    language.set_en()
    app = CalendarApp()
    app.run()