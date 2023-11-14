from rest_framework import serializers
from .models import Product,Picture


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('serialnumber','getmainpicture','fullname','getbrand','getcategory')
        depth = 1

    def getmainpicture(self,obj):
        plist = Picture.objects.filter(product = obj).first()
        print(f'picture list :  {plist.img.url}')
        return str(plist.img.url)
    
