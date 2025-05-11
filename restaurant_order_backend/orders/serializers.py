from rest_framework import serializers
from .models import MenuItem, Order, OrderItem

class MenuItemSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()  # Trả về URL đầy đủ của ảnh

    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price', 'image', 'available', 'category']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

class OrderItemDetailSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name')
    item_price = serializers.DecimalField(source='item.price', max_digits=10, decimal_places=2)

    class Meta:
        model = OrderItem
        fields = ['item_name', 'quantity', 'item_price']

class OrderSerializer(serializers.ModelSerializer):
    formatted_total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'created_at', 'status', 'is_paid', 'formatted_total_price']  # Sử dụng giá trị định dạng

    def get_formatted_total_price(self, obj):
        return f"{int(obj.total_price):,} VND"  # Định dạng giá trị
