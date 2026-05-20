import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Draw, Ticket

def index(request):
    # 가장 최근에 추첨된 회차 가져옴
    last_draw = Draw.objects.order_by('-round_number').first()
    
    # 현재 구매 중인 회차는 (마지막 추첨 회차 + 1) 회차임 (아무것도 없으면 1회차)
    current_round_number = (last_draw.round_number + 1) if last_draw else 1

    # 지난 추첨 결과 전체 목록
    past_rounds = Draw.objects.order_by('-round_number')

    # 접속한 사람의 신분에 따라 보여줄 복권을 다르게 가져옴
    if request.user.is_authenticated:
        if request.user.is_staff:
            # 관리자: 이 사이트에서 팔린 '모든' 복권을 최신순으로 가져옴
            all_tickets = Ticket.objects.order_by('-purchase_date')
        else:
            # 일반 사용자: (request.user)가 구매한 복권만 필터링해서 가져옴
            all_tickets = Ticket.objects.filter(user=request.user).order_by('-purchase_date')
    else:
        # 비회원(로그아웃 상태): 아무 복권도 보여주지 않음
        all_tickets = []

    # 티켓마다 당첨 번호와 대조하여 실시간으로 등수 매기기
    processed_tickets = []
    for ticket in all_tickets:
        draw = Draw.objects.filter(round_number=ticket.draw_round).first()
        rank_result = "추첨 대기 중"
        match_count = 0

        if draw:
            win_set = {draw.num1, draw.num2, draw.num3, draw.num4, draw.num5, draw.num6}
            ticket_set = {ticket.num1, ticket.num2, ticket.num3, ticket.num4, ticket.num5, ticket.num6}
            
            match_count = len(win_set.intersection(ticket_set))

            if match_count == 6:
                rank_result = "1등 !!!"
            elif match_count == 5 and draw.bonus_num in ticket_set:
                rank_result = "2등 !!"
            elif match_count == 5:
                rank_result = "3등 !"
            elif match_count == 4:
                rank_result = "4등"
            elif match_count == 3:
                rank_result = "5등"
            else:
                rank_result = "낙첨"

        processed_tickets.append({
            'instance': ticket,
            'numbers': [ticket.num1, ticket.num2, ticket.num3, ticket.num4, ticket.num5, ticket.num6],
            'rank': rank_result,
            'match_count': match_count
        })

    context = {
        'current_round_number': current_round_number,
        'past_rounds': past_rounds,
        'processed_tickets': processed_tickets,
    }
    return render(request, 'lotto/index.html', context)


# 로그인을 한 사람만 티켓을 살 수 있도록 막음
@login_required 
def buy_ticket(request):
    if request.method == 'POST':
        last_draw = Draw.objects.order_by('-round_number').first()
        current_round_number = (last_draw.round_number + 1) if last_draw else 1
        
        is_auto = request.POST.get('mode') == 'auto'

        if is_auto:
            nums = sorted(random.sample(range(1, 46), 6))
        else:
            selected_numbers = request.POST.getlist('manual_numbers')
            if len(selected_numbers) != 6:
                messages.error(request, "반드시 6개의 번호를 선택해야 합니다.")
                return redirect('lotto:index')
            nums = sorted(list(map(int, selected_numbers)))

        # Ticket을 생성할 때 누가 샀는지 알기위함
        Ticket.objects.create(
            user=request.user, # 현재 로그인한 유저 정보를 저장
            draw_round=current_round_number,
            num1=nums[0],
            num2=nums[1],
            num3=nums[2],
            num4=nums[3],
            num5=nums[4],
            num6=nums[5],
            is_auto=is_auto
        )
        mode_str = "자동" if is_auto else "수동"
        messages.success(request, f"로또 ({mode_str}) 구매가 완료되었습니다! 번호: {nums}")
        
    return redirect('lotto:index')


# 관리자인 사람만 추첨 버튼을 누를 수 있도록 막음
@user_passes_test(lambda u: u.is_staff) 
def admin_draw(request):
    if request.method == 'POST':
        last_draw = Draw.objects.order_by('-round_number').first()
        current_round_number = (last_draw.round_number + 1) if last_draw else 1

        all_nums = random.sample(range(1, 46), 7)
        winning_nums = sorted(all_nums[:6])
        bonus = all_nums[6]

        Draw.objects.create(
            round_number=current_round_number,
            num1=winning_nums[0],
            num2=winning_nums[1],
            num3=winning_nums[2],
            num4=winning_nums[3],
            num5=winning_nums[4],
            num6=winning_nums[5],
            bonus_num=bonus
        )
        messages.success(request, f"제 {current_round_number}회 추첨이 완료되었습니다! 당첨번호: {winning_nums} + 보너스: {bonus}")

    return redirect('lotto:index')


# 일반 사용자 회원가입 기능
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()          # 데이터베이스에 일반 사용자 계정으로 안전하게 저장
            auth_login(request, user)   # 가입이 성공하면 그 자리에서 즉시 자동 로그인 처리
            messages.success(request, f"{user.username}님, 회원가입을 축하합니다!")
            return redirect('/')        # 가입 완료 후 메인 로또 페이지로 이동
    else:
        form = UserCreationForm()
        
    return render(request, 'registration/signup.html', {'form': form})
