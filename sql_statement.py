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

    def _add_statemnt(self, tab_name, str_count, l):
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

    def add_category(self, category_title=None, category_desc=None):
        # st = 'insert into ' + self.__categoryName + ' values (\'' + category_title + '\', \'' + self._none_null(category_desc) + '\', 0);'
        st = self._add_statemnt(self.__categoryName, 2, [category_title, category_desc, 0])
        return st

    def add_user(self, name, passw, prev):
        st = self._add_statemnt(self.__userTabName, 2, [name, passw, prev, 0])
        return st

    def add_seller(self, seller_name, seller_addr, user_id):
        st = self._add_statemnt(self.__sellerName, 2, [seller_name, seller_addr, user_id])
        return st

    def add_customer(self, customer_name, customer_email, user_id):
        st = self._add_statemnt(self.__sellerName, 2, [customer_name, customer_email, user_id])
        return st

    def add_inventory(self, inventory_name, inventory_desc, picture_url, inventory_price, inventory_quantity,
                      category_id, seller_id):
        st = self._add_statemnt(self.__inventoryName, 3, [inventory_name, inventory_desc, picture_url, inventory_price, inventory_quantity,
                      category_id, seller_id, 0])
        return st

    def add_single_order(self, comment_seller, deliver_id, customer_id, payment_status, total_price, order_date, payment_date, last_update, seller_id):
        # if payment_status is None:
        #     payment_status = 0
        #     payment_date = 'NULL'
        # if payment_status > 1:
        #     payment_date = 'CURRENT'
        # order_date = last_update = 'CURRENT'
        st = self._add_statemnt(self.__orderName, 2, [comment_seller, deliver_id, customer_id, payment_status, total_price, order_date, payment_date, last_update, seller_id, 0])
        return st

    def add_detail(self, comment_inventory, order_id, inventory_id, quantitiy=1):
        st = self._add_statemnt(self.__orderName, 1, [comment_inventory, order_id, inventory_id, quantitiy])
        return st
