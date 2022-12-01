from rest_framework import serializers
from .models import User, UserProfile
from rest_framework.exceptions import AuthenticationFailed 
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken,TokenError
from django.contrib import auth
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('title', 'dob', 'address', 'country', 'city', 'zip', 'photo')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Bifrost user writable nested serializer
    """
    profile = UserProfileSerializer(required=True)

    class Meta:
        model = User
        fields = ('url', 'email', 'first_name', 'last_name', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile

        instance.email = validated_data.get('email', instance.email)
        instance.save()

        profile.title = profile_data.get('title', profile.title)
        profile.dob = profile_data.get('dob', profile.dob)
        profile.address = profile_data.get('address', profile.address)
        profile.country = profile_data.get('country', profile.country)
        profile.city = profile_data.get('city', profile.city)
        profile.zip = profile_data.get('zip', profile.zip)
        profile.photo = profile_data.get('photo', profile.photo)
        profile.save()

        return instance


class LogoutSerializer(serializers.Serializer):
    refresh=serializers.CharField()
    default_error_messages={
        'bad_token':('Token is expired or invalid')
    }
    def validate(self, attrs):
        self.token = attrs['refresh']

        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')
        
class LoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255,min_length=3)
    password=serializers.CharField(max_length=68, min_length=6,write_only=True)
    username=serializers.CharField(max_length=255,min_length=3, read_only=True)
    tokens=serializers.SerializerMethodField()

    def get_tokens(self,obj):
        user = User.objects.get(email=obj['email'])

        return {
            'access':user.tokens()['access'],
            'refresh':user.tokens()['refresh']
        }
    class Meta:
        model=User
        fields=['email','password','username','tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password=attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)
      
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        
        #if not user.is_verified:
            #raise AuthenticationFailed('email is not verified')
        if not user.is_active:
            raise AuthenticationFailed('account disabled, contact admin')
        

        
        return {
            'email': user.email,
            'username':user.username,
            'tokens':user.tokens
        } 