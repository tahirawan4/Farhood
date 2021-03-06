from django.core.serializers import json
from rest_framework import status, generics
from rest_framework.views import APIView
from farhoodapp.utils import CustomResponse, search_user, connect_members_with_event
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from farhoodapp.models import (User, Event, EventMember, EventReaction)
from farhoodapp.services import (get_user_event, get_event_comments, get_event_actions, get_follow_events,
                                 get_unfollow_events, remove_event_member, get_friends_list, get_user_profile,
                                 get_user_image_url, get_contacts_list)
from farhoodapp.serializers import (UserSerializer, EventSerializer, CommentSerializer, ActionSerializer,
                                    AddEventMemberSerializer, UnfollowEventMemberSerializer,
                                    FollowEventMemberSerializer, TemporaryUserSerializer, ProfileSerializer,
                                    UserResponseSerializer, ProfileUpdateSerializer, EventReactionSerializer,
                                    EventWishListSerializer)


class UserCreate(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format='json'):
        data = request.data.copy()
        if 'email' not in data.keys():
            data['email'] = data['phone_number'] + "@dottech.info"
        else:
            data['email'] = data['email']
        existing_user = search_user(data)
        if existing_user:
            return CustomResponse.create_response(True, status.HTTP_200_OK, "Success",
                                                  UserResponseSerializer(existing_user).data)
        else:
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                user = serializer.save()
                user.temporary_profile = False
                user.save()
                return CustomResponse.create_response(True, status.HTTP_200_OK, "Success",
                                                      UserResponseSerializer(user).data)
        return CustomResponse.create_error_response(status.HTTP_400_BAD_REQUEST, str(serializer.errors))


