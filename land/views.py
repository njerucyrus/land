from Crypto.Hash import SHA256
from django.shortcuts import (
    render,
    render_to_response,
    HttpResponse,
    HttpResponseRedirect,
    get_object_or_404,
)
from land.forms import (
    UserRegistrationForm,
    LandUserProfileForm,
    LoginForm,
    RegisterLandForm,
    LandPurchaseForm,
)
from land.models import (
    LandUserProfile,
    Land,
    Notification,
)
from payment.models import (
    Payment,
)
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from random import randint

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
                    if next == '':
                        return HttpResponseRedirect('/')
                    elif next:
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
            land = Land.objects.create(
                user=land_owner,
                title_deed_no=title_deed,
                registry_map_sheet_no=registry_map_sheet_no,
                approximate_size=approximate_size,
                sale_price=sale_price,
                location=location,
                district=district
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
    lands = Land.objects.filter(is_onsale=True)
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
            transaction_id = randint(range_start, range_end)
            id_hash = SHA256.new(str(transaction_id)).hexdigest()
            # create a payment model instance here
            payment = Payment.objects.create(
                transaction_id=id_hash,
                phone_number=buyer_phone_number,
                payment_mode="M-Pesa",
                amount=amount,
                details=details,
                status="Success"
            )
            payment.save()
            # make land not on sale
            land.is_onsale = False
            land.save()
            # create a notification
            notification_message = "Dear {0} {1} we are gland to inform you that  " \
                                   "{2}  Has Place a deposit of Ksh {3} " \
                                   "for the land you posted on-sale Contact this client on" \
                                   " {4} ".format(land.user.first_name,
                                                    land.user.last_name,
                                                    request.user,
                                                    deposit,
                                                    buyer_phone_number)
            notification = Notification.objects.create(
                sender=buyer_phone_number,
                text=notification_message
            )
            notification.save()
            message = 'Deposit made successfully Your Buyer id is {0}'.format(transaction_id)
            return render_to_response('land/deposit_success.html', {'message': message, })
    else:
        land_purchase_form = LandPurchaseForm(initial=form_initial)
    return render(request, 'land/deposit_payment.html', {
        'land_purchase_form': land_purchase_form,
    })

