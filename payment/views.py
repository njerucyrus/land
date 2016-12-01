from django.shortcuts import HttpResponse, get_object_or_404
from payment.models import LandTransFerFeePayment
from django.views.decorators.csrf import csrf_exempt
from land.AfricasTalkingGateway import AfricasTalkingGateway, AfricasTalkingGatewayException
import json
from land.models import Land, LandTransfer
from django.conf import settings


api_response = {}


@csrf_exempt
def get_transfer_fee_payment_ipn(request):
    if request.method == 'POST':
        payment_data = json.loads(request.body)

        #get the data from the api response
        transactionId = payment_data['transactionId']
        status = payment_data['status']
        phoneNumber = payment_data['source']

        # get the payment object from my database
        payment = get_object_or_404(LandTransFerFeePayment, transaction_id=transactionId)
        title_deed = payment.land_title_deed
        transfer_size = payment.transferred_size

        if status == 'Success':
            #payment was successful so we update our status
            land_transfer = get_object_or_404(LandTransfer, old_title_deed=title_deed)
            to_first_name = land_transfer.first_name
            to_last_name = land_transfer.last_name
            payment.status = status
            message = "Land transfer payment successful. You have now transferred {0} Acres To {} {}".format(
                transfer_size, to_first_name, to_last_name
            )

            # reduce the size of the land transferred
            land = get_object_or_404(Land, title_deed_no=title_deed)
            new_land_size = float(land.approximate_size) - float(transfer_size)
            land.remaining_size = new_land_size
            if new_land_size == 0:
                land.is_onsale = False
                land.transferred_completely = True
            else:
                land.transferred_completely = False
            land.save()
            payment.save()

            # send the message to tell the owner the land has been transferred
            try:
                apiKey = settings.AT_API_KEY
                username = settings.AT_USERNAME
                sender = settings.AT_SENDER
                gateway = AfricasTalkingGateway(username, apiKey, sender)
                gateway.sendMessage(phoneNumber, message)
            except AfricasTalkingGatewayException, e:
                pass
            api_response['message'] = "payment completed successfully"
            return HttpResponse(json.dumps(api_response), content_type='application/json')

        else:
            payment.status = status
            payment.save()
            api_response['message'] = "payment failed"
            return HttpResponse(json.dumps(api_response), content_type='application/json')

    else:
        api_response['message'] = "no data received"
    return HttpResponse(json.dumps(api_response), content_type='application/json')

