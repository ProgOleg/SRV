
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.template import loader
from django.core.paginator import Paginator
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
import telepot
from django.core.paginator import *
import datetime
from collections import namedtuple
#from . import utils
from srvbd.utils import *
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse_lazy
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
            new_form = form.save()
            return redirect('/person/')
        else: return render(request, 'srvbd/person_create.html', context={'form': form})



@login_required
def spar_part_add(request):
    context = {
        'form': AddPart(),
        'form_add_attachment_part': AddTypeSparPart(),
        'form_add_attachment_appliances': AddTypeAppliances(),
        'form_add_manufacturer': AddManufacturer(),
    }

    if request.method == 'GET':
        return render(request, 'srvbd/part_add.html', context)

    elif request.method =='POST':
        if 'but_1' in request.POST:
            form = AddPart(request.POST)
            new_context = {
                'form': form,
                'form_add_attachment_part': AddTypeSparPart(),
                'form_add_attachment_appliances': AddTypeAppliances(),
                'form_add_manufacturer': AddManufacturer(),
            }
            if form.is_valid():
                new_form = form.save()
                return render(request, 'srvbd/part_add.html', context)
            else:
                return render(request, 'srvbd/part_add.html', new_context)

        if 'but_2' in request.POST:
            form = AddTypeSparPart(request.POST)
            new_context = {
                'form': AddPart(),
                'form_add_attachment_part': AddTypeSparPart(request.POST),
                'form_add_attachment_appliances': AddTypeAppliances(),
                'form_add_manufacturer': AddManufacturer(),
            }
            if form.is_valid():
                new_form = form.save()
                return render(request, 'srvbd/part_add.html', context)
            else:
                return render(request, 'srvbd/part_add.html', new_context)

        if 'but_3' in request.POST:
            form = AddTypeAppliances(request.POST)
            new_context = {
                'form': AddPart(),
                'form_add_attachment_part': AddTypeSparPart(),
                'form_add_attachment_appliances': AddTypeAppliances(request.POST),
                'form_add_manufacturer': AddManufacturer(),
            }
            if form.is_valid():
                new_form = form.save()
                return render(request, 'srvbd/part_add.html', context)
            else:
                return render(request, 'srvbd/part_add.html', new_context)

        if 'but_4' in request.POST:
            form = AddManufacturer(request.POST)
            new_context = {
                'form': AddPart(),
                'form_add_attachment_part': AddTypeSparPart(),
                'form_add_attachment_appliances': AddTypeAppliances(),
                'form_add_manufacturer': AddManufacturer(request.POST),
            }
            if form.is_valid():
                new_form = form.save()
                return render(request, 'srvbd/part_add.html', context)
            else:
                return render(request, 'srvbd/part_add.html', new_context)

    else: return HttpResponse(status=404)

@login_required
def spare_parts_manual(request):
    if request.method == 'GET':
        parts_manual_list = SparPart.objects.order_by('-id')[:100]
        context = {
        'manual': parts_manual_list,
        }

    return render(request, 'srvbd/spare_parts_manual.html',context)


@login_required
def shipper_create(request):
    if request.method == "GET":
        return render(request,'srvbd/shipper_create.html',{'ship_create':ShipperCreate()})
    if request.method == "POST":
        data = ShipperCreate(request.POST)
        if data.is_valid():
            new_data = data.save()
            return render(request, 'srvbd/shipper_create.html', {'ship_create': ShipperCreate()})
        else: return render(request,'srvbd/shipper_create.html',{'ship_create':ShipperCreate(request.POST)})

@login_required
def shippers_list(request):
    ship_list = Shipper.objects.order_by('-id')[:100]
    return render(request, 'srvbd/shippers_list.html',{'ship_list': ship_list})



class IncomingList(LoginRequiredMixin, View):

    def get(self,request):
        all_incom = Incoming.objects.all()
        return render(request,'srvbd/incom_list.html', {'all_incoming':all_incom})


