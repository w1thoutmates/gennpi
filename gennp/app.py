import time
from random import choice, randint
import flet as ft
from flet import *

class DarkRedTheme:
    def __init__(self):
        self.primary_color = ft.colors.RED_500
        self.accent_color = ft.colors.RED_700
        self.text_color = ft.colors.WHITE
        self.background_color = ft.colors.BLACK
        self.font_family = "Arial"
        self.font_size = 16

    def apply_theme(self, page):
        page.theme = ft.Theme(
            color_scheme=ft.ColorScheme(
                primary=self.primary_color,
                secondary=self.accent_color,
                background=self.background_color,
                surface=self.background_color,
                on_primary=self.text_color,
                on_secondary=self.text_color,
                on_background=self.text_color,
                on_surface=self.text_color,
            ),
        )
        page.update()


def load_funny_words(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().split()


def random_case(word):
    randcase = randint(1, 4)
    if randcase == 1:
        return ''.join(choice((str.upper, str.lower))(c) for c in word)
    if randcase == 2:
        return word.capitalize()
    if randcase == 3:
        if len(word) <= 1:
            return word.upper()
        return word[0].upper() + word[1:-1].lower() + word[-1].upper()
    if randcase == 4:
        if len(word) <= 2:
            return word.lower()
        return word[0].lower() + word[1:-1].upper() + word[-1].lower()


def generate_password(scenario, funny_words):
    special_chars = "!@#$%^&*()—_+=;:,./?\\|`~[]{}"
    funny_word = choice(funny_words)
    number = f"{randint(100, 999)}"
    special_char = choice(special_chars)

    if scenario == "Первый сценарий":
        funny_word = random_case(funny_word)
        return f"{special_char}{funny_word}{number}"
    elif scenario == "Второй сценарий":
        funny_word = random_case(funny_word)
        return f"{funny_word}{number}{special_char}"
    elif scenario == "Третий сценарий":
        filtered_words = [word for word in funny_words if 4 <= len(word) <= 9]
        funny_word = random_case(choice(filtered_words))
        another_word = choice(filtered_words)
        return f"{funny_word}{special_char}{another_word}{number}"
    else:
        return "Сценарий не выбран."


def main(page: ft.Page):
    def generate(e):
        if dd.value == "":
            t.value = "Сценарий не выбран."
            t.color = ft.colors.RED
        else:
            password = generate_password(dd.value, funny_words)
            tf.value = password
            t.value = ""
            tf.border = ft.InputBorder.OUTLINE
            password_history.append(password)
        page.update()

    def close(e):
        page.window.close()

    def collapse(e):
        page.window_minimized = True
        page.update()

    def show_history(e):
        history_dialog.content.controls = [
            ft.Row([
                ft.Text(f"{i + 1}. {pw}", width=200),
                ft.IconButton(
                    icon=ft.icons.CONTENT_COPY,
                    icon_color="blue300",
                    icon_size=20,
                    on_click=lambda e, pw=pw: copy_password(pw)
                    )
            ]) for i, pw in enumerate(password_history)
        ] + [copied_text]
        history_dialog.open = True
        page.update()

    def close_history(e):
        history_dialog.open = False
        page.update()

    def copy_password(password):
        page.set_clipboard(password)
        copied_text.value = "Пароль скопирован"
        copied_text.color = ft.colors.GREEN
        page.update()

    dark_red_theme = DarkRedTheme()
    dark_red_theme.apply_theme(page)

    page.title = "Генератор паролей"
    page.window.icon = ft.icons.PASSWORD

    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window.title_bar_hidden = True
    page.window.resizable = False
    page.window.center()

    page.window.width = 550
    page.window.height = 300

    t = ft.Text()

    dd = ft.Dropdown(
        border_radius=10,
        width=185,
        label="Сценарий",
        options=[
            ft.dropdown.Option("Первый сценарий"),
            ft.dropdown.Option("Второй сценарий"),
            ft.dropdown.Option("Третий сценарий"),
        ],
        value="",
    )

    tf = ft.TextField(
        label="Ожидаемый пароль",
        border_radius=10,
        width=185,
        read_only=True,
    )

    submit_btn = ft.ElevatedButton(
        text=">>",
        on_click=generate,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=50),
            padding=2,
        ),
        content=ft.Text(
            ">>",
            size=16,
            color=ft.colors.GREY_400,
            weight=ft.FontWeight.BOLD,
        ),
    )

    cls_btn = ft.IconButton(
        icon=ft.icons.CLOSE,
        icon_color="red300",
        icon_size=20,
        on_click=close,
    )

    collapse_btn = ft.IconButton(
        icon=ft.icons.MINIMIZE_OUTLINED,
        icon_color="green300",
        icon_size=20,
        on_click=collapse,
    )

    history_btn = ft.IconButton(
        icon=ft.icons.HISTORY,
        icon_color="blue300",
        icon_size=20,
        on_click=show_history,
    )

    password_history = []
    copied_text = ft.Text(value="", color=ft.colors.GREEN)

    history_dialog = ft.AlertDialog(
        title=ft.Text("История паролей"),
        content=ft.Column(
            controls=[
                ft.Row([
                    ft.Text(f"{i + 1}. {pw}", width=200),
                    ft.IconButton(
                        icon=ft.icons.CONTENT_COPY,
                        icon_color="blue300",
                        icon_size=20,
                        on_click=lambda e, pw=pw: copy_password(pw)
                    )
                ]) for i, pw in enumerate(password_history)
            ],
            scroll=ft.ScrollMode.AUTO,
            height=200,
        ),
        actions=[
            copied_text,
            ft.TextButton("Закрыть", on_click=close_history),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    icon = ft.Image(src="icon.png", width=100, height=100, fit=ft.ImageFit.CONTAIN)

    stack = ft.Stack(
        [
            ft.Container(
                content=tf,
                left=330,
                top=100,
            ),
            ft.Container(
                content=dd,
                top=100,
            ),
            ft.Container(
                content=submit_btn,
                left=233,
                top=100,
                width=50,
                height=50,
            ),
            ft.Container(
                content=t,
                top=155,
                left=12,
            ),
            ft.Container(
                content=cls_btn,
                left=480,
                top=-5,
            ),
            ft.Container(
                content=collapse_btn,
                left=445,
                top=-5,
            ),
            ft.Container(
                content=history_btn,
                left=410,
                top=-5,
            ),
            ft.Container(
                content=icon,
                left=-20,
                top=-20,
            ),
        ]
    )

    page.add(stack)
    page.overlay.append(history_dialog)

    funny_words = load_funny_words("funny_words.txt")

    time.sleep(1)
    page.update()


ft.app(target=main)
