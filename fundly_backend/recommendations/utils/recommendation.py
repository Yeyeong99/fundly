import os
import pandas as pd
import numpy as np
import random

from sklearn.metrics.pairwise import cosine_similarity
from .make_personal_embedding_vector import parse_user_input

from django.conf import settings
from django.contrib.auth import get_user_model
from goals.models import Goal

User = get_user_model()

PRODUCT_TYPE_CATEGORIES = ["D", "S", "A"]  # 예금, 적금, 둘다

def encoding_product_type(product_type: str) -> list:
    return [1 if product_type == pt else 0 for pt in PRODUCT_TYPE_CATEGORIES]


# 사용자 정보 벡터화 하기
def vectorize_user_input(parsed):

    # 나이, 자산, 급여 >> 수치형
    numeric_vector = [parsed['age'], parsed['assets'], parsed['salary']]
    
    # work_type 그대로
    work_vector = parsed['work_type']

    # 목표 정보는 goal 이름을 바탕으로 따로 조회하기
    goal_name = parsed['goal']
    username = parsed['username']

    user = User.objects.get(username=username)
    goal = Goal.objects.get(goal_name=goal_name, user=user)

    goal_product_vector = encoding_product_type(goal.product_type)
    goal_duration = (goal.end_date - goal.start_date).days // 30
    goal_amount = goal.saving_target_amount + goal.deposit_target_amount
    goal_vector = [goal_amount, goal_duration]

    user_input_vector = numeric_vector + work_vector + goal_vector + goal_product_vector
    return np.array(user_input_vector).reshape(1, -1)

    
# 추천해주는 함수
def recommendation_with_userinfo_and_goal(user_input_vector, model):

    user_index_path = os.path.join(settings.BASE_DIR, 'recommendations', 'data', 'user_vector_index_encoded.csv')
    wishlist_path = os.path.join(settings.BASE_DIR, 'recommendations', 'data', 'dummy_wishlist.csv')
    products_path = os.path.join(settings.BASE_DIR, 'recommendations', 'data', 'financial_product_text.csv')
    userinfo_vector_path = os.path.join(settings.BASE_DIR, 'recommendations', 'data', 'final_userinfo_embeddings_encoded.npy')
    product_vector_path = os.path.join(settings.BASE_DIR, 'recommendations', 'data', 'financial_product_embeddings.npy')

    user_index = pd.read_csv(user_index_path)
    wishlist = pd.read_csv(wishlist_path)
    products = pd.read_csv(products_path)
    userinfo_vectors = np.load(userinfo_vector_path)
    product_vectors = np.load(product_vector_path)

    # 코사인 유사도 계산
    similarities = cosine_similarity(user_input_vector, userinfo_vectors).flatten()

    # 사용자와 가장 유사한 상위 5명 추출
    top_k = 5
    top_k_indices = similarities.argsort()[::-1][:top_k]
    top_k_user_ids = user_index.iloc[top_k_indices]["user_id"].tolist()

    # 찜한 상품 추출
    candidate_product_ids = wishlist[wishlist["user_id"].isin(top_k_user_ids)]["financial_product_id"].unique().tolist()
    candidate_texts = products[products["product_id"].isin(candidate_product_ids)]["text"].tolist()

    # 임베딩
    candidate_vectors = model.encode(candidate_texts)
    user_pref_vector = candidate_vectors.mean(axis=0).reshape(1, -1)

    # 전체 상품 임베딩 및 유사도 계산
    similarities = cosine_similarity(user_pref_vector, product_vectors).flatten()

    products["similarity"] = similarities
    recommended = products.sort_values(by="similarity", ascending=False).head(20).sample(5)

    return recommended[["product_id", "similarity", "text"]]