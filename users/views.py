from django.shortcuts import render
from requests import request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import UserFollowing
from .serializers import FollowingSerializer, FollowersSerializer
from rest_framework import status
from .exceptions import UserDoesNotExist
from .models import User
from rest_framework.generics import ListAPIView

# Create your views here.
# class Followers(APIView):
#     """
#     api view handles both follow and unfollow scenario
#     as two of the cases closely related to each other so yeah
#     in cost , single responsibilty is violated
#     """

#     permission_classes = [IsAuthenticated]
#     queryset = UserFollowing.objects.all()
#     serializers = {
#         'following':FollowingSerializer,
#         'followers':FollowersSerializer
#     }

#     def get_queryset(self):
#         queryset_dict={
#             self.request.query_params.get('key'): request.user
#         }
#         return self.queryset.filter(**queryset_dict)

#     def get(self, request):
#         try:
#             queryset = self.get_queryset()
#             serializer = serializer.get(request.query_params.get('key'))
#             return Response(serializer(queryset, many=True),status=status.HTTP_200_OK)

#         except KeyError:
#             raise QueryKey

#         except Exception as e:

#             return e


#     def post(self, request):
#         try:
#             key = request.data.get('key')
#             follow_id = request.data.get('follow_id')
#             user = User.objects.get(id=follow_id)


#         except User.DoesNotExist as e:
#             return e

#         except Exception as e:
#             return e


class Following(ListAPIView):
    serializer_class = FollowingSerializer
    queryset = UserFollowing.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user_id=self.request.user)


class Followers(ListAPIView):
    serializer_class = FollowersSerializer
    queryset = UserFollowing.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(following_user_id=self.request.user)


class Follow(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        try:
            user = User.objects.get(pk=id)
            already_followed = UserFollowing.objects.filter(
                user_id=request.user, following_user_id=user
            ).first()

            if not already_followed:
                new_follower = UserFollowing(
                    user_id=request.user, following_user_id=user
                )
                new_follower.save()
                return Response({"status": "followed"}, status=status.HTTP_200_OK)

            else:
                already_followed.delete()
                return Response({"status": "unfollowed"}, status=status.HTTP_200_OK)

        except User.DoesNotExist as e:
            raise UserDoesNotExist

        except Exception as e:
            return None
