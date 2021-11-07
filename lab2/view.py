from prettytable import PrettyTable


class View:
    def print_table(self, records, tab):
        table = PrettyTable()
        if tab == '1':
            table.field_names = ["user_id", "f_name", "l_name", "email", "password"]
            for sql_row in records:
                table.add_row([sql_row[0], sql_row[1], sql_row[2], sql_row[3], sql_row[4]])
        elif tab == '2':
            table.field_names = ["post_id", "title", "body", "date", "author_id"]
            for sql_row in records:
                table.add_row([sql_row[0], sql_row[1], sql_row[2], sql_row[3], sql_row[4]])
        elif tab == '3':
            table.field_names = ["like_id", "user_id", "post_id"]
            for sql_row in records:
                table.add_row([sql_row[0], sql_row[1], sql_row[2]])
        elif tab == '4':
            table.field_names = ["comment_id", "body", "date", "author_id", "post_id"]
            for sql_row in records:
                table.add_row([sql_row[0], sql_row[1], sql_row[2], sql_row[3], sql_row[4]])
        elif tab == '5':
            table.field_names = ["title", "body", "author_id"]
            for sql_row in records:
                table.add_row([sql_row[0], sql_row[1], sql_row[2]])
        elif tab == '6':
            table.field_names = ["title", "body", "date"]
            for sql_row in records:
                table.add_row([sql_row[0], sql_row[1], sql_row[2]])
        elif tab == '7':
            table.field_names = ["user_id", "f_name", "email"]
            for sql_row in records:
                table.add_row([sql_row[0], sql_row[1], sql_row[2]])
        print(table)

    @staticmethod
    def display(txt):
        return input(txt)

    @staticmethod
    def print_text(txt):
        print(str(txt))
