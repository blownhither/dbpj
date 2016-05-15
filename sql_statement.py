class SqlStatement:
    def __init__(self):
        self.__sellerName = 'seller'
        self.__categoryName = 'category'
        self.__inventoryName = 'inventory'
        self.__customerName = 'customer'
        self.__userTabName = 'user_info'
        self.__orderName = 'single_order'
        self.__currentName = 'current'
        self.__detailName = 'detail'

    @staticmethod
    def _is_none(att):
        if att is None:
            print('Unspecified Key Fields ')
            return True

    @staticmethod
    def _is_dict(obj):
        if not isinstance(obj,dict):
            print("Unexpected parameter type other than dict")

    @staticmethod
    def _none_null(obj):
        if obj is None:
            return 'NULL'
        else:
            if hasattr(obj, '__str__'):
                return obj.__str__()
            else:
                return obj

    @staticmethod
    def _add_statement(tab_name, str_count, l):
        st = 'insert into ' + tab_name + ' values ('
        for i in l:
            if i is None:
                st += 'NULL,'
            else:
                if hasattr(i, '__str__'):
                    i = i.__str__()
                if str_count > 0:
                    st += '\'' + i + '\','
                    str_count -= 1
                else:
                    st += i + ','
        st = st[0:-1]
        st += ');'
        return st

    def  _update_statement(self, tab_name, str_count, attr_list, val_list, attr_old, val_old, str_old):
        # should NOT be used when condition is ' attr is NULL '
        st = 'update ' + tab_name + ' set '
        for i in range(0, len(attr_list)):
            st += attr_list[i] + '='
            if hasattr(val_list[i], '__str__'):
                val_list[i] = val_list[i].__str__()
            if str_count > 0:
                st += '\'' + val_list[i] + '\','
                str_count -= 1
            else:
                st += val_list[i] + ','
        st = st[0:-1] + ' where '
        for i in range(0, len(attr_old)):
            st += attr_old[i] + '='
            if hasattr(val_old[i], '__str__'):
                val_old[i] = val_old[i].__str__()
            if str_old > 0:
                st += '\'' + val_old[i] + '\','
                str_old -= 1
            else:
                st += val_old[i] + ','

    def add_category(self, category_title=None, category_desc=None):
        # st = 'insert into ' + self.__categoryName + ' values (\'' + category_title + '\', \'' + self._none_null(category_desc) + '\', 0);'
        st = self._add_statement(self.__categoryName, 2, [category_title, category_desc, 0])
        return st

    def add_user(self, name, passw, prev):
        st = self._add_statement(self.__userTabName, 2, [name, passw, prev, 0])
        return st

    def add_seller(self, seller_name, seller_addr, user_id):
        st = self._add_statement(self.__sellerName, 2, [seller_name, seller_addr, user_id])
        return st

    def add_customer(self, customer_name, customer_email, user_id):
        st = self._add_statement(self.__sellerName, 2, [customer_name, customer_email, user_id])
        return st

    def add_inventory(self, inventory_name, inventory_desc, picture_url, inventory_price, inventory_quantity,
                      category_id, seller_id):
        st = self._add_statement(self.__inventoryName, 3, [inventory_name, inventory_desc, picture_url, inventory_price, inventory_quantity,
                                                           category_id, seller_id, 0])
        return st

    def add_single_order(self, comment_seller, deliver_id, customer_id, payment_status, total_price, order_date, payment_date, last_update, seller_id):
        # if payment_status is None:
        #     payment_status = 0
        #     payment_date = 'NULL'
        # if payment_status > 1:
        #     payment_date = 'CURRENT'
        # order_date = last_update = 'CURRENT'
        st = self._add_statement(self.__orderName, 2, [comment_seller, deliver_id, customer_id, payment_status, total_price, order_date, payment_date, last_update, seller_id, 0])
        return st

    def add_detail(self, comment_inventory, order_id, inventory_id, quantitiy=1):
        st = self._add_statement(self.__detailName, 1, [comment_inventory, order_id, inventory_id, quantitiy])
        return st

    def check_login(self, user_name, user_pass):
        st = 'select user_name, user_privilege, user_id from ' + self.__userTabName + ' where user_name like \'' + user_name + '\' and user_pass like \'' + user_pass + '\';'
        return st

    def update_inventory_quantity(self, inventory_id, quantity_diff):
        st = 'update ' + self.__inventoryName + ' set inventory_quantity = inventory_quantity +' + quantity_diff.__str__() + ' '
        st += 'where inventory_id = ' + inventory_id.__str__() + ' and inventory_quantity > -(' + quantity_diff.__str__() + ');'
        return st

    def update_inventory_price(self, inventory_id, new_price):
        st = 'update ' + self.__inventoryName + ' set inventory_price = ' + new_price.__str__() + ' '
        st += 'where inventory_id = ' + inventory_id.__str__() + ';'



    # def update_inventory(self, inventory_name, inventory_desc, picture_url, inventory_price, inventory_quantity,
    #                   category_id, seller_id):
    #     pass

    def delete_inventory(self, inventory_id):
        st = 'delete from ' + self.__inventoryName
        st += ' where inventory_id = ' + inventory_id.__str__()
        # TODO