class IncomingListDetail(LoginRequiredMixin, View):

    def get(self,request,identifier):
        if Incoming.objects.get(id=identifier):
            incom_obj = Incoming.objects.get(id=identifier)
            detail = incom_obj.select_incom.all()
            context = {
                'incom': incom_obj,
                'details': detail,
            }
            return render(request,'srvbd/incom_list_detail_get.html',context)
        else: None





class DetailInStockView(LoginRequiredMixin, View):


    def get(self,request):
        all_detail = Detail.objects.filter(status_delete=False).values(
            'detail_name__id','detail_name__name','detail_name__part_num','detail_name__specification',
            'detail_name__attachment_part__type_spar_part','detail_name__attachment_appliances__type_appliances',
            'detail_name__attachment_manufacturer__manufacturer','quantity','attach_for_incoming__incoming_date',
            'incoming_price')
        context = {'detail': all_detail}
        return render(request, 'srvbd/detail_in_stock.html', context)




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





class EditIncoming(LoginRequiredMixin, View):
    choice_appliances = TypeAppliances.objects.all()
    choice_type_sparpart = TypeSparPart.objects.all()
    choice_manufacturer = Manufacturer.objects.all()

    context = {
        'filter_spar_part': IncomInfoShipper(),
        'choice_appliances': choice_appliances,
        'choice_type_sparpart': choice_type_sparpart,
        'choice_manufacturer': choice_manufacturer,
    }

    def get (self,request,incom_id):

        if request.is_ajax():
            if DetailInIncomList.objects.filter(selector_incom_id=incom_id).first():
                data = list(DetailInIncomList.objects.filter(selector_incom_id=incom_id).values(
                    'id','spar_part__name', 'spar_part__part_num', 'spar_part__specification','quantity','incoming_price'))
                return JsonResponse(data,safe=False)
            else: return JsonResponse({'massage':''})

        else:
            self.context.update({'incom': Incoming.objects.filter(id=incom_id).first()})
            if DetailInIncomList.objects.filter(selector_incom = incom_id).first():
                self.context.update({'detail_incoming': DetailInIncomList.objects.filter(selector_incom = incom_id)})
            return render(request, 'srvbd/edit_incoming.html', self.context)

    def post(self,request,incom_id):
        Incoming.objects.filter(id=incom_id).update(status=True)
        data = DetailInIncomList.objects.filter(selector_incom_id=incom_id)
        for item in data:
            obj_spart = int(item.spar_part_id)

            Detail.objects.create(detail_name_id=obj_spart,incoming_price=item.incoming_price,
                quantity=item.quantity,attach_for_incoming_id=incom_id)
        return redirect('/incoming_list/get_{}/'.format(incom_id))



