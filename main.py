from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from kivy.graphics import Rectangle, Color

from kivy.lang import Builder

from kivy.garden.navigationdrawer import NavigationDrawer

import DataBase
import Languages
import Colors

########################## MainWindow Start  ################################
class Main_layout(BoxLayout):
    def __init__(self):
        super(Main_layout, self).__init__()

        # self.orientation = "vertical"
        self.top_layout = Top_menu_layout()
        self.add_widget(self.top_layout)

        self.add_widget(Week_layout())

        self.month_layout = Month_layout(self.top_layout)
        self.add_widget(self.month_layout)

        self.add_widget(Widget(size_hint=(1, .1)))
        self.add_widget(Bottom_layout(self))
        self.add_widget(Widget(size_hint=(1, .4)))
        self.update()

    def update(self):
        self.month_layout.update_month()
        self.top_layout.update_label()
        with self.canvas.before:
            Color(style.main_bg[0], style.main_bg[1], style.main_bg[2])
            self.rect = Rectangle(size=(3000, 3000), pos=self.pos)


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
        self.add_widget(Button(text="Menu", on_release=self.menu_btn, size_hint=(.3, 1)))
        self.date_label = Label(text="")
        self.update_label()
        self.add_widget(self.date_label)

    def menu_btn(self, args):
        app.window.main_window.sidebar.toggle_state()

    def update_label(self):
        self.date_label.text = str(date.active_year) + " " + language.months[date.active_month - 1]


class Month_layout(GridLayout):
    def __init__(self, top_layout):
        super(Month_layout, self).__init__()
        self.cols = 7
        self.top_layout = top_layout
        self.add_day_btns()
        # self.clear_days()

    def add_day_btns(self):
        month = date.active_month
        year = date.active_year

        days_in_month = date.days_in_months[month - 1]
        last_weekday = date.get_weekday(days_in_month, month, year)

        if date.active_day > days_in_month:
            date.active_day = days_in_month

        self.add_prev_month_days(month, year)


        self.days = [0] * days_in_month
        for i in range(days_in_month):
            if i+1 == date.current_date.day and date.current_date.month == month and date.current_date.year == year:
                self.days[i] = Button(text=str(i+1), on_release=self.day_btn, background_color="blue")
            elif i+1 == date.active_day:
                self.days[i] = Button(text=str(i + 1), on_release=self.day_btn, background_color="green")
            else:
                self.days[i] = Button(text=str(i+1), on_release=self.day_btn)
            self.add_widget(self.days[i])

        self.days_in_next_month_btns = []
        if last_weekday != 6:
            self.days_in_next_month_btns = [0] * (6 - last_weekday)
            for i in range(6 - last_weekday):
                self.days_in_next_month_btns[i] = Button(text=str(i + 1), on_release=self.next_btn, background_color="black")
                self.add_widget(self.days_in_next_month_btns[i])

    # def set_active_date(self, day: int, month: int, year: int):
    #     self.active_day = day
    #     self.active_month = month
    #     self.active_year = year
    def add_prev_month_days(self, current_month, current_year):
        first_weekday = date.get_weekday(1, current_month, current_year)
        self.days_in_prev_month_btns = []
        if first_weekday != 0:
            if current_month - 2 == -1:
                days_in_prev_month = date.days_in_months[11]
            else:
                days_in_prev_month = date.days_in_months[current_month - 2]

            self.days_in_prev_month_btns = [0] * first_weekday
            for i in range(first_weekday):
                self.days_in_prev_month_btns[i] = Button(text=str(days_in_prev_month - first_weekday + i + 1),
                                                         on_release=self.prev_btn, background_color="black")
                self.add_widget(self.days_in_prev_month_btns[i])

    def clear_days(self):
        for button in self.days_in_prev_month_btns:
            self.remove_widget(button)

        for button in self.days:
            try:
                self.remove_widget(button)
            except:
                continue

        for button in self.days_in_next_month_btns:
            self.remove_widget(button)

    def update_month(self):
        self.clear_days()
        self.add_day_btns()

    def day_btn(self, args):
        date.active_day = int(args.text)
        app.window.update_day_window()
        app.window.transition.direction = "left"
        app.window.current = "day"

    def next_btn(self, args):
        date.active_day = int(args.text)
        if date.active_month == 12:
            date.active_month = 1
            date.active_year += 1
        else:
            date.active_month += 1
        self.update_month()
        self.top_layout.update_label()

    def prev_btn(self, args):
        date.active_day = int(args.text)
        if date.active_month == 1:
            date.active_month = 12
            date.active_year -= 1
        else:
            date.active_month -= 1
        self.update_month()
        self.top_layout.update_label()


class Bottom_layout(BoxLayout):
    def __init__(self, main_layout):
        super(Bottom_layout, self).__init__()
        self.main_layout = main_layout
        self.add_widget(Button(text=language.prev, on_release=self.prev_btn))
        self.add_widget(Button(text=language.next, on_release=self.next_btn))

    def next_btn(self, args):
        if date.active_month == 12:
            date.active_month = 1
            date.active_year += 1
        else:
            date.active_month += 1
        self.main_layout.update()

    def prev_btn(self, args):
        if date.active_month == 1:
            date.active_month = 12
            date.active_year -= 1
        else:
            date.active_month -= 1
        self.main_layout.update()


