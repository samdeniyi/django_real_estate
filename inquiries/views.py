from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import Inquiry

# Create your views here.


def inquiry(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        # check if the user has made inquiry already

        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Inquiry.objects.all().filter(listing_id=listing_id, user_id=user_id)

            if has_contacted:
                messages.error(request, 'You have already made an inquiry for this listing')
                return redirect('/listings/'+listing_id)

        new_contact = Inquiry(listing=listing, listing_id=listing_id, name=name, email=email, phone=phone,
                              message=message, user_id=user_id)
        new_contact.save()

        # send mail
        send_mail(
            'Property Listing Inquries',
            'There has been an inqury for '+ listing +'. sign into the admin panel for more info',
            'samdeniyi@gmail.com',
            [realtor_email, 'info@samadeiyi.com'],
            fail_silently=False
        )

        messages.success(request, 'Your request has been submited, a realtor will get back to you soon')

        return redirect('/listings/'+listing_id)