@login_required
def tools_ajax_create_incom_filter(request):
    if request.method=='GET':
        data = IncomInfoShipper(request.GET)
        if data.is_valid():
            valid_data = data.cleaned_data
            filter_data = None

            if 'attachment_part' in valid_data and valid_data['attachment_part']:
                val = valid_data['attachment_part']
                if filter_data:
                    filter_data = filter_data.filter(
                        attachment_part__type_spar_part=val)
                else:
                    filter_data = SparPart.objects.filter(
                        attachment_part__type_spar_part=val)

            if 'attachment_appliances'in valid_data and valid_data['attachment_appliances']:
                val = valid_data['attachment_appliances']
                if filter_data:
                    filter_data = filter_data.filter(
                        attachment_appliances__type_appliances=val)
                else:
                    filter_data = SparPart.objects.filter(
                        attachment_appliances__type_appliances=val)

            if 'attachment_manufacturer' in valid_data and valid_data['attachment_manufacturer']:
                val = valid_data['attachment_manufacturer']
                if filter_data:
                    filter_data = filter_data.filter(
                        attachment_manufacturer__manufacturer=val)
                else:
                    filter_data = SparPart.objects.filter(
                        attachment_manufacturer__manufacturer=val)

            new_data = list(filter_data.values('id', 'name', 'part_num', 'specification', 'attachment_part__type_spar_part',
                                           'attachment_appliances__type_appliances','attachment_manufacturer__manufacturer'))
            return JsonResponse(new_data,safe=False)


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

    def get(self,request):
        context = {
            'person_create':PersonCreate(),
            'exchange_rates':ExchangeRatesForm(),
        }
        return render(request,'srvbd/create_sales_to_customer.html',context)

    def post(self,request):
        data = request.POST
        data_exchange_rates = ExchangeRatesForm(request.POST)
        person = PersonCreate(data)
        if data_exchange_rates.is_valid():
            bar = data_exchange_rates.save()
        else: return render(request, 'srvbd/create_sales_to_customer.html', {'exchange_rates':data_exchange_rates.errors})
        if person.is_valid():
            obj = person.save()
            foo = SalesPersonInvoice(person_attach=obj,exchange_rates=bar)
            foo.save()
            return redirect('/sales_to_customer/{}/'.format(foo.id))
        else:

            tell = data['tell']
            try:
                obj = Person.objects.get(tell=tell)
            except ObjectDoesNotExist:
                return render(request, 'srvbd/create_sales_to_customer.html', {'person_create':PersonCreate(data)})
            foo = SalesPersonInvoice(person_attach=obj,exchange_rates=bar)
            foo.save()
            return redirect('/sales_to_customer/{}/'.format(foo.id))




class SalesToCustomer(LoginRequiredMixin, View):

    def get(self,request,invoice_id):
        #import pdb
        #pdb.set_trace()
        if request.is_ajax():
            obj = MaterialSaleObject.objects.filter(person_invoice_attach=invoice_id).values(
                'detail_attach__detail_name__name', 'detail_attach__detail_name__part_num',
                'detail_attach__detail_name__specification',
                'quantity', 'detail_attach__incoming_price','sale_price', 'id',)
            if obj:
                return JsonResponse(list(obj),safe=False)
            else: return HttpResponse(status=404)
        else:
            try:
                obj = SalesPersonInvoice.objects.get(pk=invoice_id)
            except ObjectDoesNotExist:
                return HttpResponse(status=404)
            context = {
                'invoice_id': invoice_id,
                'person': obj.person_attach,
                'specification_filter': IncomInfoShipper(),
                'detail_filter': FilterDetail(),
                'payment_state':obj.payment_state
            }
            return render(request,'srvbd/sales_to_customer.html',context)


    def post(self,request,invoice_id):
        import pdb
        pdb.set_trace()
        if request.is_ajax():
            obj = MaterialSaleObject.objects.filter(person_invoice_attach=invoice_id).select_related(
                'detail_attach')
            for item in obj:
                if item.quantity == 0:
                    item.delete()
                    continue
                invc = item.quantity * item.sale_price
                item.detail_attach.quantity = item.detail_attach.quantity - item.quantity
                if item.detail_attach.quantity < 0 :
                    return JsonResponse({'quant_val_error': item.id})
                if item.detail_attach.quantity == 0:
                    item.detail_attach.status_delete = True
                item.detail_attach.save()
            if obj:
                sum_invoice = MaterialSaleObject.objects.filter(person_invoice_attach=invoice_id).aggregate(
                    sum_sales=Sum(F('quantity') * F('sale_price')))
                if request.POST['payment_status']:
                    payment_status = request.POST['payment_status']
                    if payment_status == 'true':
                        payment_status = True
                    elif payment_status == 'false':
                        payment_status = False
                    else: return HttpResponse(status=403)
                else:
                    return HttpResponse(status=403)
                SalesPersonInvoice.objects.filter(id=invoice_id).update(status=True,invoice_sum=sum_invoice['sum_sales'],
                                                                        payment_state=payment_status)
                return redirect('/sales_invoice/{}'.format(invoice_id))
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
        obj = list(Detail.objects.filter(**valid_data,status_delete=False)[:50].values(
            'id','detail_name__id','detail_name__name','detail_name__part_num','detail_name__specification',
            'detail_name__attachment_part__type_spar_part','detail_name__attachment_appliances__type_appliances',
            'detail_name__attachment_manufacturer__manufacturer','attach_for_incoming__id','quantity','incoming_price',
        ))
        return JsonResponse(obj,safe=False)
    return HttpResponse(status=404)

