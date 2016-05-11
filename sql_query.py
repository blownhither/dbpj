class SqlStatement:
    def __init__(self):
        print("New SqlQuery")
        self.__database = 'd_1460371357365469'
        self.__server = 'ifxserver1'
        self.__username = 'tqbodnho'
        self.__password = 'JSe2lR1cH6'
        self.__categoryName = 'category'
        # self.__itemName = 'item'
        self.__sellerName = 'seller'
        self.__inventoryName = 'inventory'
        self.__customerName = 'customer'
        self.__userName = 'user_info'
        self.__orderName = 'single_order'
        self.__currentName = 'current'
        self.__detailName = 'detail'

    @staticmethod
    def _is_none(att):
        if att is None:
            print('Unspecified Key Fields ')
            return True

    @staticmethod
    def _none_null(att):
        if att is None:
            return 'NULL'
        else:
            return att.__str__()

    def _add_fields(self, tab_name, n, v_list, char_count=0):
        s = "insert into " + tab_name + " values( "
        v_count = 0
        for i in v_list:
            if char_count > 0:
                s += '\'' + self._none_null(i) + '\','
                char_count -= 1
            else:
                s += self._none_null(i) + ','
            v_count += 1
        while v_count < n:
            v_count += 1
            s += 'NULL,'
        s = s[:-1]
        s += ');'
        return s

    def add_category(self, title, desc=None):  # used by administrator
        return self._add_fields(self.__categoryName, 3, [title, desc, None], 2)

    def add_user(self, name, passw, prev):
        if id in None or name is None or passw is None or prev is None:
            print("Unspecified Key Field(s) When add user")
            return
        return self._add_fields(self.__userName, 4, [name, passw, prev, None], 2)

    def add_seller(self, id, name, addr=None):
        print("make sure to add user first.")
        return self._add_fields(self.__sellerName, 3, [name, addr, None], 2)

    def add_inventory(self, name, price, desc, picture, quantity, category, seller):
        if price is None or name is None:
            print("Unspecified Key Field(s) When add inventory")
            return
        return self._add_fields(self.__inventoryName, 8, [name, desc, picture, price, quantity, category, seller, None],
                                3)

    def add_customer(self, name, email, id):
        print("make sure to add user first.")
        return self._add_fields(self.__customerName, 3, [name, email, id], 2)

    def add_order(self, deliver_id, comment_seller, customer_id, payment_status, total_price, order_date, payment_date,
                  last_update, seller_id, order_id):
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

    def search_inventory(self, inventory_name, category_title=None, ):
        
