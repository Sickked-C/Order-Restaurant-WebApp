from django.contrib import admin
from django.utils.timezone import localtime
from django.utils.formats import date_format
from .models import MenuItem, Order, OrderItem
from rangefilter.filters import DateRangeFilter
from django.contrib.admin.views.main import ChangeList
from django.template.response import TemplateResponse

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'formatted_price', 'available')  # Sử dụng phương thức tùy chỉnh để hiển thị giá
    list_filter = ('available',)
    search_fields = ('name',)

    def formatted_price(self, obj):
        return f"{int(obj.price):,} VND"  # Chuyển giá trị thành số nguyên và định dạng
    formatted_price.short_description = "Giá"  # Tiêu đề cột trong Admin

class OrderItemInline(admin.TabularInline):  # Hiển thị các mục trong đơn hàng dưới dạng bảng
    model = OrderItem
    extra = 0  # Không thêm dòng trống mặc định
    fields = ('item', 'quantity')  # Hiển thị các trường cần thiết

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'formatted_total_price', 'status', 'is_paid', 'formatted_created_at')  # Sử dụng phương thức định dạng
    list_filter = ('status', 'is_paid', ('created_at', DateRangeFilter))  # Bộ lọc theo trạng thái và ngày tạo
    search_fields = ('id',)
    inlines = [OrderItemInline]  # Thêm danh sách các mục vào giao diện đơn hàng

    def formatted_total_price(self, obj):
        return f"{int(obj.total_price):,} VND"  # Định dạng giá trị
    formatted_total_price.short_description = "Tổng tiền"  # Tiêu đề cột trong Admin
    
    def formatted_created_at(self, obj):
        # Định dạng ngày giờ theo múi giờ Việt Nam và tiếng Việt
        return date_format(localtime(obj.created_at), "DATETIME_FORMAT")
    formatted_created_at.short_description = "Ngày tạo"  # Tiêu đề cột trong Admin
    
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        
        try:
            cl = response.context_data['cl']
            queryset = cl.queryset
            total = sum(obj.total_price for obj in queryset)
            response.context_data['total_price_sum'] = f"{int(total):,} VND"
        except (AttributeError, KeyError):
            pass

        return response


