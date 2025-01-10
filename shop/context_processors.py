from .models import Cart

def cart_count(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        count = Cart.objects.filter(customer=customer).count()
        return {'cart_count': count}
    return {'cart_count': 0}
