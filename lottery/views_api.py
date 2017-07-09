from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from lottery.models import Prize, UserByPrize, Result


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def buy(request):
    user_id = request.user.id
    prize_id = request.data.get('prize_id')

    prize = Prize.objects.get(id=prize_id)
    prize.lucky_num += 1
    lucky_num = prize.lucky_num
    prize.save()

    UserByPrize.objects.create(user_id=user_id, prize_id=prize_id, lucky_num=lucky_num)

    return Response({'lucky_num': lucky_num}, status=status.HTTP_200_OK)
