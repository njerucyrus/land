from Crypto.Hash import SHA256
from django.shortcuts import (
    render,
    render_to_response,
    HttpResponse,
    HttpResponseRedirect,
    get_object_or_404,
)
from django.conf import settings

from land.forms import (
    UserRegistrationForm,
    LandUserProfileForm,
    LoginForm,
    RegisterLandForm,
    LandPurchaseForm,
    LandTransferForm,
    ConfirmCodeForm,
)
from land.models import (
    LandUserProfile,
    Land,
    Notification,
    LandSales,
    ChangeLandOwnership,
    LandTransfer,
    LandTransferHistoryLog,

)
from payment.models import (
    Payment,
    LandTransferFee,
    LandTransFerFeePayment,
)
from payment.forms import (
    LandTransFerFeeForm,
)
from land.AfricasTalkingGateway import AfricasTalkingGateway, AfricasTalkingGatewayException
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from random import randint
from django.conf import settings


def index(request):
    return render(request, 'land/index.html', {})

# create a user account and land profile as well


def create_account(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = LandUserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password2'])
            user.save()

            # get the data posted in the form
            cd = profile_form.cleaned_data
            id_no = cd['id_no']
            location = cd['location']
            ward = cd['ward']
            address = cd['address']
            district = cd['district']
            phone_no = cd['phone_number']

            profile = LandUserProfile.objects.create(
                user=user,
                id_no=id_no,
                location=location,
                ward=ward,
                district=district,
                address=address,
                phone_number=phone_no
            )
            profile.save()
            message = "Account Created Successfully"
            return render_to_response('land/create_account_success.html',
                                      {'message': message,
                                      })

    else:
        profile_form = LandUserProfileForm()
        user_form = UserRegistrationForm()
    return render(request, 'land/create_account.html',
                  {
                      'user_form': user_form,
                      'profile_form': profile_form,
                  })


# handle the user log in to the system


def user_login(request):
    user = request.user
    next_url = request.GET.get('next', '')
    if user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    request.session['username'] = cd['username']
                    login(request, user)

                    if next_url == '':
                        return HttpResponseRedirect('/')
                    elif next_url:
                        return HttpResponseRedirect(next_url)
            else:

                message = 'Wrong username or password'
                form = LoginForm()
                return render(request, 'land/login.html', {'form': form, 'message': message, })
    else:
        form = LoginForm()
    return render(request, 'land/login.html', {'form': form, })


@login_required(login_url='/login/')
def user_logout(request):
    logout(request)
    try:
        del request.session['username']
        request.session.modified = True
        return render(request, 'land/logout_then_login.html', {})
    except KeyError, e:
        pass
    return render(request, 'land/logout_then_login.html', {})


# register land details

@transaction.atomic()
@login_required(login_url='/login/')
def register_land(request):
    if request.method == 'POST':
        data = request.POST.copy()
        land_form = RegisterLandForm(data)
        # perform checks to ensure all form data is clean
        if land_form.is_valid():
            # form passes the checks now process the data
            cd = land_form.cleaned_data
            title_deed = cd['title_deed']
            approximate_size = cd['approximate_size']
            registry_map_sheet_no = cd['registry_map_sheet_no']
            district = cd['district']
            location = cd['location']
            sale_price = cd['sale_price']
            # create user model instance to link to the actual land owner
            username = request.session.get('username')
            land_owner = get_object_or_404(User, username=username)
            profile = get_object_or_404(LandUserProfile, user=land_owner)
            land = Land.objects.create(
                user=land_owner,
                profile=profile,
                title_deed_no=title_deed,
                registry_map_sheet_no=registry_map_sheet_no,
                approximate_size=approximate_size,
                sale_price=sale_price,
                location=location,
                district=district,
                remaining_size=approximate_size

            )
            land.save()
            error = False
            message = "Your land information has been saved successfully."
            return render_to_response('land/register_land_success.html',
                                      {'message': message,
                                       'error': error,
                                      })

    else:
        land_form = RegisterLandForm()
    return render(request, 'land/register_land.html', {'land_form': land_form, })


# display all the lands that are on sale


def display_lands(request):
    lands = Land.objects.filter(is_onsale=True, )
    return render(request, 'land/lands.html', {'lands': lands, })


# get land details for a given land


def land_detail(request, pk=None):
    land = get_object_or_404(Land, pk=pk)
    return render(request, 'land/land_details.html', {'land': land, })


@transaction.atomic()
def buy_land(request, pk=None):
    land = get_object_or_404(Land, pk=pk)
    sale_price = float(land.sale_price)
    deposit = 0.75 * sale_price
    form_initial = {'deposit_amount': deposit}
    if request.method == 'POST':
        data = request.POST.copy()
        land_purchase_form = LandPurchaseForm(data, initial=form_initial)

        if land_purchase_form.is_valid():
            cd = land_purchase_form.cleaned_data
            buyer_phone_number = cd['phone_number']
            amount = cd['deposit_amount']

            """
             perform m-pesa payment logic here
             for now we bypass the logic and save the data in
             the database later we will implement the payment api
             this is for demo purposes

            """
            # generate a random transaction id
            range_start = 10 ** (10 - 1)
            range_end = (10 ** 10) - 1
            details = "Land Purchase Deposit 0f Ksh {0} For Land On-sale by {1}  {2}".format(
                deposit, land.user.first_name, land.user.last_name
            )
            id_prefix = "HTech"
            transaction_id = randint(range_start, range_end)
            id_hash = SHA256.new(str(transaction_id)).hexdigest()
            t_id = id_prefix+id_hash
            # create a payment model instance here
            username = str(request.user)
            user = get_object_or_404(User, username=username)
            payment = Payment.objects.create(
                user=user,
                transaction_id=t_id,
                phone_number=buyer_phone_number,
                payment_mode="M-Pesa",
                amount=amount,
                details=details,
                status="Success"
            )
            payment.save()
            # record the deposit on the land sales model

            land_owner = land.user.username
            uncleared_amount = sale_price - deposit
            land_sale = LandSales.objects.create(
                land=land,
                owner=land_owner,
                buyer=username,
                deposit_amount=amount,
                uncleared_amount=uncleared_amount,
            )
            land_sale.save()
            # make land not on sale
            land.is_onsale = False
            land.bought = True
            land.save()
            # create a notification
            receiver = land.profile.phone_number
            notification_message = "Dear {0} {1} we are gland to inform you that  " \
                                   "{2}  Has Place a deposit of Ksh {3} " \
                                   "for the land you posted on-sale Contact this client on" \
                                   " {4} ".format(land.user.first_name,
                                                    land.user.last_name,
                                                    request.user,
                                                    deposit,
                                                    buyer_phone_number)
            notification = Notification.objects.create(
                land_id=land,
                sender=buyer_phone_number,
                sent_to=receiver,
                text=notification_message
            )
            notification.save()
            message = 'Deposit made successfully Your Buyer id is {0}'.format(transaction_id)
            return render(request, 'land/deposit_success.html', {'message': message, })
    else:
        land_purchase_form = LandPurchaseForm(initial=form_initial)
    return render(request, 'land/deposit_payment.html', {
        'land_purchase_form': land_purchase_form,
    })


@login_required(login_url='/login/')
def show_bought_land(request):
    owner = str(request.user)
    user = get_object_or_404(User, username=owner)
    profile = get_object_or_404(LandUserProfile, user=user)
    lands_bought = LandSales.objects.filter(owner=owner)
    return render(request, 'land/lands_bought.html',
                  {
                      'lands_bought': lands_bought,
                      'profile': profile,
                  })

# pay land transfer fee


def pay_land_transfer_fee(request, pk=None):
    land = get_object_or_404(Land, pk=pk)
    size = float(land.approximate_size)
    fee = get_object_or_404(LandTransferFee,)
    fee_amt = fee.fee_amount
    amount = fee_amt * size
    initial = {'amount': amount, }
    if request.method == 'POST':
        payment_form = LandTransFerFeeForm(request.POST, initial=initial)
        # ensure valid data is sent to the form
        if payment_form.is_valid():
            # get the data submitted from the data
            cd = payment_form.cleaned_data
            phone_number = cd['phone_number']
            amount = cd['amount']

            range_start = 10 ** (10 - 1)
            range_end = (10 ** 10) - 1
            transaction_id = randint(range_start, range_end)
            id_prefix = "HTech"
            id_hash = SHA256.new(str(transaction_id)).hexdigest()
            t_id = id_prefix+id_hash
            user = get_object_or_404(User, username=str(request.user))
            payment_detail = "Payment for land transfer TitleDeedNo {0}".format(
                land.title_deed_no
            )
            # create fee payment object
            payment = LandTransferFee.objects.create(
                user=user,
                transaction_id=t_id,
                land=land,
                amount=amount,
                phone_number=phone_number,
                payment_mode="M-Pesa",
                details=payment_detail,
                status="success",
            )
            payment.save()
            return HttpResponse('payment done successfully.')
    else:
        payment_form = LandTransFerFeeForm(initial=initial)
    return render(request, 'land/transfer_payment.html', {'payment_form': payment_form, })


def transfer_bought_land(request, pk=None):
    land = get_object_or_404(LandSales, pk=pk)
    buyer_user = land.buyer
    user = get_object_or_404(User, username=buyer_user)
    # check if transfer fee has been paid
    l_query = get_object_or_404(Land, pk=land.pk)
    payment = get_object_or_404(LandTransFerFeePayment, user=user, land=l_query)
    payment_status = payment.status.lower()
    if payment_status == 'success':
        #payment was successful now we can transfer land ownership
        owner = get_object_or_404(User, username=str(request.user))
        transfer_size = land.land.approximate_size
        old_title_deed = land.land.title_deed_no
        range_start = 10 ** (8 - 1)
        range_end = (10 ** 8) - 1
        new_title_deed = randint(range_start, range_end)
        new_mapsheet = randint(range_start, range_end)
        land_transfer = ChangeLandOwnership.objects.create(
            owner=owner,
            new_owner=user,
            old_title_deed_no=old_title_deed,
            new_title_deed_no=new_title_deed,
            transfer_size=transfer_size
        )
        land_transfer.save()
        initial_map_sheet = land.land.registry_map_sheet_no
        transfer_log = LandTransferHistoryLog.objects.create(
            transfer_from=str(request.user),
            transfer_to=user.username,
            initial_title_deed=old_title_deed,
            initial_map_sheet=initial_map_sheet,
            new_map_sheet=new_mapsheet,
            new_title_deed=new_title_deed
        )
        transfer_log.save()

    else:
        return HttpResponseRedirect('/transfer-payment/')

    return render(request, 'land/transfer_land.html', {'land': land, 'user': user, })


def my_land(request):
    user = get_object_or_404(User, username=str(request.user))
    land = Land.objects.filter(user=user, transferred_completely=False)
    return render(request, 'land/my_land.html', {'lands': land, })


@login_required(login_url='/login/')
def transfer_land(request, land_id=None):
    land = get_object_or_404(Land, id=land_id)
    # get the details of the land you for transfer
    land_size = land.remaining_size
    initial = {'land_size': land_size, 'transfer_from': str(request.user), }
    if request.method == 'POST':
        data = request.POST.copy()
        form = LandTransferForm(data, initial=initial)
        if form.is_valid():
            cd = form.cleaned_data
            first_name = cd['first_name']
            middle_name = cd['middle_name']
            last_name = cd['last_name']
            id_no = cd['id_no']
            district = cd['district']
            location = cd['location']
            sub_location = cd['sub_location']
            transfer_from = cd['transfer_from']
            transfer_size = cd['transfer_size']

            range_start = 10 ** (10 - 1)
            range_end = (10 ** 10) - 1
            map_sheet = "mpsh"+str(randint(range_start, range_end))
            title_deed = "tld"+str(randint(range_start, range_end))

            land_transfer = LandTransfer.objects.create(
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                id_no=id_no,
                district=district,
                location=location,
                sub_location=sub_location,
                transfer_from=transfer_from,
                map_sheet=map_sheet,
                title_deed=title_deed,
                transfer_size=transfer_size
            )
            land_transfer.save()
            new_land_size = float(land.approximate_size) - float(transfer_size)

            land.remaining_size = new_land_size
            if new_land_size == 0:
                land.is_onsale = False
                land.transferred_completely = True
            else:
                land.transferred_completely = False
            land.save()

            # send notification to the owner confirming the transfer
            user = get_object_or_404(User, username=str(request.user))
            profile = get_object_or_404(LandUserProfile, user=user)
            phone_number = profile.phone_number
            message = "Land was successfully transferred {0} Acres of your land to {1} {2} {3}".format(
                transfer_size, first_name, middle_name, last_name
            )
            try:
                username = settings.AT_USERNAME
                api_key = settings.AT_API_KEY
                sender = str(settings.AT_SENDER)
                gateway = AfricasTalkingGateway(username, api_key, sender)

                gateway.sendMessage(phone_number, message)
                return HttpResponse(message)

            except AfricasTalkingGatewayException, e:
                print str(e)
                return HttpResponse("Error{}".format(str(e)))
    else:
        form = LandTransferForm(initial=initial)
    return render(request, 'land/transfer.html', {'form': form})


@login_required(login_url='/login/')
def get_notification(request):
    username = request.user
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(LandUserProfile, user=user)
    receiver = profile.phone_number
    notification = Notification.objects.filter(sent_to=receiver, is_read=False)
    all_notf = Notification.objects.filter(sent_to=receiver,)

    return render(request, 'land/notification.html',
                  {
                      'notification': notification,
                      'all': all_notf,
                  })
