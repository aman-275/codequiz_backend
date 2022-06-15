from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class TokenUserObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        """_summary_

        Overiding serializer so that user information is also available in one go, need to handle error case as well in future

        """
        data = super().validate(attrs)
        data["username"] = str(self.user.username)
        data["email"] = str(self.user.email)
        data["first_name"] = str(self.user.first_name)
        data["last_name"] = str(self.user.last_name)
        data["pk"] = str(self.user.id)

        return data
