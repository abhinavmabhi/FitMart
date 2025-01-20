# context_processors.py
from store.models import Cart_item

def cart_item_count(request):
    if request.user.is_authenticated:
        # Get the basket for the logged-in user
        basket = request.user.basket
        # Count the items in the basket that are not ordered
        cart_item_count = basket.basket_item.filter(is_order_placed=False).count()

    else:

        cart_item_count = 0

    return {'cart_item_count': cart_item_count}
