from rest_framework.views import APIView
from django.shortcuts import render
from django.http import HttpResponse
from urllib.request import Request, urlopen
from rest_framework.response import Response
import urllib.request
import urllib
import pyotp
import time
import datetime
import json
from users.models import *
# Create your views here.



class SEMSendView(APIView):

    def post(self, request, format=None):
        #print('request',request.data)
        totp = pyotp.TOTP('base32secret3232')
        current_timestamp = time.time()
        current_timestamp_ext_15 = current_timestamp + 900
        if request.data['sender_no']:
            if request.data['otp']:

                verification = totp.verify(request.data['otp'], current_timestamp_ext_15)
                if verification:
                    msg = "OTP has been verified"
                else:
                    msg = "OTP has been expired"
                return Response({"message ":msg})

            otp_gen = totp.at(current_timestamp_ext_15)
            print("Current OTP:", otp_gen)
            username = 'shail'
            password = '6209'
            numbers = request.data['sender_no']
            sender = 'BNAPPS1' #'BNAPPS'
            message = 'Congrats! You are just about to complete the app creation process. '+otp_gen+' is your requested Banao.App OTP and the code is valid only for the next 15 minutes.'
            message = message.encode('utf-8')
            url = "http://sms.faresms.com/api/pushsms.php"
            port = 80
            api_url = url+"?username="+urllib.parse.quote_plus(username)+"&password="+ urllib.parse.quote_plus(password)+"&sender="+ sender+\
                      "&message="+ urllib.parse.quote_plus(message)+"&numbers="+numbers+"&unicode=false&flash=false"
            print('api_url',api_url)
            req = Request(api_url,headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req).read()
            print('webpage',webpage.decode('utf-8'))
            json_raw_response = webpage.decode('utf-8')
            json_decode_response = json.loads(json_raw_response)
            return Response(json_decode_response)