@login_required
def sales_to_customer_add_detail(request,invoice_id):

    if request.method == 'POST' and request.is_ajax():
        data = request.POST['value']
        if MaterialSaleObject.objects.filter(detail_attach_id=int(data),person_invoice_attach_id=invoice_id).exists():
            return JsonResponse({'error':'Эта запчасть уже есть в списке!'},safe=False)
        if not SalesPersonInvoice.objects.filter(id=invoice_id).exists():
            return HttpResponse(status=404)
        exchangee_rates = SalesPersonInvoice.objects.filter(id=invoice_id).values('exchange_rates__exchange_rates')
        exchangee_rates = exchangee_rates[0]['exchange_rates__exchange_rates']
        detail_info = Detail.objects.filter(id=int(data)).values('incoming_price',
                                                                      'attach_for_incoming__exchange_rates__exchange_rates')
        detail_info = detail_info[0]
        incoming_price = detail_info['incoming_price']
        incoming_exchange_rates = detail_info['attach_for_incoming__exchange_rates__exchange_rates']
        val = (incoming_price / incoming_exchange_rates) * exchangee_rates
        print(val)
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
            val = materialSaleObject_check_actual_salePrice(pk)
            if Decimal(new_val) < val:
                return JsonResponse({'error':'Цена не меньше - "{}"'.format(val)},safe=False)
            else:
                foo = MaterialSaleObject.objects.filter(id=pk).update(sale_price=new_val)
                if foo: return HttpResponse(status=200)
                else: return HttpResponse(status=403)

        elif data['field'] == 'quantity':
            res = materialSaleObject_check_actual_quantity(pk,new_val)
            if not res:
                foo = MaterialSaleObject.objects.filter(id=pk).update(quantity=new_val)
                if foo:
                    return HttpResponse(status=200)
                else:
                    return HttpResponse(status=403)
            else:
                return JsonResponse({'error': 'Кол-во не больше фактического - "{}"'.format(res)})
    else: return HttpResponse(status=403)




class Sales_to_customer_list(LoginRequiredMixin, View):
    def get(self,request):
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
            print(request.GET['page'])
            if obj:
                for i in obj:
                    try:
                        i['date_create'] = i['date_create'].strftime("%d.%m.%Y %H:%M")
                    except KeyError:
                        continue
            Template = namedtuple('Sale_to_customer_list','id full_name date_create status payment_state date_of_payment invoice_sum')
            new_obj = [ Template(**i) for i in obj]
            return JsonResponse(new_obj,safe=False)

        else:
            return render(request,'srvbd/sales_to_customer_list.html')




class Sales_invoice(View):
    def get(self,request,sales_invoice):
        obj = SalesPersonInvoice.objects.filter(id=sales_invoice).values(
            'person_attach__last_name','person_attach__first_name','person_attach__patronymic_name','person_attach__tell',
            'exchange_rates','status','payment_state','invoice_sum')
        details = MaterialSaleObject.objects.filter(person_invoice_attach=sales_invoice).annotate(
            sum=F('sale_price')*F('quantity')).values('sum','detail_attach__detail_name__name','detail_attach__detail_name__part_num',
                                                     'detail_attach__detail_name__specification','detail_attach__detail_name__id',
                                                     'quantity','sale_price')
        #import pdb
        #pdb.set_trace()
        return render(request,'srvbd/sales_invoice.html',{'person_data':obj,'details':details})





