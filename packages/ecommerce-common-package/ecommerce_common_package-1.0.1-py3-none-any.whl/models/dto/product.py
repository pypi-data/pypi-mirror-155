from complex_json.complex_serializer import ComplexJsonSerializer
from validation.common_validator import NumberValidator, StringValidator

class Category(ComplexJsonSerializer):
    
    name = StringValidator(255)
    description = StringValidator(255)
    origin = StringValidator(255)
    
    def __init__(self, name, description, origin, child_categories: list['Category']):
        self.errors: list[ValueError] = []
        try:
            self.name = name
        except ValueError as e:
            self.errors.append(e)
        try:
            self.description = description
        except ValueError as e:
            self.errors.append(e)
        try:
            self.origin = origin
        except ValueError as e:
            self.errors.append(e)
        self.child_categories = child_categories
        
    def toJson(self):
        return dict(name=self.name, description=self.description, child_categories=[x.toJson() for x in self.child_categories])
        

class Product(ComplexJsonSerializer):    
    
    name = StringValidator(255)
    sku = StringValidator(255)
    description = StringValidator(255)
    price = NumberValidator(max_value=None)
    product_code = StringValidator(255)
    origin = StringValidator(255)
    VATCode = NumberValidator(max_value=None)
    
    def __init__(self, product_code, name, sku, description, price, category: Category, origin, VATCode):
        self.errors: list[ValueError] = []
        try:
            self.name = name
        except ValueError as e:
            self.errors.append(e)
        try:
            self.sku = sku
        except ValueError as e:
            self.errors.append(e)
        try:
            self.description = description
        except ValueError as e:
            self.errors.append(e)
        try:
            self.price = price
        except ValueError as e:
            self.errors.append(e)
        try:
            self.product_code = product_code
        except ValueError as e:
            self.errors.append(e)
        try:
            self.origin = origin
        except ValueError as e:
            self.errors.append(e)
        try:
            self.VATCode = VATCode
        except ValueError as e:
            self.errors.append(e)
        self.category = category
        
    def toJson(self):
        return dict(name=self.name, sku=self.sku, description=self.description, price=self.price, category=self.category, product_code=self.product_code, origin=self.origin, VATCode=self.VATCode)