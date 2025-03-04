
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate, login, logout
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required, user_passes_test
# from django import forms
# from .models import Product, UserProfile, CartItem, ShopkeeperRequest
# # from django.urls import reverse  # Import reverse



# # Home page view
# def index_view(request):
#     products = Product.objects.all()
#     search_query = request.GET.get('search')
#     if search_query:
#         products = products.filter(name__icontains=search_query)
#     return render(request, 'index.html', {'products': products})

# # Static page views
# def about_view(request):
#     return render(request, 'about.html')

# def contact_view(request):
#     return render(request, 'contact.html')

# def account_view(request):
#     return render(request, 'account.html')

# def user_dashboard(request):
#     user_cart_items = CartItem.objects.filter(user=request.user)
#     return render(request, 'user_dashboard.html', {'cart_items': user_cart_items})

# # Registration form with validation
# class RegisterForm(forms.ModelForm):
#     password1 = forms.CharField(widget=forms.PasswordInput())
#     password2 = forms.CharField(widget=forms.PasswordInput())

#     class Meta:
#         model = User
#         fields = ['username', 'email']

#     def clean_username(self):
#         username = self.cleaned_data.get("username")
#         if User.objects.filter(username=username).exists():
#             raise forms.ValidationError("Username already exists. Please choose a different one.")
#         return username

#     def clean_password2(self):
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 != password2:
#             raise forms.ValidationError("Passwords do not match.")
#         return password2

# # Registration view
# def register(request):
#     if request.method == "POST":
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data["password1"])
#             user.save()
#             role = request.POST.get("role")
#             if role not in ["user", "shopkeeper", "admin"]:
#                 messages.error(request, "Invalid role selection.")
#                 return redirect("home:register")
#             UserProfile.objects.create(user=user, role=role)
#             messages.success(request, "Registration successful. Please log in.")
#             return redirect('home:login')
#     else:
#         form = RegisterForm()
#     return render(request, "register.html", {"form": form})


# def login_view(request):
#     if request.method == "POST":
#         username = request.POST["username"]
#         password = request.POST["password"]
#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)

#             # Ensure UserProfile exists for the user
#             try:
#                 profile = UserProfile.objects.get(user=user)
#             except UserProfile.DoesNotExist:
#                 messages.error(request, "User profile not found. Please contact support.")
#                 return redirect("home:login")

#             # Redirect based on role
#             if profile.role == "user":
#                 return redirect('home:user_dashboard')
#             elif profile.role == "shopkeeper":
#                 return redirect('home:shopkeeper_dashboard')
#             elif profile.role == "admin":
#                 return redirect('home:admin_dashboard')
#             else:
#                 messages.error(request, "Invalid role assigned.")
#                 return redirect("home:index")

#         else:
#             return render(request, "login.html", {"error": "Invalid credentials"})

#     return render(request, "login.html")

# # Logout view
# def logout_view(request):
#     logout(request)
#     messages.success(request, "Logged out successfully.")
#     return redirect('home:index')

# # Admin dashboard
# @login_required(login_url='home:login')
# def admin_dashboard(request):
#     pending_requests = ShopkeeperRequest.objects.filter(approved=False)
#     return render(request, 'admin_dashboard.html', {'pending_requests': pending_requests})

# # Approve shopkeeper request
# @login_required(login_url='home:login')
# def approve_product_request(request, request_id):
#     product_request = get_object_or_404(ShopkeeperRequest, id=request_id)
#     if request.method == "POST":
#         product_request.approved = True
#         product_request.save()
#         Product.objects.create(
#             name=product_request.product_name,
#             description=product_request.product_description,
#             price=product_request.product_price,
#             category=product_request.product_category,
#             image=product_request.product_image,
#             stock=10
#         )
#         messages.success(request, "Product approved and added successfully!")
#         return redirect('home:admin_dashboard')
#     return render(request, 'approve_request.html', {'request': product_request})

# # Reject shopkeeper product request
# @login_required(login_url='home:login')
# def reject_product_request(request, request_id):
#     product_request = get_object_or_404(ShopkeeperRequest, id=request_id)
#     if request.method == "POST":
#         product_request.approved = False
#         product_request.save()
#         messages.info(request, "Product request rejected.")
#         return redirect('home:admin_dashboard')
#     return render(request, 'reject_request.html', {'request': product_request})

# # Shopkeeper adds product request
# @login_required(login_url='home:login')
# def add_product(request):
#     if request.method == "POST":
#         name = request.POST.get('name')
#         description = request.POST.get('description')
#         price = request.POST.get('price')
#         category = request.POST.get('category')
#         image = request.FILES.get('image')

#         if not all([name, description, price, category, image]):
#             messages.error(request, "All fields are required.")
#             return redirect('home:add_product')

#         ShopkeeperRequest.objects.create(
#             user=request.user,
#             product_name=name,
#             product_description=description,
#             product_price=price,
#             product_category=category,
#             product_image=image
#         )
#         messages.success(request, "Product request submitted. Awaiting admin approval.")
#         return redirect('home:shopkeeper_dashboard')

