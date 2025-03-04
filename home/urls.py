from django.urls import path
from . import views

app_name = 'home'  # Namespace for 'home' app

urlpatterns = [
    # Home and Authentication
    path('', views.index_view, name='index'),  # Home page
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboards
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('shopkeeper_dashboard/', views.shopkeeper_dashboard, name='shopkeeper_dashboard'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),

    # Product Management
    path('products/', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('category/<str:category>/', views.filter_products_by_category, name='filter_products_by_category'),
    path('add_product/', views.add_product, name='add_product'),
    path('buy-now/<int:product_id>/', views.buy_now_view, name='buy_now'),
    path('payment/process/', views.payment_process_view, name='payment_process'),


    # Shopkeeper Requests
    path('shopkeeper/request/', views.shopkeeper_request_view, name='shopkeeper_request'),
    path('approve_request/<int:request_id>/', views.approve_product_request, name='approve_product_request'),
    path('reject_request/<int:request_id>/', views.reject_product_request, name='reject_product_request'),

    # Cart Operations
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('remove-from-cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('buy-now/<int:product_id>/', views.buy_now_view, name='buy_now'),

    # Checkout
    path('checkout/', views.checkout_view, name='checkout'),

    # Static Pages
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('account/', views.account_view, name='account'),

    # Redirect for unauthenticated users
    path('redirect-to-login/', views.login_view, name='redirect_to_login'),
]
