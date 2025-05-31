from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Recommendation
from .serializers import RecommendationSerializer
from finance.models import FinancialProduct
from .utils.make_personal_embedding_vector import parse_user_input
from .utils.recommendation import recommendation_with_userinfo_and_goal, vectorize_user_input
from .utils.model_loader import get_model

# 추천 요청 + 결과 조회 함수
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def ask_recommendation(request):

    if request.method == 'POST':

        input_data = request.data

        print(f'받은 데이터 : {input_data}')

        parsed_data = parse_user_input(input_data)
        user_input_vector = vectorize_user_input(parsed_data)

        model = get_model()
        result = recommendation_with_userinfo_and_goal(user_input_vector, model)
        print(result)
        product_ids = []
        for recommend in result.to_dict(orient='records'):
            product_ids.append(recommend['product_id'])
        
        products = FinancialProduct.objects.filter(id__in=product_ids)
        
        # 결과 저장하기
        recommendation = Recommendation.objects.create(user=request.user)
        recommendation.products.set(products)

        return Response(status=status.HTTP_201_CREATED)

    if request.method == 'GET':
        user = request.user
        user_recommendation = Recommendation.objects.filter(user=request.user).order_by('-created_at').first()
        serialzier = RecommendationSerializer(user_recommendation)
        return Response(serialzier.data, status=status.HTTP_200_OK)