class UpdateProfileUser(APIView):
    def put(self, request, format='json'):
        user_data = request.user
        request_data = request.data.copy()
        request_data['is_active'] = True
        serializer = ProfileUpdateSerializer(user_data, data=request_data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            user.temporary_profile = False
            user.save()
            return CustomResponse.create_response(True, status.HTTP_200_OK, "Success",
                                                  ProfileUpdateSerializer(user, context={'request': request}).data)
        return CustomResponse.create_error_response(status.HTTP_400_BAD_REQUEST, str(serializer.errors))


class LogoutView(APIView):
    queryset = User.objects.all()

    def get(self, request):
        request.user.auth_token.delete()
        return CustomResponse.create_response(True, status.HTTP_200_OK, "Logout Successfully", {})


class GetUserProfileView(APIView):
    def get(self, request):
        id = request.user.id
        resp = get_user_profile(id=id, request=request)
        return CustomResponse.create_response(True, status.HTTP_200_OK, "Success", resp)


class UserImageView(APIView):
    def get(self, request):
        id = request.user.id
        resp = get_user_image_url(id=id, request=request)
        return CustomResponse.create_response(True, status.HTTP_200_OK, "Success", resp)


class EventCreateView(generics.GenericAPIView):
    serializer_class = EventSerializer

    def post(self, request, format='json'):
        request_data = request.data.copy()
        request_data['user'] = request.user.id
        serializer = self.get_serializer(data=request_data)
        if serializer.is_valid():
            event = serializer.save()
            connect_members_with_event(event, request.data.get('users'))
            return CustomResponse.create_response(True, status.HTTP_200_OK, "Success", EventSerializer(event).data)
        return CustomResponse.create_error_response(status.HTTP_400_BAD_REQUEST, str(serializer.errors))


class EventEditView(APIView):
    def post(self, request, format='json'):
        request_data = request.data.copy()
        request_data['user'] = request.user.id
        event_id = request_data.get('id')
        event_data = Event.objects.get(id=event_id, user=request.user)
        serializer = EventSerializer(event_data, data=request_data)
        if serializer.is_valid():
            event = serializer.save()
            return CustomResponse.create_response(True, status.HTTP_200_OK, "Success", EventSerializer(event).data)
        return CustomResponse.create_error_response(status.HTTP_400_BAD_REQUEST, str(serializer.errors))


class CreateCommentView(APIView):

    def post(self, request):
        request_data = request.data.copy()
        request_data['user'] = request.user.id
        event_id = int(request.data.get('event'))
        if event_id:
            serializer = CommentSerializer(data=request_data)
            if serializer.is_valid():
                comment = serializer.save()
                return CustomResponse.create_response(True, status.HTTP_200_OK, "Success",
                                                      CommentSerializer(comment).data)
            return CustomResponse.create_error_response(status.HTTP_400_BAD_REQUEST, str(serializer.errors))


class CreateEventWishListView(APIView):

    def post(self, request):
        request_data = request.data.copy()
        request_data['user'] = request.user.id
        event_id = int(request.data.get('event'))
        if event_id:
            serializer = EventWishListSerializer(data=request_data)
            if serializer.is_valid():
                wish_list = serializer.save()
                return CustomResponse.create_response(True, status.HTTP_200_OK, "Success",
                                                      EventWishListSerializer(wish_list).data)
            return CustomResponse.create_error_response(status.HTTP_400_BAD_REQUEST, str(serializer.errors))


class CreateEventReactionView(APIView):

    def post(self, request):
        request_data = request.data.copy()
        request_data['user'] = request.user.id
        user_id = request.user.id
        event_id = int(request.data.get('event'))
        event_reaction = EventReaction.objects.filter(event_id=event_id, user_id=user_id).first()

        if event_id:
            if event_reaction:
                serializer = EventReactionSerializer(data=request_data, instance=event_reaction)
            else:
                serializer = EventReactionSerializer(data=request_data)
            if serializer.is_valid():
                reaction = serializer.save()
                return CustomResponse.create_response(True, status.HTTP_200_OK, "Success",
                                                      EventReactionSerializer(reaction).data)
            return CustomResponse.create_error_response(status.HTTP_400_BAD_REQUEST, str(serializer.errors))


class CreateActionView(APIView):
    def post(self, request, format='json'):
        request_data = request.data.copy()
        request_data['user'] = request.user.id
        event_id = int(request.POST.get('event'))
        if event_id:
            serializer = ActionSerializer(data=request_data)
            if serializer.is_valid():
                action = serializer.save()
                return CustomResponse.create_response(True, status.HTTP_200_OK, "Success",
                                                      ActionSerializer(action).data)
            return CustomResponse.create_error_response(status.HTTP_400_BAD_REQUEST, str(serializer.errors))


class CreateFollowEventMemberView(APIView):
    def post(self, request, format='json'):
        request_data = request.data.copy()
        request_data['user'] = request.user.id
        event_id = int(request.POST.get('event'))
        if event_id:
            serializer = FollowEventMemberSerializer(data=request_data)
            if serializer.is_valid():
                member = serializer.save()
                return CustomResponse.create_response(True, status.HTTP_200_OK, "Success",
                                                      FollowEventMemberSerializer(member).data)
            return CustomResponse.create_error_response(status.HTTP_400_BAD_REQUEST, str(serializer.errors))


class CreateUnfollowEventMemberView(APIView):
    def post(self, request, format='json'):
        request_data = request.data.copy()
        request_data['user'] = request.user.id
        event_id = int(request.POST.get('event'))
        if event_id:
            check_member = EventMember.objects.filter(event_id=event_id, user=request.user).first()
            if not check_member:
                serializer = UnfollowEventMemberSerializer(data=request_data)
                if serializer.is_valid():
                    member = serializer.save()
                    return CustomResponse.create_response(True, status.HTTP_200_OK, "Success",
                                                          UnfollowEventMemberSerializer(member).data)
            else:
                return Response({'error': 'Member Already Exists'}, status=status.HTTP_400_BAD_REQUEST)


class AddEventMemberView(APIView):
    def post(self, request, format='json'):
        request_data = request.data.copy()
        request_data['user'] = request.user.id
        event_id = int(request.POST.get('event'))
        if event_id:
            member = EventMember.objects.filter(event_id=event_id, user=request.user).first()
            if not member:
                serializer = AddEventMemberSerializer(data=request_data)
                if serializer.is_valid():
                    add_member = serializer.save()
                    return CustomResponse.create_response(True, status.HTTP_200_OK, "Success",
                                                          AddEventMemberSerializer(add_member).data)
            else:
                return CustomResponse.create_error_response(status.HTTP_400_BAD_REQUEST, "")  # str(serializer.errors))


class RemoveEventMemberView(APIView):
    def post(self, request, format='json'):
        user_id = request.user.id
        event_id = request.POST.get('event')
        if event_id:
            resp = remove_event_member(event_id=event_id, user_id=user_id)
            return CustomResponse.create_response(True, status.HTTP_200_OK, "Success", resp)


class UserEventView(APIView):
    def get(self, request):
        user_id = request.user.id
        resp = get_user_event(user_id=user_id)
        return CustomResponse.create_response(True, status.HTTP_200_OK, "Success", resp)


class CommentEventView(APIView):
    def get(self, request):
        user_id = request.user.id
        event_id = request.GET.get('event_id', 1)
        resp = get_event_comments(event_id=event_id, user_id=user_id)
        return CustomResponse.create_response(True, status.HTTP_200_OK, "Success", resp)


class EventActionView(APIView):
    def get(self, request):
        user_id = request.user.id
        event_id = request.GET.get('event_id', 1)
        resp = get_event_actions(event_id=event_id, user_id=user_id)
        return CustomResponse.create_response(True, status.HTTP_200_OK, "Success", resp)


class FollowEventView(APIView):
    def get(self, request):
        user_id = request.user.id
        follow = request.GET.get('follow', True)
        resp = get_follow_events(follow=follow, user_id=user_id)
        return CustomResponse.create_response(True, status.HTTP_200_OK, "Success", resp)


class UnfollowEventView(APIView):
    def get(self, request):
        user_id = request.user.id
        follow = request.GET.get('follow', False)
        resp = get_unfollow_events(follow=follow, user_id=user_id)
        return CustomResponse.create_response(True, status.HTTP_200_OK, "Success", resp)


class UnfollowFriends(APIView):
    def post(self, request):
        user = request.user
        user_id = request.POST.get('user_id')
        friend = User.objects.filter(id=user_id).first()
        if friend in user.ref_user.all():
            user.ref_user.filter(id=friend.id).delete()
            return CustomResponse.create_response(True, status.HTTP_200_OK, 'Success', {})
        else:
            return CustomResponse.create_response(True, status.HTTP_200_OK, 'Not friend of this User', {})


class FollowFriends(APIView):
    def post(self, request):
        user = request.user
        user_id = request.POST.get('user_id')
        friend = User.objects.filter(id=user_id).first()
        if friend and friend not in user.ref_user.all():
            request.user.ref_user.add(friend)
            return CustomResponse.create_response(True, status.HTTP_200_OK, 'Success', {})
        else:
            return CustomResponse.create_response(True, status.HTTP_200_OK, 'User not exists', {})


class FriendsView(APIView):
    def get(self, request):
        id = request.user.id
        resp = get_friends_list(id=id)
        return CustomResponse.create_response(True, status.HTTP_200_OK, "Success", resp)


class ContactsView(APIView):
    def get(self, request):
        id = request.user.id
        resp = get_contacts_list(id=id)
        return CustomResponse.create_response(True, status.HTTP_200_OK, "Success", resp)


class ImportContacts(APIView):
    parser_classes = (JSONParser,)

    def post(self, request):
        # import pdb;pdb.set_trace()
        dict_list = request.data
        users = request.user.ref_user.all()
        # friend_users = request.user.ref_user.filter(temporary_profile=False)
        for item in dict_list:
            phone_number = item.get('phone_number')
            email = item.get('email')
            name = item.get('name')
            friend = User.objects.filter(phone_number=phone_number).first()
            if friend and friend not in users:
                request.user.ref_user.add(friend)
                friend.first_name = name
                friend.save()
            elif not friend:
                if email:
                    data = {"email": email, "password": "123456789"}
                elif not email:
                    phone = phone_number + "@dottech.info"
                    data = {"email": phone, "password": "123456789"}
                serializer = TemporaryUserSerializer(data=data)
                if serializer.is_valid():
                    s = serializer.save()
                    s.temporary_profile = True
                    s.phone_number = phone_number
                    s.first_name = name
                    id = s.id
                    new_friend = User.objects.filter(id=id).first()
                    request.user.ref_user.add(new_friend)
                    s.save()
        return CustomResponse.create_response(True, status.HTTP_200_OK, "Success", {})
