from django.shortcuts import get_object_or_404

from rest_framework import serializers

from .models import Goal, WishList, ConnectedToGoal
from accounts.serializers import UserSimpleInfoSerializer
from finance.models import FinancialProduct, AdditionalProduct
from finance.serializers import OptionSerializer, AdditionalOptionSerializer, FinancialCompanySerializer, FinancialProductSerializer

from dateutil import relativedelta

# 목표 시리얼라이저
class GoalSerializer(serializers.ModelSerializer):
    class ConnectedToGoalSerializer(serializers.ModelSerializer):
        class Meta:
            model = ConnectedToGoal
            fields = '__all__'

    user = UserSimpleInfoSerializer(read_only=True)
    connected_to_goal = ConnectedToGoalSerializer(read_only=True, many=True)

    class Meta:
        model = Goal
        fields = ('id', 'user', 'goal_name', 'product_type', 'total_target_amount', 'saving_target_amount', 'deposit_target_amount', 
                  'start_date', 'end_date', 'connected_to_goal', )


# checkgoal에 목표들 보여주는 시리얼라이저 
class GoalTitleSerializer(serializers.ModelSerializer):
    class AchievementSerializer(serializers.ModelSerializer):
        
        class Meta:
            model = ConnectedToGoal
            fields = ('id', 'user', 'goal', 'current_amount', 'target_amount', 'financial_product', 'monthly_pay' )
            read_only_fields = ('current_amount', 'target_amount', )
            
        
    connected_to_goal = AchievementSerializer(read_only=True, many=True)
    user = UserSimpleInfoSerializer(read_only=True)
    duration_months = serializers.SerializerMethodField()
    achievement_rate = serializers.SerializerMethodField()

    class Meta:
        model = Goal
        fields = ('id', 'user', 'goal_name', 'product_type', 'start_date', 'end_date', 'total_target_amount', 'duration_months', 'connected_to_goal', 'achievement_rate', )

    def get_duration_months(self, obj):
        if obj.start_date and obj.end_date:
            delta = relativedelta.relativedelta(obj.end_date, obj.start_date)
            return delta.years * 12 + delta.months
        return None
    
    def get_achievement_rate(self, obj):
        total_current_amount = 0
        for product in obj.connected_to_goal.all():
            total_current_amount += product.current_amount
        
        if total_current_amount:
            return round(total_current_amount / obj.total_target_amount * 100, 2)
        else:
            return 0
            

# 찜한 상품 확인 시리얼라이저
class WishListReadSerializer(serializers.ModelSerializer):
    class FinancialProductDetailSerializer(serializers.ModelSerializer):
        
        financial_company = FinancialCompanySerializer(read_only=True)
        
        class Meta:
            model = FinancialProduct
            fields = ('id', 'financial_company', 'product_name', 'product_type', 'special_condition', 'join_way', 'etc_note', 'come_from', )
    
    class AdditionalProductDetailSerializer(serializers.ModelSerializer):
        class Meta:
            model = AdditionalProduct
            fields = ('id', 'financial_company', 'product_name', 'product_type', 'special_condition', 'join_way', 'etc_note', 'come_from', )
            
            
    user = UserSimpleInfoSerializer(read_only=True)
    financial_product = FinancialProductDetailSerializer(read_only=True)
    additional_product = AdditionalProductDetailSerializer(read_only=True)
    
    class Meta:
        model = WishList
        fields = ('user', 'financial_product', 'additional_product', )


# 찜한 상품 등록 및 삭제
class WishListCreateSerializer(serializers.ModelSerializer):
    
    product_pk = serializers.IntegerField()
    come_from = serializers.CharField()

    class Meta:
        model = WishList
        fields = ('product_pk', 'come_from', )

    def validate(self, data):
        product_pk = data['product_pk']
        come_from = data['come_from']
        
        if come_from == 'original':
            product = get_object_or_404(FinancialProduct, pk=product_pk)
            data['product'] = product
            return data
        
        elif come_from == 'additional':
            product = get_object_or_404(AdditionalProduct, pk=product_pk)
            data['product'] = product
            return data
        
        else:
            raise serializers.ValidationError("잘못된 상품입니다.")
        
        
# 사용자 설정 상품 전체 조회용 시리얼라이저
class TotalCustomReadSerializer(serializers.ModelSerializer):
    goal = GoalTitleSerializer(read_only=True, many=True)
    
    class Meta:
        model = ConnectedToGoal
        fields = ('id', 'goal', 'start_date', 'duration_months', 'is_active', )


# 사용자 설정 상품 생성용 시리얼라이저
class CustomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectedToGoal
        fields = '__all__'
        
        
# 사용자 설정 상품 상세 정보 시리얼라이저
class CustomDetailSerializer(serializers.ModelSerializer):
    
    goal = GoalTitleSerializer()
    option_product = OptionSerializer()
    additionaloption_product = AdditionalOptionSerializer()
    
    class Meta:
        model = ConnectedToGoal
        exclude = ('created_at', 'updated_at', )


class CustomDetailUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectedToGoal
        fields = [  # 수정 가능한 필드만 명시
            'current_amount',
            'target_amount',
            'start_date',
            'duration_months',
            'is_active',
            'monthly_pay',
        ]