import os
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, SelectionList, Button
from textual.widgets.selection_list import Selection
from textual.screen import Screen

class ManualSelectionScreen(Screen):
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
        #self.app.pop_screen()
        self.app.exit(selected_dirs)

class GuidedSelectionScreen(Screen):
    CSS = """
    SelectionList {
        width: 100%;
        height: 80%;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield SelectionList()
        yield Button("Backup Using Options", id="backup_button")
        yield Footer()

    def on_mount(self):
        selection_list = self.query_one(SelectionList)
        selection_list.border_title = "Select options for backup"

        # Add detection code here
        selection_list.add_option(Selection("your mom", "your dad"))

    def on_selection_list_selected(self, event: SelectionList.selected):
        selected_dirs = [option.value for option in self.query_one(SelectionList).selected]
        self.query_one("#backup_button").label = f"Backup Using {len(selected_dirs)} Options"

    def on_button_pressed(self, event: Button.Pressed):
        selected_dirs = [option for option in self.query_one(SelectionList).selected]
        #self.app.pop_screen()
        self.app.exit(selected_dirs)

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
            Button("Manual", id="manual"),
            Button("Guided", id="guided"),
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "manual":
            self.switch_to_app("Manual")
        elif event.button.id == "guided":
            self.switch_to_app("Guided")

    def switch_to_app(self, app_name: str) -> None:
        if app_name == "Manual":
            backup_app = ManualSelectionScreen()
            self.push_screen(backup_app)
        else:
            backup_app = GuidedSelectionScreen()
            self.push_screen(backup_app)


def main():
    #app = BackupSelectionApp()
    app = AppSwitcher()
    selected_directories = app.run()
    print("Final selection:", selected_directories)

