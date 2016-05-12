import informixdb
import os
import sql_statement


class SqlRequest:
    def __init__(self):
        self.__Database = 'd_1460371357365469'
        self.__Server = 'ifxserver1'
        self.__Username = 'tqbodnho'
        self.__Password = 'JSe2lR1cH6'
        self.__sellerName = 'seller'
        self.__inventoryName = 'inventory'
        self.__customerName = 'customer'
        self.__userTabName = 'user_info'
        self.__orderName = 'single_order'
        self.__currentName = 'current'
        self.__detailName = 'detail'
        self.stat = sql_statement.SqlStatement()
        self.conn = None
        self.conn = informixdb.connect(self.__Database + '@' + self.__Server, self.__Username, self.__Password)
        if not self.conn:
            raise Exception("Failed to connect via SQL to informixdb")
        else:
            print("connected to database " + self.__Database)

    @staticmethod
    def _is_none(att):
        if att is None:
            print('Unspecified Key Fields ')
            return True

    @staticmethod
    def _is_dict(obj):
        if not isinstance(obj,dict):
            print("Unexpected parameter type other than dict")

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def _new_cursor(self):
        if self.conn is None:
            print("reconnect to SQL server ...")
            self.conn = informixdb.connect(self.__Database + '@' + self.__Server, self.__Username, self.__Password)
            if self.conn is None:
                raise Exception("Failed to connect via SQL to informixdb")
        c = self.conn.cursor()
        if c is None:
            raise Exception("Failed to get a cursor on SQL connect")

    def _sql_execute(self, sql_str):
        cur = self._new_cursor()
        cur.execute(sql_str)
        cur.close()

    def _sql_count(self, sql_str):
        cur = self._new_cursor()
        cur.execute(sql_str)
        ans = cur.rowcount()
        cur.close()
        return ans

    def _sql_fetchall(self, sql_str):
        cur = self._new_cursor()
        cur.execute(sql_str)
        a = cur.fetchall()
        cur.close()
        return a

    def add_category(self, dic):
        if self._is_none(dic) or not self._is_dict(dic):
            return
        dic.get('title',None)








    def exist_user(self, id):
        if self._is_none(id):
            return
        sql_str = 'select * from ' + self.__userTabName + 'where user_id = ' + id.__str__()
        ans = self._sql_count(sql_str)
        if ans > 1:
            print("User ID replication found on " + id.__str__())
        return ans == 1



update, seller_id, order_id):
        if customer_id is None or total_price is None:
            print("Unspecified Key Fields")
            return
        # for i in [order_date, payment_date, last_update]:
        #     i = self.__currentName
        order_date =  payment_date = last_update = self.__currentName
        return self._add_fields(self.__orderName, 10,
                                [deliver_id, comment_seller, customer_id, payment_status, total_price, order_date,
                                 payment_date,
                                 last_update, seller_id, order_id], 2)

    def add_detail(self, comment_inventory, order_id, inventory_id, quantity):
        if order_id is None or inventory_id is None:
            print("Unspecified Key Fields")
            return
        return self._add_fields(self.__detailName, 4, [comment_inventory, order_id, inventory_id, quantity], 1)

    def exist_user(self, user_id = None):
        if self._is_none(user_id):
            return
        return "select count(*) from user_info where user_id = " + user_id.__str__() + ';'

    def search_inventory(self, inventory_name=None, category_title=None, ):
        if inventory_name is None and category_title is None:
            print("Unspecified Key Fields")
            return
        s = "select "


