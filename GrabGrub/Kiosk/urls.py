from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login, name="login"),
    path('create_account', views.create_account, name="create_account"),
    path('homepage', views.homepage, name="homepage"),
    path('add_order', views.add_order, name="add_order"),
    path('view_order_details/<int:pk>', views.view_order_details, name="view_order_details"),
    path('update_order_details/<int:pk>', views.update_order_details, name="update_order_details"),
    path('confirm_delete_order/<int:pk>', views.confirm_delete_order, name="confirm_delete_order"),
    path('delete_order/<int:pk>', views.delete_order, name="delete_order"),
    path('view_food_items', views.view_food_items, name="view_food_items"),
    path('update_food_item/<int:pk>', views.update_food_item, name="update_food_item"),
    path('confirm_delete_food/<int:pk>', views.confirm_delete_food, name="confirm_delete_food"),
    path('delete_food/<int:pk>', views.delete_food, name="delete_food"),
    path('add_food_item', views.add_food_item, name="add_food_item"),
    path('view_customers', views.view_customers, name="view_customers"),
    path('update_customer_details/<int:pk>', views.update_customer_details, name="update_customer_details"),
    path('confirm_delete_customer/<int:pk>', views.confirm_delete_customer, name="confirm_delete_customer"),
    path('delete_customer/<int:pk>', views.delete_customer, name="delete_customer")
]
