from enum import Enum
from view import View


class MenuTypes(Enum):
    def __str__(self):
        return str(self.value)

    ACTIONS = """Choose option: \nPRESS: 1 to add... 2 to update...  3 to delete...  4 to specific_select... 5 to show_table...\n"""
    TABLES = """Choose table: \n press 1 - users...   press 2 - posts...   press 3 - likes... press 4 - comments\n"""


class MenuItem(str, Enum):
    INSERT = '1',
    EDIT = '2',
    DELETE = '3',
    SPECIFIC_SELECT = '4',
    SHOW_TABLE = '5'


class Menu:
    def __init__(self, text: str, items: int):
        self.text = text
        self.items = items
        self.choice = self.make_choice()

    def make_choice(self) -> str:
        choice = ""
        valid_items = [str(i) for i in range(1, self.items + 1)]
        while choice not in valid_items:
            choice = View.display(self.text)
        return choice
