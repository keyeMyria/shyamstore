from django.shortcuts import render
from django.http import HttpResponse
from django.utils.translation import get_language
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
from rest_framework.generics import*
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from . import Checksum1


from paytm.models import PaytmHistory
# Create your views here.

@login_required
def home(request):
    print('check')
    return HttpResponse("<html><a href='"+ settings.HOST_URL +"/paytm/payment'>PayNow</html>")


def payment(request):
    MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
    MERCHANT_ID = settings.PAYTM_MERCHANT_ID
    get_lang = "/" + get_language() if get_language() else ''
    CALLBACK_URL = settings.HOST_URL + settings.PAYTM_CALLBACK_URL
    # Generating unique temporary ids
    order_id = Checksum1.__id_generator__()

    bill_amount = 10
    if bill_amount:
        data_dict = {
                    'MID':MERCHANT_ID,
                    'ORDER_ID':order_id,
                    'CUST_ID':'rupam@gmail.com',
                    'TXN_AMOUNT': bill_amount,
                    'CHANNEL_ID':'WEB',
                    'INDUSTRY_TYPE_ID':'Retail',
                    'WEBSITE': settings.PAYTM_WEBSITE,
                    # 'PAYMENT_MODE_ONLY': 'Yes',
                    # 'AUTH_MODE': 'USRPWD',
                    # 'PAYMENT_TYPE_ID': 'NB',
                    'PROMO_CAMP_ID': 'TESTSYREG',
                    'CALLBACK_URL':CALLBACK_URL,
                }
        param_dict = data_dict
        param_dict['CHECKSUMHASH'] = Checksum1.generate_checksum(data_dict, MERCHANT_KEY)
        print('param_dict::',param_dict)
        return render(request,"payment.html",{'paytmdict':param_dict})
    return HttpResponse("Bill Amount Could not find. ?bill_amount=10")


@csrf_exempt
def response(request):
    if request.method == "POST":
        MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
        data_dict = {}
        for key in request.POST:
            data_dict[key] = request.POST[key]

        print('data_dict::',data_dict)
        verify = Checksum1.verify_checksum(data_dict, MERCHANT_KEY, data_dict['CHECKSUMHASH'])
        print('verify::',verify)
        return render(request,"response.html",{"paytm":data_dict})
        # verify = Checksum1.verify_checksum(data_dict, MERCHANT_KEY, data_dict['CHECKSUMHASH'])
        # print('verify::',verify)
        # if verify:
        #     PaytmHistory.objects.create(user=request.user, **data_dict)
        #     return render(request,"response.html",{"paytm":data_dict})
        # else:
        #     return HttpResponse("checksum verify failed")
    return HttpResponse(status=200)




class PaymentRequestView(RetrieveAPIView):
        renderer_classes = [TemplateHTMLRenderer]
        def get(self, request, *args, **kwargs):
            MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
            print('MERCHANT_KEY::',MERCHANT_KEY)
            MERCHANT_ID = settings.PAYTM_MERCHANT_ID
            get_lang = "/" + get_language() if get_language() else ''
            CALLBACK_URL = settings.HOST_URL + get_lang + settings.PAYTM_CALLBACK_URL
            # Generating unique temporary ids
            order_id = Checksum1.__id_generator__()
            param_dict = {}
            bill_amount = 100
            if bill_amount:
                data_dict = {
                    'MID': MERCHANT_ID,
                    'ORDER_ID': order_id,
                    'TXN_AMOUNT': bill_amount,
                    'CUST_ID': 'rupam@gmail.com',
                    'INDUSTRY_TYPE_ID': 'Retail',
                    'WEBSITE': settings.PAYTM_WEBSITE,
                    'CHANNEL_ID': 'WEB',
                    'CALLBACK_URL': CALLBACK_URL,
                }
                param_dict = data_dict
                param_dict['CHECKSUMHASH'] = Checksum1.generate_checksum(data_dict, MERCHANT_KEY)
                print('param_dict::', param_dict)

            return Response({'paytmdict': param_dict}, template_name='payment_rest.html')
        #return render(request, "payment.html", {'paytmdict': param_dict})

class GetPaymentDetailsView(RetrieveAPIView):

    def get(self, request, *args, **kwargs):
        txn_amount = self.request.query_params.get('order_amount')
        #print(self.request.query_params.get('txn_amount'))
        MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
        #print('MERCHANT_KEY::', MERCHANT_KEY)
        MERCHANT_ID = settings.PAYTM_MERCHANT_ID
        get_lang = "/" + get_language() if get_language() else ''
        #CALLBACK_URL = settings.HOST_URL + get_lang + settings.PAYTM_CALLBACK_URL
        CALLBACK_URL = settings.HOST_URL + settings.PAYTM_CALLBACK_URL
        # Generating unique temporary ids
        order_id = Checksum1.__id_generator__()
        param_dict = {}
        #bill_amount = 100
        if txn_amount:
            data_dict = {
                'MID': MERCHANT_ID,
                'ORDER_ID': order_id,
                'TXN_AMOUNT': txn_amount,
                'CUST_ID': 'rupam@gmail.com',
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': settings.PAYTM_WEBSITE,
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL': CALLBACK_URL,
            }
            param_dict = data_dict
            param_dict['CHECKSUMHASH'] = Checksum1.generate_checksum(data_dict, MERCHANT_KEY)
            return Response(param_dict)