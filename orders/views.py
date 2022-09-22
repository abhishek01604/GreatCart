import datetime
from django.template.loader import render_to_string
from carts.models import CartItem
from django.shortcuts import redirect, HttpResponse,render
from django.core.mail import EmailMessage
from .forms import OrderForm
from .models import Order,OrderProduct
from store.models import Product


# Create your views here.


def payments(request):
    ord = request.GET.get('on')
    # print(order_number)
    order = Order.objects.get(order_number=ord)
    order.is_ordered = True
    order.save()

    cart_item = CartItem.objects.filter(user=request.user)

    for item in cart_item:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price= item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        cart_item = CartItem.objects.get(id=item.id)
        product_variations = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variations)
        orderproduct.save()

        #reducing the quantity of the sold product
        product = Product.objects.get(id = item.product_id)
        product.stock -= item.quantity
        product.save()

    #clearing cart after ordered
    CartItem.objects.filter(user=request.user).delete()


    #Sending email after successfull order

    mail_subject = 'Thankyou for your order from our store'
    message = render_to_string('accounts/order_recieved_email.html', {
        'user': request.user,
        'order':order,
    })
    to_mail = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_mail])
    send_email.send()


    #Send order number and transaction id back to senddata method via JsonResponse

    ordered_product = OrderProduct.objects.filter(order_id = order.id)
    total=0
    for i in ordered_product:
         total += i.product_price*i.quantity
    orderr = Order.objects.get(order_number=ord)
    orderrr = orderr.order_total-orderr.tax
    ortax = orderr.tax
    GT = float(ortax)+float(orderrr)
    dt = orderr.created_at
    context = {
        'order_number':ord,
        'transID':str('121')+ord+str('101'),
        'order':ordered_product,
        'add':orderr,
        'orderr':orderrr,
        'ortax':ortax,
        'gt':GT,
        'dt':dt,
        'it':total
    }
    # print(context.transID)
    return render(request,'orders/order_complete.html',context)

    # return render(request,'orders/payments.html',context)

def order_complete(request):

    # order_number = request.
    return render(request,'orders/order_complete.html')







def place_order(request, total=0, quantity=0,):
    current_user = request.user
    #
    # if the cart count is less than or equal to 0 then redirect back to shop

    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total) / 100
    grand_total = total + tax
    if request.method == "POST":
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        form = OrderForm(request.POST)
        # print(form)
        if form.is_valid():
            print('True')
        else:
            print('false')
        if form.is_valid():
            print('3333333333333333333333333')
            # store all the information insde order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime('%Y%d%m')
            order_number = current_date + str(data.id)
            print(data.id)

            data.order_number = order_number
            data.save()

            print(data.id)


            order = Order.objects.get(user=current_user,is_ordered = False,order_number=order_number)

            context = {
                'order':order,
                'cart_items':cart_items,
                'total':total,
                'tax':tax,
                'grand_total':grand_total
            }
            # return HttpResponse('ok')
            return render(request,'orders/payments.html',context)

    else:
        return redirect('dashboard')
