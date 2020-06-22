from django.db import models
from django.utils import timezone
from django.db.models.functions import Concat
from django.db.models import Value as V
from django.db.models import Sum


class Person(models.Model):
    MASTER = 'MA'
    CLIENT = 'CL'

    PERSON_ROLE = [
        (MASTER,'Мастер'),
        (CLIENT,'Клиент')
    ]

    first_name = models.CharField("Имя", max_length=30)
    last_name = models.CharField("Фамилия",max_length=30)
    patronymic_name = models.CharField("Отчество",max_length=30)
    tell = models.CharField("Телефонный номер",max_length=13,unique = True)
    addres = models.CharField("Адресс",max_length=200,blank=True)
    email = models.EmailField("Почта",max_length=254,blank=True)
    pub_date = models.DateTimeField(auto_now_add = True)
    discount = models.FloatField(default=0,null=True)
    role = models.CharField(max_length=2,choices=PERSON_ROLE,default=CLIENT)


    def __str__(self):
        return "{} {}.{}, {}".format(self.last_name, self.first_name[0],self.patronymic_name[0],self.role)

    @property
    def fulll_name(self):
        "Returns the person's full name."
        return '{} {}.{}'.format(self.last_name,self.first_name[0],self.patronymic_name[0])


class Markup(models.Model):

    markup = models.FloatField(default=2)

#***_Запчасти справочник_***

class SparPart(models.Model):
    name = models.CharField("Наименование",max_length=100)
    part_num = models.CharField("Парт номер", max_length=30, unique=True, blank=True,null=True)
    specification = models.TextField("Описание",max_length=2000,blank=True,null=True)

    attachment_part = models.ForeignKey('TypeSparPart',on_delete=models.SET_NULL,
                                    related_name='attachment_for_part',null=True)
    attachment_appliances = models.ForeignKey('TypeAppliances',on_delete=models.SET_NULL,
                                            related_name='attachment_for_appliances',null=True)
    attachment_manufacturer = models.ForeignKey('Manufacturer',on_delete=models.SET_NULL,
                                            related_name='attachment_for_manufacturer',blank=True,null=True)

    def __str__(self):
        return "{} {}".format(self.pk, self.name)




class TypeSparPart(models.Model):

    type_spar_part = models.CharField("Тип запчасти", max_length=50, unique=True)


    def __str__(self):
        return str(self.type_spar_part)




class TypeAppliances(models.Model):

    type_appliances = models.CharField("Вид техники", max_length=50, unique=True)


    def __str__(self):
        return str(self.type_appliances)



class Manufacturer(models.Model):

    manufacturer = models.CharField("Производитель",max_length=20,unique = True)


    def __str__(self):
        return str(self.manufacturer)
 

#***__Приходы зачастей__***

class Incoming(models.Model):
    CURRENCY_CHOICES = [('UAH','UAH'),('EUR','EUR')]

    incoming_date = models.DateField()
    ship = models.ForeignKey('Shipper',null=True,on_delete=models.SET_NULL,
                             related_name='attash_incoming_list')
    exchange_rates = models.ForeignKey('ExchangeRates', on_delete=models.SET_NULL, null=True, default=None,
                                        related_name='incoming_exchange_rates')

    status = models.BooleanField(default=False)
    currency = models.CharField(max_length=3,choices=CURRENCY_CHOICES,default='UAH  ')

    def __str__(self):
        return "{} {}".format(self.incoming_date,self.ship)


#***__Поставщик__***

class Shipper(models.Model):
    first_name = models.CharField("Имя", max_length=30)
    last_name = models.CharField("Фамилия", max_length=30)
    patronymic_name = models.CharField("Отчество", max_length=30)
    store_website = models.CharField('Сайт магазина',max_length=100,null=True,default=None)
    specification = models.CharField("Описание",max_length=50,blank=True,unique=True)


    def __str__(self):
        return "{}... {} {}.{}".format(self.specification[:20] , self.last_name,self.first_name[0],self.patronymic_name[0])


#***__Промежуточная таблица(используется только при добавлении в приход,и хранится как зч в приходе***

class DetailInIncomList(models.Model):
    spar_part = models.ForeignKey('SparPart', on_delete=models.SET_NULL, related_name='detail_detail_in_list',null=True)
    selector_incom = models.ForeignKey('Incoming', on_delete=models.SET_NULL, related_name='select_incom',null=True)
    incoming_price = models.FloatField(default=0, null=True)
    quantity = models.FloatField(default=0, null=True)


    def __str__(self):
        return "{} {}".format(self.spar_part, self.incoming_price)


#***__Модель_запчастей_на складе__***

class Detail(models.Model):
    detail_name = models.ForeignKey('SparPart', on_delete=models.SET_NULL, related_name='detail_in_detail',null=True)
    incoming_price = models.FloatField(default=0,null=True)
    quantity = models.FloatField(default=0,null=True)
    attach_for_incoming = models.ForeignKey('Incoming',on_delete=models.SET_NULL,related_name='attash_incom',null=True)
    status_delete = models.BooleanField(default=False)

    def __str__(self):
        return "{} {}".format(self.detail_name, self.incoming_price)


#***__Приходный ордер изделия в ремонт__***