@login_required
def tools_ajax_exchange_rates_usd_privat24(request):
    if request.method == 'GET' and request.is_ajax():
        result = tools_get_exchange_rates_USD_privat24()
        if result:
            #ExchangeRates.objects.create(exchange_rates=result)
            result = {'exchange_rates': result}
            print(result)
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
        import pdb;
        pdb.set_trace()







#import pdb; pdb.set_trace()



















"""
class BaseDetailIncom(View):
    choice_appliances = TypeAppliances.objects.all()
    choice_type_sparpart = TypeSparPart.objects.all()
    choice_manufacturer = Manufacturer.objects.all()
    all_incoming_status_false = Incoming.objects.filter(status=False)
    context = {
        'create_incom': CreateIncom(),
        'filter_spar_part': None,
        'choice_appliances': choice_appliances,
        'choice_type_sparpart': choice_type_sparpart,
        'choice_manufacturer': choice_manufacturer,
        'new_detail_in_list': None,
        'spart_view': None,
        'incom': None,
        'incming_stat_false': None,
    }
    incom_pk = None


class DetailIncoming(BaseDetailIncom):

    def get(self,request):
        if self.context['incom']:
            self.context.update({'filter_spar_part': IncomInfoShipper()})
        if self.all_incoming_status_false.count():
            self.context.update({'incming_stat_false': self.all_incoming_status_false,})

        return render(request, 'srvbd/create_incom.html', self.context)

    def post(self,request):
        filter_value = IncomInfoShipper(request.POST)
        if filter_value.is_valid():
            value_choice_appliances = filter_value.cleaned_data['attachment_appliances']
            value_choice_type_sparpart = filter_value.cleaned_data['attachment_part']
            value_choice_manufacturer = filter_value.cleaned_data['attachment_manufacturer']
        else:
            return render(request, 'srvbd/test.html', self.context)
        if value_choice_type_sparpart:
            filter_data = SparPart.objects.filter(attachment_part__type_spar_part=value_choice_type_sparpart)
        if value_choice_appliances:
            filter_data = filter_data.filter(attachment_appliances__type_appliances=value_choice_appliances)
        if value_choice_manufacturer:
            filter_data = filter_data.filter(attachment_manufacturer__manufacturer=value_choice_manufacturer)
        self.context.update({'spart_view': filter_data})
        return render(request, 'srvbd/create_incom.html', self.context)


class ToolsDetailIncoming(BaseDetailIncom):

    def post(self,request):
        if 'add_spart_obj' in request.POST:
            spar_id = int(request.POST['add_spart_obj'])
            self.incom_pk = self.context['incom'].id
            if not DetailInList.objects.filter(selector_incom_id=self.incom_pk).filter(spar_part_id=spar_id).count():
                DetailInList.objects.create(spar_part_id = spar_id,selector_incom_id = self.incom_pk)
                item = DetailInList.objects.filter(selector_incom_id = self.incom_pk)
                self.context.update({'new_detail_in_list': item})
                return render(request, 'srvbd/create_incom.html', self.context)

            else:
                #import pdb;pdb.set_trace()
                return render(request, 'srvbd/create_incom.html', self.context)



class ToolsCreateIncoming(BaseDetailIncom):

    def post(self,request):
        if not self.context['incom']:
            data = CreateIncom(request.POST)
            if data.is_valid():
                new_incom = data.save()
                self.context.update({'incom': new_incom,'create_incom': None,
                                     'filter_spar_part': IncomInfoShipper()})
                return render(request, 'srvbd/create_incom.html', self.context)

            else:
                return render(request, 'srvbd/test.html', self.context)
        else: return render(request, 'srvbd/create_incom.html', self.context)


class ToolsIncomDetailDelete(BaseDetailIncom):

    def post(self,request):
        data = request.POST
        if data['delete_obj']:
            obj_id = data['delete_obj']
            DetailInList.objects.get(id=obj_id).delete()
            self.incom_pk = self.context['incom'].id
            item = DetailInList.objects.filter(selector_incom_id=self.incom_pk)
            self.context.update({'new_detail_in_list': item})

        return render(request, 'srvbd/create_incom.html', self.context)



class ToolsIncomEditDetail(BaseDetailIncom):

    def iterate(self, **data):
        new_dict = {}
        for item in data:
            if item.startswith('quant'):
                val = data[item]
                match = re.search(r'\d+', r'{}'.format(item))
                match = match.group()
                if match in new_dict:
                    new_dict[match].update({'quant': val[0]})
                else:
                    new_dict.update({match: {'quant': val[0]}})
            elif item.startswith('price'):
                val = data[item]
                match = re.search(r'\d+', r'{}'.format(item))
                match = match.group()
                if match in new_dict:
                    new_dict[match].update({'price': val[0]})
                else:
                    new_dict.update({match: {'price': val[0]}})
        return new_dict


    def change_obj_ver1(self,**new_data):
        for item in new_data:
            val = new_data[item]
            if 'quant' and 'price' in val:
                DetailInList.objects.filter(pk=int(item)).update(
                    quantity=val.get('quant'),
                    incoming_price=val.get('price'))
            elif 'quant' in val:
                DetailInList.objects.filter(pk=int(item)).update(
                    quantity=val.get('quant'))
            elif 'price' in val:
                DetailInList.objects.filter(pk=int(item)).update(
                    incoming_price=val.get('price'))

    def change_obj_ver2(self,**new_data):
        for item in new_data:
            val = new_data[item]
            obj = DetailInList.objects.get(pk=new_data[item])
            if 'quant' and 'price' in val:
                obj.quantity = val.get('quant')
                obj.attach_for_incoming = val.get('price')
            elif 'quant' in val:
                obj.quantity = val.get('quant')
            elif 'price' in val:
                obj.attach_for_incoming = val.get('price')
            return obj

    def funk_1(self,**new_data):
            self.change_obj_ver1(**new_data)

    def funk_2(self,**new_data):
        new_obj = {}
        for item in new_data:
            i = self.change_obj_ver2(**new_data)
            new_data.update(i)
        return new_obj

    # new_obj = self.funk_2(self, new_data)
    # new_context = new_obj.save()
    # self.context.update({'new_detail_in_list': new_context})

    def post(self, request):
        import pdb;
        pdb.set_trace()
        data = request.POST
        new_data = self.iterate(**data)
        if new_data:
            self.change_obj_ver1(**new_data)
            self.incom_pk = self.context['incom'].id
            item = DetailInList.objects.filter(selector_incom_id=self.incom_pk)
            self.context.update({'new_detail_in_list': item})

        return render(request, 'srvbd/create_incom.html', self.context)


class ToolsIncomDetailSave(BaseDetailIncom):

    def post(self,request):
        self.incom_pk = self.context['incom'].id
        Incoming.objects.filter(id=self.incom_pk).update(status=True)
        data = DetailInList.objects.filter(selector_incom_id=self.incom_pk)
        for item in data:
            obj_spart = int(item.spar_part_id)

            Detail.objects.create(detail_name_id=obj_spart,incoming_price=item.incoming_price,
                quantity=item.quantity,attach_for_incoming_id=self.incom_pk)
        return redirect('/incoming_list/get_{}/'.format(self.incom_pk))



class ToolsEditIncom(BaseDetailIncom):

    def post(self,request):
        data = request.POST
        if 'edit' in data:
            val = data['edit']
            self.incom_pk = int(val)
            obj = Incoming.objects.get(id=int(val))
            item = DetailInList.objects.filter(selector_incom_id=self.incom_pk)
            self.context.update({
                'incom': obj,'create_incom':None,'filter_spar_part': IncomInfoShipper(),'new_detail_in_list': item,
            })
        return render(request, 'srvbd/create_incom.html', self.context)
"""











































