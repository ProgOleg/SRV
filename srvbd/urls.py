from django.urls import path
from srvbd import views

urlpatterns = [
    path("login/", views.AuthUser.as_view(), name="auth_user"),
    path("logout/", views.LogOut.as_view(), name="logout_url"),
    path("", views.index, name="index_url"),
    # Клиенты
    path("person/", views.person_list, name="person_list"),
    path("create_person/", views.person_create, name="create_persons_url"),
    # __Справочники__
    path("add_part/", views.spar_part_add, name="add_part_url"),
    path("ajax_add_specification", views.ajax_add_specification, name="add_specification"),
    #
    path("spare_parts_manual/", views.spare_parts_manual, name="spare_parts_manual_list"),
    # Поставщики
    path("create_shipper/", views.shipper_create, name="create_shipper_url"),
    path("shippers/", views.shippers_list, name="shipper_url"),
    # Устройство
    path("add_device/", views.AddDevice.as_view(), name="add_device_url"),
    path("ajax_add_part_set_list/", views.tools_ajax_add_part_set_list, name="ajax_add_part_set_list_url"),
    #
    path("incoming_list/<int:incom_id>/", views.IncomingListDetail.as_view(), name="incom_list_detail_url"),
    path("incoming_list/", views.IncomingList.as_view(), name="incom_list_url"),
    #
    path("deteil_in_stock/", views.DetailInStockView.as_view(), name="detail_in_stock_url"),
    path(
        "ajax_detail_in_stock_filter/<int:page>/", views.ajax_detail_in_stock_filter, name="ajax_detail_in_stock_filter"
    ),
    #
    path("create_incoming/", views.CreateIncoming.as_view(), name="create_incoming_url"),
    path("create_incoming/<int:incom_id>/", views.EditIncoming.as_view(), name="edit_incoming_url"),
    path("ajax_create_incoming_filter_spart/", views.tools_ajax_create_incom_filter, name="ajax_create_incom_filter"),
    path(
        "ajax_create_incoming_detail/<int:incom_id>/",
        views.tools_ajax_create_incom_detail,
        name="ajax_create_incom_incom_detail",
    ),
    path(
        "ajax_create_incoming_change_detail/<int:incom_id>/",
        views.tools_ajax_create_incom_change_detail,
        name="ajax_create_incom_change_detail",
    ),
    path(
        "ajax_create_incoming_delete_detail/<int:incom_id>/",
        views.tools_ajax_create_incom_delete_detail,
        name="ajax_create_incom_delete_detail",
    ),
    # Продажа клиенту
    path("sales_to_customer/", views.CreateSalesToCustomer.as_view(), name="create_sales_to_customer_url"),
    path("ajax_check_tell/", views.tools_ajax_check_tell, name="ajax_check_tell_url"),
    path("sales_to_customer/<int:invoice_id>/", views.SalesToCustomer.as_view(), name="sales_to_customer_url"),
    path(
        "sales_to_customer_create/<int:s_invoice_pk>/",
        views.sales_to_customer_create,
        name="sales_to_customer_create_url",
    ),
    # Выборка по "Тип устройства(select_applience)" для рендеринка <datalist> !!!ЖЕСТКО ОДИРОВАНЫЕ УРЛЫ В ФОРМЕ!!!
    path("ajax_tools_select_applience/", views.data_list_select_appliances, name="option_select_applience"),
    path("ajax_tools_select_type_sparpart/", views.data_list_select_type_sparpart, name="option_select_type_sparpart"),
    path("ajax_tools_select_manufacturer/", views.data_list_select_manufacturer, name="option_select_manufacturer"),
    #
    path("ajax_tools_sales_to_customer_filter/", views.sales_to_customer_filter, name="ajax_sales_to_customer_filter"),
    path(
        "ajax_tools_sales_to_customer_add_detail/<int:invoice_id>/",
        views.sales_to_customer_add_detail,
        name="ajax_tools_sales_to_customer_add_detail",
    ),
    path(
        "ajax_tools_sales_to_customer_delete_detail",
        views.sales_to_customer_delete_detail,
        name="ajax_sales_to_customer_delete_detail",
    ),
    path(
        "ajax_tools_sales_to_customer_change_quant_price",
        views.sales_to_customer_change_quant_price,
        name="ajax_sales_to_customer_change_quant_price",
    ),
    path("ajax_get_own_coefficient", views.ajax_get_own_coefficient, name="ajax_get_own_coefficient_url"),
    path("ajax_calculate_coefficient", views.ajax_calculate_coefficient, name="ajax_calculate_coefficient_url"),
    # Список продажных ордеров
    path("sales_to_customer_list", views.SalesToCustomerList.as_view(), name="sales_to_customer_list_url"),
    path(
        "ajax_tools_sales_to_customer_list_change_payment_state/",
        views.sales_to_customer_list_change_payment_state,
        name="customer_list_change_payment_state",
    ),
    # Возврат запчастей
    path("parts_return/<int:invoice_id>/", views.PartsReturn.as_view(), name="parts_return_url"),
    # path("ajax_return_parts_del_part/", views.ajax_return_parts_del_part, name="ajax_url_return_parts_del_part"),
    # Продажный ордер
    path("sales_invoice/<int:sales_invoice>", views.SalesInvoice.as_view(), name="sales_invoice_url"),
    # Аналитика
    # Запчасти необходимые к заказу
    path("parts_required_to_order/", views.parts_required_to_order, name="parts_required_to_order_url"),
    # TEST
    path(
        "ajax_tools_exchange_rates_usd_privat24/",
        views.tools_ajax_exchange_rates_usd_privat24,
        name="get_usd_exchange_rates",
    ),
    path("print_receipt/<int:invoice_id>/", views.print_receipt, name="print_receipt_url"),
    path("telegram_bot/", views.telegram_bot, name="telegram_bot_url"),
    path("telegram_hook/", views.telegram_hook, name="telegram_hook_url"),
]
