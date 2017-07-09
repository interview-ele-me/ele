from django.contrib import admin
from lottery.models import Prize, UserByPrize, Result


admin.site.register(Prize)
admin.site.register(UserByPrize)
admin.site.register(Result)
