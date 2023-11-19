from django.db import models
from django_extensions.db.fields import AutoSlugField
from django.contrib.auth.models import User
from colorfield.fields import ColorField
import jdatetime
from datetime import datetime,timedelta
from ckeditor_uploader.fields import RichTextUploadingField

class Payaddress(models.Model):
    Address = models.CharField(max_length=100)
    barcode = models.ImageField(upload_to='Payaddress')
    amount = models.FloatField(default=0)

class Image(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='images')

class Magazine(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    text = RichTextUploadingField()
    img = models.ImageField(upload_to='magazine')











class Category(models.Model):
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank = 
    True, null=True)
    title = models.CharField(max_length=100) 
    name = models.CharField(max_length=100) 
    slug = models.SlugField(unique=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    icon = models.ImageField(upload_to='img_category')

    def __str__(self):
        return self.title

    class Meta:
        #enforcing that there can not be two categories under a parent with same slug

        # __str__ method elaborated later in post.  use __unicode__ in place of

        unique_together = ('slug', 'parent',)    
        verbose_name_plural = "categories"     

    def __str__(self):                           
        full_path = [self.title]                  
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])  

    def get_brands(self):
        print(self.title)
        list = []
        try:
            list = Brand.objects.filter(category = self )
        except:
            pass
        return list



class Brand(models.Model):
    title = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category,on_delete=models.CASCADE, null=True, blank=True)
    article =  RichTextUploadingField()
    img = models.ImageField(upload_to='brands_img')
    def __str__(self):
        return self.name
    def get_products(self):
        print(self.title)
        list = []
        try:
            list = Product.objects.filter(brand = self )
        except:
            pass
        return list

class Product(models.Model):
    serialnumber = models.IntegerField(default=0)
    rate = models.IntegerField(default=5)
    nrate = models.IntegerField(default=0)


    color = ColorField()
    colorname = models.CharField(max_length=200)

    name = models.CharField(max_length=200)
    fullname = models.TextField(max_length=2000)
    price = models.IntegerField(default=0)
    offer = models.IntegerField(default=0)

    amount = models.IntegerField(default=0)
    saleamount = models.IntegerField(default=0)

    brand = models.ForeignKey(Brand,on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE, null=True, blank=True)


    present = RichTextUploadingField()
    specialpresent = RichTextUploadingField()

    def __str__(self):
        return self.name
    
    def getmainpicture(self):
        plist = Picture.objects.filter(product = self).first()
        print(f'picture list :  {plist.img.url}')
        return str(plist.img.url)
    
    def getpicture(self):
        return Picture.objects.filter(product = self)
    def getdetail(self):

        return Detail.objects.filter(product=self).exclude(key='color')
    def getflag(self):
        return Flag.objects.filter(product=self)
    
    def getncomment(self):
        return len(Comment.objects.filter( replytoproduct =self ))
    def getnfaq(self):
        return len(Faq.objects.filter( replytoproduct =self ))
    
    def getpath(self):                           
        full_path = [self.category.title]                  
        k = self.category.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        print('path:')
        return ' / '.join(full_path[::-1])  


    def getbrand(self):
        return str(self.brand.name)
    
    def getcategory(self):
        return str(self.category)
    def getofferprice(self):
        return int(self.price)- int(self.price)*int(self.offer)/100

class Detail(models.Model):
    product = models.ForeignKey( Product , on_delete=models.CASCADE )

    key = models.CharField(max_length=200)
    value = models.CharField(max_length=200)

    def __str__(self):
        return self.key


class Detailoption(models.Model):
    detail = models.ForeignKey( Detail , on_delete=models.CASCADE )

    name = models.CharField(max_length=200)
    info = models.TextField(max_length=2000)
    def __str__(self):
        return self.name
    
class Flag(models.Model):
    product = models.ForeignKey( Product , on_delete=models.CASCADE )

    name = models.CharField(max_length=200)
    info = models.TextField(max_length=2000)
    def __str__(self):
        return self.name

