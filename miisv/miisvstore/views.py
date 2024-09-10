from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Brand, Cart, CartItem
from .forms import ReviewForm
from django.db.models import Q
from django.http import JsonResponse

# Create your views here.


def productList(request):
    query = request.GET.get('q')
    rating = request.GET.get('rating')  # Rating filter
    min_price = request.GET.get('min_price')  # Minimum price filter
    max_price = request.GET.get('max_price')  # Maximum price filter
    brands = request.GET.getlist('brand')  # Brand filter
    colors = request.GET.getlist('color')  # Color filter
    products = Product.objects.all()
    # Step 1: Perform the initial search based on the query
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description=query))

    # Step 2: Apply additional filters on the search results
    if rating:
        products = products.filter(reviews__rating__gte=rating)

    if min_price:
        products = products.filter(selling_price__gte=min_price)

    if max_price:
        products = products.filter(selling_price__lte=max_price)

    if brands:
        products = products.filter(brand__name__in=brands)

    if colors:
        products = products.filter(color__in=colors)

    # Fetch distinct brands and colors for filter options
    available_brands = Brand.objects.all()
    available_colors = Product.objects.values_list(
        'color', flat=True).distinct()
    return render(request, 'store/product_list.html', {'products': products,
                                                       'available_brands': available_brands,
                                                       'available_colors': available_colors,
                                                       'selected_rating': rating,
                                                       'selected_brands': brands,
                                                       'selected_colors': colors,
                                                       'min_price': min_price,
                                                       'max_price': max_price, })


def productDetails(request, slug):
    product = get_object_or_404(Product, slug=slug)
    reviews = product.reviews.all()  # Fetch all reviews for this product
    # Fetch relevant products based on the same category, excluding the current product
    relevant_products = Product.objects.filter(
        category=product.category).exclude(id=product.id)[:4]
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_details', slug=product.slug)
    else:
        form = ReviewForm()
    return render(request, 'store/product_details.html', {'product': product, 'reviews': reviews, 'form': form, 'relevant_products': relevant_products})


def get_cart(request):
    # Retrieve or create a cart for the user or session
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key or request.session.create()
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart


def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    cart = get_cart(request)

    # Check if the item is already in the cart
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_detail')  # Redirect to the cart details page


def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('cart_detail')


def update_cart_item(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id)
        new_quantity = int(request.POST.get('quantity', 1))
        cart_item.quantity = new_quantity
        cart_item.save()
    return redirect('cart_detail')  # Adjust the redirect as per your setup


def cart_detail(request):
    cart = get_cart(request)
    return render(request, 'store/cart_detail.html', {'cart': cart})
