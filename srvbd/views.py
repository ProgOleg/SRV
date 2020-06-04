from datetime import time

from django.db import transaction
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template import loader
from django.core.paginator import Paginator
from .models import *
from .forms import *
from django.views.generic import View
import copy
from copy import deepcopy
import re
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from datetime import *
from time import sleep
import requests
import json
import telepot
import django.utils.timezone
from django.core.paginator import *
import datetime
from collections import namedtuple
#from . import utils
from srvbd.utils import *
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class AuthUser(LoginView):
    template_name = 'srvbd/auth_user.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('index_url')
    redirect_field_name = ''


class LogOut(LogoutView):
    pass

@login_required
def index(request):
    return render(request, 'srvbd/index.html')


@login_required
def person_list(request):
    if request.method == 'GET':
        person_last_add = Person.objects.order_by('-pub_date')[:20]
        template = loader.get_template('srvbd/person_list.html')
        context = {'person_last_add': person_last_add}
        return HttpResponse(template.render(context,request))


@login_required
def person_create(request):

    if request.method == 'GET':
        form = PersonCreate()
        return render(request, 'srvbd/person_create.html', context={'form': form})

    if request.method == 'POST':
        form = PersonCreate(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/person/')
        else: return render(request, 'srvbd/person_create.html', context={'form': form})



@login_required
def spar_part_add(request):
    context = {
        'form_add_part': AddPart(),
        'specification_filter' : IncomInfoShipper(),
        'form_add_attachment_part': AddTypeSparPart(),
        'form_add_attachment_appliances': AddTypeAppliances(),
        'form_add_manufacturer': AddManufacturer(),
    }

    if request.method == 'GET':
        return render(request, 'srvbd/part_add.html', context)

    elif request.method =='POST':

        def return_invalid_feedback(request,form_add_part,specification_filter):
            context['form_add_part'] = form_add_part
            context['specification_filter'] = specification_filter
            return render(request, 'srvbd/part_add.html', context)
        values = {'attachment_part':['type_spar_part',TypeSparPart],'attachment_appliances':['type_appliances',TypeAppliances],
                  'attachment_manufacturer':['manufacturer',Manufacturer]}
        data = request.POST
        form_add_part = AddPart(data)
        specification_filter = IncomInfoShipper(data)
        if form_add_part.is_valid():
            form_add_part_cleaned_data = form_add_part.cleaned_data
        else:
            return return_invalid_feedback(request,form_add_part,specification_filter)
        if specification_filter.is_valid():
            specification_filter_cleaned_data = specification_filter.cleaned_data
        else:
            return return_invalid_feedback(request, form_add_part, specification_filter)
        data_to_create = {}
        for item in values.keys():
            mod_name = values[item][1]
            field_name = values[item][0]
            val = specification_filter_cleaned_data.get(item)
            obj = mod_name.objects.filter(**{field_name:val}).values('id')
            if obj.exists():
                pk = obj[0].get('id')
                data_to_create.update({item + '_id': pk})
            else:
                specification_filter.add_error(field=item,error='Такая спецификация не создана')
                return return_invalid_feedback(request, form_add_part, specification_filter)
        data_to_create = {**data_to_create,**form_add_part_cleaned_data}
        SparPart.objects.create(**data_to_create)
        return render(request, 'srvbd/part_add.html', context)

    else: return HttpResponse(status=404)


@login_required
def ajax_add_specification(request):
    if request.is_ajax() and request.method == 'POST':
        data = request.POST
        values ={'type_spar_part': AddTypeSparPart ,'type_appliances': AddTypeAppliances,
                 'manufacturer': AddManufacturer}
        for elem in values.keys():
            if data.get(elem):
                form = values.get(elem)
                form = form(request.POST)
                #import pdb
                #pdb.set_trace()
                if form.is_valid():
                    form.save()
                    return JsonResponse({'success':'True'})
                else:
                    return JsonResponse({'success':'False','error_message':form.errors})
    return HttpResponse(status=404)


@login_required
def spare_parts_manual(request):
    if request.method == 'GET':
        parts_manual_list = SparPart.objects.order_by('-id')
        context = {'manual': parts_manual_list}

    return render(request, 'srvbd/spare_parts_manual.html',context)


@login_required
def shipper_create(request):
    context = {'ship_create':ShipperCreate()}
    if request.method == "GET":
        return render(request,'srvbd/shipper_create.html',context)
    if request.method == "POST":
        data = ShipperCreate(request.POST)
        if data.is_valid():
            data.save()
            return render(request, 'srvbd/shipper_create.html', context)
        else:
            context['ship_create'] = data
            return render(request,'srvbd/shipper_create.html',context)



@login_required
def shippers_list(request):
    ship_list = Shipper.objects.order_by('-id')[:100]
    return render(request, 'srvbd/shippers_list.html',{'ship_list': ship_list})



class IncomingList(LoginRequiredMixin, View):

    def get(self,request):
        all_incom = Incoming.objects.all()
        return render(request,'srvbd/incom_list.html', {'all_incoming':all_incom})


class IncomingListDetail(LoginRequiredMixin, View):

    def get(self,request,incom_id):
        if Incoming.objects.filter(id=incom_id).exists():
            incom = Incoming.objects.filter(pk=incom_id).annotate(full_name=Concat(
                'ship__last_name', V(' '), 'ship__first_name', V(' '), 'ship__patronymic_name')).values(
                'incoming_date', 'exchange_rates__exchange_rates', 'full_name', 'id')
            details = DetailInIncomList.objects.filter(selector_incom=incom_id).annotate(sum=F('incoming_price') * F('quantity'))
            equal_details = details.aggregate(Sum('sum'))
            details = details.values('spar_part__id', 'spar_part__name', 'spar_part__part_num', 'spar_part__specification',
                    'spar_part__attachment_part__type_spar_part', 'spar_part__attachment_appliances__type_appliances',
                    'spar_part__attachment_manufacturer__manufacturer', 'incoming_price', 'quantity', 'sum')

            context = {'incom': incom[0],'details': details,'equal_details':equal_details['sum__sum']}
            return render(request,'srvbd/incom_list_detail.html',context)
        else: return HttpResponse(status=404)




class DetailInStockView(LoginRequiredMixin, View):

    def get(self,request):
        detail_count = Detail.objects.filter(status_delete=False).count()
        equal_details = Detail.objects.filter(status_delete=False).annotate(
            equal=F('quantity')*F('incoming_price')).aggregate(Sum('equal'))
        context = {'specification_filter': IncomInfoShipper(),'detail_filter': FilterDetail(),
                    'detail_count':detail_count,'equal_details':equal_details['equal__sum'] }
        return render(request, 'srvbd/detail_in_stock.html', context)


@login_required
def ajax_detail_in_stock_filter(request,page):

    if request.is_ajax() and request.method == 'GET':
        data = dict(request.GET)
        if data:
            set_field_name = {
                'name':'detail_name__name__icontains','specification':'detail_name__specification__icontains',
                'part_num':'detail_name__part_num__icontains','attachment_part': 'detail_name__attachment_part__type_spar_part',
                'attachment_appliances': 'detail_name__attachment_appliances__type_appliances',
                'attachment_manufacturer': 'detail_name__attachment_manufacturer__manufacturer'}
            for item in set_field_name:
                el = data.pop(item, None)
                if el != None:
                    data.update({set_field_name.get(item): el[0]})
                else:
                    return HttpResponse(status=400)
            filtered_data = data.copy()
            for item in data:
                element = data.get(item)
                if isinstance(element, list):
                    element = element[0]
                if len(element) == 0:
                    filtered_data.pop(item)
            filtered_data.update({'status_delete':False})
        else:
            filtered_data = {'status_delete':False}

        quer = Detail.objects.filter(**filtered_data).annotate(
            date_and_exch=Concat('attach_for_incoming__incoming_date', V(' '),
                                 'attach_for_incoming__exchange_rates__exchange_rates', V('$'),
                                 output_field=CharField())).values(
            'detail_name__id', 'detail_name__name', 'detail_name__part_num', 'detail_name__specification',
            'detail_name__attachment_part__type_spar_part', 'detail_name__attachment_appliances__type_appliances',
            'detail_name__attachment_manufacturer__manufacturer', 'incoming_price', 'date_and_exch', 'quantity',
            'attach_for_incoming__id')
        obj = Paginator(quer, 5)
        try:
            obj = obj.page(page)
        except InvalidPage:
            return HttpResponse(status=404)
        Template = namedtuple(
            'Detai_in_stock', 'detail_name__id detail_name__name detail_name__part_num detail_name__specification '
                              'detail_name__attachment_part__type_spar_part '
                              'detail_name__attachment_appliances__type_appliances '
                              'detail_name__attachment_manufacturer__manufacturer'
                              ' date_and_exch quantity incoming_price attach_for_incoming__id')
        new_obj = [Template(**i)._asdict() for i in obj]
        return JsonResponse(new_obj, safe=False)
    else: return HttpResponse(status=404)











class CreateIncoming(LoginRequiredMixin, View):

    context = {
        'incming_stat_false': Incoming.objects.filter(status = False),
        'create_incom': CreateIncom(),
        'exchange_rates': ExchangeRatesForm(),
    }

    def get(self,request):
        return render(request,'srvbd/create_incoming.html',self.context)

    def post(self,request):

        data = request.POST
        if 'edit' in data:
            incom_id = int(data.get('edit'))
            return redirect('/create_incoming/{}/'.format(incom_id))

        data_incom = CreateIncom(request.POST)
        data_exchange_rates = ExchangeRatesForm(request.POST)
        if data_incom.is_valid() and data_exchange_rates.is_valid():
            obj = ExchangeRates.objects.create(exchange_rates=data_exchange_rates.cleaned_data['exchange_rates'])
            new_data = Incoming.objects.create(**data_incom.cleaned_data,exchange_rates=obj)
            return redirect('/create_incoming/{}/'.format(new_data.id))
        else:
            return HttpResponse(status=404)




class EditIncoming(LoginRequiredMixin, View):


    def get (self,request,incom_id):

        if request.is_ajax():
            if DetailInIncomList.objects.filter(selector_incom_id=incom_id).first():
                data = list(DetailInIncomList.objects.filter(selector_incom_id=incom_id).values(
                    'id','spar_part__name', 'spar_part__part_num', 'spar_part__specification','quantity','incoming_price'))
                return JsonResponse(data,safe=False)
            else: return JsonResponse({'massage':''})
        else:
            context = {'specification_filter': IncomInfoShipper(),
                'detail_filter': FilterDetail()}
            if Incoming.objects.filter(pk=incom_id).exists():
                incom = Incoming.objects.filter(pk=incom_id).annotate(full_name=Concat(
                    'ship__last_name', V(' '), 'ship__first_name', V(' '),'ship__patronymic_name')).values(
                    'incoming_date','exchange_rates__exchange_rates','full_name','id')
                context.update({'incom': incom[0]})
                return render(request, 'srvbd/edit_incoming.html', context)
            else: return HttpResponse(status=404)


    def post(self,request,incom_id):
        Incoming.objects.filter(id=incom_id).update(status=True)
        data = DetailInIncomList.objects.filter(selector_incom_id=incom_id)
        for item in data:
            obj_spart = int(item.spar_part_id)

            Detail.objects.create(detail_name_id=obj_spart,incoming_price=item.incoming_price,
                quantity=item.quantity,attach_for_incoming_id=incom_id)
        revers_url = reverse('incom_list_detail_url',args=[incom_id])
        return redirect(revers_url)



@login_required
def tools_ajax_create_incom_filter(request):

    if request.is_ajax() and request.method == 'GET':
        data = dict(request.GET)
        if data:
            set_field_name = {
                'name':'name__icontains','part_num':'part_num__icontains',
                'specification':'specification__icontains',
                'attachment_appliances':'attachment_appliances__type_appliances',
                'attachment_part':'attachment_part__type_spar_part',
                'attachment_manufacturer':'attachment_manufacturer__manufacturer',}
            for item in set_field_name:
                el = data.pop(item,None)
                if el != None:
                    data.update({set_field_name.get(item):el[0]})
                else: return HttpResponse(status=400)
        filtered_data = data.copy()
        for item in data:
            element = data.get(item)
            if isinstance(element,list):
                element = element[0]
            if len(element) == 0: filtered_data.pop(item)
        response_data = SparPart.objects.filter(**filtered_data)[:30].values('id', 'name', 'part_num', 'specification', 'attachment_part__type_spar_part',
                                           'attachment_appliances__type_appliances','attachment_manufacturer__manufacturer')

        return JsonResponse(list(response_data),safe=False)
    else:return HttpResponse(status=404)



@login_required
def tools_ajax_create_incom_detail(request,incom_id):
    if request.method == 'POST':
        data = request.POST
        spart_part_obj = int(data['id_spar_part'])
        if not DetailInIncomList.objects.filter(selector_incom_id=incom_id).filter(spar_part_id=spart_part_obj).count():
            DetailInIncomList.objects.create(spar_part_id=spart_part_obj, selector_incom_id=incom_id)
            item = list(DetailInIncomList.objects.filter(spar_part_id=spart_part_obj,selector_incom_id=incom_id).values(
                'id','spar_part__name', 'spar_part__part_num', 'spar_part__specification','quantity','incoming_price'))
            return JsonResponse(item, safe=False)
        else:
            item = list(DetailInIncomList.objects.filter(selector_incom_id=incom_id).values(
                'spar_part__name', 'spar_part__part_num', 'spar_part__specification', 'incoming_price', 'quantity'))
            item.append({'error':'Такая запчасть уже есть в приходе'})
            return JsonResponse({'error':'Такая запчасть уже есть в приходе'},safe=False)
    else: return HttpResponse(status=404)


@login_required
def tools_ajax_create_incom_change_detail(request,incom_id):
    if request.method == 'POST':
        data = request.POST
        field = data['field']
        if data['new_val']:
            val = data['new_val']
        else:
            val = 0

        if field == "quantity":
            obj = DetailInIncomList.objects.filter(id=int(data['id'])).update(quantity=val)
        elif field == "incoming_price":
            obj = DetailInIncomList.objects.filter(id=int(data['id'])).update(incoming_price=val)
        return JsonResponse(obj,safe=False)
    else: return HttpResponse(status=404)


@login_required
def tools_ajax_create_incom_delete_detail(request,incom_id):
    if request.method == 'POST':
        data = request.POST
        if data['delete_obj']:
            obj_id = int(data['delete_obj'])
            if DetailInIncomList.objects.filter(id=obj_id).count():
                result = DetailInIncomList.objects.get(id=obj_id).delete()
                return JsonResponse(result, safe=False)
            else: return JsonResponse({'error':'"delete_obj_id" нет в BD!'}, safe=False)
        else: return JsonResponse({'error':'Request obj нe содержит "delete_obj"'}, safe=False)
    else: return HttpResponse(status=404)




class AddDevice(LoginRequiredMixin, View):

    def get(self,request):
        context = {'form': AddDeviceForm(),'select_form':SelectManufacturTypeAppliances()}
        return render(request,'srvbd/add_device.html',context)

    def post(self,request):
        #import pdb;pdb.set_trace()
        if request.is_ajax():
            data = request.POST
            data_mod_pnc = AddDeviceForm(data)
            data_select = SelectManufacturTypeAppliances(data)
            if data_select.is_valid():
                try:
                    type_appliances_obj = TypeAppliances.objects.get(
                        type_appliances=data_select.cleaned_data['type_appliances'])
                except ObjectDoesNotExist:
                    return JsonResponse({'error':{'type_appliances':'Введенного типа техники нет в BD!'}})
                try:
                    manufacturer_obj = Manufacturer.objects.get(
                        manufacturer=data_select.cleaned_data['manufacturer'])
                except ObjectDoesNotExist:
                    return JsonResponse({'error':{'manufacturer':'Введенного производителя нет в BD!'}})
            else:
                return JsonResponse({'error': 'Вы ввели некорректные данные'})
            if data_mod_pnc.is_valid():
                Device.objects.create(manufacturer=manufacturer_obj,type_appliances=type_appliances_obj,
                                      mod=data_mod_pnc.cleaned_data['mod'],pnc=data_mod_pnc.cleaned_data['pnc'])
            else:
                return JsonResponse({'error': 'Вы ввели некорректные данные'})
        else: return HttpResponse(status=404)




@login_required
def tools_ajax_add_part_set_list(request):
    if request.is_ajax():
        if request.method == 'GET':
            data = request.GET
            if data.get('field')=="manufacturer":
                item = list(Manufacturer.objects.filter(
                    manufacturer__istartswith = data.get('val')).values_list('manufacturer'))
            elif data.get('field')=="type_appliances":
                item = list(TypeAppliances.objects.filter(
                    type_appliances__istartswith = data.get('val')).values_list('type_appliances'))
            else: item = {'error':'Какие-то траблы,чувааак!!'}
            return JsonResponse(item,safe=False)
        else: return HttpResponse(status=404)
    else: return HttpResponse(status=404)






class CreateSalesToCustomer(LoginRequiredMixin, View):

    context = {
        'person_create': PersonCreate(),
        'exchange_rates': ExchangeRatesForm(),
    }

    def get(self,request):
        return render(request,'srvbd/create_sales_to_customer.html',self.context)

    def post(self,request):
        data = request.POST
        data_exchange_rates = ExchangeRatesForm(data)
        person = PersonCreate(data)
        if data_exchange_rates.is_valid():
            bar = data_exchange_rates.save()
        else:
            return render(request, 'srvbd/create_sales_to_customer.html',{'person_create': person,
                                                                          'exchange_rates': data_exchange_rates})
        if person.is_valid():
            obj = person.save()
        else:
            tell = data['tell']
            try:
                obj = Person.objects.get(tell=tell)
            except ObjectDoesNotExist:
                return render(request, 'srvbd/create_sales_to_customer.html', {'person_create': person,
                                                                          'exchange_rates': data_exchange_rates})
        foo = SalesPersonInvoice(person_attach=obj, exchange_rates=bar)
        foo.save()
        reverse_url = reverse('sales_to_customer_url',args=[foo.id])
        return redirect(reverse_url)




class SalesToCustomer(LoginRequiredMixin, View):

    def get(self,request,invoice_id):

        try:
            obj = SalesPersonInvoice.objects.get(pk=invoice_id)
        except ObjectDoesNotExist:
            return HttpResponse(status=404)
        if obj.status:
            return HttpResponse(status=404)
        if request.is_ajax():
            obj = MaterialSaleObject.objects.filter(person_invoice_attach=invoice_id).values(
                'detail_attach__detail_name__name', 'detail_attach__detail_name__part_num',
                'detail_attach__detail_name__specification',
                'quantity', 'detail_attach__incoming_price','sale_price', 'id',)
            if obj.exists():
                return JsonResponse(list(obj),safe=False)
            else: return HttpResponse(status=200)
        else:
            context = {
                'invoice_id': invoice_id,
                'person': obj.person_attach,
                'specification_filter': IncomInfoShipper(),
                'detail_filter': FilterDetail(),
                'payment_state':obj.payment_state
            }
            return render(request,'srvbd/sales_to_customer.html',context)


    def post(self,request,invoice_id):
        #import pdb
        #pdb.set_trace()
        if request.is_ajax():
            person_invoice = SalesPersonInvoice.objects.filter(id=invoice_id)
            if person_invoice[0].status:
                return JsonResponse({'error_status': 'Этот ордер уже сохранен, редактирование его запрещненно!'})
            else:
                obj = MaterialSaleObject.objects.filter(person_invoice_attach=invoice_id).select_related(
                    'detail_attach')
                #with transaction.atomic():
                    #obj.update(detail_attach__quantity=F('detail_attach__quantity')-F('quantity'))
                obj.filter(quantity=0).delete()
                for item in obj:
                    #invc = item.quantity * item.sale_price
                    item.detail_attach.quantity = item.detail_attach.quantity - item.quantity
                    if item.detail_attach.quantity < 0 :
                        return JsonResponse({'quant_val_error': item.id})
                    if item.detail_attach.quantity == 0:
                        item.detail_attach.status_delete = True
                    item.detail_attach.save()

                if obj:
                    sum_invoice = MaterialSaleObject.objects.filter(person_invoice_attach=invoice_id).aggregate(
                        sum_sales=Sum(F('quantity') * F('sale_price')))
                    payment_status = request.POST.get('payment_status')
                    if payment_status:
                        if payment_status == 'true':
                            payment_status = True
                        elif payment_status == 'false':
                            payment_status = False
                        else: return HttpResponse(status=400)
                    else:
                        return HttpResponse(status=403)
                    sum_inv = round(sum_invoice['sum_sales'],2)
                    person_invoice.update(status=True,invoice_sum=sum_inv,payment_state=payment_status)
                    response = reverse('sales_invoice_url',args=[invoice_id])
                    return JsonResponse({'url':response})
                response = reverse('sales_invoice_url', args=[invoice_id])
                return JsonResponse({'url': response})
        else: return HttpResponse(status=404)



@login_required
def sales_to_customer_filter(request):
    if request.method=='GET' and request.is_ajax():
        data = request.GET
        incom_info_chiper = IncomInfoShipper(data)
        incom_info_chiper.is_valid()
        filter_detail =  FilterDetail(data)
        filter_detail.is_valid()
        incom_info_chiper = incom_info_chiper.cleaned_data
        filter_detail = filter_detail.cleaned_data

        def mixin_add_prefix_search_by_attachment_field(**kwargs):
            # Добавляет необходимы префиксы для фильтра в модели Detail, по полям Производителябтипа техникуи тиа запчасти
            new_valid_data = kwargs.copy()
            for key in kwargs:
                if new_valid_data[key] == '':
                    new_valid_data.pop(key)
                else:
                    result = new_valid_data.pop(key)
                    if key == 'attachment_appliances':
                        a = '__type_appliances'
                    elif key == 'attachment_part':
                        a = '__type_spar_part'
                    elif key == 'attachment_manufacturer':
                        a = '__manufacturer'

                    new_valid_data.update({'detail_name__'+key+a :result})

            return new_valid_data

        def mixin_add_prefix_search_by_specification(**kwargs):
            new_valid_data = kwargs.copy()
            for key in kwargs:
                if new_valid_data[key] == '':
                    new_valid_data.pop(key)
                else:
                    result = new_valid_data.pop(key)
                    new_valid_data.update({('detail_name__'+key+'__icontains'): result})

            return new_valid_data

        valid_data = {**(mixin_add_prefix_search_by_specification(**filter_detail)),
                      **(mixin_add_prefix_search_by_attachment_field(**incom_info_chiper))
                      }
        obj = Detail.objects.filter(**valid_data,status_delete=False)[:50].annotate(
            date_and_exch=Concat('attach_for_incoming__incoming_date', V(' '),
                                 'attach_for_incoming__exchange_rates__exchange_rates', V('$'),
                                 output_field=CharField())).values(
            'id', 'detail_name__id', 'detail_name__name', 'detail_name__part_num', 'detail_name__specification',
            'detail_name__attachment_part__type_spar_part', 'detail_name__attachment_appliances__type_appliances',
            'detail_name__attachment_manufacturer__manufacturer', 'quantity', 'date_and_exch', 'incoming_price',
            'attach_for_incoming__id')

        Template = namedtuple(
            'Detai_in_stock', 'id detail_name__id detail_name__name detail_name__part_num detail_name__specification '
                              'detail_name__attachment_part__type_spar_part '
                              'detail_name__attachment_appliances__type_appliances '
                              'detail_name__attachment_manufacturer__manufacturer'
                              ' date_and_exch quantity incoming_price  attach_for_incoming__id')
        new_obj = [Template(**i)._asdict() for i in obj]
        return JsonResponse(new_obj, safe=False)
    return HttpResponse(status=404)


@login_required
def sales_to_customer_add_detail(request,invoice_id):

    if request.method == 'POST' and request.is_ajax():
        data = request.POST['value']
        if MaterialSaleObject.objects.filter(detail_attach_id=int(data),person_invoice_attach_id=invoice_id).exists():
            return JsonResponse({'error':'Эта запчасть уже есть в списке!'},safe=False)
        if not SalesPersonInvoice.objects.filter(id=invoice_id).exists():
            return HttpResponse(status=404)
        foo = SalesPersonInvoice.objects.filter(id=invoice_id).values(
            'exchange_rates__exchange_rates','person_attach__discount')
        exchangee_rates = float(foo[0]['exchange_rates__exchange_rates'])
        discount = float(foo[0]['person_attach__discount'])
        discount = discount / 100
        markup = Markup.objects.last()
        markup = float(markup.markup)
        detail_info = Detail.objects.filter(id=int(data)).values('incoming_price',
                                                                      'attach_for_incoming__exchange_rates__exchange_rates')
        detail_info = detail_info[0]
        incoming_price = detail_info['incoming_price']
        incoming_exchange_rates = detail_info['attach_for_incoming__exchange_rates__exchange_rates']
        val = (incoming_price / incoming_exchange_rates) * exchangee_rates
        if val < incoming_price:
            val = incoming_price
        # место для наценки
        val =  (val * markup)
        val = val - val*discount
        val = round(val,0)
        obj = MaterialSaleObject.objects.create(detail_attach_id=int(data), person_invoice_attach_id=invoice_id,sale_price=val)
        obj = MaterialSaleObject.objects.filter(id = obj.id).values(
                'detail_attach__detail_name__name', 'detail_attach__detail_name__part_num',
                'detail_attach__detail_name__specification',
                'quantity', 'detail_attach__incoming_price','sale_price', 'id',
            )
        return JsonResponse(list(obj),safe=False)

    else:return HttpResponse(status=404)


@login_required
def sales_to_customer_delete_detail(request):
    if request.method == 'POST' and request.is_ajax():
        data = int(request.POST['delete_obj'])
        try:
            MaterialSaleObject.objects.get(id=data).delete()
        except ObjectDoesNotExist:
            return HttpResponse(status=403)
        return HttpResponse(status=200)
    else:return HttpResponse(status=403)


@login_required
def sales_to_customer_change_quant_price(request):

    def tools_validate_quant_price(data):
        #Валидация полей quantity and price
        if data == '': return {'error':'Значение не должно быть пустым'}
        if '-' in data: return {'error':'Значение не должно быть отрицательным'}
        result = re.findall(r'\.',data)
        if len(result) >= 1:
            result = re.split(r'\.', data)
            if len(result[0]) > 4 or len(result[1]) > 2:
                return {'error': 'Макс длинна целого 4, дробного 2'}
        elif not len(result):
            if len(data) > 4: return {'error': 'Макс длинна целого числа 4, дробного 2'}
        else:
            return {'error':'"." должна быть одна'}

        return data


    if request.method == "POST" and request.is_ajax():
        data = request.POST
        obj = data['new_val']
        pk = data['id']
        new_val = tools_validate_quant_price(obj)

        if 'error' in new_val:
            return JsonResponse(new_val,safe=False)

        if data['field'] == 'sale_price':
            val = materialSaleObject_check_actual_salePrice(pk,new_val)
            if not val:
                foo = MaterialSaleObject.objects.filter(id=pk).update(sale_price=new_val)
                if foo: return HttpResponse(status=200)
                else: return HttpResponse(status=403)
            else:
                return val

        elif data['field'] == 'quantity':
            #import pdb
            #pdb.set_trace()
            res = materialSaleObject_check_actual_quantity(pk,new_val)
            if not res:
                foo = MaterialSaleObject.objects.filter(id=pk).update(quantity=new_val)
                if foo:return HttpResponse(status=200)
                else:return HttpResponse(status=403)
            else: return res
        return HttpResponse(status=403)

class Sales_to_customer_list(LoginRequiredMixin, View):
    def get(self,request):
        #import pdb
        #pdb.set_trace()
        if request.is_ajax():
            quer = SalesPersonInvoice.objects.all().annotate(
                full_name=Concat('person_attach__last_name',V(' '),'person_attach__first_name',V(' '),
                                 'person_attach__patronymic_name')).values(
                'id', 'full_name','date_create', 'status', 'payment_state','date_of_payment','invoice_sum').order_by('-id')
            obj = Paginator(quer,25)
            if request.GET.get('page'):
                try:
                    obj = obj.page(request.GET['page'])
                except InvalidPage:
                    return HttpResponse(status=404)
            else: obj.get_page(1)
            #print(request.GET['page'])
            if obj:
                for i in obj:
                    try:
                        i['date_create'] = i['date_create'].strftime("%d.%m.%Y %H:%M")
                        if i['date_of_payment']:
                            i['date_of_payment'] = i['date_of_payment'].strftime("%d.%m.%Y %H:%M")
                    except KeyError:
                        continue
            Template = namedtuple('Sale_to_customer_list','id full_name date_create status payment_state date_of_payment invoice_sum')
            new_obj = [ Template(**i) for i in obj]
            return JsonResponse(new_obj,safe=False)

        else:
            return render(request,'srvbd/sales_to_customer_list.html')


@login_required
def sales_to_customer_list_change_payment_state(request):
    if request.POST:
        data = request.POST
        pk = data.get('id')
        val = data.get('status')
        if val == 'true':
            val = True
        else: val = False
        try:
            obj = SalesPersonInvoice.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return HttpResponse(status=404)
        obj.payment_state = val
        data = django.utils.timezone.now()
        obj.date_of_payment = data
        obj.save()
        return HttpResponse(status=200)



class Sales_invoice(LoginRequiredMixin,View):
    def get(self,request,sales_invoice):
        obj = SalesPersonInvoice.objects.filter(id=sales_invoice).values(
            'person_attach__last_name','person_attach__first_name','person_attach__patronymic_name','person_attach__tell',
            'exchange_rates__exchange_rates','status','payment_state','invoice_sum')
        details = MaterialSaleObject.objects.filter(person_invoice_attach=sales_invoice).annotate(
            sum=F('sale_price')*F('quantity')).values('sum','detail_attach__detail_name__name','detail_attach__detail_name__part_num',
                                                     'detail_attach__detail_name__specification','detail_attach__detail_name__id',
                                                     'quantity','sale_price')
        #import pdb
        #pdb.set_trace()
        return render(request,'srvbd/sales_invoice.html',{'person_data':obj,'details':details})


class PartsReturn(LoginRequiredMixin, View):

    def get(self,request,invoice_id):
        if SalesPersonInvoice.objects.filter(id=invoice_id, status=True).exists():
            obj = SalesPersonInvoice.objects.filter(id=invoice_id).values(
                'person_attach__last_name', 'person_attach__first_name', 'person_attach__patronymic_name',
                'person_attach__tell','exchange_rates__exchange_rates', 'date_create', 'payment_state',
                'invoice_sum')
            if obj[0]['date_create']:
                obj[0]['date_create'] = obj[0]['date_create'].strftime("%d.%m.%Y %H:%M")
            parts = MaterialSaleObject.objects.filter(person_invoice_attach=invoice_id).values(
                'id','detail_attach__detail_name__id','detail_attach__detail_name__name',
                'detail_attach__detail_name__part_num','detail_attach__detail_name__specification',
                'quantity','sale_price')
            return render(request,'srvbd/parts_return.html',{'inv_id':invoice_id,'person_data': obj,'parts':parts})
        else: return HttpResponse(status=404)

    def post(self,request,invoice_id):
        if request.is_ajax():
            data = request.POST.get('data')
            if data:
                data = json.loads(data)
                for el in data:
                    pk = el.get('id')
                    value = float(el.get('value'))
                    obj = MaterialSaleObject.objects.filter(pk=pk,person_invoice_attach=invoice_id).values(
                        'quantity','detail_attach__quantity')
                    if obj.exists():
                        mat_quantity = obj[0]['quantity']
                        det_quantity = obj[0]['detail_attach__quantity']
                        quantity_update = mat_quantity - value
                        if quantity_update < 0:
                            continue
                        new_det_quantity = det_quantity + value
                        MaterialSaleObject.objects.filter(pk=pk).update(quantity=quantity_update)
                        Detail.objects.filter(material_sale = pk).update(
                            quantity = new_det_quantity,status_delete = False)
                    else: continue
                person_invoice = SalesPersonInvoice.objects.filter(id=invoice_id)
                sum_invoice = MaterialSaleObject.objects.filter(person_invoice_attach=invoice_id).aggregate(
                    sum_sales=Sum(F('quantity') * F('sale_price')))
                sum_inv = round(sum_invoice['sum_sales'], 2)
                person_invoice.update(status=True, invoice_sum=sum_inv,)
                url = reverse('sales_invoice_url', args=[invoice_id])
                return JsonResponse({'data':url},safe=False)
            return HttpResponse(status=404)
        else: return HttpResponse(status=404)

@login_required
def ajax_return_parts_del_part(request):
    if request.method == 'POST':
        pass


@login_required
def tools_ajax_exchange_rates_usd_privat24(request):
    if request.method == 'GET' and request.is_ajax():
        result = tools_get_exchange_rates_USD_privat24()
        if result:
            #ExchangeRates.objects.create(exchange_rates=result)
            result = {'exchange_rates': result}
            #print(result)
            return JsonResponse(result,safe=False)
        else: return HttpResponse(status=200)
    else: return HttpResponse(status=403)


@login_required
def telegram_bot(request):
    token = '582672380:AAHxkZmTD6HvoOaOCoAZY7kq66Mz3Xw3qVI'
    url = 'https://api.telegram.org/bot{}/'.format(token)

    # команды
    command_get = 'getMe'
    command_updates = 'getUpdates'
    command_sendmes = 'sendMessage'
    command_set_webhook = 'setWebhook?url=https://127.0.0.1/telegram_hook/'

    def send_message(chat_id,data):
        url_r = url+command_sendmes
        message = {'chat_id':chat_id,'text':data}
        r = requests.post(url_r,message)
        print(r.json())


    def send_update():
        request_url = url + command_updates
        r = requests.get(request_url)
        print(r.text)
        resp = r.json()
        chat_id = resp['result'][-1]['message']['chat']['id']
        message = resp['result'][-1]['message']['text']
        return {'chat_id':chat_id,'message':message}

    if request.method == 'POST':
        ansver = request.POST['ansver']

        a = send_update()

        context = a['message']
        chat_id = a['chat_id']
        send_message(chat_id,ansver)

    return render(request, 'srvbd/index.html',{'context':context})

@login_required
def telegram_hook(request):
    if request.method == 'POST':
        print(request.POST)
        #import pdb;
        #pdb.set_trace()












































