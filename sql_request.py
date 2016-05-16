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
                            filename='log_sql_request.log',
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
        # big const
        self.__inventoryAttr = (
            'inventory_name', 'inventory_desc', 'picture_url', 'inventory_price', ' inventory_quantity', 'category_id',
            'seller_id', 'inventory_id 	'
        )
        self.__sql_last_serial = 'SELECT DBINFO(\'SQLCA.SQLERRD1\') FROM systables WHERE tabname = \'systables\''

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
            return True
        except Exception as e:
            logging.exception(e)
            return False
        finally:
            cur.close()

    def _sql_count(self, sql_str):
        cur = self._new_cursor()
        try:
            cur.execute(sql_str)
            ans = cur.fetchall()
            return len(ans)
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
        if self._sql_execute(st):
            return True
        else:
            return False

    def _add_user(self, name, passw, prev):
        try:
            st = self.stat.add_user(name, passw, prev)
            cur = self._new_cursor()
            cur.execute(st)
            cur.execute(self.__sql_last_serial)
            ans = cur.fetchall()
            user_id = ans[0][0]
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
        uid = self._add_user(user_name, user_pass, 1)
        st = self.stat.add_seller(seller_name, seller_addr, uid)
        if self._sql_execute(st):
            return True
        else:
            return False

    def add_customer(self, user_name, user_pass, customer_name, customer_email):
        if self._is_none(customer_name) or self._is_none(customer_email):
            return False
        uid = self._add_user(user_name, user_pass, 2)
        st = self.stat.add_seller(customer_name, customer_email, uid)
        if self._sql_execute(st):
            return True
        else:
            return False

    def add_inventory(self, inventory_name, inventory_desc, picture_url, inventory_price, inventory_quantity,
                      category_id, seller_id):
        if self._any_none([inventory_name, inventory_price, inventory_quantity, seller_id]):
            return False
        st = self.stat.add_inventory(inventory_name=inventory_name, inventory_desc=inventory_desc,
                                     picture_url=picture_url,
                                     inventory_price=inventory_price, inventory_quantity=inventory_quantity,
                                     category_id=category_id,
                                     seller_id=seller_id)
        if self._sql_execute(st):
            return True
        else:
            return False

    # def _add_detail(self, comment_inventory, order_id, inventory_id, quantity=1):
    #     if self._any_none([order_id, inventory_id, quantity]):
    #         return False
    #     st = self.stat.add_detail(comment_inventory, order_id, inventory_id, quantity)
    #     self._sql_execute(st)
    #     return True

    @staticmethod
    def _check_detail(l):
        for i in l:
            if not isinstance(i, tuple) or not len(tuple) == 3:
                return False

    def _add_detail(self, l, order_id):
        # l in format of [(cmt, (o_id OMITTED!!) i_id, qua), (), ...]
        cur = None
        try:
            cur = self._new_cursor()
            for i in l:
                # add detail entry
                st = self.stat.add_detail(l[i][0], order_id, l[i][1], l[i][2])
                cur.execute(st)
                # cut inventory stock count
                st = self.stat.update_inventory_quantity(inventory_id=l[i][1], quantity_diff=l[i][2])
                cur.excute(st)
            return True
        except Exception:
            logging.error(Exception(
                "Adding detail to order[" + order_id.__str__() + '] encountered exceptions, try rolling back'))
            return False
        finally:
            if cur is not None:
                cur.close()

    # TODO: delete order when detail insertion failed, maybe rollback?
    def add_single_order(self, comment_seller, deliver_id, customer_id, payment_status, total_price, order_date,
                         payment_date, last_update, seller_id, detail):
        if self._any_none([customer_id, total_price, detail]):
            return False
        # type check on detail: should be [(cmt, (o_id OMITTED!!) i_id, qua), (), ...]
        if not isinstance(detail, list):
            return False
        if not self._check_detail(detail):
            return False
        if payment_status is None or payment_status == 0:
            payment_status = 0
            payment_date = 'NULL'
        if payment_status > 1:
            payment_date = 'CURRENT'
        order_date = last_update = 'CURRENT'
        st = self.stat.add_single_order(comment_seller, deliver_id, customer_id, payment_status, total_price,
                                        order_date, payment_date, last_update, seller_id)
        self._sql_execute(st)
        order_id = self._sql_last_insert()
        if self._add_detail(detail, order_id):
            return True
        else:
            # TODO: please implement me
            pass

    # end of adding methods

    def exist_user_id(self, user_id):
        try:
            if self._is_none(user_id):
                return
            sql_str = 'select * from ' + self.__userTabName + ' where user_id = ' + user_id.__str__()
            ans = self._sql_count(sql_str)
            if ans > 1:
                raise Exception("User ID replication found on " + user_id.__str__())
            return ans == 1
        except Exception as e:
            logging.exception(e)
            return False

    def exist_user_name(self, user_name):
        try:
            if self._is_none(user_name):
                return
            st = 'select * from ' + self.__userTabName + ' where user_name like \'' + user_name + '\''
            ans = self._sql_count(st)
            return ans > 0
        except Exception as e:
            logging.exception(e)
            return False

    def check_login(self, user_name, user_pass):
        st = self.stat.check_login(user_name, user_pass)
        ans = self._sql_fetchall(st)
        if len(ans) != 1:
            return None
        else:
            return {'user_name': ans[0][0], 'user_privilege': ans[0][1], 'user_id': ans[0][2]}

    # TODO: check roll back possibilities, or use valid bit
    # TODO: check db's return on update statement
    # TODO: check optimistic lock or pessimistic lock

    def update_inventory_quantity(self, inventory_id, quantity_diff):
        st = self.stat.update_inventory_quantity(inventory_id, quantity_diff)
        if self._sql_execute(st):
            return True
        else:
            return False

    def update_inventory_price(self, inventory_id, new_price):
        st = self.stat.update_inventory_price(inventory_id, new_price)
        if self._sql_execute(st):
            return True
        else:
            return False

    @staticmethod
    def _make_dict_list(att, val):
        if att is None or val is None or len(att) != len(val[0]):
            raise Exception('sql_request._make_dict receive invalid param')
        ans = []
        for tup in val:
            dic = {}
            for i in range(0, len(att)):
                dic[att[i]] = tup[i]
            ans.append(dic)
        return ans

    def _make_inventory_dict(self, val):
        return self._make_dict_list(self.__inventoryAttr, val)

    def search_inventory_id(self, inventory_id):
        st = self.stat.search_inventory_id(inventory_id)
        ans = self._sql_fetchall(st)
        if ans:
            return self._make_inventory_dict(ans)
        else:
            return False

    def search_inventory(self, page_size=10, page_num=0, inventory_name=None, inventory_desc=None, price_up=None,
                         price_down=None, category_id=None, seller_id=None):
        # st = self.stat.search_inventory(inventory_name, inventory_desc, price_up, price_down, category_id, seller_id)
        # ans = self._sql_fetchall(st)
        # return self._make_inventory_dict(ans)
        st = self.stat.search_inventory_page(page_size, page_num, inventory_name, inventory_desc, price_up, price_down,
                                             category_id, seller_id)
        ans = self._sql_fetchall(st)
        if ans:
            return self._make_inventory_dict(ans)
        else:
            return False


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



