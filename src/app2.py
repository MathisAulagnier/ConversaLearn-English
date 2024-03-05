import time
import flet as ft
import flet
from flet import AppBar
from flet import Card
from flet import Column
from flet import Container
from flet import ElevatedButton
from flet import IconButton
from flet import NavigationRail
from flet import NavigationRailDestination
from flet import Page
from flet import Row
from flet import Stack
from flet import Switch
from flet import Text
from flet import VerticalDivider
from flet import colors
from flet import icons
from flet.utils import slugify


class ResponsiveMenuLayout(Row):
    def __init__(
        self,
        page,
        pages,
        *args,
        support_routes=True,
        menu_extended=True,
        minimize_to_icons=False,
        landscape_minimize_to_icons=False,
        portrait_minimize_to_icons=False,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.page = page
        self.pages = pages

        self._minimize_to_icons = minimize_to_icons
        self._landscape_minimize_to_icons = landscape_minimize_to_icons
        self._portrait_minimize_to_icons = portrait_minimize_to_icons
        self._support_routes = support_routes

        self.expand = True

        self.navigation_items = [navigation_item for navigation_item, _ in pages]
        self.routes = [
            f"/{item.pop('route', None) or slugify(item['label'])}"
            for item in self.navigation_items
        ]
        self.navigation_rail = self.build_navigation_rail()
        self.update_destinations()
        self._menu_extended = menu_extended
        self.navigation_rail.extended = menu_extended

        page_contents = [page_content for _, page_content in pages]

        self.menu_panel = Row(
            controls=[self.navigation_rail, VerticalDivider(width=1)],
            spacing=0,
            tight=True,
        )
        self.content_area = Column(page_contents, expand=True)

        self._was_portrait = self.is_portrait()
        self._panel_visible = self.is_landscape()

        self.set_navigation_content()

        if support_routes:
            self._route_change(page.route)
            self.page.on_route_change = self._on_route_change
        self._change_displayed_page()

        self.page.on_resize = self.handle_resize

    def select_page(self, page_number):
        self.navigation_rail.selected_index = page_number
        self._change_displayed_page()

    @property
    def minimize_to_icons(self) -> bool:
        return self._minimize_to_icons or (
            self._landscape_minimize_to_icons and self._portrait_minimize_to_icons
        )

    @minimize_to_icons.setter
    def minimize_to_icons(self, value: bool):
        self._minimize_to_icons = value
        self.set_navigation_content()

    @property
    def landscape_minimize_to_icons(self) -> bool:
        return self._landscape_minimize_to_icons or self._minimize_to_icons

    @landscape_minimize_to_icons.setter
    def landscape_minimize_to_icons(self, value: bool):
        self._landscape_minimize_to_icons = value
        self.set_navigation_content()

    @property
    def portrait_minimize_to_icons(self) -> bool:
        return self._portrait_minimize_to_icons or self._minimize_to_icons

    @portrait_minimize_to_icons.setter
    def portrait_minimize_to_icons(self, value: bool):
        self._portrait_minimize_to_icons = value
        self.set_navigation_content()

    @property
    def menu_extended(self) -> bool:
        return self._menu_extended

    @menu_extended.setter
    def menu_extended(self, value: bool):
        self._menu_extended = value

        dimension_minimized = (
            self.landscape_minimize_to_icons
            if self.is_landscape()
            else self.portrait_minimize_to_icons
        )
        if not dimension_minimized or self._panel_visible:
            self.navigation_rail.extended = value

    def _navigation_change(self, e):
        self._change_displayed_page()
        self.check_toggle_on_select()
        self.page.update()

    def _change_displayed_page(self):
        page_number = self.navigation_rail.selected_index
        if self._support_routes:
            self.page.route = self.routes[page_number]
        for i, content_page in enumerate(self.content_area.controls):
            content_page.visible = page_number == i

    def _route_change(self, route):
        try:
            page_number = self.routes.index(route)
        except ValueError:
            page_number = 0

        self.select_page(page_number)

    def _on_route_change(self, event):
        self._route_change(event.route)
        self.page.update()

    def build_navigation_rail(self):
        return NavigationRail(
            selected_index=0,
            label_type="none",
            on_change=self._navigation_change,
        )

    def update_destinations(self, icons_only=False):
        navigation_items = self.navigation_items
        if icons_only:
            navigation_items = deepcopy(navigation_items)
            for item in navigation_items:
                item.pop("label")

        self.navigation_rail.destinations = [
            NavigationRailDestination(**nav_specs) for nav_specs in navigation_items
        ]
        self.navigation_rail.label_type = "none" if icons_only else "all"

    def handle_resize(self, e):
        if self._was_portrait != self.is_portrait():
            self._was_portrait = self.is_portrait()
            self._panel_visible = self.is_landscape()
            self.set_navigation_content()
            self.page.update()

    def toggle_navigation(self, event=None):
        self._panel_visible = not self._panel_visible
        self.set_navigation_content()
        self.page.update()

    def check_toggle_on_select(self):
        if self.is_portrait() and self._panel_visible:
            self.toggle_navigation()

    def set_navigation_content(self):
        if self.is_landscape():
            self.add_landscape_content()
        else:
            self.add_portrait_content()

    def add_landscape_content(self):
        self.controls = [self.menu_panel, self.content_area]
        if self.landscape_minimize_to_icons:
            self.update_destinations(icons_only=not self._panel_visible)
            self.menu_panel.visible = True
            if not self._panel_visible:
                self.navigation_rail.extended = False
            else:
                self.navigation_rail.extended = self.menu_extended
        else:
            self.update_destinations()
            self.navigation_rail.extended = self._menu_extended
            self.menu_panel.visible = self._panel_visible

    def add_portrait_content(self):
        if self.portrait_minimize_to_icons and not self._panel_visible:
            self.controls = [self.menu_panel, self.content_area]
            self.update_destinations(icons_only=True)
            self.menu_panel.visible = True
            self.navigation_rail.extended = False
        else:
            if self._panel_visible:
                dismiss_shield = Container(
                    expand=True,
                    on_click=self.toggle_navigation,
                )
                self.controls = [
                    Stack(
                        controls=[self.content_area, dismiss_shield, self.menu_panel],
                        expand=True,
                    )
                ]
            else:
                self.controls = [
                    Stack(controls=[self.content_area, self.menu_panel], expand=True)
                ]
            self.update_destinations()
            self.navigation_rail.extended = self.menu_extended
            self.menu_panel.visible = self._panel_visible

    def is_portrait(self) -> bool:
        # Return true if window/display is narrow
        # return self.page.window_height >= self.page.window_width
        return self.page.height >= self.page.width

    def is_landscape(self) -> bool:
        # Return true if window/display is wide
        return self.page.width > self.page.height


############################################
# Variables :

############################################
    


if __name__ == "__main__":

    def main(page: Page,):

        page.title = "ConversaLearn"
        
    

        menu_button = IconButton(icons.MENU)

        page.appbar = AppBar(
            leading=menu_button,
            leading_width=40,
            bgcolor=colors.SURFACE_VARIANT,
        )

        pages = [
            (
                dict(
                    icon=icons.HOME_OUTLINED,
                    selected_icon=icons.HOME,
                    label="Home",
                ),
                create_page(
                    "Bienvenue dans ConversaLearn 🎉 / Welcome to Conversalearn 🎉/\n",
                    "Nous sommes ravis de vous compter parmi nos nouveaux utilisateurs !\n"
                    "Notre application innovante est conçue spécialement pour les apprenants avancés en anglais qui cherchent à améliorer leurs compétences conversationnelles.\n"
                    "Avec ConversaLearn-English, vous aurez l'opportunité de vous engager dans des conversations réalistes avec deux AI uniques :\n"
                    "           - un compagnon AI amical\n"
                    "           - un mentor AI enseignan\n" 
                    "Ces interactions dynamiques et basées sur l'IA vous aideront à améliorer votre anglais de manière engageante et efficace.\n"
                    "________________________\n"
                    "We are thrilled to have you as one of our new users! Our innovative app is designed specifically for advanced English learners who are looking to improve their conversational skills.\n"
                    "With ConversaLearn-English, you will have the opportunity to engage in realistic conversations with two unique AI:\n"
                    "           - a friendly AI companion\n"
                    "           - a teaching AI mentor\n"
                    "These dynamic, AI-based interactions will help you improve your English in an engaging and effective way."

                ),
            ),
            (
                dict(
                    icon=icons.CHAT_OUTLINED,
                    selected_icon=icons.CHAT,
                    label="The CHAT",
                ),
                create_chat_page(),
                
                
            ),
            (
                dict(
                    icon=icons.MUSIC_NOTE_OUTLINED,
                    selected_icon=icons.MUSIC_NOTE,
                    label="Singer",
                ),
                create_page(
                    "Singer",
                    "daedze",
                ),
            ),
            (
                dict(
                    icon=icons.BOOK_OUTLINED,
                    selected_icon=icons.BOOK,
                    label="Lessons",
                ),
                create_page(
                    "Lessons",
                    "BLABLA",
                ),
            ),
            (
                dict(
                    icon=icons.PLUS_ONE_OUTLINED,
                    selected_icon=icons.PLUS_ONE,
                    label="Fine control",
                ),
                create_page(
                    "Adjust navigation rail",
                    "NavigationRail is accessible via the navigation_rail attribute of the ResponsiveMenuLayout. "
                    "In this demo it is used to add the leading button control."
                    "\n\n"
                    "These NavigationRail attributes are used by the ResponsiveMenuLayout, and changing them directly "
                    "will probably break it:\n"
                    "- destinations\n"
                    "- extended\n"
                    "- label_type\n"
                    "- on_change\n",
                ),
            ),
        ]

        menu_layout = ResponsiveMenuLayout(page, pages)


        ### Boutons de la barre de navigation
        page.appbar.title = Text("ConversaLearn")
        page.appbar.actions = [
            Row(
                [
                    Text("Theme"),
                    IconButton(icon=icons.LIGHT_MODE, selected_icon=icons.DARK_MODE , on_click=lambda e: switch_theme(menu_layout,)),
                    # Text("Minimize\nto icons"),
                    # Switch(on_change=lambda e: toggle_icons_only(menu_layout)),
                    Text("Menu\nwidth"),
                    Switch(
                        value=True, on_change=lambda e: toggle_menu_width(menu_layout)
                    ),
                ]
            )
        ]

        menu_layout.navigation_rail.leading = ElevatedButton(
            "Add", icon=icons.ADD, expand=True, on_click=lambda e: print("Add clicked")
        )
        menu_button.on_click = lambda e: menu_layout.toggle_navigation()
        page.add(menu_layout)

       

    def create_page(title: str, body: str):
        return Row(
            controls=[
                Column(
                    horizontal_alignment="stretch",
                    controls=[
                        Card(content=Container(Text(title, weight="bold"), padding=8)),
                        Text(body),
                    ],
                    expand=True,
                ),
            ],
            expand=True,
        )

    def create_chat_page():
        return ft.Row(
            controls=[
                ft.Column(
                    horizontal_alignment="stretch",
                    controls=[
                        ft.Column(expand=1, wrap=False, scroll="always"),
                        ft.TextField(hint_text="Type a message...",),
                        ft.ElevatedButton("Send",),
                    ],
                    expand=True,
                )
        ],
        expand=True,
    )

    def switch_theme(menu: ResponsiveMenuLayout ):
        # SWITCH THE THEME
        menu.page.theme_mode = "light" if menu.page.theme_mode =="dark" else "dark"
        menu.page.update()
        


    def toggle_icons_only(menu: ResponsiveMenuLayout):
        menu.minimize_to_icons = not menu.minimize_to_icons
        menu.page.update()

    def toggle_menu_width(menu: ResponsiveMenuLayout):
        menu.menu_extended = not menu.menu_extended
        menu.page.update()

    ft.app(target=main, view=ft.WEB_BROWSER)