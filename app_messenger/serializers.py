from rest_framework.serializers import ModelSerializer
from app_messenger.models import *
import datetime

# class AppMessengerSerializer(ModelSerializer):
#     class Meta:
#         model=AppMessenger
#         fields="__all__"
#
#     def create(self, validated_data):
#         import string
#         import random
#         customer_id = 0
#         if validated_data.get("sender_type")=='customer' :
#             customer_id = validated_data.get("sender_id")
#         elif validated_data.get("receiver_type")=='customer':
#             customer_id = validated_data.get("receiver_id")
#
#         msg_session = str(customer_id) + ''.join(random.choice(string.ascii_uppercase) for _ in range(3)) +datetime.datetime.now().strftime("%H%M%S")
#
#         print(msg_session)
#
#         return validated_data

