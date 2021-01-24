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

class MonthWindow(Screen):
    def __init__(self):
        super(MonthWindow, self).__init__()
        self.sidebar = SideBar()
        self.sidebar.add_widget(self.draw_month())
        self.add_widget(self.sidebar)

    def draw_top_menu_bar(self):
        pass

    def draw_month(self):
        month_grid = GridLayout()
        return month_grid

    def open_day(self, args):
        app.window.transition.direction = "left"
        app.window.current = "data"


class DayWindow(Screen):
    def __init__(self):
        super(DayWindow, self).__init__()
        self.add_widget(Button(text="Back", on_press=self.changewindow))

    def changewindow(self, args):
        app.window.transition.direction = "right"
        app.window.current = "month"

class WindowManager(ScreenManager):
    def __init__(self):
        super(WindowManager, self).__init__()
        month = MonthWindow()
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