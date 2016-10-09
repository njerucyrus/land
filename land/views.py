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
)
from land.models import (
    LandUserProfile,
    Land,
)
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction

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
            #form passes the checks now process the data
            cd = land_form.cleaned_data
            title_deed = cd['title_deed']
            approximate_size = cd['approximate_size']
            registry_map_sheet_no = cd['registry_map_sheet_no']
            district = cd['district']
            location = cd['location']
            # create user model instance to link to the actual land owner
            username = request.session.get('username')
            land_owner = get_object_or_404(User, username=username)
            land = Land.objects.create(
                user=land_owner,
                title_deed_no=title_deed,
                registry_map_sheet_no=registry_map_sheet_no,
                approximate_size=approximate_size,
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


def display_lands(request):
    lands = Land.objects.filter(is_onsale=True)
    return render(request, 'land_display.html', {'lands': lands, })