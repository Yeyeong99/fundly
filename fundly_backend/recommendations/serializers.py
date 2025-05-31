from rest_framework import serializers

from .models import Recommendation
from finance.serializers import ProductReadSerializer
from accounts.serializers import UserProfileSerializer

class RecommendationSerializer(serializers.ModelSerializer):
    
    user = UserProfileSerializer(read_only=True)
    products = ProductReadSerializer(many=True, read_only=True)
    
    class Meta:
        model = Recommendation
        fields = ('user', 'products', )