from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.graphics import Rectangle, Color
from kivy.core.window import Window
Window.size = (360, 640)

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
        # self.add_widget(Button(background_color=(2, 2, 2, 1), disabled=True, size_hint=(1, .055)))
        self.week_line1 = Label(text="_"*100, size_hint=(1, .005), color=style.text_color)
        self.add_widget(self.week_line1)
        self.week_layout = Week_layout()
        self.add_widget(self.week_layout)
        self.week_line2 = Label(text="_" * 100, size_hint=(1, .005), color=style.text_color)
        self.add_widget(self.week_line2)

        self.month_layout = Month_layout(self.top_layout)
        self.add_widget(self.month_layout)

        self.preview = Preview_note()
        self.add_widget(self.preview)
        self.bottom = Bottom_layout(self)
        self.add_widget(self.bottom)

        self.update()

    def update(self):
        self.month_layout.update_month()
        self.top_layout.update()
        self.bottom.update()
        self.preview.update()
        self.week_line1.color = style.text_color
        self.week_line2.color = style.text_color

        with self.canvas.before:
            Color(style.main_bg[0], style.main_bg[1], style.main_bg[2])
            self.rect = Rectangle(size=(3000, 3000), pos=self.pos)


class Top_menu_layout(BoxLayout):
    def __init__(self):
        super(Top_menu_layout, self).__init__()
        self.menu_btn = Button(on_release=self.press_menu_btn, size_hint=(.3, 1), background_normal=style.menu)
        self.add_widget(self.menu_btn)
        self.date_label = Button(text="", on_release=self.date_btn)
        self.update()
        self.add_widget(self.date_label)

    def press_menu_btn(self, args):
        app.window.main_window.sidebar.toggle_state()

    def date_btn(self, args):
        app.window.change_month_window.change_month_layout.update()
        app.window.transition.direction = "down"
        app.window.current = "change_month"

    def update(self):
        self.menu_btn.background_normal = style.menu
        self.date_label.text = str(date.active_year) + " " + language.months[date.active_month - 1]
        self.date_label.color = style.text_color

class Week_layout(BoxLayout):
    def __init__(self):
        super(Week_layout, self).__init__()
        self.week_days = [0]*7
        for numb, day in enumerate(language.week):
            self.week_days[numb] = Label(text=day)
            if numb <= 4:
                self.week_days[numb].color = style.text_color
            else:
                self.week_days[numb].color = style.text_weekend_color
            self.add_widget(self.week_days[numb])

    def update(self):
        for numb, day in enumerate(language.week):
            self.week_days[numb].text = day
            if numb <= 4:
                self.week_days[numb].color = style.text_color
            else:
                self.week_days[numb].color = style.text_weekend_color

class Day_of_month_layout(BoxLayout):
    def __init__(self, grid, day):
        super(Day_of_month_layout, self).__init__()
        self.day = day
        self.grid = grid
        self.add_button()
        self.add_mark()

    def add_button(self):
        self.day_btn = Button()

        if (self.day == date.current_date.day
            and date.current_date.month == date.active_month
            and date.current_date.year == date.active_year):
            self.day_btn.background_normal = style.bg_n_current_btn
        elif self.day == date.active_day:
            self.day_btn.background_normal = style.bg_n_active_btn

        self.day_btn.color = style.text_color
        self.day_btn.text = str(self.day)
        self.day_btn.bind(on_release=self.press_day_btn)
        self.add_widget(self.day_btn)

    def add_mark(self):
        self.mark = Label(text="",
                          size_hint=(1, .01),
                          color="white",
                          text_size=(self.size[0]*1.15, self.size[1]*1.15),
                          halign="center",
                          valign="top")
        if db.is_noted_day(day=self.day,
                           month=date.active_month,
                           year=date.active_year):
            self.mark.text = "."
        self.mark.color = style.mark_color
        self.mark.font_size = 50
        self.add_widget(self.mark)

    def press_day_btn(self, args):
        if date.active_day == int(args.text):
            app.window.update_day_window()
            app.window.transition.direction = "left"
            app.window.current = "day"
        else:
            date.active_day = int(args.text)
            self.grid.update_month()
            app.window.main_window.main_layout.preview.update()


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
        for iday in range(days_in_month):
            self.days[iday] = Day_of_month_layout(self, iday+1)
            self.add_widget(self.days[iday])

        self.days_in_next_month_btns = []
        if last_weekday != 6:
            self.days_in_next_month_btns = [0] * (6 - last_weekday)
            for i in range(6 - last_weekday):
                self.days_in_next_month_btns[i] = Button(text=str(i + 1), on_release=self.next_btn,
                                                         background_color="black", color=style.gray_for_text_in_btn)
                self.add_widget(self.days_in_next_month_btns[i])

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
                                                         on_release=self.prev_btn, background_color="black",
                                                         color=style.gray_for_text_in_btn)
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