class Picture(models.Model):
    product = models.ForeignKey( Product , on_delete=models.CASCADE )

    name = models.CharField(max_length=200)
    img = models.ImageField(upload_to='product_images')
    def __str__(self):
        return self.name



    






class Comment(models.Model):
    replytoproduct = models.ForeignKey( Product , on_delete=models.CASCADE )
    
    user = models.ForeignKey( User , on_delete=models.CASCADE )
    serialofcomment = models.IntegerField(default=0)

    title = models.CharField(max_length=200)
    text = models.TextField(max_length=2000)
    rate = models.IntegerField(default=5)
    rateofcomment = models.IntegerField(default=0)

    date = models.DateTimeField()
    def __str__(self):
        return f'Comment of({self.user.username}) : '  + ' on product: ' + str(self.replytoproduct.serialnumber)
    
    def getcomments(product):
        return Comment.objects.filter( replytoproduct = product )
    
    def shamsidate(self):
        jalili_date =  jdatetime.date.fromgregorian(day=self.date.day,month=self.date.month,year=self.date.year)
        print(jalili_date)
        return str(jalili_date)
    
class Faq(models.Model):
    replytoproduct = models.ForeignKey( Product , on_delete=models.CASCADE )
    serialtofaq = models.IntegerField(default=0)
    user = models.ForeignKey( User , on_delete=models.CASCADE )
    serialoffaq = models.IntegerField(default=0)


    title = models.CharField(max_length=200)
    text = models.TextField(max_length=2000)
    rate = models.IntegerField(default=5)
    rateoffaq = models.IntegerField(default=0)

    date = models.DateTimeField()
    def shamsidate(self):
        jalili_date =  jdatetime.date.fromgregorian(day=self.date.day,month=self.date.month,year=self.date.year)
        print(jalili_date)
        return str(jalili_date)
    

    def __str__(self):
        return f'Faq of : ({self.user.username})  on product :  + {str(self.replytoproduct.serialnumber)} on freply : {self.serialtofaq}' 
    
    def getmainfaqs(product):
        return Faq.objects.filter( replytoproduct = product , serialtofaq = 0 )
    def getfaqof(product,serialtofaq):
        return Faq.objects.filter( replytoproduct = product , serialoffaq = serialtofaq)





class Userprofile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    payaddress = models.ForeignKey(Payaddress,on_delete=models.CASCADE)

    charge = models.FloatField(default=0)

    name = models.CharField(max_length=200,default='')
    mobile = models.IntegerField(default=0)
    idcode = models.IntegerField(default=0)
    email = models.CharField(max_length=200,default='' )
    job = models.CharField(max_length=200,default='' )

    def get_checkout_i(self):
        chlist = Checkout.objects.filter(userprofile = self)
        if chlist:
            count = 0
            for item in chlist:
                count = count + 1
            return count
        else:
            return 'empty'
        
    def __str__(self):
        return self.name

class Address(models.Model):
    userprofile = models.ForeignKey(Userprofile,on_delete=models.CASCADE)

    nameofreceiver = models.CharField(max_length=200,default='')
    familyofreceiver = models.CharField(max_length=200,default='')
    county = models.CharField(max_length=200,default='')
    city = models.CharField(max_length=200,default='')
    street = models.CharField(max_length=200,default='')
    pelak  = models.CharField(max_length=200,default='')
    block = models.CharField(max_length=200,default='')
    postalcode = models.IntegerField(default=0)
    telephone = models.IntegerField(default=0)

    address = models.CharField(max_length=200)

    default = models.IntegerField(default=0)










class Checkout(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    userprofile  = models.ForeignKey(Userprofile,on_delete=models.CASCADE)

    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    offer = models.IntegerField(default=0)
    step = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.user.username)+ '* buy item'
    
    def get_checkout_price(self):
        return (int(self.product.price)-int(self.product.offer))*int(self.amount)
    



