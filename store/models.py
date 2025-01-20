from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from random import randint

# Create your models here.

class CustomUser(AbstractUser):
    
    is_verified = models.BooleanField(default=False)

    otp = models.CharField(max_length=10,null=True,blank=True)

    def generate_otp(self):

        self.otp=str(randint(1000,9000)) + str(self.id)

        self.save()


class BaseModel(models.Model):

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)


class Brand(BaseModel):

    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

class Suppliment_Category(BaseModel):

    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

class Equipment_category(BaseModel):

    name=models.CharField(max_length=200)

    def __str__(self):

        return self.name


class Flavour(BaseModel):

    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

class tags(BaseModel):

    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

class Suppliment(BaseModel):

    title=models.CharField(max_length=200)

    description=models.TextField()

    price=models.PositiveIntegerField(help_text="price in INR")

    price_without_offer=models.PositiveIntegerField(null=True,blank=True)

    stock=models.PositiveIntegerField(default=0)

    picture=models.ImageField(upload_to='Suppliment_picture',null=True,blank=True)

    brand_obj=models.ForeignKey(Brand,on_delete=models.CASCADE)

    Suppliment_Category_obj=models.ForeignKey(Suppliment_Category,on_delete=models.CASCADE,related_name='suppliment_category')

    weight=models.DecimalField(max_digits=5, decimal_places=2,help_text="weight in (kg)")

    flavour_obj=models.ManyToManyField(Flavour)

    tag_obj=models.ManyToManyField(tags)


class Equipments(BaseModel):

    title=models.CharField(max_length=200)

    description=models.TextField()

    price=models.PositiveIntegerField(help_text="Price in INR")

    price_without_offer=models.PositiveIntegerField(null=True,blank=True)

    stock=models.PositiveIntegerField(default=0)

    weight=models.DecimalField(max_digits=5, decimal_places=0,help_text="weight in (kg)",null=True,blank=True)

    picture=models.ImageField(upload_to='Equipment_picture',null=True,blank=True)

    brand_obj=models.ForeignKey(Brand,on_delete=models.CASCADE)

    equipment_category_obj=models.ForeignKey(Equipment_category,on_delete=models.CASCADE,related_name='equipment_category')

    Tag_obj=models.ManyToManyField(tags)
    

class Cart(BaseModel):

    owner=models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name="basket")


class Cart_item(BaseModel):

    cart_obj=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="basket_item")

    suppliment_obj=models.ForeignKey(Suppliment,on_delete=models.CASCADE,related_name="product_suppliment",null=True,blank=True)

    equipment_obj=models.ForeignKey(Equipments,on_delete=models.CASCADE,related_name="product_equipment",null=True,blank=True)

    selected_flavour = models.ForeignKey(Flavour, on_delete=models.SET_NULL, null=True, blank=True)

    # tag_obj=models.ManyToManyField(tags) 

    quantity=models.PositiveIntegerField(default=1)

    is_order_placed=models.BooleanField(default=False)


class Orders(BaseModel):

    customer=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="orders")

    address=models.TextField()

    phone=models.CharField(max_length=20)

    PAYMENT_OPTIONS={
        ('COD','COD'),
        ('ONLINE','ONLINE'),
    }

    payment=models.CharField(max_length=100,choices=PAYMENT_OPTIONS,default='ONLINE')

    rzr_order_id=models.CharField(max_length=100,null=True)

    is_paid=models.BooleanField(default=False)


class Order_item(BaseModel):

    order_obj=models.ForeignKey(Orders,on_delete=models.CASCADE,related_name='order_items')

    suppliment_obj=models.ForeignKey(Suppliment,on_delete=models.CASCADE,null=True,blank=True)

    equipment_obj=models.ForeignKey(Equipments,on_delete=models.CASCADE,null=True,blank=True)

    price=models.PositiveIntegerField()

class BMICalculation(BaseModel):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)

    height = models.FloatField(help_text="Height in centimeters")

    weight = models.FloatField(help_text="Weight in kilograms")

    bmi = models.FloatField()

    result = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user} - {self.bmi} ({self.result})"




def create_cart(sender,instance,created,**kwargs):

    if created:

        Cart.objects.create(owner=instance)

post_save.connect(create_cart,sender=CustomUser)