class Preview_note(TextInput):
    def __init__(self):
        super(Preview_note, self).__init__()
        self.size_hint = (1, .5)
        self.disabled = True
        self.disabled_foreground_color = style.preview_text
        self.background_color = style.bg_preview
        self.update()

    def update(self):
        day = date.active_day
        month = date.active_month
        year = date.active_year
        if db.is_noted_day(day, month, year):
            text = db.get_note_of_day(day, month, year)
            if text[50:51]:
                self.text = text[0:50] + '...'
            else:
                self.text = text
        else:
            self.text = language.day_is_empty


class Bottom_layout(BoxLayout):
    def __init__(self, main_layout):
        super(Bottom_layout, self).__init__()
        self.main_layout = main_layout
        self.prev_btn = Button(background_normal=style.arrow_left, on_release=self.press_prev_btn)
        self.next_btn = Button(background_normal=style.arrow_right, on_release=self.press_next_btn)
        self.add_widget(self.prev_btn)
        self.add_widget(self.next_btn)

    def press_next_btn(self, args):
        if date.active_month == 12:
            date.active_month = 1
            date.active_year += 1
        else:
            date.active_month += 1
        self.main_layout.update()

    def press_prev_btn(self, args):
        if date.active_month == 1:
            date.active_month = 12
            date.active_year -= 1
        else:
            date.active_month -= 1
        self.main_layout.update()

    def update(self):
        self.prev_btn.background_normal = style.arrow_left
        self.next_btn.background_normal = style.arrow_right


class SideBar(NavigationDrawer):
    def __init__(self):
        super(SideBar, self).__init__()
        side_Layout = BoxLayout(orientation="vertical")

        title_name = Label(text="CalendarApp", size_hint=(1, .5), halign="left")
        side_Layout.add_widget(title_name)

        self.open_day_btn = Button(text=language.day, on_press=self.open_day)
        side_Layout.add_widget(self.open_day_btn)

        # self.open_month_btn = Button(text=language.month, on_press=self.open_month,  disabled=True)
        # side_Layout.add_widget(self.open_month_btn)
        # self.open_month_btn.disabled = True

        self.back_to_current_date = Button(text=language.current_day,
                                           on_press=self.back_to_current_date_btn)
        side_Layout.add_widget(self.back_to_current_date)

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
        app.window.day_window.day_layout.update()
        app.window.transition.direction = "left"
        app.window.current = "day"

    def back_to_current_date_btn(self, args):
        self.toggle_state()
        date.set_current_date()
        app.window.main_window.main_layout.update()

    def open_month(self, args):
        # args.disabled = True
        # self.toggle_state()
        # self.open_day_btn.disabled = False
        pass

    def show_language_setting(self, args):
        self.lang = Language_popup()
        popup = Popup(size_hint=(1, 0.5), title=language.choose_language, content=self.lang)
        self.lang.set_popup(popup)
        popup.open()

    def show_theme_setting(self, args):
        self.theme = Theme_popup()
        popup = Popup(size_hint=(1, 0.5), title=language.choose_theme, content=self.theme)
        self.theme.set_popup(popup)
        popup.open()

    def update(self):
        self.open_day_btn.text = language.day
        self.back_to_current_date.text = language.current_day
        self.language_btn.text = language.language
        self.theme_btn.text = language.theme


class Language_popup(BoxLayout):
    def __init__(self):
        super(Language_popup, self).__init__()

        self.language_buttons = [None] * len(language.languages)
        for i, key_lang in enumerate(language.languages):
            self.language_buttons[i] = Button(text=language.languages[key_lang], on_release=self.press_change_btn)
            if key_lang == language.current_lang:
                self.language_buttons[i].disabled = True
            self.add_widget(self.language_buttons[i])
        bottom = BoxLayout()
        self.confirm = Button(text=language.confirm)
        bottom.add_widget(Widget())
        bottom.add_widget(self.confirm)
        self.add_widget(bottom)

    def press_change_btn(self, args):
        for key, lang in language.languages.items():
            if lang == args.text:
                language.current_lang = key
                language.update()
                break
        app.window.update_app()
        for btn in self.language_buttons:
            if btn.disabled:
                btn.disabled = False
                break
        args.disabled = True
        self.update()

    def set_popup(self, popup):
        self.popup = popup
        self.confirm.bind(on_release=self.press_confirm)

    def press_confirm(self, args):
        db.update_setting("Language", language.current_lang)
        self.popup.dismiss()

    def update(self):
        self.popup.title = language.choose_language
        self.confirm.text = language.confirm


