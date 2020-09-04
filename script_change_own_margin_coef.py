from srvbd.models import *

obj = MaterialSaleObject.objects.values(
        'pk', 'person_invoice_attach__exchange_rates__exchange_rates','person_invoice_attach__person_attach__discount',
        'sale_price', 'detail_attach__attach_for_incoming__exchange_rates__exchange_rates',
        'detail_attach__incoming_price')
for item in obj:
    pk = item['pk']
    person_discount = float(item['person_invoice_attach__person_attach__discount'])
    incoming_exchange_rates = float(item['detail_attach__attach_for_incoming__exchange_rates__exchange_rates'])
    incoming_price = float(item['detail_attach__incoming_price'])
    sale_price = float(item['sale_price'])
    sales_exchange_rates = float(item['person_invoice_attach__exchange_rates__exchange_rates'])
    # Нориализация курса
    try:
        incoming_price_normal = (incoming_price / incoming_exchange_rates) * sales_exchange_rates
        # Вычисление коэфициента
        margin_coefficient = sale_price / (incoming_price_normal - incoming_price_normal * (person_discount / 100))
        margin_coefficient = round(margin_coefficient, 2)
        MaterialSaleObject.objects.filter(pk=pk).update(own_margin=margin_coefficient)
    except ZeroDivisionError:
        continue
