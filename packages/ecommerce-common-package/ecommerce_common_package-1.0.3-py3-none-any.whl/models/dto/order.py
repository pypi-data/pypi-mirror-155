from validation.common_validator import DateValidator, NumberValidator, StringValidator
from .product import Product
from .customer import Customer

from complex_json.complex_serializer import ComplexJsonSerializer

class OrderItem(ComplexJsonSerializer):
    
    quantity = NumberValidator(max_value=None)
    price = NumberValidator(max_value=None)
    origin = StringValidator(255)
    
    def __init__(self, quantity, price, origin, product: Product):
        self.errors: list[ValueError] = []
        try:
            self.quantity = quantity
        except ValueError as e:
            self.errors.append(e)
        try:
            self.price = price
        except ValueError as e:
            self.errors.append(e)
        try:
            self.origin = origin
        except ValueError as e:
            self.errors.append(e)
        self.product = product
        
    def toJson(self):
        return {
            'quantity': self.quantity,
            'price': self.price,
            'product': self.product.toJson()
        }
        
class OrderStatus(ComplexJsonSerializer):
    
    status_code = NumberValidator(max_value=None)
    status_description = StringValidator(255)
    
    def __init__(self, status_code, status_description):
        self.errors: list[ValueError] = []
        try:
            self.status_code = status_code
        except ValueError as e:
            self.errors.append(e)
        try:
            self.status_description = status_description
        except ValueError as e:
            self.errors.append(e)
            
    def toJson(self):
        return {
            'status_code': self.status_code,
            'status_description': self.status_description
        }

class Order(ComplexJsonSerializer):
    
    order_code = StringValidator(255)
    order_date = DateValidator()
    origin = StringValidator(255)
    
    def __init__(self, order_code, order_date, origin, customer: Customer, order_status: OrderStatus, items: list[OrderItem]):
        self.errors: list[ValueError] = []
        try:
            self.order_code = order_code
        except ValueError as e:
            self.errors.append(e)
        try:
            self.order_date = order_date
        except ValueError as e:
            self.errors.append(e)
        try:    
            self.origin = origin
        except ValueError as e:
            self.errors.append(e)
        
        self.customer = customer
        self.order_status = order_status
        self.items = items
        
    def toJson(self):
        return {
            'order_code': self.order_code,
            'customer': self.customer.toJson(),
            'order_status': self.order_status.toJson(),
            'items': [x.toJson() for x in self.items],
            'order_date': self.order_date,
            'origin': self.origin
        }
            