class Theme_popup(BoxLayout):
    def __init__(self):
        super(Theme_popup, self).__init__()

        self.theme_buttons = [None] * len(style.themes)
        for i, key_theme in enumerate(style.themes):
            self.theme_buttons[i] = Button(text=language.themes[style.themes[key_theme]],
                                           on_release=self.press_change_btn)
            if style.themes[key_theme] == style.current_theme:
                self.theme_buttons[i].disabled = True
            self.add_widget(self.theme_buttons[i])
        bottom = BoxLayout()
        self.confirm = Button(text=language.confirm)
        bottom.add_widget(Widget())
        bottom.add_widget(self.confirm)
        self.add_widget(bottom)

    def press_change_btn(self, args):
        for key, theme in style.themes.items():
            if language.themes[theme] == args.text:
                style.current_theme = theme
                style.update()
                break
        app.window.update_app()
        for btn in self.theme_buttons:
            if btn.disabled:
                btn.disabled = False
                break
        args.disabled = True
        self.update()

    def set_popup(self, popup):
        self.popup = popup
        self.confirm.bind(on_release=self.press_confirm)

    def press_confirm(self, args):
        db.update_setting("Theme", style.current_theme)
        self.popup.dismiss()

    def update(self):
        self.popup.title = language.choose_theme
        self.confirm.text = language.confirm

class MainWindow(Screen):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.sidebar = SideBar()
        self.main_layout = Main_layout()
        self.sidebar.add_widget(self.main_layout)
        self.add_widget(self.sidebar)

    def draw_top_menu_bar(self):
        top_layout = BoxLayout()
        return top_layout

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
        self.dayinfo.set_topbar(self.topbar)
        self.add_widget(self.topbar)
        self.add_widget(self.dayinfo)
        self.add_widget(Day_bottom_layout(self))


    def update(self):
        self.topbar.update_day_label()
        self.dayinfo.update()

        with self.canvas.before:
            Color(style.main_bg[0], style.main_bg[1], style.main_bg[2])
            self.rect = Rectangle(size=(3000, 3000), pos=self.pos)

class Day_topbar(BoxLayout):
    def __init__(self, dayinfo):
        super(Day_topbar, self).__init__()
        self.dayinfo = dayinfo
        self.add_widget(Button(text="<-", on_release=self.back_btn, size_hint=(0.5, 1)))
        self.day_label = Label()
        self.update_day_label()
        self.add_widget(self.day_label)
        self.save = Button(text="|/", on_release=self.save_btn, size_hint=(0.5, 1), disabled=True)
        self.add_widget(self.save)

    def update_day_label(self):
        self.day_label.text = (str(date.active_day) + " " +
                               language.months[date.active_month - 1] + " " +
                               str(date.active_year))
        self.day_label.color = style.text_color

    def back_btn(self, args):
        app.window.main_window.main_layout.update()
        app.window.transition.direction = "right"
        app.window.current = "month"

    def save_btn(self, args):
        self.dayinfo.modify_note()
        self.save.disabled = True


class DayInfo(BoxLayout):
    def __init__(self):
        super(DayInfo, self).__init__()
        self.topbar = None
        self.day_text_input = TextInput()
        self.day_text_input.bind(focus=self.on_focus)
        self.update()
        self.add_widget(self.day_text_input)

    def set_topbar(self, topbar):
        self.topbar = topbar

    def on_focus(self, args, focus):
        if focus:
            self.topbar.save.disabled = False

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
        self.add_widget(Button(background_normal=style.arrow_left, on_release=self.prev_btn))
        self.add_widget(Button(background_normal=style.arrow_right, on_release=self.next_btn))

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

##################### ChangeMonthWindow Start ###########################

class ChangeMonthWindow(Screen):
    def __init__(self):
        super(ChangeMonthWindow, self).__init__()
        self.change_month_layout = Change_month_layout()
        self.add_widget(self.change_month_layout)


