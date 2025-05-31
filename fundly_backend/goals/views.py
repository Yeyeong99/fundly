from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .serializers import (
                            GoalSerializer, 
                            GoalTitleSerializer, 
                            WishListReadSerializer, 
                            WishListCreateSerializer,
                            TotalCustomReadSerializer,
                            CustomCreateSerializer,
                            CustomDetailSerializer,
                            CustomDetailUpdateSerializer,
                        )

from .models import Goal, WishList, ConnectedToGoal
from finance.models import FinancialProduct, AdditionalProduct
from .utils import simulate_precise_savings, simulate_precise_deposit
from .utils_openai import finance_chatbot

import json

User = get_user_model()

# Create your views here.
# 목표 조회, 생성
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def goals(request):
    user = request.user
    print(request.user)
    if request.method == 'GET':
        goals = Goal.objects.filter(user=user)
        serializer = GoalTitleSerializer(goals, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = GoalSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

# 목표 상세 조회, 수정, 삭제
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def goal_detail(request, goal_pk):
    user = request.user
    goal = get_object_or_404(Goal, pk=goal_pk)

    if request.method == 'GET':
        serializer = GoalSerializer(goal)
        return Response(serializer.data)
    
    if goal.user.id == user.pk:
        if request.method == 'PUT':
            serializer = GoalSerializer(goal, request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
            
        if request.method == 'DELETE':
            goal.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        

# 찜한 상품 전체 목록 조회 (마이페이지에서), 상품 찜하기/삭제하기 (상품 목록에서)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def wish_list(request):
    user = request.user
    
    if request.method == 'GET':
        wish_list = WishList.objects.filter(user=user)
        serializer = WishListReadSerializer(wish_list, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = WishListCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            product = serializer.validated_data['product']
            come_from = serializer.validated_data['come_from']
            if come_from == 'original':
                wish_list, created = WishList.objects.get_or_create(
                    user=user, financial_product=product
                )
            elif come_from == 'additional':
                wish_list, created = WishList.objects.get_or_create(
                    user=user, additional_product=product
                )
            
            # 이미 찜한 상품이라면
            if not created:
                wish_list.delete()    # 삭제
                return Response({'message': '찜 해제', 'is_liked': False}, status=status.HTTP_200_OK)
            else:
                return Response({'message': '찜 등록', 'is_liked': True}, status=status.HTTP_201_CREATED)

       
# 사용자가 설정한 상품 전체 조회 및 생성/수정
@api_view(['GET', 'POST'])
def custom_product(request):
    user = request.user

    if request.method == 'GET':
        user_custom_products = ConnectedToGoal.objects.all()
        serializer = TotalCustomReadSerializer(user_custom_products, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        data = request.data.copy()
        data['user'] = request.user.id

        goal = Goal.objects.get(pk=data['goal'])
        product = FinancialProduct.objects.get(pk=data['financial_product'])

        if ConnectedToGoal.objects.filter(goal=goal, financial_product=product, user=user).exists():
            return Response({'error': '중복 상품입니다.'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        custom_serializer = CustomCreateSerializer(data=data)
        if custom_serializer.is_valid(raise_exception=True):
            custom_serializer.save()
        
            product_pk = data['financial_product']
            financial_product = FinancialProduct.objects.get(pk=product_pk)
            product_type = financial_product.product_type
            target_amount = data['target_amount']
            
            goal_pk = data['goal']
            goal = Goal.objects.get(pk=goal_pk)

            if product_type == 'D':
                goal.deposit_target_amount = target_amount
                goal.save()
                
            elif product_type == 'S':
                goal.saving_target_amount = target_amount
                goal.save()
    
            return Response(status=status.HTTP_201_CREATED)
            

        

# 사용자가 설정한 특정 상품 조회, 삭제, 수정
@api_view(['GET', 'PUT', 'DELETE'])
def custom_detail(request, goal_pk, come_from, product_pk):
    user = request.user

    goal = Goal.objects.get(pk=goal_pk)
    if come_from == 'original':
        product = FinancialProduct.objects.get(pk=product_pk)
        connected_to_goal = ConnectedToGoal.objects.get(goal=goal, financial_product=product, user=user)

    elif come_from == 'additional':
        product = AdditionalProduct.objects.get(pk=product_pk)
        connected_to_goal = ConnectedToGoal.objects.get(goal=goal, additional_product=product, user=user)
    
    if request.method == 'GET':
        serializer = CustomDetailSerializer(connected_to_goal)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = CustomDetailUpdateSerializer(connected_to_goal, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    if request.method == 'DELETE':
        connected_to_goal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def check_product_connected(request, goal_id, product_id):
    user = request.user
    exists = ConnectedToGoal.objects.filter(
        goal_id=goal_id,
        product_id=product_id,
        user=user
    ).exists()
    return Response({'is_connected': exists})


@api_view(['POST'])
def use_finance_chatbot(request):
    question = request.data.get('question')
    result = finance_chatbot(question)
    result = result.replace('**', "")
    data = json.loads(result)
    return Response(data, status=status.HTTP_201_CREATED)