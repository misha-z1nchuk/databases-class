from view import View
import datetime


def insert_query(opt, err_func):
    times = get_times("add")
    record_to_insert = ""
    if opt == '1':
        for i in range(times):
            print("Enter values following this sequence: f_name, l_name, email, password")
            f_name = View.display("f_name: ")
            validation_string_value(f_name, err_func)

            l_name = View.display("l_name: ")
            validation_string_value(l_name, err_func)

            email = View.display("email: ")
            validation_string_value(email, err_func)

            password = View.display("password: ")
            validation_string_value(password, err_func)

            record_to_insert = [(f_name, l_name, email, password)]
    elif opt == '2':
        for i in range(int(times)):
            print("Enter values following this sequence: title, body, author_id")
            title = View.display("title: ")
            validation_string_value(title, err_func)

            body = View.display("body: ")
            validation_string_value(body, err_func)

            author_id = View.display("author_id: ")
            validation_int_value(author_id, err_func)

            record_to_insert = [(title, body, author_id)]
    elif opt == '3':
        for i in range(int(times)):
            print("Enter values following this sequence: user_id, post_id")
            user_id = View.display("user_id: ")
            validation_int_value(user_id, err_func)

            post_id = View.display("post_id: ")
            validation_int_value(post_id, err_func)

            record_to_insert = [(user_id, post_id)]
    elif opt == '4':
        for i in range(int(times)):
            print("Enter values following this sequence: body, author_id, post_id")
            body = View.display("body: ")
            validation_string_value(body, err_func)

            user_id = View.display("user_id: ")
            validation_int_value(user_id, err_func)

            post_id = View.display("post_id: ")
            validation_int_value(post_id, err_func)

            record_to_insert = [(body, user_id, post_id)]
    return record_to_insert


def insert_type(table_num):
    if table_num == '1':
        sql_insert_query = """ INSERT INTO users (f_name, l_name, email, password)
        VALUES (%s, %s, %s, %s)"""
    elif table_num == '2':
        sql_insert_query = """ INSERT INTO posts (title, body, author_id)
        VALUES (%s, %s, %s)"""
    elif table_num == '3':
        sql_insert_query = """ INSERT INTO likes (user_id, post_id)
        VALUES (%s, %s)"""
    elif table_num == '4':
        sql_insert_query = """ INSERT INTO comments (body, author_id, post_id)
        VALUES (%s, %s, %s)"""
    return sql_insert_query


def insert_random_type(table_num):
    if table_num == '1':
        sql_random_query = """ INSERT INTO users (f_name, l_name, email, password)
       SELECT
                    chr(trunc(65+random()*25)::int) || chr(trunc(65+random()*25)::int) ||
                    chr(trunc(65+random()*25)::int) || chr(trunc(65+random()*25)::int),
                    chr(trunc(64+random()*25)::int) || chr(trunc(65+random()*25)::int) ||
                    chr(trunc(65+random()*25)::int) || chr(trunc(65+random()*25)::int) ||
                    chr(trunc(65+random()*25)::int) || chr(trunc(65+random()*25)::int),
                    chr(trunc(63+random()*25)::int) || chr(trunc(65+random()*25)::int) ||
                    chr(trunc(65+random()*25)::int) || chr(trunc(65+random()*25)::int) ||
                    chr(trunc(65+random()*25)::int) || chr(trunc(64+random()*25)::int) ||
                    chr(trunc(65+random()*25)::int) || chr(trunc(65+random()*25)::int),
                    chr(trunc(62+random()*25)::int) || chr(trunc(65+random()*25)::int) ||
                    chr(trunc(65+random()*25)::int) || chr(trunc(65+random()*25)::int) ||
                    chr(trunc(65+random()*25)::int) || chr(trunc(65+random()*25)::int) ||
                    chr(trunc(65+random()*25)::int) || chr(trunc(65+random()*25)::int) ||
                    chr(trunc(65+random()*25)::int) || chr(trunc(65+random()*25)::int)
            FROM
                generate_series(1, %s)
        """
    elif table_num == '2':
        sql_random_query = """ INSERT INTO posts (title, body, author_id)
        SELECT ttl, bdy, author_id FROM 
        (SELECT md5((random()*1)::text) as ttl,
            md5((random()*2)::text) as bdy,
            author_id
        FROM posts tablesample BERNOULLI(100)
        ORDER BY random()) k, generate_series(1, 100000) LIMIT %s 
        """
    elif table_num == '3':
        sql_random_query = """ INSERT INTO likes (user_id, post_id)
                    SELECT user_id, post_id FROM
                    (SELECT 
                    user_id, post_id
                    FROM users, posts tablesample BERNOULLI(100)
                    ORDER BY random()) k ,generate_series(1, 100000) LIMIT %s
                    """
    elif table_num == '4':
        sql_random_query = """ INSERT INTO comments (body, author_id, post_id)
        SELECT body, user_id, post_id FROM
                    (SELECT md5((random()*1)::text) as body,
                    user_id, post_id
                    FROM users, posts tablesample BERNOULLI(100)
                    ORDER BY random()) k ,generate_series(1, 100000) LIMIT %s
                    """
    return sql_random_query


