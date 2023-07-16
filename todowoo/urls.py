
from django.contrib import admin
from django.urls import path
from todo import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth web pages
    path('signup/', views.signupuser, name='signupuser'),
    path('login/', views.loginuser, name='loginuser'),
    path('logout/', views.logoutuser, name='logoutuser'),


    path('about/', views.about, name='about'),
    path('product/', views.product, name='product'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),



    # general web pages
    path('', views.home, name='home'),
    path('product_inventory/', views.product_inventory, name='product_inventory'),
    path('raw_material_inventory/', views.raw_material_inventory, name='raw_material_inventory'),
    path('purchase_forcasting/', views.purchase_forcasting, name='purchase_forcasting'),

    path('your_profile/', views.your_profile, name='your_profile'),
    path('place_your_order/', views.place_your_order, name='place_your_order'),
    path('placed_orders/', views.placed_orders, name='placed_orders'),
    path('order_history/', views.order_history, name='order_history'),
    path('placed_orders_by_retailer/', views.placed_orders_by_retailer, name='placed_orders_by_retailer'),
    path('placed_orders_history_of_retailer/', views.placed_orders_history_of_retailer, name='placed_orders_history_of_retailer'),
    path('placed_orders_by_distributor/', views.placed_orders_by_distributor, name='placed_orders_by_distributor'),
    path('placed_orders_history_of_distributor/', views.placed_orders_history_of_distributor, name='placed_orders_history_of_distributor'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