class SideBar(NavigationDrawer):
    def __init__(self):
        super(SideBar, self).__init__()
        self.separator_image = "images/test.jpg"
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

        self.theme_btn = Button(text=language.theme, on_press=self.show_theme_setting)
        side_Layout.add_widget(self.theme_btn)

        self.add_widget(side_Layout)

        self.update()

    def open_day(self, args):
        # args.disabled = True
        self.toggle_state()
        # self.open_month_btn.disabled = False
        app.window.transition.direction = "left"
        app.window.current = "day"


    def open_month(self, args):
        # args.disabled = True
        # self.toggle_state()
        # self.open_day_btn.disabled = False
        pass

    def show_language_setting(self, args):
        pass

    def show_theme_setting(self, args):
        pass

    def update(self):
        self.open_day_btn = language.day
        self.open_month_btn = language.month
        self.language_btn = language.language
        self.theme_btn.text = language.theme


class MainWindow(Screen):
    def __init__(self):
        super(MainWindow, self).__init__()


        self.sidebar = SideBar()
        # self.sidebar.add_widget(self.draw_top_menu_bar())
        self.main_layout = Main_layout()
        self.sidebar.add_widget(self.main_layout)
        self.add_widget(self.sidebar)
    # def view_month(self):
    #     pass

    def draw_top_menu_bar(self):
        top_layout = BoxLayout()
        return top_layout

    # def draw_month(self, month):
    #
    #     return

    # def open_day(self, args):
    #     app.window.transition.direction = "left"
    #     app.window.current = "data"
########################## MainWindow End  ################################

########################## DayWindow Start ################################
class DayWindow(Screen):
    def __init__(self):
        super(DayWindow, self).__init__()
        self.day_layout = Day_layout()
        self.add_widget(self.day_layout)


class Day_layout(BoxLayout):
    def __init__(self):
        super(Day_layout, self).__init__()
        self.dayinfo = DayInfo()
        self.topbar = Day_topbar(self.dayinfo)
        self.add_widget(self.topbar)
        self.add_widget(self.dayinfo)
        self.add_widget(Day_bottom_layout(self))

    def update(self):
        self.topbar.update_day_label()
        self.dayinfo.update()

class Day_topbar(BoxLayout):
    def __init__(self, dayinfo):
        super(Day_topbar, self).__init__()
        self.dayinfo = dayinfo
        self.add_widget(Button(text="<-", on_release=self.back_btn, size_hint=(0.5, 1)))
        self.day_label = Label()
        self.update_day_label()
        self.add_widget(self.day_label)
        self.save = Button(text="|/", on_release=self.save_btn, size_hint=(0.5, 1))
        self.add_widget(self.save)

    def update_day_label(self):
        self.day_label.text = (str(date.active_day) + " " +
                               language.months[date.active_month - 1] + " " +
                               str(date.active_year))

    def back_btn(self, args):
        app.window.main_window.main_layout.update()
        app.window.transition.direction = "right"
        app.window.current = "month"

    def save_btn(self, args):
        self.dayinfo.modify_note()


class DayInfo(BoxLayout):
    def __init__(self):
        super(DayInfo, self).__init__()
        self.day_text_input = TextInput()
        self.update()
        self.add_widget(self.day_text_input)

    def update(self):
        self.day_text_input.text = db.get_note_of_day(date.active_day, date.active_month, date.active_year)

    def modify_note(self):
        db.modify_note_of_day(day=date.active_day,
                              month=date.active_month,
                              year=date.active_year,
                              note=self.day_text_input.text)


class Day_bottom_layout(BoxLayout):
    def __init__(self, day_layout):
        super(Day_bottom_layout, self).__init__()
        self.day_layout = day_layout
        # self.topbar = topbar
        self.add_widget(Button(text=language.prev, on_release=self.prev_btn))
        self.add_widget(Button(text=language.next, on_release=self.next_btn))

    def next_btn(self, args):
        if date.active_day == date.days_in_months[date.active_month - 1]:
            if date.active_month == 12:
                date.active_month = 1
                date.active_year += 1
            else:
                date.active_month += 1
            date.active_day = 1
        else:
            date.active_day += 1
        # self.topbar.update_day_label()
        self.day_layout.update()

    def prev_btn(self, args):
        if date.active_day == 1:
            if date.active_month == 1:
                date.active_month = 12
                date.active_year -= 1
            else:
                date.active_month -= 1
            date.active_day = date.days_in_months[date.active_month - 1]
        else:
            date.active_day -= 1
        # self.topbar.update_day_label()
        self.day_layout.update()


########################## DayWindow End ################################


class WindowManager(ScreenManager):
    def __init__(self):
        super(WindowManager, self).__init__()
        self.main_window = MainWindow()
        self.add_widget(self.main_window)
        self.day_window = DayWindow()
        self.add_widget(self.day_window)

    def update_day_window(self):
        self.day_window.day_layout.update()


class CalendarApp(App):
    def build(self):
        self.window = WindowManager()
        return self.window


if __name__ == "__main__":
    db = DataBase.DB()
    style = Colors.Style()
    date = DataBase.Date()
    language = Languages.Language()
    language.set_en()
    app = CalendarApp()
    app.run()