#     return render(request, 'add_product.html')

# # Product details
# def product_detail(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     return render(request, 'product_detail.html', {'product': product})

# def product_list(request):
#     products = Product.objects.all()
#     return render(request, 'product_list.html', {'products': products})

# # Filter products by category
# def filter_products_by_category(request, category):
#     filtered_products = Product.objects.filter(category=category)
#     return render(request, 'filtered_products.html', {'products': filtered_products, 'category': category})

# # Add product to cart with stock validation
# @login_required(login_url='home:login')
# def add_to_cart(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     if product.stock <= 0:
#         messages.error(request, "Not enough stock available!")
#         return redirect('home:product_detail', product_id=product.id)

#     cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
#     if not created:
#         cart_item.quantity += 1

#     try:
#         cart_item.save()
#         messages.success(request, "Product added to cart successfully!")
#     except ValueError as e:
#         messages.error(request, str(e))
#         return redirect('home:product_detail', product_id=product.id)

#     return redirect('home:user_dashboard')


# # Cart view
# @login_required(login_url='home:login')
# def cart_view(request):
#     cart_items = CartItem.objects.filter(user=request.user)
#     return render(request, 'cart.html', {'cart_items': cart_items})

# # Buy now view
# def buy_now_view(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     return render(request, 'buy_now.html', {'product': product})

# # Remove product from cart
# @login_required(login_url='home:login')
# def remove_from_cart(request, cart_item_id):
#     cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
#     cart_item.delete()
#     messages.success(request, "Product removed from cart successfully.")
#     return redirect('home:user_dashboard')

# # Checkout view
# def checkout_view(request):
#     if request.method == 'POST':
#         # Handle payment logic here
#         return redirect('payment_success')
#     return render(request, 'checkout.html')

# def logout_view(request):
#     logout(request)
#     return redirect('home:index')
# # ✅ Check if user is shopkeeper (MUST be defined before use)
# def is_shopkeeper(user):
#     return user.groups.filter(name='shopkeeper').exists()

# # 🏪 Shopkeeper Dashboard View
# @login_required
# @user_passes_test(is_shopkeeper)
# def shopkeeper_dashboard(request):
#     # Retrieve shopkeeper's requests
#     requests = ShopkeeperRequest.objects.filter(user=request.user)
#     return render(request, 'shopkeeper_dashboard.html', {'requests': requests})


# # 🛒 Shopkeeper request view without forms.py
# @login_required
# @user_passes_test(is_shopkeeper)
# def shopkeeper_request_view(request):
#     if request.method == 'POST':
#         product_name = request.POST.get('product_name')
#         product_description = request.POST.get('product_description')
#         product_category = request.POST.get('product_category')
#         product_price = request.POST.get('product_price')
#         product_image = request.FILES.get('product_image')

#         # ✅ Simple validation
#         if product_name and product_description and product_category and product_price and product_image:
#             ShopkeeperRequest.objects.create(
#                 user=request.user,
#                 product_name=product_name,
#                 product_description=product_description,
#                 product_category=product_category,
#                 product_price=product_price,
#                 product_image=product_image
#             )
#             return redirect('shopkeeper_dashboard')
#         else:
#             error = "All fields are required."
#             return render(request, 'shopkeeper_request.html', {'error': error})

#     return render(request, 'shopkeeper_request.html')
# # ✅ Admin approval view
# @login_required
# @user_passes_test(lambda u: u.is_superuser)
# def admin_approve_requests(request):
#     requests = ShopkeeperRequest.objects.filter(approved=False)
#     if request.method == 'POST':
#         req_id = request.POST.get('request_id')
#         action = request.POST.get('action')
#         shop_request = get_object_or_404(ShopkeeperRequest, id=req_id)
#         if action == 'approve':
#             shop_request.approved = True
#             shop_request.save()

#             # Move approved product to main Product model
#             Product.objects.create(
#                 name=shop_request.product_name,
#                 description=shop_request.product_description,
#                 category=shop_request.product_category,
#                 price=shop_request.product_price,
#                 image=shop_request.product_image
#             )
#         elif action == 'reject':
#             shop_request.delete()
#         return redirect('home:admin_approve_requests')

#     return render(request, 'admin_approve_requests.html', {'requests': requests})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django import forms
from .models import Product, UserProfile, CartItem, ShopkeeperRequest

# Home page view
def index_view(request):
    products = Product.objects.all()
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(name__icontains=search_query)
    return render(request, 'index.html', {'products': products})

# Static page views
def about_view(request):
    return render(request, 'about.html')

def contact_view(request):
    return render(request, 'contact.html')

def account_view(request):
    return render(request, 'account.html')

def user_dashboard(request):
    user_cart_items = CartItem.objects.filter(user=request.user)
    return render(request, 'user_dashboard.html', {'cart_items': user_cart_items})

# Registration form with validation
class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists. Please choose a different one.")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

