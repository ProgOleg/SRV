from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.template import loader
from .models import *
from .forms import *
from django.views.generic import View
import copy
from copy import deepcopy
import re
from decimal import *
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from datetime import *
from time import sleep
import requests
import json
from django.db.models import *




#Выборкадля рендеринка <datalist>
def data_list_select_type_sparpart(request):
    if request.method=='GET' and request.is_ajax():
        data = request.GET['val']
        if data:
            try:
                obj = list(TypeSparPart.objects.filter(type_spar_part__istartswith=data)[:100].values_list('type_spar_part'))
                return JsonResponse(obj, safe=False)
            except IndexError:
                obj = []
        else: obj = []
        return JsonResponse(obj, safe=False)

    return HttpResponse(status=404)

# Выборкадля рендеринка <datalist>
def data_list_select_manufacturer(request):
    if request.method=='GET' and request.is_ajax():
        data = request.GET['val']
        if data:
            try:
                obj = list(Manufacturer.objects.filter(manufacturer__istartswith=data).values_list('manufacturer'))
            except IndexError:
                obj =[]
        else:
            obj = []
        return JsonResponse(obj, safe=False)
    return HttpResponse(status=404)


#Выборка по "Тип устройства(select_applience)" для рендеринка <datalist>
def data_list_select_appliances(request):
    if request.method =='GET' and request.is_ajax():
        data = request.GET['val']
        if data:
            try:
                obj = list(TypeAppliances.objects.filter(type_appliances__istartswith=data)[:100].values_list('type_appliances'))
            except IndexError:
                obj = []
        else: obj = []
        return JsonResponse(obj, safe=False)

    return HttpResponse(status=404)




def lead_time(func):
    def time_show(*args, **kwargs):
        start = datetime.now()
        a = func(*args, **kwargs)
        finish = datetime.now()
        print('Время выполнения функции: {}'.format((finish - start).seconds))
        return a

    return time_show



def tools_get_exchange_rates_USD_privat24():
    #Возвращает курс доллара

    def date_for_requests(val):
        #Возвращает дату, в зависимости от входго значения (int) возвращает дат
        return (datetime.now() - timedelta(val)).date().strftime('%d.%m.%Y')


    def requests_get(date_val):
        #Делает запрос на урл и возвращает list('exchangeRate')
        url = 'https://api.privatbank.ua/p24api/exchange_rates?json&date={}'.format(date_val)
        r = requests.get(url)
        foo = r.text
        foo = json.loads(foo)
        bar = foo.get('exchangeRate')
        return bar

    def get_usd_saleRate(data):
        #достает курс USD из data
        result = {}
        for el in data:
            if el.get('currency') == 'USD':
                result = el
                break
        result = str(result.get('saleRate'))
        return result

    exchange_rate = None
    i = 1
    while not exchange_rate:
        date = date_for_requests(i)
        exchange_rate = requests_get(date)
        if not exchange_rate:
            i += 1
        else:
            exchange_rate = str(get_usd_saleRate(exchange_rate))
            break
    print(exchange_rate)
    return exchange_rate


def materialSaleObject_check_actual_salePrice(pk):
    obj = MaterialSaleObject.objects.filter(id=pk).values('sale_price')
    if not obj:
        return HttpResponse(status=404)
    val = obj[0]['sale_price']
    return  val


def materialSaleObject_check_actual_quantity(pk,val):
    obj_detail_quantity = MaterialSaleObject.objects.filter(id=pk).values('detail_attach__quantity')
    if not obj_detail_quantity:
        return None
    obj_detail_quantity = obj_detail_quantity[0]['detail_attach__quantity']
    values = Decimal(str(val))
    if values > obj_detail_quantity:
        return str(obj_detail_quantity)
    else: return False


def tools_ajax_check_tell(request):

    def valid_tell(tell):
        result = {}
        n = '+38'
        if tell[:3] != n:
            if len(tell) == 10:
                tell = n+tell
            else:
                result.update({'error':'Номер должен начинатся с +380!'})
                return result
        if len(tell) != 13:
            result.update({'error': 'Номер не соотвествующей длинны!'})
            return result
        for i in tell:
            if i == '+':
                continue
            try: int(i)
            except ValueError:
                result.update({'error': 'Номер не должен состоять из букв!'})
                return result
        return tell


    if request.method == 'GET':
        if request.is_ajax():
            data_tell = request.GET['tell']
            valid_data = valid_tell(data_tell)
            if 'error' in valid_data:
                return JsonResponse(valid_data,safe=False)
            obj = list(Person.objects.filter(tell=valid_data).values('first_name','last_name','patronymic_name',
                                                                     'tell','addres','email'))
            if obj:
                return JsonResponse(obj,safe=False)
            else: return JsonResponse({'message':'Телефонный номер свободный'})


class Round2(Func):
    function = "ROUND"
    template = "%(function)s(%(expressions)s::numeric, 2)"


def check_actual_sales_meterial_sales_obj(sale_person_id,material_sale_obj_id):
    """
    foo = SalesPersonInvoice.objects.get(id=sale_person_id).values('exchange_rates__exchange_rates')
    bar = MaterialSaleObject.objects.get(id=material_sale_obj_id).values(
        'detail_attach__attach_for_incoming__exchange_rates__exchange_rates','detail_attach__incoming_price')
    exchange_sale = Decimal(foo)
    exchange_incom = Decimal(bar['detail_attach__attach_for_incoming__exchange_rates__exchange_rates'])
    incom_price = Decimal(bar['detail_attach__incoming_price'])
    sales_price = (incom_price/exchange_incom)*exchange_sale
    """


    obj = MaterialSaleObject.objects.filter(person_invoice_attach=sale_person_id).annotate(sum_exchange=Round2((
        F('detail_attach__incoming_price') / F('detail_attach__attach_for_incoming__exchange_rates__exchange_rates'))*
        F('person_invoice_attach__exchange_rates__exchange_rates'))).values(
        'detail_attach__detail_name__name', 'detail_attach__detail_name__part_num',
        'detail_attach__detail_name__specification',
        'detail_attach__quantity', 'detail_attach__incoming_price','sum_exchange', 'id')