class Change_month_layout(BoxLayout):
    def __init__(self):
        super(Change_month_layout, self).__init__()
        self.year_button = Button(text="#Year", on_release=self.year_btn, color=style.text_color)
        self.add_widget(self.year_button)
        self.add_buttons_of_months()
        self.update()

    def add_buttons_of_months(self):
        self.buttons_of_months = [0] * 12
        for month in range(12):
            self.buttons_of_months[month] = Button(text="#Month", on_release=self.month_btn, color=style.text_color)
            self.add_widget(self.buttons_of_months[month])

    def year_btn(self, args):
        app.window.change_year_window.change_year_layout.update()
        app.window.transition.direction = "down"
        app.window.current = "change_year"

    def month_btn(self, args):
        month = language.months.index(args.text) + 1
        date.active_month = month
        app.window.main_window.main_layout.update()
        app.window.transition.direction = "down"
        app.window.current = "month"

    def update(self):
        for month, button in enumerate(self.buttons_of_months):
            button.text = language.months[month]
            if month + 1 == date.active_month and self.year_button.text == str(date.active_year):
                button.background_normal = style.bg_n_current_btn
            else:
                button.background_normal = style.bg_empty
            button.color = style.text_color
        self.year_button.text = str(date.active_year)
        self.year_button.color = style.text_color

        with self.canvas.before:
            Color(style.main_bg[0], style.main_bg[1], style.main_bg[2])
            self.rect = Rectangle(size=(3000, 3000), pos=self.pos)

##################### ChangeMonthWindow End ############################

##################### ChangeYearWindow Start ###########################


class ChangeYearWindow(Screen):
    def __init__(self):
        super(ChangeYearWindow, self).__init__()
        self.range_years = [1951, 2100]
        self.scroll = Scroll()
        self.scroll.scroll_y = self.get_scroll_pos()
        self.change_year_layout = Change_year_layout(self.range_years)
        self.scroll.add_widget(self.change_year_layout)
        self.add_widget(self.scroll)

    def get_scroll_pos(self):
        return (self.range_years[1] - date.active_year) / ((self.range_years[1] - self.range_years[0]) / 100) / 100


class Scroll(ScrollView):
    def __init__(self):
        super(Scroll, self).__init__()
        self.update()

    def update(self):
        with self.canvas.before:
            Color(style.main_bg[0], style.main_bg[1], style.main_bg[2])
            self.rect = Rectangle(size=(3000, 3000), pos=self.pos)

class Change_year_layout(BoxLayout):
    def __init__(self, range_years):
        super(Change_year_layout, self).__init__()
        self.buttons_of_years = []
        self.range_years = range_years
        self.numb_year = self.range_years[1] - self.range_years[0]
        self.add_btns()

    def add_btns(self):
        self.buttons_of_years = [0] * self.numb_year
        for num, year in enumerate(range(self.range_years[0], self.range_years[1])):
            self.buttons_of_years[num] = Button(text=str(year), on_release=self.year_btn, color=style.text_color)
            if year == date.active_year:
                self.buttons_of_years[num].background_normal = style.bg_n_current_btn
            else:
                self.buttons_of_years[num].background_normal = style.bg_empty
            self.add_widget(self.buttons_of_years[num])


    def year_btn(self, args):
        date.active_year = int(args.text)
        app.window.change_month_window.change_month_layout.update()
        app.window.transition.direction = "down"
        app.window.current = "change_month"

    def remove_btns(self):
        if self.buttons_of_years == []:
            return
        for btn in self.buttons_of_years:
            self.remove_widget(btn)
        self.buttons_of_years = []

    def update(self):
        for btn in self.buttons_of_years:
            btn.color = style.text_color
            if int(btn.text) == date.active_year:
                btn.background_normal = style.bg_n_current_btn
            else:
                btn.background_normal = style.bg_empty


        # self.remove_btns()
        # self.add_btns()



##################### ChangeYearWindow End #############################


class WindowManager(ScreenManager):
    def __init__(self):
        super(WindowManager, self).__init__()
        self.main_window = MainWindow()
        self.add_widget(self.main_window)
        self.day_window = DayWindow()
        self.add_widget(self.day_window)
        self.change_year_window = ChangeYearWindow()
        self.add_widget(self.change_year_window)
        self.change_month_window = ChangeMonthWindow()
        self.add_widget(self.change_month_window)


    def update_app(self):
        self.main_window.main_layout.update()
        self.day_window.day_layout.update()
        self.change_month_window.change_month_layout.update()
        self.main_window.sidebar.update()
        self.main_window.main_layout.week_layout.update()
        self.change_year_window.scroll.update()

    def update_day_window(self):
        self.day_window.day_layout.update()


class CalendarApp(App):
    def build(self):
        self.window = WindowManager()
        return self.window

def get_setting():
    lang = db.get_setting("Language")
    if lang is None:
        db.insert_setting("Language", "en")
        lang = "en"
    language.current_lang = lang
    language.update()

    theme = db.get_setting("Theme")
    if theme is None:
        db.insert_setting("Theme", "light")
        theme = "light"
    style.current_theme = theme
    style.update()



if __name__ == "__main__":
    db = DataBase.DB()
    style = Colors.Style()
    date = DataBase.Date()
    language = Languages.Language()
    get_setting()
    app = CalendarApp()
    app.run()