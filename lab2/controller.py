from model import Model
from view import View
from middleware.menu import Menu, MenuTypes, MenuItem
from middleware.sqlmiddle import insert_type, insert_query, check_default, validation_int_value, \
    insert_random_type, update_query, update_type, delete_type, delete_query, spec_choose, \
    specific_query, specific_type, select_type


class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()

    def manage_choice(self):
        table_menu = Menu(MenuTypes.ACTIONS, 5)
        if table_menu.choice == MenuItem.INSERT:
            table_to_insert = Menu(MenuTypes.TABLES, 4)
            if_rand = self.rand_or_man()
            if if_rand == 'M':
                while True:
                    sql_insert = insert_type(table_to_insert.choice)
                    record = insert_query(table_to_insert.choice, self.if_exit)
                    self.model.add_table(record, sql_insert)
                    if self.to_continue() is False:
                        break
            elif if_rand == 'R':
                pass
                times = View.display("What number of row do you want to add(type 'd' to set default)? - ")
                times = check_default(times)
                validation_int_value(times, self.if_exit)
                sql_random = insert_random_type(table_to_insert.choice)
                self.model.add_table([(times,)], sql_random)
            self.if_exit()
        elif table_menu.choice == MenuItem.EDIT:
            table_to_update = Menu(MenuTypes.TABLES, 4)
            while True:
                sql_update = update_type(table_to_update.choice)
                record = update_query(table_to_update.choice, self.if_exit, self.model.only_possible)
                self.model.update_table(record, sql_update)
                if self.to_continue() is False:
                    break
            self.if_exit()
        elif table_menu.choice == MenuItem.DELETE:
            table_to_delete = Menu(MenuTypes.TABLES, 4)
            while True:
                sql_delete = delete_type(table_to_delete.choice)
                record = delete_query(table_to_delete.choice, self.if_exit, self.model.only_possible)
                self.model.del_table(record, sql_delete)
                if self.to_continue() is False:
                    break
            self.if_exit()
        elif table_menu.choice == MenuItem.SPECIFIC_SELECT:
            table = spec_choose()
            tab = str(int(table) + 4)
            record = specific_query(table, self.if_exit)
            sql_spec = specific_type(table)
            show = self.model.show_table(sql_spec, tab, record, True)
            self.view.print_table(show, tab)
            self.if_exit()
        elif table_menu.choice == MenuItem.SHOW_TABLE:
            table = Menu(MenuTypes.TABLES, 4)
            sql_select = select_type(table.choice)
            show = self.model.show_table(sql_select, table.choice, None, False)
            self.view.print_table(show, table.choice)
            self.if_exit()

    def rand_or_man(self):
        option = View.display("Do you want to insert rows manually or randomly? \nPress M if manually, R if randomly: ")
        if option != 'M' and option != 'R':
            View.print_text("You entered wrong value")
            self.if_exit()
        return option;

    def if_exit(self):
        ext = View.display("Do you want to exit? Press M to go to the main menu, or E to exit: ")
        if ext == 'M':
            self.manage_choice()
        elif ext == 'E':
            # self.model.close_connect()
            exit()
        else:
            View.print_text("You entered wrong character...")
            self.if_exit()

    def to_continue(self):
        cont = View.display("Do you want to continue? Press Y if yes, N if no: ")
        if cont == 'Y':
            return True
        elif cont == 'N':
            return False
        else:
            View.print_text("You entered wrong value, please try again")
            self.to_continue()

