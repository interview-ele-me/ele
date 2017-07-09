from django.shortcuts import render
from lottery.models import Prize, Result


def index(request):
    prize_list = Prize.objects.all()
    context = {"prize_list": prize_list}
    return render(request, 'lottery/index.html', context)


def result(request, prize_id):
    try:
        result = Result.objects.get(prize_id=prize_id)
    except:
        result = None

    context = {'result': result}
    return render(request, 'lottery/result.html', context)
