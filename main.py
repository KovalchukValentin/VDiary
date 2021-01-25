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
        for day in language.week:
            self.add_widget(Label(text=day))

class Top_menu_layout(BoxLayout):
    def __init__(self):
        super(Top_menu_layout, self).__init__()
        self.add_widget(Button())

class Month_layout(GridLayout):
    def __init__(self):
        super(Month_layout, self).__init__()
        self.cols = 7
        self.active_day = int(data.current_day)
        self.active_month = int(data.current_month)
        self.add_day_btns(self.active_month)

    def add_day_btns(self, month: int):
        self.days = [0] * 31
        for i in range(data.days_in_months[month-1]):
            if i+1 == data.current_day and data.current_month == month:
                self.days[i] = Button(text=str(i+1), on_release=self.day_btn)
            elif i+1 == self.active_day:
                self.days[i] = Button(text=str(i + 1), on_release=self.day_btn)
            else:
                self.days[i] = Button(text=str(i+1), on_release=self.day_btn)
            self.add_widget(self.days[i])

    def day_btn(self, args):
        pass


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
        self.sidebar.add_widget(self.draw_month(data.current_month))
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

        self.days_in_month = []
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
    data = DataBase.Data()
    language = Languages.Language()
    language.set_en()
    app = CalendarApp()
    app.run()