from django.contrib import admin
from .models import *
from django_json_widget.widgets import JSONEditorWidget

# Register your models here.

class Pictureinline(admin.TabularInline):
    model=Picture
class Detailinline(admin.TabularInline):
    model=Detail
class Detailoptioninline(admin.TabularInline):
    model=Detailoption
class Flaginline(admin.TabularInline):
    model=Flag
class Categoryinline(admin.TabularInline):
    model=Category
class Faqinline(admin.TabularInline):
    model=Faq
class Productinline(admin.TabularInline):
    model=Product
class Commentinline(admin.TabularInline):
    model=Comment
class Brandinline(admin.TabularInline):
    model=Brand
class Addressinline(admin.TabularInline):
    model=Address

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    def regroup_by(self):
        return 'category'
    list_display = ('name','category')
    inlines = [

        Productinline,

    ]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    def regroup_by(self):
        return 'category'
    list_display = ('name','price','amount','brand')
    inlines = [

        Pictureinline,
        Detailinline,
        Flaginline,
        Faqinline,

    ]
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title','get_sub')
    inlines = [
        Categoryinline,
        Brandinline,
    ]
    def get_sub(self,obj):
        return obj.parent

@admin.register(Detail)
class DetailAdmin(admin.ModelAdmin):
    list_display = ('get_product','key','value')
    inlines=[
        Detailoptioninline,
    ]
    def get_product(self,obj):
        return obj.product.name
    
@admin.register(Detailoption)
class DetailoptionAdmin(admin.ModelAdmin):
    list_display = ('get_detail','name','info')

    def get_detail(self,obj):
        return obj.detail.key
     
@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ('get_product','name')

    def get_product(self,obj):
        return obj.product.name
    
@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ('get_product','title','text','date')

    def get_product(self,obj):
        return obj.replytoproduct.name
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('get_product','title','text','date','rate','rateofcomment')

    def get_product(self,obj):
        return obj.replytoproduct.name










class Checkoutinline(admin.TabularInline):
    model=Checkout

@admin.register(Userprofile)
class UserprofileAdmin(admin.ModelAdmin):
    list_display = ('get_user','name','mobile','get_checkout')
    inlines = [
        Checkoutinline,
        Addressinline,
    ]
    def get_user(self,obj):
        return obj.user.username
    def get_checkout(self,obj):
        chlist = Checkout.objects.filter(user = obj.user)
        if chlist:
            count = 0
            for item in chlist:
                count = count + int(item.amount)
            return count
        else:
            return 'empty'
        
class Productinline(admin.TabularInline):
    model=Product

@admin.register(Checkout)
class CheckoutAdmin(admin.ModelAdmin):
    list_display = ('get_user','get_product','amount')

    def get_user(self,obj):
        return obj.user.username
    def get_product(self,obj):
        return obj.product.name
    


admin.site.register(Address)
admin.site.register(Payaddress)
admin.site.register(Image)
admin.site.register(Magazine)