def update_type(table_num):
    if table_num == '1':
        sql_update_query = """UPDATE users set f_name = %s, l_name = %s, email = %s, password = %s
        WHERE "user_id" = %s """
    elif table_num == '2':
        sql_update_query = """UPDATE posts set title = %s, body = %s, author_id = %s 
        WHERE "post_id" = %s """
    elif table_num == '3':
        sql_update_query = """UPDATE likes set user_id = %s, post_id = %s
        WHERE like_id = %s"""
    elif table_num == '4':
        sql_update_query = """UPDATE comments set body = %s, author_id = %s, post_id = %s
          WHERE comment_id = %s """
    return sql_update_query


def update_query(opt, err_func, is_valid_func) -> str:
    times = get_times("update")
    record_to_insert = ""
    if opt == '1':
        for i in range(int(times)):
            print("Enter values following this sequence f_name, l_name, email, password:")
            f_name = View.display("f_name: ")
            validation_string_value(f_name, err_func)

            l_name = View.display("l_name: ")
            validation_string_value(l_name, err_func)

            email = View.display("email: ")
            validation_string_value(email, err_func)

            password = View.display("password: ")
            validation_string_value(password, err_func)

            user_id = View.display("User_id :")
            validation_int_value(user_id, err_func)
            is_valid_func(user_id, 1, err_func)
            record_to_update = [(f_name, l_name, email, password, user_id)]
    elif opt == '2':
        for i in range(int(times)):
            print("Enter values following this sequence: title, body, author_id")
            title = View.display("title: ")
            validation_string_value(title, err_func)

            body = View.display("body: ")
            validation_string_value(body, err_func)

            author_id = View.display("author_id: ")
            validation_int_value(author_id, err_func)

            post_id = View.display("post_id :")
            validation_int_value(post_id, err_func)
            is_valid_func(post_id, 2, err_func)
            record_to_update = [(title, body, author_id, post_id)]
    elif opt == '3':
        for i in range(int(times)):
            print("Enter values following this sequence: user_id, post_id")
            user_id = View.display("user_id: ")
            validation_int_value(user_id, err_func)

            post_id = View.display("post_id: ")
            validation_int_value(post_id, err_func)

            like_id = View.display("like_id :")
            validation_int_value(post_id, err_func)
            is_valid_func(like_id, 3, err_func)
            record_to_update = [(user_id, post_id, like_id)]
    elif opt == '4':
        for i in range(int(times)):
            print("Enter values following this sequence: body, author_id, post_id comment_id")
            body = View.display("body: ")
            validation_string_value(body, err_func)

            user_id = View.display("user_id: ")
            validation_int_value(user_id, err_func)

            post_id = View.display("post_id: ")
            validation_int_value(post_id, err_func)

            comment_id = View.display("comment_id :")
            validation_int_value(comment_id, err_func)
            is_valid_func(comment_id, 4, err_func)
            record_to_update = [(body, user_id, post_id, comment_id)]
    return record_to_update


def delete_type(table_num):
    if table_num == '1':
        sql_delete_query = """ DELETE FROM users WHERE user_id = %s"""
    elif table_num == '2':
        sql_delete_query = """ DELETE FROM posts WHERE post_id = %s"""
    elif table_num == '3':
        sql_delete_query = """ DELETE FROM likes WHERE like_id = %s"""
    elif table_num == '4':
        sql_delete_query = """ DELETE FROM comments WHERE comment_id = %s"""
    return sql_delete_query


def delete_query(opt, err_func, is_valid_func):
    times = get_times("delete")
    record_to_delete = ""
    if opt == '1':
        for i in range(int(times)):
            user_id = View.display("Enter value that marks user_id:")
            validation_int_value(user_id, err_func)
            is_valid_func(user_id, 1, err_func)
            record_to_delete = [(user_id,)]
    elif opt == '2':
        for i in range(int(times)):
            post_id = View.display("Enter value that marks post_id: ")
            validation_int_value(post_id, err_func)
            is_valid_func(post_id, 2, err_func)
            record_to_delete = [(post_id,)]
    elif opt == '3':
        for i in range(int(times)):
            like_id = View.display("Enter value that marks like_id: ")
            validation_int_value(like_id, err_func)
            is_valid_func(like_id, 3, err_func)
            record_to_delete = [(like_id,)]
    elif opt == '4':
        for i in range(int(times)):
            comment_id = View.display("Enter value that marks comment_id: ")
            validation_int_value(comment_id, err_func)
            is_valid_func(comment_id, 3, err_func)
            record_to_delete = [(comment_id,)]
    return record_to_delete


