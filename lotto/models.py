from django.db import models
from django.contrib.auth.models import User

# 추첨 회차 모델 (관리자가 생성)
class Draw(models.Model):
    round_number = models.IntegerField(unique=True, verbose_name="회차")
    # 당첨 번호 6개 + 보너스 번호
    num1 = models.IntegerField()
    num2 = models.IntegerField()
    num3 = models.IntegerField()
    num4 = models.IntegerField()
    num5 = models.IntegerField()
    num6 = models.IntegerField()
    bonus_num = models.IntegerField()
    
    draw_date = models.DateTimeField(auto_now_add=True, verbose_name="추첨일")

    def __str__(self):
        return f"{self.round_number}회차 당첨번호"


# 복권 구매 내역 모델 (일반 사용자가 생성)
class Ticket(models.Model):

    # 누가 구매하였는지를 기록하기 위함
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name="구매자")
    draw_round = models.IntegerField(verbose_name="응모 회차") 
    
    # 사용자가 선택한 번호 6개
    num1 = models.IntegerField()
    num2 = models.IntegerField()
    num3 = models.IntegerField()
    num4 = models.IntegerField()
    num5 = models.IntegerField()
    num6 = models.IntegerField()
    
    is_auto = models.BooleanField(default=True, verbose_name="자동 여부")
    purchase_date = models.DateTimeField(auto_now_add=True, verbose_name="구매일")

    def __str__(self):
        type_str = "자동" if self.is_auto else "수동"
        return f"[{self.draw_round}회차] {type_str} 구매 내역"

# Create your models here.
