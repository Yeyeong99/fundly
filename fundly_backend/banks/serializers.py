from rest_framework import serializers

# from .models import Bank, Province, City

# class BankSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Bank
#         fields = '__all__'


# class ProvinceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Province
#         fields = '__all__'


# class CitySerializer(serializers.ModelSerializer):
    
#     province = ProvinceSerializer(read_only=True)
    
#     class Meta:
#         model = City
#         fields = ('id', 'province', 'name', )