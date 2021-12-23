import datetime
from sqlalchemy import create_engine, exc, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey

import controller
from middleware.sqlmiddle import origin_type


class Model:
    # connection to PostgreSQL server
    Base = declarative_base()

    def __init__(self):
        try:
            self.engine = create_engine('postgresql://postgres:root@127.0.0.1:5432/blog')
            self.Session = sessionmaker(bind=self.engine)
            self.s = self.Session()
        except exc.SQLAlchemyError as e:
            print(type(e))

    def showTable(self, sql_select_query):
        try:
            records = sql_select_query.all()
        except exc.SQLAlchemyError as error:
            print("Error while fetching data from PostgreSQL", error)
            self.s.rollback()
        return records

    def updateTable(self):
        try:
            self.s.commit()
            print("Successfully updated")
        except exc.SQLAlchemyError as error:
            print("Failed updating record of the table {}", error)
            self.s.rollback()

    def addTable(self, sql_insert_query):
        try:
            self.s.add(sql_insert_query)
            self.s.commit()
            print("Successfully inserted")
        except exc.SQLAlchemyError as error:
            print("Failed inserting record into table {}".format(error))
            self.s.rollback()

    # delete table row
    def delTable(self, sql_delete_query):
        try:
            self.s.delete(sql_delete_query)
            self.s.commit()
            print("Successfully deleted")
        except exc.SQLAlchemyError as error:
            print("Failed deleting record into table {}".format(error))
            self.s.rollback()

    def only_possible(self, val, num, if_exit):
        try:
            sql_origin = self.origin_type(num, val)
            if sql_origin is None:
                raise exc.SQLAlchemyError
        except exc.SQLAlchemyError as error:
            print("Failed, there are no records with such id")
            if_exit()

    # close connection of Postgre table
    def close_connect(self):
        if self.s:
            self.s.close()
            print("PostgreSQL connection is closed")

    # choose command to insert data to specific table
    def insert_type(self, table_num, rec):
        if table_num == '1':
            sql_insert_query = User(rec[0], rec[1], rec[2], rec[3])
        elif table_num == '2':
            sql_insert_query = Post(rec[2], rec[0], rec[1])
        elif table_num == '3':
            sql_insert_query = Like(rec[0], rec[1])
        elif table_num == '4':
            sql_insert_query = Comment(rec[0], rec[1], rec[2])
        return sql_insert_query

    # choose command to update data of specific table
    def update_type(self, table_num, val, if_exit):
        try:
            if table_num == '1':
                sql_update_query = self.s.query(User).filter(User.user_id == val[4]). \
                    update({User.password: val[3], User.f_name: val[0], User.l_name: val[1]})
            elif table_num == '2':
                sql_update_query = self.s.query(Post).filter(Post.post_id == val[3]). \
                    update({Post.title: val[0], Post.body: val[1], Post.author_id: val[2]})
            elif table_num == '3':
                sql_update_query = self.s.query(Like).filter(Like.like_id == val[2]).update(
                    {Like.user_id: val[0], Like.post_id: val[1]})
            elif table_num == '4':
                sql_update_query = self.s.query(Comment).filter(Comment.comment_id == val[3]). \
                    update({Comment.body: val[0], Comment.author_id: val[1], Comment.post_id: val[2]})
        except exc.SQLAlchemyError as error:
            print("Failed updating record of the table {}", error)
            if_exit()

        return sql_update_query

        # choose command to delete data of specific table

    def delete_type(self, table_num, rec):
        sql_delete_query = ''
        try:
            if table_num == '1':
                sql_delete_query = self.s.query(User).filter_by(user_id=rec[0]).one()
            elif table_num == '2':
                sql_delete_query = self.s.query(Post).filter_by(post_id=rec[0]).one()
            elif table_num == '3':
                sql_delete_query = self.s.query(Like).filter_by(like_id=rec[0]).one()
            elif table_num == '4':
                sql_delete_query = self.s.query(Comment).filter_by(comment_id=rec[0]).one()
        except exc.SQLAlchemyError as error:
            print("Failed deleting record from table {}".format(error))
        finally:
            return sql_delete_query

    def select_type(self, table_num):
        if table_num == '1':
            sql_select_query = self.s.query(User).order_by(User.user_id)
        elif table_num == '2':
            sql_select_query = self.s.query(Post).order_by(Post.post_id)
        elif table_num == '3':
            sql_select_query = self.s.query(Like).order_by(Like.like_id)
        elif table_num == '4':
            sql_select_query = self.s.query(Comment).order_by(Comment.comment_id)
        return sql_select_query

    def origin_type(self, table_num, val):
        if table_num == 1:
            sql_origin_val = self.s.query(User).filter_by(user_id=val).one_or_none()
        elif table_num == 2:
            sql_origin_val = self.s.query(Post).filter_by(post_id=val).one_or_none()
        elif table_num == 3:
            sql_origin_val = self.s.query(Like).filter_by(like_id=val).one_or_none()
        elif table_num == 4:
            sql_origin_val = self.s.query(Comment).filter_by(comment_id=val).one_or_none()
        return sql_origin_val

    # check if int is valid
    def Repr_init(self, n):
        try:
            int(n)
            return True
        except ValueError:
            return False


class Comment(Model.Base):
    __tablename__ = 'comments'
    comment_id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('users.user_id'))
    post_id = Column(Integer, ForeignKey('posts.post_id'))
    body = Column(String)
    date = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User")
    post = relationship("Post")

    def __init__(self, body, author_id, post_id):
        self.body = body
        self.author_id = author_id
        self.post_id = post_id


class Like(Model.Base):
    __tablename__ = 'likes'
    like_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    post_id = Column(Integer, ForeignKey('posts.post_id'))

    user = relationship("User")
    post = relationship("Post")

    def __init__(self, user_id, post_id):
        self.user_id = user_id
        self.post_id = post_id


class Post(Model.Base):
    __tablename__ = 'posts'
    post_id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('users.user_id'))
    title = Column(String)
    body = Column(String)
    date = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User")

    def __init__(self, author_id, title, body):
        self.author_id = author_id
        self.title = title
        self.body = body


class User(Model.Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    f_name = Column(String)
    l_name = Column(String)
    email = Column(String)
    password = Column(String)

    def __init__(self, f_name, l_name, email, password):
        self.f_name = f_name
        self.l_name = l_name
        self.email = email
        self.password = password