class DeviceUnderRepair(models.Model):
    outside_srv = 'OU'
    inside_srv = "IN"
    choices_of_type_repair = ((outside_srv,'выездная'),(inside_srv,'в сервисе'))

    type_of_repair = models.CharField(max_length=2,choices=choices_of_type_repair,default=inside_srv)
    external_condition = models.CharField("Внешнее стостояние",max_length=500)
    date_create = models.DateTimeField(auto_now_add=True)
    date_ready = models.DateTimeField()
    date_delivery = models.DateTimeField()
    status_ready = models.BooleanField(default=False)
    status_delivery = models.BooleanField(default=False)

    device_attach = models.ForeignKey("Device",on_delete=models.SET_NULL,related_name='device_in_repair',null=True)
    person_attach = models.ForeignKey("Person",on_delete=models.SET_NULL,related_name='device_person',null=True)
    comment = models.ForeignKey("Comment", on_delete=models.SET_NULL, related_name='device_comment',blank=True,null=True)


    def __str__(self):
        return "{}".format(self.device_attach)


#***__Изделия(техника)__***

class Device(models.Model):
    manufacturer = models.ForeignKey('Manufacturer',on_delete=models.SET_NULL,related_name='device_manufacturer',null=True)
    type_appliances = models.ForeignKey('TypeAppliances',on_delete=models.SET_NULL,related_name='device_type_appliances',null=True)

    mod = models.CharField("Модель:",max_length=50,unique=True)
    serial_number = models.CharField("Серийный номер:",max_length=50,blank=True,default=None,null=True)
    pnc = models.CharField("PNC-код:",max_length=50,blank=True)


    def __str__(self):
        return "{} {} {}".format(self.type_appliances,self.mod,self.manufacturer)


#***__Коментарии к ремонтам__***

class Comment(models.Model):
    date_create = models.DateTimeField(auto_now_add=True)
    text = models.TextField("Коментарий",max_length=2000)

    def __str__(self):
        return "{} {}".format(self.date_create,(self.text)[:30])


#***__Виртуальная запчасть(не существует на складе).Объект расходного ордера!__***

class VirtualSaleObject(models.Model):
    spar_part_attach = models.ForeignKey("SparPart",on_delete=models.SET_NULL,related_name='virtual_sale',null=True)

    repair_invoice_attach = models.ForeignKey("RepairInvoice", on_delete=models.SET_NULL, related_name='virtual_repair_invoice',
                                              default=None,null=True)
    person_invoice_attach = models.ForeignKey("SalesPersonInvoice", on_delete=models.SET_NULL, related_name='virtual_person_invoice',
                                              default=None,null=True)

    quantity = models.FloatField(default=0,null=True)
    sale_price = models.FloatField(default=0,null=True)


    def __str__(self):
        return "{} {} {}".format(self.spar_part_attach,self.quantity,self.sale_price)


#***__Материально существующая  запчасть на складе).Объект расходного ордера!__***

class MaterialSaleObject(models.Model):
    detail_attach = models.ForeignKey("Detail", on_delete=models.SET_NULL, related_name='material_sale',null=True)

    repair_invoice_attach = models.ForeignKey("RepairInvoice", on_delete=models.SET_NULL, related_name='material_repair_invoice',
                                              default=None,null=True)
    person_invoice_attach = models.ForeignKey("SalesPersonInvoice", on_delete=models.SET_NULL, related_name='material_person_invoice',
                                              default=None,null=True)

    quantity = models.FloatField(default=0,null=True)
    sale_price = models.FloatField(default=0,null=True)


    def __str__(self):
        return "{} {} {}".format(self.detail_attach,self.quantity,self.sale_price)


#***__Расходный ордер продажи запчастей клиенту__***

class SalesPersonInvoice(models.Model):
    person_attach = models.ForeignKey("Person", on_delete=models.SET_NULL, related_name='detail_sale',null=True)
    exchange_rates = models.ForeignKey('ExchangeRates', on_delete=models.SET_NULL, null=True, default=None,
                                       related_name='sale_person_exchange_rates')

    invoice_sum = models.FloatField(default=0,null=True)
    date_create = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    payment_state = models.BooleanField(default=False)
    date_of_payment = models.DateTimeField(default=None,null=True)

    def __str__(self):
        return "{} {} {}".format(self.date_create,self.person_attach,self.invoice_sum)


#***__Расходная накладная запчастей использованых в ремонте__***

class RepairInvoice(models.Model):
    repair_attach = models.ForeignKey("DeviceUnderRepair", on_delete=models.SET_NULL, related_name='detail_invoice',null=True)
    exchange_rates = models.ForeignKey('ExchangeRates', on_delete=models.SET_NULL, null=True, default=None,
                                        related_name='repair_exchange_rates')

    invoice_sum = models.FloatField(default=0,null=True)
    date_create = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)


    def __str__(self):
        return "{} {} {}".format(self.repair_attach,self.date_create,self.invoice_sum)


class ExchangeRates(models.Model):

    data_create = models.DateField(auto_now_add=True)
    exchange_rates = models.FloatField(default=0,null=True)
    status_own_change = models.BooleanField(default=False)

    def __str__(self):
        return "{}, {}".format(self.exchange_rates,self.data_create)
























