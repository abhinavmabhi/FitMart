from django.shortcuts import render,redirect

from django.core.mail import send_mail

from django.views.generic import View

from django.contrib import messages

from django.contrib.auth import authenticate,login,logout

from store.forms import SignUpForm,SignInForm,OrderForm

from store.models import CustomUser,Suppliment,Equipments,Cart_item,Order_item,Orders

from django.shortcuts import get_object_or_404

from django.db.models import Sum,Q

from django.views.decorators.csrf import csrf_exempt

from django.utils.decorators import method_decorator

from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.decorators.cache import never_cache

from store.forms import BMIForm

from store.models import BMICalculation


# -------  razor pay keyID nd key_secret-----

key_id='rzp_test_dPs5y38lQYvpmD'
key_secret='0QndYvbERbFunjlHjOucovUP'


import razorpay


# Create your views here.

def send_email_otp(user):

    user.generate_otp()

    subject = "Kindly Verify your Email Address"

    message = f"otp for your Account verification is {user.otp}"

    from_email = "abhinavabhi192018@gmail.com"

    recipient_list = [user.email]

    send_mail(subject,message,from_email,recipient_list)

class signUpView(View):

    template_name="SignUp.html"

    form_class = SignUpForm

    def get(self,request,*args,**kwargs):

        form_instance = self.form_class()

        return render(request,self.template_name,{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance = self.form_class(request.POST)

        if form_instance.is_valid():

            user_object=form_instance.save(commit=False)

            user_object.is_active=False

            user_object.save()

            send_email_otp(user_object)

            return redirect("verify-email")
        
        return render(request,self.template_name,{"form":form_instance})

class verifyEmailView(View):

    template_name = "verify_email.html"

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):

        otp = request.POST.get("otp") 

        if not otp:  

            messages.error(request, "Please enter the OTP.") 
            return render(request, self.template_name)  

        print(f"Submitted OTP: {otp}")  

        try:
            user_object = CustomUser.objects.get(otp=otp)  

            user_object.is_active = True
            user_object.is_verified = True
            user_object.otp = None  # Clear OTP after successful verification
            user_object.save()

            return redirect("signin")

        except CustomUser.DoesNotExist: 
            
            messages.error(request, "User DoesNotExist") 

            return render(request, self.template_name) 

        
class SignInView(View):

    template_name = "login.html"

    form_class = SignInForm

    def get(self,request,*args,**kwargs):

        form_instance = self.form_class()

        return render(request,self.template_name,{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance = self.form_class(request.POST)

        if form_instance.is_valid():

            uname = form_instance.cleaned_data.get("username")

            pwd = form_instance.cleaned_data.get("password")

            user_object = authenticate(request, username=uname,password=pwd)

            if user_object:

                login(request, user_object)

                messages.success(request,"login success")

                return redirect("customer_page")
                
            else:

                messages.error(request,"invalid username or password")

        return render(request,self.template_name,{"form":form_instance})
    
class LogOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect('signin')

class Customer_1st_page(LoginRequiredMixin,View):

    login_url = '/login/'

    def get(self,request,*args,**kwargs):

        return render(request,"customer_1st_page.html")

class Customer_Suppliment_index(LoginRequiredMixin,View):

    login_url = '/login/'

    template_name="Customer_suppliment_index.html"

    def get(self,request,*args,**kwargs):

        search_text=request.GET.get("search-text")

        if search_text!=None:

            qs=Suppliment.objects.filter(stock__gt=0)

            qs=qs.filter(Q(title__icontains=search_text) |
                         Q(brand_obj__name__icontains=search_text) |
                         Q(Suppliment_Category_obj__name__icontains=search_text) |
                         Q(tag_obj__name__icontains=search_text)).distinct()
            
        else:

            qs=Suppliment.objects.filter(stock__gt=0)

        return render(request,self.template_name,{"suppliment_data":qs})


class Customer_Equipment_index(LoginRequiredMixin,View):

    login_url = '/login/'

    template_name="Customer_equipment_index.html"

    def get(self,request,*args,**kwargs):

        search_text=request.GET.get("search-text")

        if search_text!=None:

            qs=Equipments.objects.filter(stock__gt=0)

            qs=qs.filter(Q(title__icontains=search_text) |
                         Q(brand_obj__name__icontains=search_text) |
                         Q(equipment_category_obj__name__icontains=search_text) |
                         Q(Tag_obj__name__icontains=search_text)).distinct()
            
        else:

            qs=Equipments.objects.filter(stock__gt=0)
            

        return render(request,self.template_name,{"eqipment_data":qs})
    
class Customer_Suppliment_details(LoginRequiredMixin,View):

    login_url = '/login/'

    template_name="Customer_suppliment_details.html"

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        qs = Suppliment.objects.get(id=id)

        return render(request,self.template_name,{"details":qs})    

class Customer_Equipment_details(LoginRequiredMixin,View):

    login_url = '/login/'

    template_name="Customer_equipment_details.html"

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        qs=Equipments.objects.get(id=id)

        return render(request,self.template_name,{"details":qs})
    
class Add_To_Cart_Item(LoginRequiredMixin,View):

    login_url = '/login/'

    def post(self,request,*args,**kwargs):

        suppliment_id=kwargs.get("suppliment_pk")

        equipment_id=kwargs.get("equipment_pk")

        quantity = int(request.POST.get('quantity', 1))

        try:

            if suppliment_id:

                suppliment_obj=get_object_or_404(Suppliment,id=suppliment_id)

                request.user.basket.basket_item.create(suppliment_obj=suppliment_obj,quantity=quantity)

                messages.success(request, f"Added {Suppliment.title} to your wishlist")

            elif equipment_id:

                 equipment_obj=get_object_or_404(Equipments,id=equipment_id)

                 request.user.basket.basket_item.create(equipment_obj=equipment_obj,quantity=quantity)

                 messages.success(request, f"Added {Equipments.title} to your wishlist")

            else:

                messages.error(request,'No valid product selected')

        except Exception as e:

            messages.error(request, f"failed to add item to the cart: {e}")

        return redirect("cart-list")



class CartListView(LoginRequiredMixin,View):

    login_url = '/login/'
    
    template_name = "cart_list.html"

    def get(self, request, *args, **kwargs):

        qs = request.user.basket.basket_item.filter(is_order_placed=False)
    
        suppliment_total=qs.values('suppliment_obj').aggregate(total=Sum('suppliment_obj__price')).get('total') or 0
        equipment_total=qs.values('equipment_obj').aggregate(total=Sum('equipment_obj__price')).get('total') or 0

        total=suppliment_total+equipment_total

        suppliment_total_without_offer=qs.values('suppliment_obj').aggregate(total=Sum('suppliment_obj__price_without_offer')).get('total') or 0
        equipment_total_without_offer=qs.values('equipment_obj').aggregate(total=Sum('equipment_obj__price_without_offer')).get('total') or 0

        total_without_offer=suppliment_total_without_offer+equipment_total_without_offer

        selected_flavour = request.POST.get('selected_flavour')

        discound=total_without_offer-total

        for item in qs:

            if item.suppliment_obj:

                item.total_price = item.quantity * item.suppliment_obj.price

            elif item.equipment_obj:

                item.total_price = item.quantity * item.equipment_obj.price
            else:
                item.total_price = 0  # Handle case where there is no price available

            context={
                    "data": qs,
                    "total":total_without_offer,
                    "discound":discound,
                    "subtotal": total,
                    "flavor":selected_flavour,
                      }

        return render(request, self.template_name,context)
    

class Cart_item_delete_view(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get('pk')

        Cart_item.objects.get(id=id).delete()

        return redirect('cart-list')
            
class PlaceOrderView(View):

    template_name='place_order.html'

    form_class=OrderForm

    def get(self,request,*args,**kwargs):

        form_instance=self.form_class()

        return render(request,self.template_name,{'form':form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=self.form_class(request.POST)

        if form_instance.is_valid():

            form_instance.instance.customer=request.user

            order_object=form_instance.save()

            basket_item=request.user.basket.basket_item.filter(is_order_placed=False)

            for bi in basket_item:

                if bi.suppliment_obj:
                    price = bi.suppliment_obj.price
                elif bi.equipment_obj:
                    price = bi.equipment_obj.price
                else:
                    price = 0  # Fallback in case neither is set
                    

                Order_item.objects.create(

                    order_obj=order_object,
                    suppliment_obj=bi.suppliment_obj,
                    equipment_obj=bi.equipment_obj,
                    price=price,

                )
                bi.is_order_placed=True 
                bi.save()


            payment_method=form_instance.cleaned_data.get("payment")
            print(payment_method)
            
            if payment_method=="ONLINE":

                client=razorpay.Client(auth=(key_id,key_secret))

                total = sum(bi.quantity * (bi.suppliment_obj.price if bi.suppliment_obj else bi.equipment_obj.price) for bi in basket_item) * 100

                print("Total Order Amount:", total)

                data = {"amount": total, "currency": "INR", "receipt": "order_rcptid_11" }

                payment=client.order.create(data=data)

                rzr_order_id=payment.get('id')

                order_object.rzr_order_id=rzr_order_id

                order_object.save()

                context={
                    'amount':total,
                    'currency':'INR',
                    'key_id':key_id,
                    'order_id':rzr_order_id,
                }

                return render(request,'Payment.html',context)
            
        return redirect('list-orders')

class orders_List_view(View):

    template_name='orders_list.html'

    def get(self,request,*args,**kwargs):

        qs=request.user.orders.all()
        
        return render(request,self.template_name,{'orders':qs})


# class Payment verify
@method_decorator([csrf_exempt],name="dispatch")
class Payment_verification_view(View):

    def post(self,request,*args,**kwargs):

        client=razorpay.Client(auth=(key_id,key_secret))

        try:

            client.utility.verify_payment_signature(request.POST)

            print("payment success")

            order_id=request.POST.get("razorpay_order_id")

            order_object=Orders.objects.get(rzr_order_id=order_id)

            order_object.is_paid=True

            order_object.save()

        except:

            print("payment failed")

        return redirect('list-orders')
        
    
class BMICalculatorView(View):

    template_name = "bmi_calculator.html"

    def get(self, request):

        form = BMIForm()

        return render(request, self.template_name, {"form": form})

    def post(self, request):

        form = BMIForm(request.POST)

        if form.is_valid():

            height_cm = form.cleaned_data['height']

            weight_kg = form.cleaned_data['weight']

            # BMI Calculation
            height_m = height_cm / 100
            
            bmi = weight_kg / (height_m ** 2)

            # Determine the BMI category
            if bmi < 18.5:
                result = "Underweight"
            elif 18.5 <= bmi < 24.9:
                result = "Normal weight"
            elif 25 <= bmi < 29.9:
                result = "Overweight"
            else:
                result = "Obesity"

            # Save the calculation if user is authenticated
            if request.user.is_authenticated:
                BMICalculation.objects.create(
                    user=request.user,
                    height=height_cm,
                    weight=weight_kg,
                    bmi=bmi,
                    result=result
                )

            return render(request, self.template_name, {
                "form": form,
                "bmi": round(bmi, 2),
                "result": result
            })

        return render(request, self.template_name, {"form": form})