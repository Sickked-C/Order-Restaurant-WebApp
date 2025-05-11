from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .models import MenuItem, Order, OrderItem
from .serializers import MenuItemSerializer, OrderSerializer
from django.utils.dateparse import parse_date
from django.db.models import Q

class MenuItemList(generics.ListAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

class MenuItemListView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            menu_items = MenuItem.objects.all()
            serializer = MenuItemSerializer(menu_items, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            order = Order.objects.create()
            total_price = 0
            for item in data['items']:
                try:
                    menu_item = MenuItem.objects.get(id=item['item'])
                    quantity = item['quantity']
                    OrderItem.objects.create(order=order, item=menu_item, quantity=quantity)
                    total_price += menu_item.price * quantity
                except MenuItem.DoesNotExist:
                    return Response({"error": f"Không tìm thấy món ăn với id {item['item']}"}, status=status.HTTP_400_BAD_REQUEST)
            order.total_price = total_price
            order.save()
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": "Lỗi khi tạo đơn hàng"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrderUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def list(self, request, *args, **kwargs):
        # Lấy các tham số lọc từ query params
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        month = request.query_params.get('month')

        # Lọc theo khoảng ngày
        if start_date and end_date:
            try:
                start_date = parse_date(start_date)
                end_date = parse_date(end_date)
                self.queryset = self.queryset.filter(created_at__date__range=(start_date, end_date))
            except ValueError:
                return Response({"error": "Ngày không hợp lệ"}, status=status.HTTP_400_BAD_REQUEST)

        # Lọc theo tháng
        if month:
            try:
                month = int(month)
                self.queryset = self.queryset.filter(created_at__month=month)
            except ValueError:
                return Response({"error": "Tháng không hợp lệ"}, status=status.HTTP_400_BAD_REQUEST)

        # Trả về thông tin cơ bản của đơn hàng
        orders = self.queryset.values('id', 'table_number', 'created_at', 'status', 'is_paid', 'total_price')
        return Response(orders)

    def retrieve(self, request, *args, **kwargs):
        # Trả về chi tiết đơn hàng khi admin nhấn vào
        return super().retrieve(request, *args, **kwargs)
