from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.template import loader
from django.template.loader import get_template

from .models import *
from .forms import *
from django.views.generic import View
import copy
from copy import deepcopy
import re
from decimal import *
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist

from time import sleep
import requests
import json
from django.db.models import *
from .views import *
from io import StringIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from cgi import escape


#Выборкадля рендеринка <datalist>
def data_list_select_type_sparpart(request):
    if request.method=='GET' and request.is_ajax():
        data = request.GET.get('val')
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
        data = request.GET.get('val')
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
        data = request.GET.get('val')
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



def tools_get_exchange_rates_EUR_privat24():
    #Возвращает курс евро

    def date_for_requests(val):
        #Возвращает дату, в зависимости от входго значения (int) возвращает дат
        foo = (datetime.now() - timedelta(val)).date().strftime('%d.%m.%Y')

        return foo


    def requests_get(date_val):
        #Делает запрос на урл и возвращает list('exchangeRate')
        url = 'https://api.privatbank.ua/p24api/exchange_rates?json&date={}'.format(date_val)
        r = requests.get(url)
        foo = r.text
        foo = json.loads(foo)
        bar = foo.get('exchangeRate')
        return bar

    def get_usd_saleRate(data):
        #достает курс (EUR) из data
        result = {}
        for el in data:
            if el.get('currency') == 'EUR':
                result = el
                break
        result = str(result.get('saleRateNB'))
        return result

    exchange_rate = None
    i = 1
    while not exchange_rate:
        date = date_for_requests(i)
        exchange_rate = requests_get(date)
        if not exchange_rate:
            i += 1
        else:
            exchange_rate = float(get_usd_saleRate(exchange_rate))
            exchange_rate = round(exchange_rate, 2)
            break
    #print(exchange_rate)
    return exchange_rate


def materialSaleObject_check_actual_salePrice(pk,new_val):
    #место для наценки
    obj = MaterialSaleObject.objects.filter(id=pk).values('detail_attach__incoming_price',
                                                          'detail_attach__attach_for_incoming__exchange_rates__exchange_rates',
                                                          'person_invoice_attach__exchange_rates__exchange_rates')
    if not obj.exists():
        return HttpResponse(status=404)
    incom_price = float(obj[0]['detail_attach__incoming_price'])
    incom_exchange_rates = float(obj[0]['detail_attach__attach_for_incoming__exchange_rates__exchange_rates'])
    sales_exchange_rates = float(obj[0]['person_invoice_attach__exchange_rates__exchange_rates'])
    price_in_currency = incom_price / incom_exchange_rates
    price_for_sale = price_in_currency * sales_exchange_rates
    price_for_sale = round(price_for_sale, 2)

    if price_for_sale < incom_price:
        price_for_sale = incom_price
    if price_for_sale > float(new_val):
        return JsonResponse({'error': 'Цена не меньше - "{}"'.format(price_for_sale)}, safe=False)
    return False


def materialSaleObject_check_actual_quantity(pk, val):
    obj_detail_quantity = MaterialSaleObject.objects.filter(id=pk).values('detail_attach__quantity')
    if not obj_detail_quantity.exists():
        return HttpResponse(status=404)
    obj_detail_quantity = float(obj_detail_quantity[0]['detail_attach__quantity'])
    val = float(val)
    if float(val) > obj_detail_quantity:
        return JsonResponse({'error': 'Кол-во не больше фактического - "{}"'.format(obj_detail_quantity)})
    else:
        MaterialSaleObject.objects.filter(pk=pk).update(quantity=val)
        return HttpResponse(status=200)


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
                                                                     'tell','addres','email','discount','role'))
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



def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    #context = Context(context_dict)
    context = context_dict
    html = template.render(context)
    result = StringIO()

    pdf = pisa.pisaDocument(StringIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))



def check_actual_sales_price(obj_pk):
    # Прод запчасть цена

    spart_part = Detail.objects.filter(pk=obj_pk).values('detail_name')

    if spart_part.exists():
        spart_part_pk = int(spart_part[0]['detail_name'])
    else: return HttpResponse(status=404)

    another_mat_sale_obj = MaterialSaleObject.objects.filter(detail_attach__detail_name_pk=spart_part_pk)
    if another_mat_sale_obj.exists():
        another_mat_sale_obj = another_mat_sale_obj.values('sale_price')[:2]
    else: pass

class OwnMarginMatSalesObj():
    pass


def calculation_and_save_own_margin_mat_sales_obj(*args, **kwargs):

    obj = MaterialSaleObject.objects.filter(*args,**kwargs).values(
        'pk', 'person_invoice_attach__exchange_rates__exchange_rates','person_invoice_attach__person_attach__discount',
        'sale_price', 'detail_attach__attach_for_incoming__exchange_rates__exchange_rates',
        'detail_attach__incoming_price')
    if not obj.exists():
        return
    for item in obj:
        pk = item['pk']
        person_discount = float(item['person_invoice_attach__person_attach__discount'])
        incoming_exchange_rates = float(item['detail_attach__attach_for_incoming__exchange_rates__exchange_rates'])
        incoming_price = float(item['detail_attach__incoming_price'])
        sale_price = float(item['sale_price'])
        sales_exchange_rates = float(item['person_invoice_attach__exchange_rates__exchange_rates'])
        # Нориализация курса
        incoming_price_normal = (incoming_price / incoming_exchange_rates) * sales_exchange_rates
        if incoming_price_normal < incoming_price:
            incoming_price_normal = incoming_price
        # Вычисление коэфициента
        margin_coefficient = sale_price / (incoming_price_normal - incoming_price_normal * (person_discount / 100))
        margin_coefficient = round(margin_coefficient, 2)
        MaterialSaleObject.objects.filter(pk=pk).update(own_margin=margin_coefficient)


class HistotySales():

    def all_history_mat_sales_obj(self,catalog_pk):

        obj = MaterialSaleObject.objects.filter(detail_attach__detail_name__pk=catalog_pk)
        obj = obj.values(

        )














