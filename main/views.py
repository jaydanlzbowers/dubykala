from django.shortcuts import render
from .models import *
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect,Http404
from .serializer import ProductSerializer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
import random
# Create your views here.
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required


    
def search(request):
    if request.method=='POST':
        keyword = request.POST.get('keyword')

        search = Product.objects.filter(name__contains = keyword )
        search |= Product.objects.filter(fullname__contains = keyword )
        search |= Product.objects.filter(brand__name__contains = keyword )

        pasnameserial = ProductSerializer(search ,many=True)
        print(f'search:  {pasnameserial}')
 
        print(f'fullname: { pasnameserial.data }')



        return JsonResponse(pasnameserial.data,safe=False)





def register(request):
    logo = Image.objects.get(name='pagelogo')
    username = request.user.username
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            User.objects.create_user(username=username,email=username,password=password)
            user = authenticate(username=username, password=password)
            payaddress = Payaddress.objects.all().order_by('?').first()
            print(payaddress)

            login(request , user)

            

            Userprofile.objects.create( user = user , payaddress = payaddress ,name = username, mobile=username ,email=username )

            return HttpResponseRedirect('/profile/editprofile')
        except:
            print(OSError.strerror)
            try:
                user = authenticate(username=username, password=password)
                login(request,user)
                return HttpResponseRedirect('/')
            except:
                print(OSError)
                return HttpResponseRedirect('/register')


    
    d={
        'logo':logo,
    }
    return render(request , 'registration/login.html',d)

















def magazine(request,name=''):
    cats = Category.objects.filter(slug=0)

    magazine = Magazine.objects.filter(name=name).first()

    d = {
        'categories':cats,
        'magazine':magazine,

    }
    return render(request,'magazine.html',d)




def homepage(request):
    cats = Category.objects.filter(slug=0)
    brands = Brand.objects.all()
    bestsell = Product.objects.all().order_by('saleamount')[0:10]
    offers = Product.objects.all().exclude(offer=0)[0:10]
    magazines = Magazine.objects.all().order_by('-pk')[0:4]

    bannerimg = Image.objects.filter(name='bannerimg')[0]

    d = {
        'categories':cats,
        'brands':brands,
        'bestsell':bestsell,
        'offers':offers,
        'magazines':magazines,
        'bannerimg':bannerimg,

    }
    return render(request,'homepage.html',d)


def category(request):
    cats = Category.objects.filter(slug=0)
    d = {
        'categories':cats,

    }
    return render(request,'category.html',d)

def checkout(request):
    cats = Category.objects.filter(slug=0)
    chlist =[]
    try:
        chlist = Checkout.objects.filter(user= request.user ).exclude(amount=0)
    except:
        pass
    plist = []
    if chlist:
        for ch in chlist:
            print(ch)
            product = ch.product
            plist.append(product)
            print(plist)

    if request.method=='POST':
        productid = int(request.POST.get('productid'))
        counter = int(request.POST.get('counter'))
        if counter == 0:
            Checkout.objects.get(user= request.user, product__serialnumber = productid  ).delete()
            print('delete sucsessfull')
        else:
            ch = Checkout.objects.get(user= request.user, product__serialnumber = productid  )
            ch.amount = counter
            ch.save()
    d = {

        'categories':cats,
        'productlist':plist,
        'numberofp':len(plist),

    }
    return render(request,'checkout/checkout.html',d)
def checkoutaddress(request):
    cats = Category.objects.filter(slug=0)
    chlist = Checkout.objects.filter(user= request.user)
    userprofile = Userprofile.objects.get(user= request.user)
    address = Address.objects.filter(userprofile=userprofile,default=1).first()

    d = {

        'categories':cats,
        'address':address,

    }
    return render(request,'checkout/selectaddress.html',d)


