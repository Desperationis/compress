import os
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, SelectionList, Button
from textual.widgets.selection_list import Selection

class BackupSelectionApp(App):
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
        selected_dirs = [option.value for option in self.query_one(SelectionList).selected]
        print("Selected directories for backup:", selected_dirs)
        self.exit(selected_dirs)

def main():
    app = BackupSelectionApp()
    selected_directories = app.run()
    print("Final selection:", selected_directories)

