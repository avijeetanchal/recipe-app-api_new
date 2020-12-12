from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _ # to convert to diff languages

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for USers_object"""

    class Meta:
        model = get_user_model()
        # model that you want to base serializer on

        #fields that is convert to and from json
        fields = ('email', 'password','name') # add more if you like, DOB< GENDER
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encripted password and return it"""
        # we mofidy the create function and cll our create_user method
        return get_user_model().objects.create_user(**validated_data)

class AuthTokenSerializer(serializers.serializer):
    """serializer for user authentication objects"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type':'password'},
        trim_whitespace=False,
    )

    ## all the field created is passed as attrs as dict in validate
    def validate(self, attrs):
        """Validate and authenticate our user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request = self.context.get('request'),
            username = email,
            password = password
        )
        if not user: # if after authentication user isnt passed.
            msg = _('unlable to authenticate with given credentails')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
