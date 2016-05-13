import logging
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
        # configure error logging
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename='sql_request.log',
                            filemode='w')
        # sql statement object
        self.stat = sql_statement.SqlStatement()
        # informix sql server connection
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
    def _any_none(l):
        for i in l:
            if i is None:
                print('Unspecified Key Fields ')
            return True
        return False

    @staticmethod
    def _is_dict(obj):
        if obj is None or not isinstance(obj, dict):
            print("Unexpected parameter type other than dict")

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    # TODO: consider connection/cursor pool

    def _new_cursor(self):
        try:
            if self.conn is None:
                print("reconnect to SQL server ...")
                self.conn = informixdb.connect(self.__Database + '@' + self.__Server, self.__Username, self.__Password)
                if self.conn is None:
                    raise Exception("Failed to connect via SQL to informixdb")
            c = self.conn.cursor()
            if c is None:
                raise Exception("Failed to get a cursor on SQL connect")
            return c
        except Exception as e:
            logging.exception(e)
            return None

    def _sql_execute(self, sql_str):
        cur = self._new_cursor()
        try:
            cur.execute(sql_str)
        except Exception as e:
            logging.exception(e)
            return None
        finally:
            cur.close()

    def _sql_count(self, sql_str):
        cur = self._new_cursor()
        try:
            cur.execute(sql_str)
            ans = cur.rowcount()
            return ans
        except Exception as e:
            logging.exception(e)
            return None
        finally:
            if cur is not None:
                cur.close()

    def _sql_fetchall(self, sql_str):
        try:
            cur = self._new_cursor()
            cur.execute(sql_str)
            a = cur.fetchall()
            cur.close()
            return a
        except Exception as e:
            logging.exception(e)
            return None

    def _sql_last_insert(self):
        try:
            st = 'SELECT DBINFO(\'SQLCA.SQLERRD1\') FROM systables WHERE tabname = \'systables\''
            ans = self._sql_fetchall(st)  # ans is [(number, )]
            return ans[0][0]
        except Exception as e:
            logging.exception(e)
            return None

    def add_category(self, category_title=None, category_desc=None):
        if self._any_none([category_title, category_desc]):
            return False
        st = self.stat.add_category(category_title, category_desc)
        self._sql_execute(st)
        return True

    def _add_user(self, name, passw):
        try:
            st = self.stat.add_user(name, passw, 1)
            self._sql_execute(st)
            user_id = self._sql_last_insert()
            # debug
            check = self._sql_fetchall('select user_id from user_info where user_name like \'' + name + '\'')
            if check[0][0] != user_id:
                raise Exception('_sql_last_insert() function failed to fetch correct id in add_customer')
            return user_id
        except Exception as e:
            logging.exception(e)
            return None

    def add_seller(self, user_name, user_pass, seller_name, seller_addr):
        if self._is_none(seller_name):
            return False
        uid = self._add_user(user_name, user_pass)
        st = self.stat.add_seller(uid, seller_name, seller_addr)
        self._sql_execute(st)
        return True

    def add_customer(self, user_name, user_pass, customer_name, customer_email):
        if self._is_none(customer_name):
            return False
        uid = self._add_user(user_name, user_pass)
        st = self.stat.add_seller(uid, customer_name, customer_email)
        self._sql_execute(st)
        return True

    def add_inventory(self, inventory_name, inventory_desc, picture_url, inventory_price, inventory_quantity,
                      category_id, seller_id):
        if self._any_none([inventory_name, inventory_price, inventory_quantity, seller_id]):
            return False
        st = self.stat.add_inventory(name=inventory_name, desc=inventory_desc, picture=picture_url,
                                     price=inventory_price, quantity=inventory_quantity, category=category_id,
                                     seller=seller_id)
        self._sql_execute(st)
        return True

        # def add_category(self, dic):
        #     if self._is_none(dic) or not self._is_dict(dic):
        #         return
        #     title = dic.get('category_title', None)
        #     desc = dic.get('category_desc', None)
        #     st = self.stat.add_category(title, desc)
        #     self._sql_execute(st)

        # def add_customer(self, dic):
        #     if self._is_none(dic) or not self._is_dict(dic):
        #         return
        #     name = dic.get('user_name', None)
        #     passw = dic.get('user_pass', None)
        #     cus_name = dic.get('customer_name', None)
        #     cus_email = dic.get('customer_email', None)
        #     if self._any_none([name, passw, cus_email]):
        #         return
        #     user_id = self._add_user(name, passw)
        #     st = self.stat.add_customer(cus_name, cus_email, user_id)
        #     self._sql_execute(st)

        # def exist_user_name(self, user_name):
        #     if self._is_none:
        #         return
        #     sql_st = 'select user_id from ' + self.__userTabName + 'where user_name like \'' + user_name.__str__() + '\''
        #     ans = self._sql_fetchall(sql_st)

        # def exist_user(self, id):
        #     if self._is_none:
        #         return
        #     sql_str = 'select * from ' + self.__userTabName + 'where user_id = ' + id.__str__()
        #     ans = self._sql_count(sql_str)
        #     if ans > 1:
        #         print("User ID replication found on " + id.__str__())
        #     return ans == 1
