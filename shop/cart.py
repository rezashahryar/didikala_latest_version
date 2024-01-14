from products.models import Product
from .models import Coupon
from decimal import Decimal


class Cart:
    def __init__(self, request):
        self.session = request.session

        self.coupon_id = self.session.get('coupon_id')

        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}

        self.cart = cart

    def __iter__(self):
        cart = self.cart.copy()

        for item in cart.values():
            product = Product.objects.get(id=int(item['id']))

            item['product'] = product
            if product.discount:
                item['total_price'] = int(item['quantity']) * int(item['product'].get_price_after_discount())
            else:
                item['total_price'] = int(item['quantity']) * int(item['product'].price)
            item['unique_id'] = self.unique_id_generator(product.title, product.slug, item['color'])
            yield item

    def unique_id_generator(self, product_name, slug, color):
        result = f'{slug}-{color}-{product_name}'
        return result

    def add(self, product, quantity, color, replace_current_quantity=False):
        unique = self.unique_id_generator(product.title, product.slug, color)

        if unique not in self.cart:
            self.cart[unique] = {'quantity': 0, 'color': color, 'id': str(product.id)}

        if replace_current_quantity:
            self.cart[unique]['quantity'] = int(quantity)
        else:
            self.cart[unique]['quantity'] += int(quantity)

        self.save()

    def save(self):
        self.session.modified = True

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session['cart']
        self.save()

    def get_total_price(self):
        return sum(item['quantity'] * item['product'].price for item in self.cart.values())

    def amount_payable(self):
        product_ids = self.cart.keys()
        for item in self.cart.values():
            if item['product'].discount:
                result = sum(item['quantity'] * item['product'].get_price_after_discount())
            else:
                result = sum(item['quantity'] * item['product'].price)
            return result
        # return sum(item['quantity'] * item['product'].price for item in self.cart.values())

    def delete(self, id):
        if id in self.cart:
            del self.cart[id]
            self.save()

        # to Coupons
    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    def get_discount(self):
        if self.coupon_id:
            return (self.coupon.discount / Decimal(100)) * self.get_total_price()
        return Decimal(0)

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()

    def get_total_price(self):
        product_ids = self.cart.keys()
        return sum(item['quantity'] * item['product'].price for item in self)