def addtocheckout(request):
    try:
        user=request.user
        userprofile = Userprofile.objects.get(user= user)
    except:
        return Http404()

    if request.method == 'POST':
        serialnumber = int(request.POST['serialnumber'])
        print(serialnumber)
        product=Product.objects.get(serialnumber=serialnumber)

        if Checkout.objects.filter(user=user,userprofile=userprofile,product=product):
            return HttpResponse('در سبد موجود است ')
        else :
            Checkout.objects.create(user=user,userprofile=userprofile,product=product,amount=1,step=1)
            return HttpResponse('اضافه شد')

def payment(request):
    cats = Category.objects.filter(slug=0)
    chlist = Checkout.objects.filter(user= request.user)
    userprofile = Userprofile.objects.get(user= request.user)

    totalprice=0
    totaloffer=0
    for ch in chlist:
        totalprice = totalprice + ch.get_checkout_price()
        totaloffer = totaloffer + ch.amount*ch.product.offer

    totalpay = totalprice-totaloffer
    d = {

        'categories':cats,
        'totalprice':totalprice,
        'totaloffer':totaloffer,
        'totalpay':totalpay,


    }
    return render(request,'checkout/payment.html',d)

def pay(request):
    cats = Category.objects.filter(slug=0)
    chlist = Checkout.objects.filter(user= request.user)
    userprofile = Userprofile.objects.get(user= request.user)

    totalprice=0
    totaloffer=0
    for ch in chlist:
        totalprice = totalprice + ch.get_checkout_price()
        totaloffer = totaloffer + ch.amount*ch.product.offer

    totalpay = totalprice-totaloffer


    payaddress = Payaddress.objects.get(userprofile=userprofile)
    banner = Image.objects.get(name='paycoins')
    loading = Image.objects.get(name='loading')
    d = {

        'categories':cats,
        'totalprice':totalprice,
        'totaloffer':totaloffer,
        'totalpay':totalpay,

        'payaddress':payaddress,
        'banner':banner,
        'loading':loading,


    }
    return render(request,'checkout/pay.html',d)










def selectaddress(request):
    cats = Category.objects.filter(slug=0)
    chlist = Checkout.objects.filter(user= request.user)
    userprofile = Userprofile.objects.get(user= request.user)
    plist = []
    if chlist:
        for ch in chlist:
            print(ch)
            product = ch.product
            plist.append(product)
            print(plist)

    if request.method=='POST':
        addresspk = request.POST.get('addresspk')
        print(addresspk)
        selectedaddress = Address.objects.get(userprofile = userprofile , pk=int(addresspk))
        selectedaddress.default = 1
        selectedaddress.save()
        for ad in  Address.objects.filter(userprofile = userprofile).exclude(pk=addresspk):
            ad.default=0
            ad.save()
    d = {

        'categories':cats,
        'productlist':plist,
        'numberofp':len(plist),

    }
    return render(request,'profile/address.html',d)


def product(request,serialnumber=0):
    cats = Category.objects.filter(slug=0)

    product = Product.objects.get(serialnumber=int(serialnumber))
    colors = Detail.objects.filter(product=product , key = 'color')
    maincomments = Comment.getcomments(product = product)
    faqs = Faq.getmainfaqs(product = product)
    details = product.getdetail()

    if request.method == 'POST':
        commenttext = request.POST.get('commenttext')
        commenttitle = request.POST.get('commenttitle')
        Comment.objects.create(replytoproduct=product,user=request.user,serialofcomment=random.randint(10000000,99999999),title=commenttitle,text=commenttext,date=datetime.now())
        print(commenttitle)



    d = {
        'categories':cats,
        'product':product,
        'colors':colors,
        'maincomments':maincomments,
        'faqs':faqs,
        'nmaincomments':len(maincomments),
        'nfaqs':len(faqs),
        'details':details,



    }
    return render(request,'product/product.html',d)

