from django.db import models
from django.utils.timezone import now
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('mi', 'Mì'),
        ('com', 'Cơm'),
        ('nuoc', 'Nước uống'),
        ('nuoc_tra_sua', 'Trà sữa'),
        ('nuoc_tra', 'Trà'),
        ('nuoc_topping', 'Topping'),
        ('nuoc_khac', 'Các loại khác'),
        ('anvat', 'Ăn vặt'),
        ('mon_them', 'Món thêm'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='mi', verbose_name="Thể loại") 
    name = models.CharField(max_length=100, verbose_name="Tên món")
    description = models.TextField(default="Mô tả mặc định")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Giá")
    image = models.ImageField(upload_to='menu_images/', null=True, blank=True)
    available = models.BooleanField(default=True, verbose_name="Có sẵn")
    
    class Meta:
        verbose_name = "Món ăn"
        verbose_name_plural = "Các món ăn"
    def __str__(self):
        return self.name

class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Đang chờ'), ('completed', 'Hoàn thành')],
        default='pending',
        verbose_name="Trạng thái"
    )
    is_paid = models.BooleanField(default=False, verbose_name="Đã thanh toán")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Tổng tiền")

    def update_total_price(self):
        total = sum(item.item.price * item.quantity for item in self.orderitem_set.all())
        self.total_price = total
        self.save()

    class Meta:
        verbose_name = "Đơn hàng"
        verbose_name_plural = "Các đơn hàng"

    def __str__(self):
        return f"Order {self.id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Đơn hàng")
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, verbose_name="Món ăn")
    quantity = models.IntegerField(verbose_name="Số lượng")

    class Meta:
        verbose_name = "Mục trong đơn hàng"
        verbose_name_plural = "Các mục trong đơn hàng"

@receiver(post_save, sender=OrderItem)
def update_order_total_on_save(sender, instance, **kwargs):
    instance.order.update_total_price()

@receiver(post_delete, sender=OrderItem)
def update_order_total_on_delete(sender, instance, **kwargs):
    instance.order.update_total_price()
