"""
Usage:
    compress <DISK>
"""

import os
from compress import utils
from docopt import docopt
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, SelectionList, Button
from textual.widgets.selection_list import Selection
from textual.screen import Screen

class ManualSelectionData:
    def __init__(self, dirs):
        self.dirs = []

class GuidedSelectionData:
    def __init__(self, funcs):
        self.funs = funcs

home_directory = os.path.expanduser('~')


# How it works is that we just copy everything into a directory.
def backup_firefox(tmp_directory):
    target = ".mozilla"
    print(f"Backing up {target} to {tmp_directory}")
    path = os.path.join(home_directory, target)
    utils.copy_dir(path, tmp_directory)

def backup_ssh(tmp_directory):
    target = ".ssh"
    print(f"Backing up {target} to {tmp_directory}")
    path = os.path.join(home_directory, target)
    utils.copy_dir(path, tmp_directory)


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
        directories = [d for d in os.listdir(home_directory) if os.path.isdir(os.path.join(home_directory, d))]
        for directory in directories:
            selection_list.add_option(Selection(directory, directory))

    def on_selection_list_selected(self, event: SelectionList.selected):
        selected_dirs = [option.value for option in self.query_one(SelectionList).selected]
        self.query_one("#backup_button").label = f"Backup {len(selected_dirs)} Selected Directories"

    def on_button_pressed(self, event: Button.Pressed):
        selected_dirs = [option for option in self.query_one(SelectionList).selected]
        selected_dirs = list(map(lambda a: os.path.join(home_directory, a), selected_dirs))
        #self.app.pop_screen()
        self.app.exit(ManualSelectionData(selected_dirs))

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
        if os.path.exists(os.path.join(home_directory, ".mozilla")):
            selection_list.add_option(Selection("Firefox", backup_firefox))
        if os.path.exists(os.path.join(home_directory, ".ssh")):
            selection_list.add_option(Selection("SSH", backup_ssh))

    def on_selection_list_selected(self, event: SelectionList.selected):
        selected_dirs = [option.value for option in self.query_one(SelectionList).selected]
        self.query_one("#backup_button").label = f"Backup Using {len(selected_dirs)} Options"

    def on_button_pressed(self, event: Button.Pressed):
        selected_options = [option for option in self.query_one(SelectionList).selected]
        #self.app.pop_screen()
        self.app.exit(GuidedSelectionData(selected_options))

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
            _ = self.push_screen(backup_app)
        else:
            backup_app = GuidedSelectionScreen()
            _ = self.push_screen(backup_app)


def main():
    args = docopt(__doc__)
    app = AppSwitcher()
    option = app.run()

    if isinstance(option, GuidedSelectionData):
        for i in option.funs:
            i("/tmp/hehhehehe")


    if isinstance(option, ManualSelectionData):
        mount_point = utils.mount_disk(args["<DISK>"])
        if mount_point != None:
            print(f"Mounted {mount_point}")
            print(f"Is linux partition?")
            print(utils.check_if_linux_home(mount_point, "adhoc"))
            res = utils.unmount_disk(mount_point)
            if res:
                print(f"Unmounted {mount_point}")
            else:
                print("Error on dismount.")
        else:
            print("Error on mount.")
