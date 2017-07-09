from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
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


@api_view(['POST'])
@permission_classes((AllowAny, ))
def get_lucky_num(request):
    shanghai = float(request.data.get('shanghai'))
    shenzhen = float(request.data.get('shenzhen'))

    n = int(str(int(shanghai * shenzhen * 10000))[::-1])
    print(n)
    prize_list = Prize.objects.all()
    for prize in prize_list:
        total_num = prize.total_num
        if total_num:
            prize.lucky_num = n % total_num + 1
        prize.save()

    lucky_user_list = []
    user_by_prize_list = UserByPrize.objects.values('user_id', 'prize_id', 'lucky_num')
    lucky_dict = {(d['prize_id'], d['lucky_num']): d['user_id'] for d in user_by_prize_list}
    for prize in Prize.objects.values('id', 'lucky_num'):
        prize_id = prize['id']
        lucky_num = prize['lucky_num']
        if lucky_num:
            user_id = lucky_dict[(prize_id, lucky_num)]
            lucky_user_list.append((user_id, prize_id, lucky_num))

    Result.objects.bulk_create([Result(user_id=user_id, prize_id=prize_id, lucky_num=lucky_num)
                                for user_id, prize_id, lucky_num in lucky_user_list])
    return Response(status=status.HTTP_200_OK)
