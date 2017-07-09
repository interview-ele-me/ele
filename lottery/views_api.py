from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from lottery.models import Prize, UserByPrize, Result, CountUserByPrize


# makemigrate 时将以下代码注释
# 添加新的Prize之后，需要将系统重启

def low_bit(x):
    return x & (-x)

def update(i, x, M, t):
    while i < M:
        t[i] += x
        i += low_bit(i)

def sum_(x, t):
    cnt = 0
    while x > 0:
        cnt += t[x]
        x -= low_bit(x)
    return cnt

# 假设没有人在同一个prize抽奖超过100000次
M = 100000
cnt_list = [0 for _ in range(M)]
d2list = {prize['id']: list(cnt_list) for prize in Prize.objects.values('id')}
for count_user_by_prize in CountUserByPrize.objects.values('prize_id', 'count'):
    prize_id = count_user_by_prize['prize_id']
    count = count_user_by_prize['count']
    update(count, 1, M, d2list[prize_id])

#  makemigrate 时 讲以上代码注释


# 运行一次
# 产品经理提出后，讲这个接口运行一次
@api_view(['GET'])
def init_CountUserByPrize(request):
    from collections import Counter

    cnt = Counter()
    for user_by_prize in UserByPrize.objects.values('user_id', 'prize_id'):
        cnt[(user_by_prize['user_id'], user_by_prize['prize_id'])] += 1
    CountUserByPrize.objects.bulk_create([CountUserByPrize(user_id=x[0], prize_id=x[1], count=cnt[x]) for x in cnt])
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def buy(request):
    user_id = request.user.id
    prize_id = request.data.get('prize_id')

    prize = Prize.objects.get(id=prize_id)
    prize.total_num += 1
    lucky_num = prize.total_num
    prize.save()

    UserByPrize.objects.create(user_id=user_id, prize_id=prize_id, lucky_num=lucky_num)
    count_user_by_prize, created = CountUserByPrize.objects.get_or_create(user_id=user_id, prize_id=prize_id,
                                                                           defaults={'count': 1})

    prize_id = int(prize_id)
    if not created:
        count = count_user_by_prize.count + 1
        count_user_by_prize.count += 1
        count_user_by_prize.save()

        update(count, 1, M, d2list[prize_id])
        update(count - 1, -1, M, d2list[prize_id])
    else:
        count = 1
        update(count, 1, M, d2list[prize_id])

    cnt_less = sum_(count - 1, d2list[prize_id])
    cnt_all = sum_(M - 1, d2list[prize_id])

    if cnt_all == 1:
        percentage = 100.0
    else:
        percentage = cnt_less / cnt_all * 100

    return Response({'lucky_num': lucky_num, 'percentage': percentage, 'cnt_num': lucky_num, 'cnt_user': cnt_all,
                     'count': count}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny, ))
def get_lucky_num(request):
    try:
        shanghai = float(request.data.get('shanghai'))
        shenzhen = float(request.data.get('shenzhen'))
    except:
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    n = int(str(int(shanghai * shenzhen * 10000))[::-1])
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
