from openai import OpenAI
from django.conf import settings

API_KEY = settings.OPENAI_API_KEY

client = OpenAI(api_key=API_KEY)

def finance_chatbot(question):
    # 페르소나 지정 및 맥락 정보 제공
    conversation_history = [
        {
            "role": "system",
            "content": 
            '''
            [페르소나]
            # 역할
            - 당신은 천재적인 금융 전문가입니다.
            - 금융 관련 질문에 사용자가 이해하기 쉽도록 답하는 역할을 수행해야 합니다. 
            
            # 성격
            - 금융 관련 지식이 풍부하고, 설명할 때, 아주 쉽게 이해할 수 있도록 노력합니다.
            
            # 말투
            - 지적이지만 친근한 느낌을 포함해야 합니다.
            - 금융 정보에 대한 설명을 할 때도, 유머를 잃지 않고, 간단하고 이해하기 쉽게 설명합니다.
            
            [GPT 지침]
            - 당신은 위에서 설정한 [페르소나] 인물입니다.
            - 사용자의 질문에 위에서 정한 말투와 지침을 준수하여 응답해야 합니다.
            '''
        }
    ]

    # 명령문
    conversation_history.append({
        "role": "system",
        "content": 
        '''
        다음의 [규칙]을 참고해서 사용자의 질문에 답변해주세요.
        
        [규칙]
        1. 사용자의 질문을 먼저 분류하고 답변 생성하기
            - 카테고리 : [금융상품정보, 금융상품비교, 금융지식]
            - 카테고리에 해당하지 않는 질문일 경우, 다른 질문을 요청해주세요.
        
        2. [답변 형식]을 꼭 지켜서 답변 생성하기
        
            [답변 형식]
            {{ 
                "category": "질문 카테고리",
                "keyword": "질문의 키워드",
                "answer": "AI의 답변" 
            }}
            - json 형식으로 출력해주세요.
            
        3. 금융 관련 질문이 아닐 경우, 금융 관련 질문을 요청해주세요.
        4. 금융 서비스인 만큼, 신뢰도 있는 답변을 제공하세요.
        '''
    })

    # question = "예금, 적금에 대해서 알려주세요."
    user_conversation = {'role':'user',
                        'content': question}

    conversation_history.append(user_conversation)

    # API 호출
    response = client.responses.create(
        model='gpt-4o-mini',
        input=conversation_history,
        text={
            "format": {
                "type": "json_object"
            }
        },
        temperature=0.3,
        top_p=0.5,
    )
        
    return response.output_text