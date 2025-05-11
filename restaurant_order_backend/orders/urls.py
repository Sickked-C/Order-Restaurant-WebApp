from django.urls import path
from django.http import JsonResponse
from .views import MenuItemList, OrderListCreateView, OrderUpdateView, MenuItemListView

urlpatterns = [
    path('menu-items/', MenuItemList.as_view(), name='menu-items'),
    path('menu-items/', MenuItemListView.as_view(), name='menu-items'),
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderUpdateView.as_view(), name='order-update'),
    path('', lambda request: JsonResponse({"message": "Welcome to the API!"})),  # Mặc định cho 'api/'
]
