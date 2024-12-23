import os
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, SelectionList, Button
from textual.widgets.selection_list import Selection
from textual.screen import Screen

class BackupSelectionScreen(Screen):
    CSS = """
    SelectionList {
        width: 100%;
        height: 80%;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield SelectionList()
        yield Button("Backup Selected Directories", id="backup_button")
        yield Footer()

    def on_mount(self):
        selection_list = self.query_one(SelectionList)
        selection_list.border_title = "Select directories to backup"
        home_directory = os.path.expanduser('~')
        directories = [d for d in os.listdir(home_directory) if os.path.isdir(os.path.join(home_directory, d))]
        for directory in directories:
            selection_list.add_option(Selection(directory, directory))

    def on_selection_list_selected(self, event: SelectionList.selected):
        selected_dirs = [option.value for option in self.query_one(SelectionList).selected]
        self.query_one("#backup_button").label = f"Backup {len(selected_dirs)} Selected Directories"

    def on_button_pressed(self, event: Button.Pressed):
        selected_dirs = [option for option in self.query_one(SelectionList).selected]
        print("Selected directories for backup:", selected_dirs)
        self.app.pop_screen()


class AppSwitcher(App):
    CSS = """
    Container {
        align: center middle;
    }
    Button {
        width: 20;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Container(
            Button("App One", id="app_one"),
            Button("App Two", id="app_two"),
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "app_one":
            self.switch_to_app("App One")
        elif event.button.id == "app_two":
            self.switch_to_app("App Two")

    def switch_to_app(self, app_name: str) -> None:
        if app_name == "App One":
            backup_app = BackupSelectionScreen()
            self.push_screen(backup_app)
        else:
            self.sub_title = f"Switched to {app_name}"


def main():
    #app = BackupSelectionApp()
    app = AppSwitcher()
    selected_directories = app.run()
    print("Final selection:", selected_directories)