# Registration view
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()
            role = request.POST.get("role")
            if role not in ["user", "shopkeeper", "admin"]:
                messages.error(request, "Invalid role selection.")
                return redirect("home:register")
            UserProfile.objects.create(user=user, role=role)
            messages.success(request, "Registration successful. Please log in.")
            return redirect('home:login')
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})

# Login view
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            try:
                profile = UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:
                messages.error(request, "User profile not found. Please contact support.")
                return redirect("home:login")

            role_redirects = {
                "user": 'home:user_dashboard',
                "shopkeeper": 'home:shopkeeper_dashboard',
                "admin": 'home:admin_dashboard'
            }
            return redirect(role_redirects.get(profile.role, "home:index"))
        else:
            messages.error(request, "Invalid credentials")
            return redirect("home:login")

    return render(request, "login.html")

# Logout view
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('home:index')

# Admin dashboard
@login_required(login_url='home:login')
def admin_dashboard(request):
    pending_requests = ShopkeeperRequest.objects.filter(approved=False)
    return render(request, 'admin_dashboard.html', {'pending_requests': pending_requests})

# Approve/reject shopkeeper request
@login_required(login_url='home:login')
def manage_product_request(request, request_id, action):
    product_request = get_object_or_404(ShopkeeperRequest, id=request_id)
    if request.method == "POST":
        if action == "approve":
            product_request.approved = True
            product_request.save()
            Product.objects.create(
                name=product_request.product_name,
                description=product_request.product_description,
                price=product_request.product_price,
                category=product_request.product_category,
                image=product_request.product_image,
                stock=10
            )
            messages.success(request, "Product approved and added successfully!")
        else:
            product_request.delete()
            messages.info(request, "Product request rejected.")
        return redirect('home:admin_dashboard')

# Shopkeeper Dashboard
@login_required
@user_passes_test(lambda u: UserProfile.objects.filter(user=u, role='shopkeeper').exists())
def shopkeeper_dashboard(request):
    requests = ShopkeeperRequest.objects.filter(user=request.user)
    return render(request, 'shopkeeper_dashboard.html', {'requests': requests})

# Shopkeeper adds product request
@login_required
@user_passes_test(lambda u: UserProfile.objects.filter(user=u, role='shopkeeper').exists())
def add_product(request):
    if request.method == "POST":
        required_fields = ['name', 'description', 'price', 'category', 'image']
        if not all(request.POST.get(field) for field in required_fields):
            messages.error(request, "All fields are required.")
            return redirect('home:add_product')

        ShopkeeperRequest.objects.create(
            user=request.user,
            product_name=request.POST['name'],
            product_description=request.POST['description'],
            product_price=request.POST['price'],
            product_category=request.POST['category'],
            product_image=request.FILES['image']
        )
        messages.success(request, "Product request submitted. Awaiting admin approval.")
        return redirect('home:shopkeeper_dashboard')

    return render(request, 'add_product.html')

# Product views
def product_list(request):
    return render(request, 'product_list.html', {'products': Product.objects.all()})

def product_detail(request, product_id):
    return render(request, 'product_detail.html', {'product': get_object_or_404(Product, id=product_id)})

# Cart functionalities
@login_required(login_url='home:login')
def cart_view(request):
    return render(request, 'cart.html', {'cart_items': CartItem.objects.filter(user=request.user)})

@login_required(login_url='home:login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.stock <= 0:
        messages.error(request, "Not enough stock available!")
    else:
        cart_item, _ = CartItem.objects.get_or_create(user=request.user, product=product)
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, "Product added to cart successfully!")
    return redirect('home:user_dashboard')

@login_required(login_url='home:login')
def remove_from_cart(request, cart_item_id):
    cart_item = CartItem.objects.filter(id=cart_item_id, user=request.user).first()

    if cart_item:
        cart_item.delete()
        messages.success(request, "Product removed from cart successfully.")
    else:
        messages.error(request, "Item not found in your cart.")

    return redirect('cart_view')
def filter_products_by_category(request, category):
    products = Product.objects.filter(category=category)
    return render(request, 'products.html', {'products': products})
def shopkeeper_request_view(request):
    return render(request, 'shopkeeper_request.html')  # Ensure this template exists

# Function to approve a product request
def approve_product_request(request, request_id):
    product_request = get_object_or_404(ShopkeeperRequest, id=request_id)
    product_request.status = 'approved'
    product_request.save()
    return redirect('shopkeeper_request')

# Function to reject a product request
def reject_product_request(request, request_id):
    product_request = get_object_or_404(ShopkeeperRequest, id=request_id)
    product_request.status = 'rejected'
    product_request.save()
    return redirect('shopkeeper_request')
def buy_now_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # You can add logic for payment processing here
    return render(request, 'buy_now.html', {'product': product})


def checkout_view(request):
    return render(request, 'checkout.html')  # Ensure this template exists
def payment_process_view(request):
    return render(request, 'payment_process.html')  # Ensure this template exists
def cart_view(request):
    return render(request, 'cart.html')  # Ensure 'cart.html' exists in your templates