def leavecomment(request,serialnumber=0):
    cats = Category.objects.filter(slug=0)

    product = Product.objects.get(serialnumber=int(serialnumber))
    colors = Detail.objects.filter(product=product , key = 'color')
    maincomments = Comment.getcomments(product = product)
    faqs = Faq.getmainfaqs(product = product)


    d = {
        'categories':cats,
        'product':product,
        'colors':colors,
        'maincomments':maincomments,
        'faqs':faqs,
        'nmaincomments':len(maincomments),
        'nfaqs':len(faqs),



    }
    return render(request,'product/leavecomment.html',d)




def productlist(request,searchtype=0,keyword=0):
    article = ''
    cats = Category.objects.filter(slug=0)
    if searchtype=='brand':
        if keyword==0:
            products = Product.objects.all()
        else:
            article = Brand.objects.get(name = keyword).article
            products = Product.objects.filter(brand__name=keyword)

    elif searchtype=='category':
        if keyword==0:
            products = Product.objects.all()
        else:
            products = Product.objects.filter(category__name=str(keyword))
    else:
        products = Product.objects.all()
    d = {
        'categories':cats,
        'products':products,
        'numberofp':len(products),
        'article':article,
        'keyword':keyword,


    }
    return render(request,'product/productlist.html',d)





@login_required()
def profile(request):
    userprofile = Userprofile.objects.get(user = request.user)
    cats = Category.objects.filter(slug=0)


    d = {
        'categories':cats,
        'userprofile':userprofile,


    }
    return render(request,'profile/profile.html',d)



def editprofile(request):

    userprofile = Userprofile.objects.get(user = request.user)

    cats = Category.objects.filter(slug=0)


    if request.method=='POST':
        print('sumited')
        name = request.POST.get('name')
        idcode = request.POST.get('idcode')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        job = request.POST.get('job')

        userprofile.name = name
        userprofile.idcode = idcode
        userprofile.mobile = mobile
        userprofile.email = email
        userprofile.job = job

        userprofile.save()
    
    d = {

        'categories':cats,
        'userprofile':userprofile,

    }
    return render(request,'profile/editprofile.html',d)



def addresses(request):
    userprofile = Userprofile.objects.get(user = request.user)
    cats = Category.objects.filter(slug=0)
    addresses = Address.objects.filter(userprofile=userprofile)
    d = {
        'categories':cats,
        'userprofile':userprofile,
        'addresses':addresses,

    }
    return render(request,'profile/address.html',d)


def editaddress(request,addresspk):
    userprofile = Userprofile.objects.get(user = request.user)
    if request.method == 'POST':
        address = request.POST.get('address')
        county= request.POST.get('county')
        city = request.POST.get('city')
        street = request.POST.get('street')
        pelak = request.POST.get('pelak')
        block = request.POST.get('block')
        
        try:
            telephone = int(request.POST.get('telephone'))
            postalcode = int(request.POST.get('postalcode'))
        except:
            telephone=0
            postalcode = 0

        nameofreceiver = request.POST.get('nameofreceiver')
        familyofreceiver = request.POST.get('familyofreceiver')

        if addresspk=='add':
            newaddress = Address.objects.create(userprofile=userprofile, nameofreceiver=nameofreceiver, familyofreceiver=familyofreceiver, county=county, city=city, street=street,pelak=pelak,block=block, postalcode=postalcode, address=address ,telephone=telephone)
            newaddress.save()
        else:
            oldaddress = Address.objects.get(userprofile=userprofile,pk=addresspk)
            oldaddress.address = address
            oldaddress.county= county
            oldaddress.city = city
            oldaddress.street = street
            oldaddress.pelak = pelak
            oldaddress.block = block
            oldaddress.postalcode = postalcode
            oldaddress.nameofreceiver = nameofreceiver
            oldaddress.familyofreceiver = familyofreceiver
            oldaddress.save()
            



    
    cats = Category.objects.filter(slug=0)

    try:
        address = Address.objects.get(userprofile=userprofile,pk=addresspk)
    except:
        address=0
    d = {
        'categories':cats,
        'userprofile':userprofile,
        'address':address,

    }
    return render(request,'profile/editaddress.html',d)

