from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import *
from rest_framework.response import Response
from app_messenger.serializers import *
from app_messenger.models import *
# from notifications.signals import notify
from customers.models import Customers
from django.db.models import Q


class ChatSessionView(APIView):
    """Manage Chat sessions."""

    # permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        """create a new chat session."""
        sender_id = request.data['sender']
        sender_type = request.data['sender_type']
        receiver_id = request.data['receiver']
        receiver_type = request.data['receiver_type']



        chat_session_exist = ChatSessionMember.objects.filter(Q(chat_session__user_id=sender_id,
                                                              chat_session__user_type=sender_type,
                                                              user_id=receiver_id, user_type=receiver_type)|
                                                              Q(chat_session__user_id=receiver_id,
                                                              chat_session__user_type=receiver_type,
                                                              user_id=sender_id, user_type=sender_type))
        print('chat_session_exist::',chat_session_exist.query)
        if chat_session_exist:
            for session_data in chat_session_exist:
                if session_data.id:
                    uri = session_data.chat_session.uri
                    msg = "alredy member exist"
        else:
            chat_session = ChatSession.objects.create(user_id=sender_id, user_type=sender_type)
            uri = chat_session.uri
            msg = 'New chat session created'
            if chat_session.id:
                ChatSessionMember.objects.get_or_create(user_id=receiver_id,
                                                    user_type=receiver_type,
                                                    chat_session=chat_session)




        return Response({
            'status': 'SUCCESS', 'uri': uri,
            'message': msg
        })

    # def patch(self, request, *args, **kwargs):
    #     """Add a user to a chat session."""
    #     # User = get_user_model()
    #     user_id = request.data['user_id']
    #     user_type = request.data['user_type']
    #
    #     uri = kwargs['uri']
    #     # username = request.data['username']
    #     # user = User.objects.get(username=username)
    #
    #     chat_session = ChatSession.objects.get(uri=uri)
    #     session_user = chat_session.user_id
    #
    #     if session_user != user_id:  # Only allow non owners join the room
    #         ChatSessionMember.objects.get_or_create(
    #             user_id=user_id, user_type=user_type, chat_session=chat_session
    #         )
    #
    #     # owner = deserialize_user(owner)
    #     members = [
    #         chat_session.user_id
    #         for chat_session in ChatSessionMember.objects.all()
    #     ]
    #     members.insert(0, user_id)  # Make the owner the first member
    #
    #     return Response ({
    #         'status': 'SUCCESS', 'members': members,
    #         'message': '%s joined that chat' % user_id,
    #         'user': user_id
    #     })

class ChatSessionMessageView(APIView):
    """Create/Get Chat session messages."""

    # permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """return all messages in a chat session."""
        uri = kwargs['uri']

        chat_session = ChatSession.objects.get(uri=uri)
        messages = [chat_session_message.to_json()
            for chat_session_message in chat_session.messages.all()]

        return Response({
            'id': chat_session.id, 'uri': chat_session.uri,
            'messages': messages
        })

    def post(self, request, *args, **kwargs):
        """create a new message in a chat session."""
        uri = kwargs['uri']
        message = request.data['message']

        user_id = request.data['user_id']
        user_type = request.data['user_type']
        chat_session = ChatSession.objects.get(uri=uri)

        chat_session_message = ChatSessionMessage.objects.create(
            user_id=user_id, user_type=user_type, chat_session=chat_session, message=message
        )
        if user_type == "app_master":
            # user_details = AppMasters.objects.filter(pk=user_id)
            user_details = AppMasters.objects.filter(pk=user_id)
            for data in user_details:
                data_dict ={'id':data.id,'name':data.user,'type':user_type}


        elif user_type == "customer":
            user_details = Customers.objects.filter(pk=user_id)
            for data in user_details:
                data_dict ={'id':data.id,'name':data.customer_name,'type':user_type}
        # notif_args = {
        #     'source': data_dict['name'],
        #     'source_display_name': user_type,
        #     'category': 'chat', 'action': 'Sent',
        #     'obj': chat_session_message.id,
        #     'short_description': 'You a new message', 'silent': True,
        #     'extra_data': {
        #         'uri': chat_session.uri,
        #         'message': chat_session_message.to_json()
        #     }
        # }
        # notify.send(
        #     sender=self.__class__,**notif_args, channels=['websocket']
        # )

        return Response ({
            'status': 'SUCCESS', 'uri': chat_session.uri, 'message': message,
            'user': user_id
        })


class ChatSessionMemberListView(APIView):
    def post(self, request, *args, **kwargs):
        receiver_id = request.data['receiver']
        receiver_type = request.data['receiver_type']
        response_list = []
        members_details = ChatSessionMember.objects.filter(Q(user_id=receiver_id,
                                           user_type=receiver_type)|Q(chat_session__user_id=receiver_id,
                                                                      chat_session__user_type=receiver_type))
        # print('members_details::', members_details)
        for member in members_details:

            messages = ChatSessionMessage.objects.filter(chat_session_id=member.chat_session.id)
            msg_list = [msg.to_json() for msg in messages]
            data_dict ={
                'status': 'SUCCESS',
                'sender': member.chat_session.user_id,
                'sender_type': member.chat_session.user_type,
                'receiver': member.user_id,
                'receiver_type':member.user_type,
                'uri': member.chat_session.uri,
                'message': msg_list
            }
            response_list.append(data_dict)

            # print('msg_list::', msg_list)

        return Response(response_list)



def raise_404(request):
    """Raise a 404 Error."""
    raise Http404