# 적금 예상 기간 결과 >> 단리S, 복리M
def simulate_precise_savings(
    monthly_amount: int,    # 단위 : 만원
    interest_rate: float,
    save_type: str,  # 'S' or 'M'
    savings_target_amount: int,    # 단위 : 만원
    max_months: int = 120
):
    deposits = []  # 각 납입액 저장
    months = 0
    current_amount = 0
    
    monthly_rate = interest_rate / 100 / 12

    # 목표치에 도달할 때까지 계산하기
    while current_amount < savings_target_amount and months < max_months:
        deposits.append(monthly_amount)
        months += 1
        total = 0

        for i, amount in enumerate(deposits):
            months_remaining = months - i
            if save_type == 'S':
                interest = amount * monthly_rate * months_remaining
                total += amount + interest
            elif save_type == 'M':  # 복리
                compound = amount * ((1 + monthly_rate) ** months_remaining)
                total += compound

        current_amount = total

    if current_amount >= savings_target_amount:
        return {
            'months': None,
            'current_amount': round(current_amount),
            'note': f'{max_months}개월 내에 목표 수령액에 도달하지 못합니다.'
        }
    return {
        'months': months,
        'current_amount': round(current_amount)
    }


# 예금 설정 기간 결과 >> 단리S, 복리M
def simulate_precise_deposit(
    principal_amount: int,    # 예치금
    interest_rate: float,    # 이자율
    save_type: str,
    deposit_target_amount: int,    # 목표 금액
    max_months: int = 240
) -> dict:
    
    monthly_rate = interest_rate / 100 / 12
    
    for months in range(1, max_months + 1):
        if save_type == 'S':
            # 단리 이자 = 원금 * 이율 * (개월 수 / 12)
            interest = principal_amount * (interest_rate / 100) * (months / 12)
            current_amount = principal_amount + interest
        
        elif save_type == 'M':
            # 복리 이자 = 원금 * ((1 + 월별 이율) ** 개월 수)
            current_amount = principal_amount * ((1 + monthly_rate) ** months)
            
        
        if current_amount >= deposit_target_amount:
            return {
                'months': months,
                'current_amount': round(current_amount)
            }
            
    return {
        'months': None,
        'current_amount': round(current_amount),
        'note': f'{max_months}개월 내에 목표 수령액에 도달하지 못합니다.'
    }

    
# 목표 조기 달성 예상 함수
    # => 사용자가 설정한 목표 기간 보다 더 빨리 도달할 수 있는지 계산하기
def is_early_achievable(principal_amount, interest_rate, save_type, duration_months, target_amount):
    result = simulate_precise_deposit(principal_amount, interest_rate, save_type, duration_months)
    return result['current_amount'] >= target_amount
    


# 추가 납입 시 변화 예측 함수
def compare_additional_deposit_effect():
    pass

    
if __name__ == "__main__":
    monthly_amount = 50    # 월별 납입액
    interest_rate = 3.0
    save_type = 'M'
    target_amount = 1000    # 목표 금액
    
    if save_type == 'M':
        save_type_name = '복리'
    elif save_type == 'S':
        save_type_name = '단리'
    
    print(f'매월 {monthly_amount}만원을 {save_type_name} {interest_rate}%로 적금했을 때')
    
    months, current_amount = simulate_precise_savings(monthly_amount,
                                                     interest_rate,
                                                     save_type,
                                                     target_amount)
    
    print(f'약 {months}개월 후 {current_amount}만원까지 도달')
    
    principal_amount = 1000
    interest_rate = 3.0
    save_type = 'S'
    target_amount = 1050
    
    if save_type == 'M':
        save_type_name = '복리'
    elif save_type == 'S':
        save_type_name = '단리'
        
    print(f'{save_type_name} {interest_rate}%로 예금했을 때,')
    
    result = simulate_precise_deposit(principal_amount,
                                      interest_rate,
                                      save_type,
                                      target_amount)

    if result['months']:
        print(f"약 {result['months']}개월 후 {result['current_amount']}만원까지 도달")
    else:
        print(result['note'])
        
