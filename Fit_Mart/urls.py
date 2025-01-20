"""
URL configuration for Fit_Mart project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from store import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('signup/',views.signUpView.as_view(),name='signup'),

    path('verify/',views.verifyEmailView.as_view(),name='verify-email'),

    path('',views.SignInView.as_view(),name='signin'),

    path('logout/',views.LogOutView.as_view(),name='logout'),

    path('customer/page/',views.Customer_1st_page.as_view(),name='customer_page'),

    # cusomer index 

    path('customer/suppliment/index/',views.Customer_Suppliment_index.as_view(),name='customer-suppliment-index'),

    path('customer/equipment/index/',views.Customer_Equipment_index.as_view(),name='customer-equipment-index'),

    # customer products details

    path('customer/suppliment/<int:pk>/',views.Customer_Suppliment_details.as_view(),name='customer-suppliment-details'),

    path('customer/equipment/<int:pk>/',views.Customer_Equipment_details.as_view(),name='customer-equipment-details'),

    # add to cart

    path('add-to-cart/suppliment/<int:suppliment_pk>/', views.Add_To_Cart_Item.as_view(), name='add-to-cart-suppliment'),

    path('add-to-cart/equipment/<int:equipment_pk>/', views.Add_To_Cart_Item.as_view(), name='add-to-cart-equipment'),

    # cart list view 

    path('cart/item/list/',views.CartListView.as_view(),name='cart-list'),

    # cart delete 

    path('cart/item/delete/<int:pk>',views.Cart_item_delete_view.as_view(),name='cart-item-delete'),

    # place order 

    path('place/order/',views.PlaceOrderView.as_view(),name='place-order'),

    # list orders 

    path('list/orders/',views.orders_List_view.as_view(),name='list-orders'),


    # payment verification 

    path('payment/verify/',views.Payment_verification_view.as_view(),name="payment-verification"),

    # bmi calculator 

    path('bmi/',views.BMICalculatorView.as_view(),name='bmi')


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
