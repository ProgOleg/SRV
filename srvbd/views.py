
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.template import loader
from .models import *
from .forms import *
from django.views.generic import View
import copy
from copy import deepcopy
import re
from decimal import Decimal
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, date, time

def index(request):
    return render(request, 'srvbd/index.html')



def person_list(request):

    person_last_add = Person.objects.order_by('-pub_date')[:20]
    template = loader.get_template('srvbd/person_list.html')
    context = {'person_last_add': person_last_add}
    return HttpResponse(template.render(context,request))


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


def spare_parts_manual(request):
    if request.method == 'GET':
        parts_manual_list = SparPart.objects.order_by('-id')[:100]
        context = {
        'manual': parts_manual_list,
        }

    return render(request, 'srvbd/spare_parts_manual.html',context)



def shipper_create(request):
    if request.method == "GET":
        return render(request,'srvbd/shipper_create.html',{'ship_create':ShipperCreate()})
    if request.method == "POST":
        data = ShipperCreate(request.POST)
        if data.is_valid():
            new_data = data.save()
            return render(request, 'srvbd/shipper_create.html', {'ship_create': ShipperCreate()})
        else: return render(request,'srvbd/shipper_create.html',{'ship_create':ShipperCreate(request.POST)})


def shippers_list(request):
    ship_list = Shipper.objects.order_by('-id')[:100]
    return render(request, 'srvbd/shippers_list.html',{'ship_list': ship_list})



class IncomingList(View):

    def get(self,request):
        all_incom = Incoming.objects.all()
        return render(request,'srvbd/incom_list.html', {'all_incoming':all_incom})


class IncomingListDetail(View):

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





class DetailInStockView(View):
    all_detail = Detail.objects.all()

    context = {
        'detail': all_detail,
    }

    def get(self,request):
        return render(request, 'srvbd/detail_in_stock.html', self.context)




class CreateIncoming(View):

    context = {
        'incming_stat_false': Incoming.objects.filter(status = False),
        'create_incom': CreateIncom(),
    }

    def get(self,request):
        return render(request,'srvbd/create_incoming.html',self.context)

    def post(self,request):
        data = request.POST
        if 'edit' in data:
            incom_id = int(data.get('edit'))
            return redirect('/create_incoming/{}/'.format(incom_id))

        data = CreateIncom(request.POST)
        if data.is_valid():
            new_data = data.save()
            return redirect('/create_incoming/{}/'.format(new_data.id))





class EditIncoming(View):
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
                quantity=item.quantity,attash_for_incoming_id=incom_id)
        return redirect('/incoming_list/get_{}/'.format(incom_id))




def tools_ajax_create_incom_filter(request):
    if request.method=='GET':
        data = IncomInfoShipper(request.GET)
        if data.is_valid():
            valid_data = data.cleaned_data
            filter_data = None

            if 'select_type_sparpart' in valid_data and valid_data['select_type_sparpart']:
                val = valid_data['select_type_sparpart']
                if filter_data:
                    filter_data = filter_data.filter(
                        attachment_part__type_spar_part=val)
                else:
                    filter_data = SparPart.objects.filter(
                        attachment_part__type_spar_part=val)

            if 'select_applience'in valid_data and valid_data['select_applience']:
                val = valid_data['select_applience']
                if filter_data:
                    filter_data = filter_data.filter(
                        attachment_appliances__type_appliances=val)
                else:
                    filter_data = SparPart.objects.filter(
                        attachment_appliances__type_appliances=val)

            if 'select_manufacturer' in valid_data and valid_data['select_manufacturer']:
                val = valid_data['select_manufacturer']
                if filter_data:
                    filter_data = filter_data.filter(
                        attachment_manufacturer__manufacturer=val)
                else:
                    filter_data = SparPart.objects.filter(
                        attachment_manufacturer__manufacturer=val)

            new_data = list(filter_data.values('id', 'name', 'part_num', 'specification', 'attachment_part__type_spar_part',
                                           'attachment_appliances__type_appliances','attachment_manufacturer__manufacturer'))
            return JsonResponse(new_data,safe=False)



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




class AddDevice(View):

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





def tools_ajax_add_part_set_list(request):
    if request.is_ajax():
        if request.method == 'GET':
            data = request.GET
            print(data)
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






class CreateSalesToCustomer(View):

    def get(self,request):
        context = {
            'person_create':PersonCreate(),
        }
        return render(request,'srvbd/create_sales_to_customer.html',context)

    def post(self,request):

        data = request.POST
        person = PersonCreate(data)
        if person.is_valid():
            obj = person.save()
            foo = SalesPersonInvoice(person_attach=obj)
            foo.save()
            return redirect('/sales_to_customer/{}/'.format(foo.id))
        else:

            tell = data['tell']
            try:
                obj = Person.objects.get(tell=tell)
            except ObjectDoesNotExist:
                return render(request, 'srvbd/create_sales_to_customer.html', {'person_create':PersonCreate(data)})
            foo = SalesPersonInvoice(person_attach=obj)
            foo.save()
            return redirect('/sales_to_customer/{}/'.format(foo.id))






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


class SalesToCustomer(View):

    def get(self,request,invoice_id):
        try:
            obj = SalesPersonInvoice.objects.get(pk=invoice_id)
        except ObjectDoesNotExist:
            return HttpResponse(status=404)
        context = {
            'person': obj.person_attach,
            'specification_filter': IncomInfoShipper(),
            'detail_filter': FilterDetail(),
        }
        return render(request,'srvbd/sales_to_customer.html',context)
























def get_exchange_rates_privat24(request):
    if request.method == 'GET':
        date_now = datetime.now().date().strftime('%d.%m.%Y')
        url = 'https://api.privatbank.ua/p24api/exchange_rates?json&date={}'.format(date_now)









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
            value_choice_appliances = filter_value.cleaned_data['select_applience']
            value_choice_type_sparpart = filter_value.cleaned_data['select_type_sparpart']
            value_choice_manufacturer = filter_value.cleaned_data['select_manufacturer']
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
                obj.attash_for_incoming = val.get('price')
            elif 'quant' in val:
                obj.quantity = val.get('quant')
            elif 'price' in val:
                obj.attash_for_incoming = val.get('price')
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
                quantity=item.quantity,attash_for_incoming_id=self.incom_pk)
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











