def spec_choose():
    print("""1) Show title, body, author_id of posts created by certain 'user', 
        where amount of likes is greater than 'value'  and date of post is later than 
        that 'date'.
                  """)

    print("""2) Show body, date of comments that were wrote by certain 'user',
                under certain post with 'specific title', and date of comment is later than that 'date' 
      
                  """)
    table = 0
    print("""3) Show user_id, f_name, email, of user that has more than "value" posts
            and which were created between 'date1 and 'date2', 
            and amount of comments is greater then 'value'
                  ''
                  """)
    while table != '1' and table != '2' and table != '3':
        table = input(
            "Choose option: \nPress: 1 or 2 or 3\n")
    return table


def specific_query(opt, err_func):
    if opt == '1':
        print("Enter values following this sequence user_id, amount, date:")
        user_id = View.display("user_id: ")
        validation_int_value(user_id, err_func)

        amount = View.display("amount : ")
        validation_int_value(amount, err_func)

        date = View.display("date: ")
        repr_date(date, err_func)
        record_to_specific = (date, user_id, amount)
    elif opt == '2':
        print("Enter values following this sequence user_id, specific_title, date:")
        user_id = View.display("user_id: ")
        validation_int_value(user_id, err_func)

        specific_title = View.display("specific_title : ")
        validation_string_value(specific_title, err_func)

        date = View.display("date: ")
        repr_date(date, err_func)
        record_to_specific = (user_id, specific_title, date)
    elif opt == '3':
        print("Enter values following this sequence post_value, date1, date2, comment_value")
        post_value = View.display("post_value: ")
        validation_int_value(post_value, err_func)

        date1 = View.display("date1: ")
        repr_date(date1, err_func)

        date2 = View.display("date2: ")
        repr_date(date2, err_func)

        comment_value = View.display("comment_value: ")
        validation_int_value(comment_value, err_func)

        record_to_specific = (post_value, date1, date2, comment_value)
    return record_to_specific


def specific_type(table_num):
    if table_num == '1':
        sql_specific_query = """select title, body, author_id from (select p.title, p.body, p.author_id, count(likes.like_id) 
        as likes_amount from posts p  left join likes on likes.post_id=p.post_id  
        where p.date > %s AND p.author_id=%s  group by p.title, p.body, p.author_id) 
        AS foo where likes_amount > %s;
        """
    elif table_num == '2':
        sql_specific_query = """ select * from (select p.title, c.body, c.date from comments c 
                                left join posts p on c.post_id = p.post_id  where p.author_id = %s) AS foo 
                                WHERE title LIKE %s AND date > %s;"""
    elif table_num == '3':
        sql_specific_query = """select uid, fn, em  from (select user_id as uid, f_name as fn, email as em, count(title) 
        from (select * from (select foo.user_id, foo.f_name, foo.email, count(c.body), foo.title, foo.date 
        from (select u.user_id, u.f_name, u.email, p.title, p.date, p.post_id  
        from users u inner join posts p on p.author_id = u.user_id) as foo 
        left join comments c on c.post_id = foo.post_id group by user_id, foo.f_name, foo.email, foo.title, foo.date) As foo3 
        where count > %s AND foo3.date between %s and %s) as foo4 group by user_id, f_name, email) as foo5 where count > %s;
        """
    return sql_specific_query


def select_type(table_num):
    if table_num == '1':
        sql_select_query = """ SELECT * FROM users ORDER BY user_id"""
    elif table_num == '2':
        sql_select_query = """ SELECT * FROM posts ORDER BY post_id"""
    elif table_num == '3':
        sql_select_query = """ SELECT * FROM likes ORDER BY like_id"""
    elif table_num == '4':
        sql_select_query = """ SELECT * FROM comments ORDER BY comment_id"""
    return sql_select_query


def get_times(val):
    print(f"How much rows do you wanna {val}? ")
    amount = input()
    try:
        return int(amount)
    except ValueError:
        print("You entered not int value")
        get_times(val)


def     validation_string_value(value, err_func):
    if value is None or value == '':
        print("Error, column cannot contain NULL value")
        err_func()
    return True


def validation_int_value(value, err_func):
    try:
        int(value)
    except ValueError:
        print("You entered wrong value, please try again!")
        err_func()


def check_default(times):
    if times == 'd':
        times = 100000
        return times
    else:
        return times


def repr_date(date, err_func):
    year = ""
    month = ""
    day = ""
    if len(date) != 10 or date[4] != '-' and date[7] != '-':
        print("You entered wrong date value, please try again!")
        err_func()
    for i in (0, 1, 2, 3):
        year += date[i]
    for i in (5, 6):
        month += date[i]
    for i in (8, 9):
        day += date[i]
    try:
        d = datetime.date(int(year), int(month), int(day))
    except ValueError:
        print("You entered wrong date value, please try again!")
        err_func()
