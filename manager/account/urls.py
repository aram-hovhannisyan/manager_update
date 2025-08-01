from django.urls import path
from account import views
from tables.views import (
    save_table_data,
    Paymant_View,
    sendOrder,
    writing_save,
    writing_table,
    writing_big_tables
    )

from .calendar import non_working_days_view

from tables.messages import (
    create_announcement_view,
    recent_messages,
    update_message,
    delete_message,
    see_messages,
    confirm_message
    )

from storage.views import (
    edit_elements,
    register_elements, 
    confirm_tmp_val
)

urlpatterns = [
    path('', views.login_view, name='login_view'),
    path('login/', views.login_view, name='login_view'),
    # path('register/', views.register, name='register'),

    path('adminpage/', views.admin, name='adminpage'),

    path('customer/', views.customer, name='customer'),
    path('ohan/', views.ohan, name='ohan'),
    path('kamo/', views.kamo, name="kamo"),

    path('ohan/saveohanstable/', views.ohanSave, name="ohanSave"),
    path('kamo/savekamostable/', views.kamoSave, name="kamoSave"),


    path('ohan/tables/', views.ohanTables, name="ohanTables"),
    path('kamo/tables/', views.kamoTables, name="kamoTables"),

    path('customers/ohanstbles/', views.tables_by_ohan, name='tablesbyohan'),
    path('customers/kamostbles/', views.tables_by_kamo, name='tablesbykamo'),

    path('employee/', views.employee, name='employee'),
    path('logout/', views.logout_view, name='logout'),
    path('customer/save-table-data/', save_table_data, name='saveTableData'),
    path('delete_item/<int:item_id>/', views.delete_item, name='delete_item'),
    path('delete_item_all/<int:item_id>/', views.delete_item_all, name='delete_item_all'),
    path('delete_item_byuser/<int:item_id>/', views.delete_item_byuser, name='delete_item_byuser'),
    path('changeitemsname/', views.cahngeItemsName, name="changeItemsName"),

    path('resetEndorse/<int:item_id>/', views.resetRejectOrEndorse, name='resetRejectOrEndorse'),

    path('edit_item/<int:item_id>/', views.edit_item, name='edit_item'),
    path('customers/', views.allCustomers, name="customers"),
    path('customers/<int:user_id>/', views.customerTables, name='customertables'),
    path('tablesbycustomer/', views.tablesByUser, name= 'tablesbyuser'),

    path('mistake/<int:table_id>/', views.mistakes, name='mistake'),
    path('changes/', views.change, name="changes"),

    path('deletechanges/<int:item_id>/', views.delChange, name="deleteChange"),

    path('endorse/<int:user_id>/', views.endorse, name='endorse'),
    path('endorsechanges/<int:item_id>/', views.endorseChange, name='endorseChange'),

    path('otherItems/', views.otherItems, name='otherItems'),
    path('mainItems/', views.mainItems, name='mainItems'),

    path('customersforAdmin/', views.allCustomersforAdmin, name='customersforadmin'),

    path('customerproducts/<int:user_id>/', views.customersProducts, name = 'customersproducts'),
    path('productsforall/', views.productsForAll, name = 'productsforall'),

    path('paymant/', Paymant_View, name = 'paymant'),
    # path('return/', Return, name = 'return'),

    # path('debt/<int:user_id>/', views.customerDebt, name = 'customersDebt'),

    path('supplier/', views.supplier, name="supplier"),
    path('supplier/orderedProducts/', views.orderedProducts, name="orderedProducts"),


    # path('toggle-seen/<int:debt_id>/', views.toggle_seen, name='toggle_seen'),
    path('employee/sendorder/', sendOrder, name="sendOrderE"),
    path('mainItems/sendorder/', sendOrder, name="sendOrderM"),
    path('otherItems/sendorder/', sendOrder, name="sendOrderO"),

    path('myorders/<int:supplier_id>/', views.myOrders, name="myorders"),
    # path('sendsalary/', views.sendSalary, name='sendSalary'),
    # path('salaries/', views.salaries, name='salaries')
    path('totalPage/', views.totalPage, name='totalPage'),

    path('debts_by_date/<str:date>/', views.debts_by_date, name='debts_by_date'),
    path('supplier_endorse/<int:user_id>/', views.endorse_supplier, name='supplier_endorse'),

    path('endorse_suppliers_mistake/<int:item_id>/', views.endorse_suppliers_mistake, name='endorse_suppliers_mistake'),
    path('reject_suppliers_mistake/<int:item_id>/', views.reject_suppliers_mistake, name='reject_suppliers_mistake'),


    path('endorse_sup_Change/<int:item_id>/', views.endorse_sup_Change, name='endorse_sup_Change'),
    path('delete_sup_Change/<int:item_id>/', views.delete_sup_Change, name='delete_sup_Change'),
    path('api/main_items/', views.main_items_api, name='main_items_api'),
    path('api/other_items/', views.other_items_api, name='other_items_api'),
    path('api/get_ordereed_tables/<int:supplier_id>/<int:page_number>/', views.ordered_tables_api, name='ordered_tables_api'),


    path('customer/writing_table/', writing_table, name='writing_table'),
    path('customer/writing_table/writing_save/', writing_save, name='writing_save'),
    path('writing/', writing_big_tables, name='writing_big'),
    path('api/writing_items/', views.writing_items_api, name='writing_items_api'),
    path('writing/sendorder/', sendOrder, name="sendOrderW"),


    path("customer/gavar", views.gavar_dproc_cucak, name="gavari_dprocn"),
    path("employee/gavar/<int:user_id>/", views.gavar_cucak, name="cucak_gavar"),

    path("is_available/", views.is_available, name="is_available"),
    path("togle_availability/<str:item_name>", views.toggle_availability, name="togle_availability"),

    path("create_mesasge/", create_announcement_view, name="create_mesasge"),
    path('recent-messages/', recent_messages, name='recent_messages'),
    path('update-message/<int:message_id>/', update_message, name='update_message'),
    path('delete-message/<int:message_id>/', delete_message, name='delete_message'),
    path('see_messages/<int:user_id>/', see_messages, name='see_messages'),
    path('confirm_message/<int:message_id>/', confirm_message, name='confirm_message'),

    path('storage/reg', register_elements, name="storage_reg"),
    path('storage/edit_element/<int:element_id>/', edit_elements, name="edit_element"),
    path('storage/confirm_tmp_val/<int:tmp_el_id>/', confirm_tmp_val, name="confirm_tmp_val"),

    path('calendar/', non_working_days_view, name='calendar'),

]
