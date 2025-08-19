from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm, LoginForm, ItemAddForm
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.db.models import Q

from django.db.models import Case, When, Value, IntegerField
from tables.messages import unreaden_messages
# Create your views here.
from django.contrib.auth.decorators import login_required
from tables.models import (
    ItemsModel,
    UserTable,
    TableItem,
    BigTable,
    Debt,
    Ordered_Products_Column,
    Ordered_Products_Table,
    # Salary,
    JoinedTables,
    Paymant,
    Week_debt,
    Global_Debt,
    Old_debt,
    BigTableRows,
    SingleTable,
    WaitingForChange,
    ordered_Itmes,
    supplier_Mistakes
)
from account.models import (
    User
)
from datetime import datetime
import json

from django.core.paginator import Paginator

import datetime as d
import random
from datetime import datetime, timedelta



from django.http import HttpResponseRedirect
from django.db import models
from django.db.models import Sum
from account.mydecorators import (
    admin_required,
    customer_required,
    employee_required,
    supplier_required,
    employee_or_supplier_required
)
import time
from django.http import JsonResponse
from storage.views import update_or_create_tmp_value

from .forms import SalaryForm, ChangeItemsName

def index(request):
    return render(request, 'index.html')

schools = [
    # '148',
    '189', "50",
    # '54',
    '170', '104', '136', '171', '117', '177', '48', '60', '87',
    '90', '188', '196', '115', '44', '52','163','143','140','154','66','144','Չարբախ_1','106','35',"35_փոքր",'93', "91",
    "134", "38", "195", "94", "53","161",
    'Դավիթ','Օհան','Գ.4-րդ', 'Գ.ավագ', 'Արա','Կամո','Գանձակ', 'Սարուխան', "Հացառատ2",'Էրանոս','Լիճք', 'Մ.1ին',
    'Մ.ավագ', 'Զոլ.2րդ', 'Զոլ.1ին', 'Ծովինար',"Գավառ_ավագ","Գավառ_4րդ", "Գավառ_5րդ", "Գ_սարուխան", "Գ_հացառատ2","Գ_գանձակ",
    #'Խանութ'
    ]

def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created'
            return redirect('login_view')
        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form, 'msg': msg})


def login_view(request):
    form = LoginForm(request.POST or None)
    users = User.objects.all()

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_employee:
                login(request, user)
                return redirect('employee')           
            elif user is not None and user.is_admin:
                login(request, user)
                return redirect('adminpage')
            elif user is not None and user.is_customer:
                login(request, user)
                if user.username == "Օհան":
                    return redirect('ohan')
                elif user.username == "Կամո":
                    return redirect('kamo')
                else:
                    return redirect('customer')
            elif user is not None and user.is_employee:
                login(request, user)
                return redirect('employee')
            elif user is not None and user.is_supplier:
                login(request, user)
                return redirect('supplier')
        else:
            return redirect('login_view')
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login_view')

# ========================== Customer Start ===================


def create_global_debt(date, user, total):
    try:
        latest_global_debt = Global_Debt.objects.filter(customer=user).latest('timeOfCreating')
        Global_Debt.objects.create(
            customer = user,
            date = date,
            debt = latest_global_debt.debt + total,
        )
    except:
        Global_Debt.objects.create(
            customer = user,
            date = date,
            debt = total
        )

def Create_old_debt(date, user):
    dateObject = datetime.strptime(date, "%Y-%m-%d").date()
    newUntil = dateObject + timedelta(days=5)
    try:
        Old_debt.objects.get(
            date = date,
            customer = user
        )
        return
    except:
        try:
            latest_global = Global_Debt.objects.filter(customer=user).latest('timeOfCreating')
            try:
                latest_old_debt = Old_debt.objects.filter(customer=user).latest('timeOfCreating')
                if latest_old_debt.until <= dateObject:
                    Old_debt.objects.create(
                        customer = user,
                        date = date,
                        debt = latest_global.debt,
                        until = newUntil
                    )
                    # print('created', latest_old_debt.until <= dateObject)
            except:
                Old_debt.objects.create(
                    customer = user,
                    date = date,
                    debt = latest_global.debt,
                    until = newUntil
                )
        except:
            Old_debt.objects.create(
                customer = user,
                date = date,
                debt = 0,
                until = newUntil
            )


# OHAN OHAN OHAN

def ohanSave(request):
    if request.method == 'POST':
        try:
            # sups = ['Արտադրամաս',"Փուռ","Կիրովական"]
            art = User.objects.get(username="Արտադրամաս")
            pur = User.objects.get(username="Փուռ")
            kir = User.objects.get(username="Կիրովական")
            data = json.loads(request.body.decode('utf-8'))
            date = data.get('date')
            ohanUser = User.objects.get(username = 'Օհան')
            gavarUser = User.objects.get(username = 'Գ.4-րդ')
            avagUser = User.objects.get(username = 'Գ.ավագ')
            araUser = User.objects.get(username = 'Արա')
            try:
                JoinedTables.objects.get(
                    customer=request.user,
                    dateOfCreating=date
                )
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            except:
                pass

            totalSums = data.get('totalSums', {})
            # print(totalSums)
            real_total_of_ohan = 0
            for total_sum in totalSums:
                real_total_of_ohan += totalSums[total_sum]
            ohanJoin = JoinedTables.objects.create(
                    tableName='ohan' + str(random.uniform(1.0, 100.0))[:15],
                    customer=ohanUser,
                    dateOfCreating=date
            )
            gavarJoin = JoinedTables.objects.create(
                    tableName='gavar' + str(random.uniform(1.0, 100.0))[:15],
                    customer=gavarUser,
                    dateOfCreating=date
            )
            avagJoin = JoinedTables.objects.create(
                    tableName='avag' + str(random.uniform(1.0, 100.0))[:15],
                    customer=avagUser,
                    dateOfCreating=date
            )
            araJoin = JoinedTables.objects.create(
                    tableName='ara' + str(random.uniform(1.0, 100.0))[:15],
                    customer=araUser,
                    dateOfCreating=date
            )
            # ohan start
            ohanArt = UserTable.objects.create(
                    user=ohanUser,
                    tableName='ohanArt' + str(random.uniform(1.0, 100.0))[:15],
                    dateOfCreating=date,
                    joinedTable=ohanJoin,
                )
            ohanPur = UserTable.objects.create(
                    user=ohanUser,
                    tableName='ohanPur' + str(random.uniform(1.0, 100.0))[:15],
                    dateOfCreating=date,
                    joinedTable=ohanJoin,
                )
            ohanKir = UserTable.objects.create(
                    user=ohanUser,
                    tableName='ohanKir' + str(random.uniform(1.0, 100.0))[:15],
                    dateOfCreating=date,
                    joinedTable=ohanJoin,
                )
            # ohan end
            gavarArt = UserTable.objects.create(
                    user=gavarUser,
                    tableName='gavarArt' + str(random.uniform(1.0, 100.0))[:15],
                    dateOfCreating=date,
                    joinedTable=gavarJoin,
                )
            gavarPur = UserTable.objects.create(
                    user=gavarUser,
                    tableName='gavarPur' + str(random.uniform(1.0, 100.0))[:15],
                    dateOfCreating=date,
                    joinedTable=gavarJoin,
                )
            gavarKir = UserTable.objects.create(
                    user=gavarUser,
                    tableName='gavarKir' + str(random.uniform(1.0, 100.0))[:15],
                    dateOfCreating=date,
                    joinedTable=gavarJoin,
                )
            # gavar end
            avagArt = UserTable.objects.create(
                    user=avagUser,
                    tableName='avagArt' + str(random.uniform(1.0, 100.0))[:15],
                    dateOfCreating=date,
                    joinedTable=avagJoin,
                )
            avagPur = UserTable.objects.create(
                    user=avagUser,
                    tableName='avagPur' + str(random.uniform(1.0, 100.0))[:15],
                    dateOfCreating=date,
                    joinedTable=avagJoin,
                )
            avagKir = UserTable.objects.create(
                    user=avagUser,
                    tableName='avagKir' + str(random.uniform(1.0, 100.0))[:15],
                    dateOfCreating=date,
                    joinedTable=avagJoin,
                )
            # avag end
            araArt = UserTable.objects.create(
                    user=araUser,
                    tableName='araArt' + str(random.uniform(1.0, 100.0))[:15],
                    dateOfCreating=date,
                    joinedTable=araJoin,
                )
            araPur = UserTable.objects.create(
                    user=araUser,
                    tableName='araPur' + str(random.uniform(1.0, 100.0))[:15],
                    dateOfCreating=date,
                    joinedTable=araJoin,
                )
            araKir = UserTable.objects.create(
                    user=araUser,
                    tableName='araKir' + str(random.uniform(1.0, 100.0))[:15],
                    dateOfCreating=date,
                    joinedTable=araJoin,
                )

            ohan_data = data.get('ohan', [])
            gavar_data = data.get('gavar', [])
            avag_data = data.get('avag', [])
            ara_data = data.get('ara', [])

            for oh in ohan_data:
                if oh['supplier'] == 'Արտադրամաս':
                    table_item = TableItem.objects.create(
                        table = ohanArt,
                        product_name = oh['productName'],
                        product_count = oh['productCount'],
                        product_price = oh['price'],
                        total_price = oh['totalPrice'],
                        customer = ohanUser,
                        supplier = art,
                        supTotal = oh['supTotal']
                    )
                    try:
                        big_tab = BigTableRows.objects.get(
                            user=ohanUser,
                            supplier=art,
                            porduct_name=oh['productName']
                            )
                        big_tab.item = table_item
                        big_tab.save()
                    except:
                        big_tab = BigTableRows.objects.create(
                            user=ohanUser,
                            supplier=art,
                            item=table_item,
                            porduct_name=oh['productName']
                            )
                        big_tab.save()
                elif oh['supplier'] == 'Փուռ':
                    table_item = TableItem.objects.create(
                        table = ohanPur,
                        product_name = oh['productName'],
                        product_count = oh['productCount'],
                        product_price = oh['price'],
                        total_price = oh['totalPrice'],
                        customer = ohanUser,
                        supplier = pur,
                        supTotal = oh['supTotal']
                    )
                    try:
                        big_tab = BigTableRows.objects.get(
                            user=ohanUser,
                            supplier=pur,
                            porduct_name=oh['productName']
                            )
                        big_tab.item = table_item
                        big_tab.save()
                    except:
                        big_tab = BigTableRows.objects.create(
                            user=ohanUser,
                            supplier=pur,
                            item=table_item,
                            porduct_name=oh['productName']
                            )
                        big_tab.save()
                elif oh['supplier'] == 'Կիրովական':
                    table_item = TableItem.objects.create(
                        table = ohanKir,
                        product_name = oh['productName'],
                        product_count = oh['productCount'],
                        product_price = oh['price'],
                        total_price = oh['totalPrice'],
                        customer = ohanUser,
                        supplier = kir,
                        supTotal = oh['supTotal']
                    )
                    try:
                        big_tab = BigTableRows.objects.get(
                            user=ohanUser,
                            supplier=kir,
                            porduct_name=oh['productName']
                            )
                        big_tab.item = table_item
                        big_tab.save()
                    except:
                        big_tab = BigTableRows.objects.create(
                            user=ohanUser,
                            supplier=kir,
                            item=table_item,
                            porduct_name=oh['productName']
                            )
                        big_tab.save()
            for oh in gavar_data:
                if oh['supplier'] == 'Արտադրամաս':
                    table_item = TableItem.objects.create(
                        table = gavarArt,
                        product_name = oh['productName'],
                        product_count = oh['productCount'],
                        product_price = oh['price'],
                        total_price = oh['totalPrice'],
                        customer = gavarUser,
                        supplier = art,
                        supTotal = oh['supTotal']
                    )
                    try:
                        big_tab = BigTableRows.objects.get(
                            user=gavarUser,
                            supplier=art,
                            porduct_name=oh['productName']
                            )
                        big_tab.item = table_item
                        big_tab.save()
                    except:
                        big_tab = BigTableRows.objects.create(
                            user=gavarUser,
                            supplier=art,
                            item=table_item,
                            porduct_name=oh['productName']
                            )
                        big_tab.save()
                elif oh['supplier'] == 'Փուռ':
                    table_item = TableItem.objects.create(
                        table = gavarPur,
                        product_name = oh['productName'],
                        product_count = oh['productCount'],
                        product_price = oh['price'],
                        total_price = oh['totalPrice'],
                        customer = gavarUser,
                        supplier = pur,
                        supTotal = oh['supTotal']
                    )
                    try:
                        big_tab = BigTableRows.objects.get(
                            user=gavarUser,
                            supplier=pur,
                            porduct_name=oh['productName']
                            )
                        big_tab.item = table_item
                        big_tab.save()
                    except:
                        big_tab = BigTableRows.objects.create(
                            user=gavarUser,
                            supplier=pur,
                            item=table_item,
                            porduct_name=oh['productName']
                            )
                        big_tab.save()
                elif oh['supplier'] == 'Կիրովական':
                    table_item = TableItem.objects.create(
                        table = gavarKir,
                        product_name = oh['productName'],
                        product_count = oh['productCount'],
                        product_price = oh['price'],
                        total_price = oh['totalPrice'],
                        customer = gavarUser,
                        supplier = kir,
                        supTotal = oh['supTotal']
                    )
                    try:
                        big_tab = BigTableRows.objects.get(
                            user=gavarUser,
                            supplier=kir,
                            porduct_name=oh['productName']
                            )
                        big_tab.item = table_item
                        big_tab.save()
                    except:
                        big_tab = BigTableRows.objects.create(
                            user=gavarUser,
                            supplier=kir,
                            item=table_item,
                            porduct_name=oh['productName']
                            )
                        big_tab.save()
            for oh in avag_data:
                if oh['supplier'] == 'Արտադրամաս':
                    table_item = TableItem.objects.create(
                        table = avagArt,
                        product_name = oh['productName'],
                        product_count = oh['productCount'],
                        product_price = oh['price'],
                        total_price = oh['totalPrice'],
                        customer = avagUser,
                        supplier = art,
                        supTotal = oh['supTotal']
                    )
                    try:
                        big_tab = BigTableRows.objects.get(
                            user=avagUser,
                            supplier=art,
                            porduct_name=oh['productName']
                            )
                        big_tab.item = table_item
                        big_tab.save()
                    except:
                        big_tab = BigTableRows.objects.create(
                            user=avagUser,
                            supplier=art,
                            item=table_item,
                            porduct_name=oh['productName']
                            )
                        big_tab.save()
                elif oh['supplier'] == 'Փուռ':
                    table_item = TableItem.objects.create(
                        table = avagPur,
                        product_name = oh['productName'],
                        product_count = oh['productCount'],
                        product_price = oh['price'],
                        total_price = oh['totalPrice'],
                        customer = avagUser,
                        supplier = pur,
                        supTotal = oh['supTotal']
                    )
                    try:
                        big_tab = BigTableRows.objects.get(
                            user=avagUser,
                            supplier=pur,
                            porduct_name=oh['productName']
                            )
                        big_tab.item = table_item
                        big_tab.save()
                    except:
                        big_tab = BigTableRows.objects.create(
                            user=avagUser,
                            supplier=pur,
                            item=table_item,
                            porduct_name=oh['productName']
                            )
                        big_tab.save()
                elif oh['supplier'] == 'Կիրովական':
                    table_item = TableItem.objects.create(
                        table = avagKir,
                        product_name = oh['productName'],
                        product_count = oh['productCount'],
                        product_price = oh['price'],
                        total_price = oh['totalPrice'],
                        customer = avagUser,
                        supplier = kir,
                        supTotal = oh['supTotal']
                    )
                    try:
                        big_tab = BigTableRows.objects.get(
                            user=avagUser,
                            supplier=kir,
                            porduct_name=oh['productName']
                            )
                        big_tab.item = table_item
                        big_tab.save()
                    except:
                        big_tab = BigTableRows.objects.create(
                            user=avagUser,
                            supplier=kir,
                            item=table_item,
                            porduct_name=oh['productName']
                            )
                        big_tab.save()
            for ar in ara_data:
                if ar['supplier'] == 'Արտադրամաս':
                    table_item = TableItem.objects.create(
                        table = araArt,
                        product_name = ar['productName'],
                        product_count = ar['productCount'],
                        product_price = ar['price'],
                        total_price = ar['totalPrice'],
                        customer = araUser,
                        supplier = art,
                        supTotal = ar['supTotal']
                    )
                    try:
                        big_tab = BigTableRows.objects.get(
                            user=araUser,
                            supplier=art,
                            porduct_name=ar['productName']
                            )
                        big_tab.item = table_item
                        big_tab.save()
                    except:
                        big_tab = BigTableRows.objects.create(
                            user=araUser,
                            supplier=art,
                            item=table_item,
                            porduct_name=ar['productName']
                            )
                        big_tab.save()
                elif ar['supplier'] == 'Փուռ':
                    table_item = TableItem.objects.create(
                        table = araPur,
                        product_name = ar['productName'],
                        product_count = ar['productCount'],
                        product_price = ar['price'],
                        total_price = ar['totalPrice'],
                        customer = araUser,
                        supplier = pur,
                        supTotal = ar['supTotal']
                    )
                    try:
                        big_tab = BigTableRows.objects.get(
                            user=araUser,
                            supplier=pur,
                            porduct_name=ar['productName']
                            )
                        big_tab.item = table_item
                        big_tab.save()
                    except:
                        big_tab = BigTableRows.objects.create(
                            user=araUser,
                            supplier=pur,
                            item=table_item,
                            porduct_name=ar['productName']
                            )
                        big_tab.save()
                elif ar['supplier'] == 'Կիրովական':
                    table_item = TableItem.objects.create(
                        table = araKir,
                        product_name = ar['productName'],
                        product_count = ar['productCount'],
                        product_price = ar['price'],
                        total_price = ar['totalPrice'],
                        customer = araUser,
                        supplier = kir,
                        supTotal = ar['supTotal']
                    )
                    try:
                        big_tab = BigTableRows.objects.get(
                            user=araUser,
                            supplier=kir,
                            porduct_name=ar['productName']
                            )
                        big_tab.item = table_item
                        big_tab.save()
                    except:
                        big_tab = BigTableRows.objects.create(
                            user=araUser,
                            supplier=kir,
                            item=table_item,
                            porduct_name=ar['productName']
                            )
                        big_tab.save()
            Debt.objects.create(
                customer = ohanUser,
                joined = True,
                debt = real_total_of_ohan,
                date = date
            )
            Create_old_debt(date, ohanUser)
            create_global_debt(date, ohanUser, real_total_of_ohan)
            Debt.objects.create(
                customer = gavarUser,
                joined = True,
                debt = totalSums['gavartotalSum'],
                date = date
            )
            create_global_debt(date, gavarUser, totalSums['gavartotalSum'])
            Create_old_debt(date, gavarUser)
            Debt.objects.create(
                customer = avagUser,
                joined = True,
                debt = totalSums['avagtotalSum'],
                date = date
            )
            create_global_debt(date, avagUser, totalSums['avagtotalSum'])
            Create_old_debt(date, avagUser)
            Debt.objects.create(
                customer = araUser,
                joined = True,
                debt = totalSums['aratotalSum'],
                date = date
            )
            create_global_debt(date, araUser, totalSums['aratotalSum'])
            Create_old_debt(date, araUser)
            # suppliers = [art, pur, kir]
            custs = [ohanUser,gavarUser,avagUser,araUser]

            ArtTable = [ohanArt,gavarArt,avagArt,araArt]
            purTable = [ohanPur,gavarPur,avagPur,araPur]
            kirTable = [ohanKir,gavarKir,avagKir,araKir]

            for at,cust in zip(ArtTable, custs):
                try:
                    bigtable = BigTable.objects.get(supplier=art, user=cust)
                    bigtable.table = at
                    bigtable.modifiedDate = date
                    bigtable.save()
                except:
                    # print(at, cust)
                    bigtable = BigTable.objects.create(
                        supplier=art,
                        table=at,
                        user=cust,
                        modifiedDate=date
                        )
            for pt,cust in zip(purTable, custs):
                try:
                    bigtable = BigTable.objects.get(supplier=pur, user=cust)
                    bigtable.table = pt
                    bigtable.modifiedDate = date
                    bigtable.save()
                except:
                    bigtable = BigTable.objects.create(
                        supplier=pur,
                        table=pt,
                        user=cust,
                        modifiedDate=date
                        )
            for kt,cust in zip(kirTable, custs):
                try:
                    bigtable = BigTable.objects.get(supplier=kir, user=cust)
                    bigtable.table = kt
                    bigtable.modifiedDate = date
                    bigtable.save()
                except:
                    bigtable = BigTable.objects.create(
                        supplier=kir,
                        table=kt,
                        user=cust,
                        modifiedDate=date
                        )

            return JsonResponse({'message': 'Data received and processed successfully'})
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


def kamoSave(request):
    if request.method == 'POST':
        art = User.objects.get(username="Արտադրամաս")
        pur = User.objects.get(username="Փուռ")
        kir = User.objects.get(username="Կիրովական")

        data = json.loads(request.body.decode('utf-8'))
        # print(data)
        date = data.get('date')
        kamo_User = User.objects.get(username = 'Կամո')
        gandak_User = User.objects.get(username = 'Գանձակ')
        sarukan_User = User.objects.get(username = 'Սարուխան')

        try:
            JoinedTables.objects.get(
                customer=request.user,
                dateOfCreating=date
            )
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except:
            pass

        totalSums = data.get('totalSums', {})
        real_total_of_kamo = 0
        for total_sum in totalSums:
            real_total_of_kamo += totalSums[total_sum]

        kamoJoin = JoinedTables.objects.create(
                tableName='kamo' + str(random.uniform(1.0, 100.0))[:15],
                customer=kamo_User,
                dateOfCreating=date
        )
        gandakJoin = JoinedTables.objects.create(
                tableName='gandak' + str(random.uniform(1.0, 100.0))[:15],
                customer=gandak_User,
                dateOfCreating=date
        )
        sarukanJoin = JoinedTables.objects.create(
                tableName='sarukan' + str(random.uniform(1.0, 100.0))[:15],
                customer=sarukan_User,
                dateOfCreating=date
        )

        kamoArt = UserTable.objects.create(
                user=kamo_User,
                tableName='kamoArt' + str(random.uniform(1.0, 100.0))[:15],
                dateOfCreating=date,
                joinedTable=kamoJoin,
            )
        kamoPur = UserTable.objects.create(
                user=kamo_User,
                tableName='kamoPur' + str(random.uniform(1.0, 100.0))[:15],
                dateOfCreating=date,
                joinedTable=kamoJoin,
            )
        kamoKir = UserTable.objects.create(
                user=kamo_User,
                tableName='kamoKir' + str(random.uniform(1.0, 100.0))[:15],
                dateOfCreating=date,
                joinedTable=kamoJoin,
            )
        # ohan end

        gandakArt = UserTable.objects.create(
                user=gandak_User,
                tableName='gandakArt' + str(random.uniform(1.0, 100.0))[:15],
                dateOfCreating=date,
                joinedTable=gandakJoin,
            )
        gandakPur = UserTable.objects.create(
                user=gandak_User,
                tableName='gandakPur' + str(random.uniform(1.0, 100.0))[:15],
                dateOfCreating=date,
                joinedTable=gandakJoin,
            )
        gandakKir = UserTable.objects.create(
                user=gandak_User,
                tableName='gandakKir' + str(random.uniform(1.0, 100.0))[:15],
                dateOfCreating=date,
                joinedTable=gandakJoin,
            )
        # gavar end

        sarukanArt = UserTable.objects.create(
                user=sarukan_User,
                tableName='sarukanArt' + str(random.uniform(1.0, 100.0))[:15],
                dateOfCreating=date,
                joinedTable=sarukanJoin,
            )
        sarukanPur = UserTable.objects.create(
                user=sarukan_User,
                tableName='sarukanPur' + str(random.uniform(1.0, 100.0))[:15],
                dateOfCreating=date,
                joinedTable=sarukanJoin,
            )
        sarukanKir = UserTable.objects.create(
                user=sarukan_User,
                tableName='sarukanKir' + str(random.uniform(1.0, 100.0))[:15],
                dateOfCreating=date,
                joinedTable=sarukanJoin,
            )

        kamo_data = data.get('kamo', [])
        gandak_data = data.get('gandak', [])
        sarukan_data = data.get('sarukan', [])

        for oh in kamo_data:
            if oh['supplier'] == 'Արտադրամաս':
                table_item = TableItem.objects.create(
                    table = kamoArt,
                    product_name = oh['productName'],
                    product_count = oh['productCount'],
                    product_price = oh['price'],
                    total_price = oh['totalPrice'],
                    customer = kamo_User,
                    supplier = art,
                    supTotal = oh['supTotal']
                )
                try:
                    big_tab = BigTableRows.objects.get(
                        user=kamo_User,
                        supplier=art,
                        porduct_name=oh['productName']
                        )
                    big_tab.item = table_item
                    big_tab.save()
                except:
                    big_tab = BigTableRows.objects.create(
                        user=kamo_User,
                        supplier=art,
                        item=table_item,
                        porduct_name=oh['productName']
                        )
                    big_tab.save()
            elif oh['supplier'] == 'Փուռ':
                table_item = TableItem.objects.create(
                    table = kamoPur,
                    product_name = oh['productName'],
                    product_count = oh['productCount'],
                    product_price = oh['price'],
                    total_price = oh['totalPrice'],
                    customer = kamo_User,
                    supplier = pur,
                    supTotal = oh['supTotal']
                )
                try:
                    big_tab = BigTableRows.objects.get(
                        user=kamo_User,
                        supplier=pur,
                        porduct_name=oh['productName']
                        )
                    big_tab.item = table_item
                    big_tab.save()
                except:
                    big_tab = BigTableRows.objects.create(
                        user=kamo_User,
                        supplier=pur,
                        item=table_item,
                        porduct_name=oh['productName']
                        )
                    big_tab.save()
            elif oh['supplier'] == 'Կիրովական':
                table_item = TableItem.objects.create(
                    table = kamoKir,
                    product_name = oh['productName'],
                    product_count = oh['productCount'],
                    product_price = oh['price'],
                    total_price = oh['totalPrice'],
                    customer = kamo_User,
                    supplier = kir,
                    supTotal = oh['supTotal']
                )
                try:
                    big_tab = BigTableRows.objects.get(
                        user=kamo_User,
                        supplier=kir,
                        porduct_name=oh['productName']
                        )
                    big_tab.item = table_item
                    big_tab.save()
                except:
                    big_tab = BigTableRows.objects.create(
                        user=kamo_User,
                        supplier=kir,
                        item=table_item,
                        porduct_name=oh['productName']
                        )
                    big_tab.save()

        for oh in gandak_data:
            if oh['supplier'] == 'Արտադրամաս':
                table_item = TableItem.objects.create(
                    table = gandakArt,
                    product_name = oh['productName'],
                    product_count = oh['productCount'],
                    product_price = oh['price'],
                    total_price = oh['totalPrice'],
                    customer = gandak_User,
                    supplier = art,
                    supTotal = oh['supTotal']
                )
                try:
                    big_tab = BigTableRows.objects.get(
                        user=gandak_User,
                        supplier=art,
                        porduct_name=oh['productName']
                        )
                    big_tab.item = table_item
                    big_tab.save()
                except:
                    big_tab = BigTableRows.objects.create(
                        user=gandak_User,
                        supplier=art,
                        item=table_item,
                        porduct_name=oh['productName']
                        )
                    big_tab.save()
            elif oh['supplier'] == 'Փուռ':
                table_item = TableItem.objects.create(
                    table = gandakPur,
                    product_name = oh['productName'],
                    product_count = oh['productCount'],
                    product_price = oh['price'],
                    total_price = oh['totalPrice'],
                    customer = gandak_User,
                    supplier = pur,
                    supTotal = oh['supTotal']
                )
                try:
                    big_tab = BigTableRows.objects.get(
                        user=gandak_User,
                        supplier=pur,
                        porduct_name=oh['productName']
                        )
                    big_tab.item = table_item
                    big_tab.save()
                except:
                    big_tab = BigTableRows.objects.create(
                        user=gandak_User,
                        supplier=pur,
                        item=table_item,
                        porduct_name=oh['productName']
                        )
                    big_tab.save()
            elif oh['supplier'] == 'Կիրովական':
                table_item = TableItem.objects.create(
                    table = gandakKir,
                    product_name = oh['productName'],
                    product_count = oh['productCount'],
                    product_price = oh['price'],
                    total_price = oh['totalPrice'],
                    customer = gandak_User,
                    supplier = kir,
                    supTotal = oh['supTotal']
                )
                try:
                    big_tab = BigTableRows.objects.get(
                        user=gandak_User,
                        supplier=kir,
                        porduct_name=oh['productName']
                        )
                    big_tab.item = table_item
                    big_tab.save()
                except:
                    big_tab = BigTableRows.objects.create(
                        user=gandak_User,
                        supplier=kir,
                        item=table_item,
                        porduct_name=oh['productName']
                        )
                    big_tab.save()

        for oh in sarukan_data:
            if oh['supplier'] == 'Արտադրամաս':
                table_item = TableItem.objects.create(
                    table = sarukanArt,
                    product_name = oh['productName'],
                    product_count = oh['productCount'],
                    product_price = oh['price'],
                    total_price = oh['totalPrice'],
                    customer = sarukan_User,
                    supplier = art,
                    supTotal = oh['supTotal']
                )
                try:
                    big_tab = BigTableRows.objects.get(
                        user=sarukan_User,
                        supplier=art,
                        porduct_name=oh['productName']
                        )
                    big_tab.item = table_item
                    big_tab.save()
                except:
                    big_tab = BigTableRows.objects.create(
                        user=sarukan_User,
                        supplier=art,
                        item=table_item,
                        porduct_name=oh['productName']
                        )
                    big_tab.save()
            elif oh['supplier'] == 'Փուռ':
                table_item = TableItem.objects.create(
                    table = sarukanPur,
                    product_name = oh['productName'],
                    product_count = oh['productCount'],
                    product_price = oh['price'],
                    total_price = oh['totalPrice'],
                    customer = sarukan_User,
                    supplier = pur,
                    supTotal = oh['supTotal']
                )
                try:
                    big_tab = BigTableRows.objects.get(
                        user=sarukan_User,
                        supplier=pur,
                        porduct_name=oh['productName']
                        )
                    big_tab.item = table_item
                    big_tab.save()
                except:
                    big_tab = BigTableRows.objects.create(
                        user=sarukan_User,
                        supplier=pur,
                        item=table_item,
                        porduct_name=oh['productName']
                        )
                    big_tab.save()
            elif oh['supplier'] == 'Կիրովական':
                table_item = TableItem.objects.create(
                    table = sarukanKir,
                    product_name = oh['productName'],
                    product_count = oh['productCount'],
                    product_price = oh['price'],
                    total_price = oh['totalPrice'],
                    customer = sarukan_User,
                    supplier = kir,
                    supTotal = oh['supTotal']
                )
                try:
                    big_tab = BigTableRows.objects.get(
                        user=sarukan_User,
                        supplier=kir,
                        porduct_name=oh['productName']
                        )
                    big_tab.item = table_item
                    big_tab.save()
                except:
                    big_tab = BigTableRows.objects.create(
                        user=sarukan_User,
                        supplier=kir,
                        item=table_item,
                        porduct_name=oh['productName']
                        )
                    big_tab.save()

        Debt.objects.create(
            customer = kamo_User,
            joined = True,
            debt = real_total_of_kamo,
            date = date
        )
        Create_old_debt(date, kamo_User)
        create_global_debt(date, kamo_User, real_total_of_kamo)

        Debt.objects.create(
            customer = gandak_User,
            joined = True,
            debt = totalSums['gandaktotalSum'],
            date = date
        )
        create_global_debt(date, gandak_User, totalSums['gandaktotalSum'])
        Create_old_debt(date, gandak_User)

        Debt.objects.create(
            customer = sarukan_User,
            joined = True,
            debt = totalSums['sarukamtotalSum'],
            date = date
        )
        create_global_debt(date, sarukan_User, totalSums['sarukamtotalSum'])
        Create_old_debt(date, sarukan_User)

        custs = [kamo_User,gandak_User,sarukan_User]

        ArtTable = [kamoArt,gandakArt,sarukanArt]
        purTable = [kamoPur,gandakPur,sarukanPur]
        kirTable = [kamoKir,gandakKir,sarukanKir]

        for at,cust in zip(ArtTable, custs):
            try:
                bigtable = BigTable.objects.get(supplier=art, user=cust)
                bigtable.table = at
                bigtable.modifiedDate = date
                bigtable.save()
            except:
                # print(at, cust)
                bigtable = BigTable.objects.create(
                    supplier=art,
                    table=at,
                    user=cust,
                    modifiedDate=date
                    )
        for pt,cust in zip(purTable, custs):
            try:
                bigtable = BigTable.objects.get(supplier=pur, user=cust)
                bigtable.table = pt
                bigtable.modifiedDate = date
                bigtable.save()
            except:
                bigtable = BigTable.objects.create(
                    supplier=pur,
                    table=pt,
                    user=cust,
                    modifiedDate=date
                    )
        for kt,cust in zip(kirTable, custs):
            try:
                bigtable = BigTable.objects.get(supplier=kir, user=cust)
                bigtable.table = kt
                bigtable.modifiedDate = date
                bigtable.save()
            except:
                bigtable = BigTable.objects.create(
                    supplier=kir,
                    table=kt,
                    user=cust,
                    modifiedDate=date
                    )
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        # return redirect(request.path_info)
        # return JsonResponse({'message': 'Data received and processed successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def kamo(request):
    usersArray = ['Կամո','Գանձակ','Սարուխան']
    for i, v in enumerate(usersArray):
        usersArray[i] = User.objects.get(username=v)
    uniq = ItemsModel.productsfor_Customer(request.user)

    items_name = [
        'Պերաշկի', 'Պոնչիկ', 'Կոտլետ', 'ՀոթԴոգ', 'Պիցցա', 'Երշիկ', 'ԲուլկիՎանիլ', 'ԲուլկիՇոկո', 'Պոնչիկ Բեռլին',
        'Խաչապուրի(Փ)', 'խաչ.մեծ', 'ԲուլկիՉամիչ', 'ԲուլկիՋեմ', 'ԲուլկիՌոլլ', 'ԲուկլիԴարչին', 'Բուլկի Խտ Կաթով', 'ԲուլկիԽորիզ',
        'Քլաբ սենդ', 'Բուլկի Կաթնային'
    ]

    itemsObjects = {
        'kamo': [],
        'gandak': [],
        'sarukan': []
    }

    for user, us in zip(usersArray, itemsObjects):
        itemsObjects[us] = ItemsModel.objects.filter(customer=user.username)

    priority_products = []  # Products to prioritize
    rest_products = []      # Products to sort

    for prod in uniq:
        if prod.productName in items_name:
            priority_products.append(prod)
        else:
            rest_products.append(prod)


    Items = []

    for prod in sorted(priority_products, key=lambda x: items_name.index(x.productName)) + rest_products:
        kamo = itemsObjects['kamo'].filter(productName=prod.productName).first()
        gandak = itemsObjects['gandak'].filter(productName=prod.productName).first()
        sarukan = itemsObjects['sarukan'].filter(productName=prod.productName).first()

        Items.append([prod.productName, kamo, gandak, sarukan])

    return render(request, 'drivers/kamo.html', {
        'Items': Items
    })

def kamoTables(request):
    page_number = request.GET.get('page')
    # Joined Tables
    kamo_User = request.user
    joinedTables = JoinedTables.objects.filter(
        customer=kamo_User,
        ).order_by('timeOfCreating')  # Reverse the order by '-id'
    joinPaginator = Paginator(joinedTables, 5)  # show 5 joinedTables per page
    join_page_obj = joinPaginator.get_page(page_number)
    reversed_join_page_obj = joinPaginator.get_page(
            joinPaginator.num_pages - join_page_obj.number + 1
        ).__reversed__()  # Reversed join_page_obj
    customers = [
        User.objects.get(username='Կամո'),
        User.objects.get(username='Գանձակ'),
        User.objects.get(username='Սարուխան')
        ]

    tables = []

    joinedTables_array = []
    for ohan_join in reversed_join_page_obj:
        mini_arr = []
        tables.append(ohan_join)
        for join in JoinedTables.objects.filter(dateOfCreating = ohan_join.dateOfCreating, customer__in = customers):
            mini_arr.append(join)
        joinedTables_array.append(mini_arr)
    misTables = []
    for mis in tables:
        misTables.append(
            [
                mis,
                JoinedTables.objects.get(dateOfCreating = mis.dateOfCreating, customer=customers[1]),
                JoinedTables.objects.get(dateOfCreating = mis.dateOfCreating, customer=customers[2])
            ]
        )
    joined_Max = []

    for i in joinedTables_array:
        for j in i:
            joined_Max.append(j)

    userTables = UserTable.objects.filter(joinedTable__in = joined_Max)
    userTables_array = []
    for us in userTables:
        userTables_array.append(us)

    suppliers = ['Արտադրամաս','Փուռ','Կիրովական']
    uniq = ItemsModel.productsfor_Customer(kamo_User)
    rows = []
    for joined_arr in joinedTables_array:
        mini_rows = []
        # print(joined_arr)
        for joinedTable in joined_arr:
            table_Rows = []
            for userTable in userTables_array:
                if userTable.joinedTable == joinedTable:
                    for product in uniq:
                        if product.supplier in suppliers:
                            try:
                                if joinedTable.customer.username == 'Կամո':
                                    us = 'kamo'
                                elif joinedTable.customer.username == 'Գանձակ':
                                    us = 'gandak'
                                elif joinedTable.customer.username == 'Սարուխան':
                                    us = "sarukan"
                                r = {
                                    'productName': product.productName,
                                    us: TableItem.objects.get(
                                        table=userTable,
                                        product_name=product.productName,
                                        customer=joinedTable.customer
                                )}
                                table_Rows.append(r)
                            except:
                                pass
            if joinedTable.customer.username == 'Կամո':
                ts = 'kamo'
            elif joinedTable.customer.username == 'Գանձակ':
                ts = 'gandak'
            elif joinedTable.customer.username == 'Սարուխան':
                ts = "sarukan"
            mini_rows.append({
                'table_name': f'{joinedTable.tableName}',
                ts : table_Rows
                })
        rows.append(mini_rows)

    complete_row = []

    for tab in tables:
        mini_comp = []
        kamo_total = 0
        gandak_total = 0
        sarukan_total = 0
        big_total = 0
        for row in rows:
            if row[2]['table_name'] == tab.tableName:
                for prod in uniq:
                    row_list = []
                    total_of_row = 0
                    row_list.append(prod.productName)
                        # print(ohan)
                    for kamo in row[2]['kamo']:
                        if kamo['productName'] == prod.productName:
                            row_list.append(kamo['kamo'])
                            total_of_row += kamo['kamo'].total_price
                            kamo_total += kamo['kamo'].total_price
                            break
                    for gandak in row[1]['gandak']:
                        if gandak['productName'] == prod.productName:
                            row_list.append(gandak['gandak'])
                            total_of_row += gandak['gandak'].total_price
                            gandak_total += gandak['gandak'].total_price
                            break
                    for sarukan in row[0]['sarukan']:
                        if sarukan['productName'] == prod.productName:
                            row_list.append(sarukan['sarukan'])
                            total_of_row += sarukan['sarukan'].total_price
                            sarukan_total += sarukan['sarukan'].total_price
                            break
                    row_list.append(total_of_row)
                    big_total += total_of_row
                    mini_comp.append(row_list)

                # print(mini_comp)
        complete_row.append({f'{tab.tableName}':mini_comp,'last_row': ['Ընդ', kamo_total, gandak_total, sarukan_total, big_total]})

    debt_array = []
    for table in tables[::-1]:
        try:
            debt = Debt.objects.get(date=table.dateOfCreating, customer = kamo_User, joined = True)
            # print(debt)
            debt_array.append([str(debt.date), debt.debt, ''])
            # print('try')
        except:
            # print('except')
            debt_array.append([str(table.dateOfCreating), 0, ''])
    try:
        paymant = Paymant.objects.get(
            date = tables[-1].dateOfCreating,
            customer=customers[0]
        )
        total_payments_money = paymant.money
        total_payments_returned = paymant.returned
        total_payments_salary = paymant.salary
    except:
        total_payments_money = 0
        total_payments_returned = 0
        total_payments_salary = 0

    total_global_debt = 0
    try:
        old_debt = Old_debt.objects.get(date = tables[-1].dateOfCreating, customer=customers[0]).debt
    except:
        old_debt = 0

    try:
        new_debt = Week_debt.objects.get(date = tables[-1].dateOfCreating, customer=customers[0]).debt
    except:
        new_debt = 0
    total_global_debt = Global_Debt.objects.filter(customer=customers[0]).latest('timeOfCreating').debt

    is_waiting = WaitingForChange.objects.filter(customer__in=customers).count() != 0

    select_old_debt = []
    Old_debts = Old_debt.objects.filter(customer=customers[0])
    for old in Old_debts:
        select_old_debt.append(
            {
                'name': f" {old.date}---{old.until}",
                'value': old.date
            }
        )
    select_old_debt.reverse()
    # print(tables[-1].dateOfCreating)
    return render(request, 'drivers/kamoTables.html', {
        'Tables': misTables,
        'CompleteRows': complete_row,
        "table" : join_page_obj,
        'is_waiting': is_waiting,
        "select_date": select_old_debt,
        'joinedDebt': debt_array,
        'Returned': total_payments_returned,
        'Salary': total_payments_salary,
        'Money': total_payments_money,
        'GlobalDebt': total_global_debt,
        'OldDebt': old_debt,
        'NewDebt': new_debt,
    })

def ohan(request):
    usersArray = [
        'Օհան',
        'Գ.4-րդ',
        'Գ.ավագ',
        'Արա'
    ]
    for i, v in enumerate(usersArray):
        usersArray[i] = User.objects.get(username=v)

    itemsObjects = {
        'ohan': [],
        'gavar': [],
        'avag': [],
        'ara': []
    }

    for user, us in zip(usersArray, itemsObjects):
        itemsObjects[us] = ItemsModel.objects.filter(customer=user.username)

    Items = []
    uniq = ItemsModel.productsfor_Customer(request.user)

    items_name = [
        'Պերաշկի', 'Պոնչիկ', 'Պիցցա', 'խաչ.մեծ', 'Խաչապուրի(Փ)', 'Բուլկի Կաթնային', 'Պան քեյք',
        'Քլաբ սենդ', 'Կոտլետ', 'ՍենդվիչԵրշ', 'ՀոթԴոգ', 'ԲուլկիՎանիլ', 'ԲուլկիՇոկո', 'Պոնչիկ Բեռլին',
        'ԲուլկիՉամիչ', 'ԲուկլիԴարչին', 'Բուլկի Խտ Կաթով', 'ԲուլկիԽորիզ'
    ]

    priority_products = []  # Products to prioritize
    rest_products = []      # Products to sort

    for prod in uniq:
        if prod.productName in items_name:
            priority_products.append(prod)
        else:
            rest_products.append(prod)

    for prod in sorted(priority_products, key=lambda x: items_name.index(x.productName)) + rest_products:
        ohan = itemsObjects['ohan'].filter(productName=prod.productName).first()
        gavar = itemsObjects['gavar'].filter(productName=prod.productName).first()
        avag = itemsObjects['avag'].filter(productName=prod.productName).first()
        ara = itemsObjects['ara'].filter(productName=prod.productName).first()

        Items.append([prod.productName, ohan, gavar, avag, ara])

    return render(request, 'drivers/ohan.html', {
        'Items': Items
    })



def ohanTables(request):
    page_number = request.GET.get('page')
    # Joined Tables
    ohan_User = request.user
    joinedTables = JoinedTables.objects.filter(
        customer=ohan_User,
        ).order_by('timeOfCreating')  # Reverse the order by '-id'
    joinPaginator = Paginator(joinedTables, 5)  # show 5 joinedTables per page
    join_page_obj = joinPaginator.get_page(page_number)
    reversed_join_page_obj = joinPaginator.get_page(
            joinPaginator.num_pages - join_page_obj.number + 1
        ).__reversed__()  # Reversed join_page_obj
    customers = [
        User.objects.get(username='Օհան'), User.objects.get(username='Գ.4-րդ'),
        User.objects.get(username='Գ.ավագ'), User.objects.get(username='Արա')
        ]

    tables = []

    joinedTables_array = []
    for ohan_join in reversed_join_page_obj:
        mini_arr = []
        tables.append(ohan_join)
        for join in JoinedTables.objects.filter(dateOfCreating = ohan_join.dateOfCreating, customer__in = customers):
            mini_arr.append(join)
        joinedTables_array.append(mini_arr)

    misTables = []
    for mis in tables:
        misTables.append(
            [
                mis,
                JoinedTables.objects.get(dateOfCreating = mis.dateOfCreating, customer=customers[1]),
                JoinedTables.objects.get(dateOfCreating = mis.dateOfCreating, customer=customers[2]),
                JoinedTables.objects.get(dateOfCreating = mis.dateOfCreating, customer=customers[3]),
            ]
        )
    joined_Max = []
    for i in joinedTables_array:
        for j in i:
            joined_Max.append(j)

    userTables = UserTable.objects.filter(joinedTable__in = joined_Max)
    userTables_array = []
    for us in userTables:
        userTables_array.append(us)
    suppliers = ['Արտադրամաս','Փուռ','Կիրովական']
    uniq = ItemsModel.productsfor_Customer(ohan_User)
    rows = []
    for joined_arr in joinedTables_array:
        mini_rows = []
        # print(joined_arr)
        for joinedTable in joined_arr:
            table_Rows = []
            for userTable in userTables_array:
                if userTable.joinedTable == joinedTable:
                    for product in uniq:
                        if product.supplier in suppliers:
                            try:
                                if joinedTable.customer.username == 'Օհան':
                                    us = 'ohan'
                                elif joinedTable.customer.username == 'Գ.4-րդ':
                                    us = 'gavar'
                                elif joinedTable.customer.username == 'Գ.ավագ':
                                    us = "avag"
                                elif joinedTable.customer.username == 'Արա':
                                    us = 'ara'
                                r = {
                                    'productName': product.productName,
                                    us: TableItem.objects.get(
                                        table=userTable,
                                        product_name=product.productName,
                                        customer=joinedTable.customer
                                )}
                                table_Rows.append(r)
                            except:
                                pass
            if joinedTable.customer.username == 'Օհան':
                ts = 'ohan'
            elif joinedTable.customer.username == 'Գ.4-րդ':
                ts = 'gavar'
            elif joinedTable.customer.username == 'Գ.ավագ':
                ts = "avag"
            elif joinedTable.customer.username == 'Արա':
                ts = 'ara'
            mini_rows.append({
                'table_name': f'{joinedTable.tableName}',
                ts : table_Rows
                })
        rows.append(mini_rows)

    complete_row = []

    for tab in tables:
        mini_comp = []
        ohan_total = 0
        gavar_total = 0
        avag_total = 0
        ara_total = 0
        big_total = 0
        try:
            for row in rows:
                if row[3]['table_name'] == tab.tableName:
                    for prod in uniq:
                        row_list = []
                        total_of_row = 0
                        row_list.append(prod.productName)
                        for ohan in row[3]['ohan']:
                            if ohan['productName'] == prod.productName:
                                row_list.append(ohan['ohan'])
                                total_of_row += ohan['ohan'].total_price
                                ohan_total += ohan['ohan'].total_price
                                break
                        for gavar in row[2]['gavar']:
                            if gavar['productName'] == prod.productName:
                                row_list.append(gavar['gavar'])
                                total_of_row += gavar['gavar'].total_price
                                gavar_total += gavar['gavar'].total_price
                                break
                        for avag in row[1]['avag']:
                            if avag['productName'] == prod.productName:
                                row_list.append(avag['avag'])
                                total_of_row += avag['avag'].total_price
                                avag_total += avag['avag'].total_price
                                break
                        for ara in row[0]['ara']:
                            if ara['productName'] == prod.productName:
                                row_list.append(ara['ara'])
                                total_of_row += ara['ara'].total_price
                                ara_total += ara['ara'].total_price
                                break
                        row_list.append(total_of_row)
                        big_total += total_of_row
                        mini_comp.append(row_list)
            complete_row.append({f'{tab.tableName}':mini_comp,'last_row': ['Ընդ', ohan_total, gavar_total, avag_total, ara_total, big_total]})
        except:
            pass
    debt_array = []
    for table in tables[::-1]:
        try:
            debt = Debt.objects.get(date=table.dateOfCreating, customer = ohan_User, joined = True)
            debt_array.append([str(debt.date), debt.debt, ''])
        except:
            debt_array.append([str(table.dateOfCreating), 0, ''])
    # PAYMANT
    try:
        paymant = Paymant.objects.get(
            date = tables[-1].dateOfCreating,
            customer=customers[0]
        )
        total_payments_money = paymant.money
        total_payments_returned = paymant.returned
        total_payments_salary = paymant.salary
    except:
        total_payments_money = 0
        total_payments_returned = 0
        total_payments_salary = 0

    total_global_debt = 0
    try:
        old_debt = Old_debt.objects.get(date = tables[-1].dateOfCreating, customer=customers[0]).debt
    except:
        old_debt = 0

    try:
        new_debt = Week_debt.objects.get(date = tables[-1].dateOfCreating, customer=customers[0]).debt
    except:
        new_debt = 0

    total_global_debt = Global_Debt.objects.filter(customer=customers[0]).latest('timeOfCreating').debt

    is_waiting = WaitingForChange.objects.filter(customer__in=customers).count() != 0
    select_old_debt = []

    Old_debts = Old_debt.objects.filter(customer=customers[0])
    for old in Old_debts:
        select_old_debt.append(
            {
                'name': f" {old.date}---{old.until}",
                'value': old.date
            }
        )
    select_old_debt.reverse()

    return render(request, 'drivers/ohanTables.html', {
        'Tables': misTables,
        'CompleteRows': complete_row,
        "table" : join_page_obj,
        'is_waiting': is_waiting,
        "select_date": select_old_debt,
        'joinedDebt': debt_array,
        'Returned': total_payments_returned,
        'Salary': total_payments_salary,
        'Money': total_payments_money,
        'GlobalDebt': total_global_debt,
        'OldDebt': old_debt,
        'NewDebt': new_debt,
    })

@customer_required
def customer(request):
    if request.user.username == 'Կամո':
        return redirect('kamo')
    elif request.user.username == 'Օհան':
        return redirect('ohan')
    # tablesUsers = UserTable.objects.all()
    items = ItemsModel.productsfor_Customer(request.user)
    # tableRows = TableItem.objects.all()
    joinedTables = User.objects.filter(is_supplier=True, username__in=["Կիրովական", "Արտադրամաս", "Փուռ"])
    # suppliers = User.objects.filter(is_supplier=True, ).exclude(username__in=joinedTables.values('username'))
    suppliers = User.objects.filter(username="Այլ.ապրանք")
    school_array = [
        'Էրանոս','Լիճք', 'Մ.1ին',
        'Մ.ավագ', 'Զոլ.2րդ', 'Զոլ.1ին', 'Ծովինար', "Չարբախ_1"
    ]
    available = request.user.username in school_array
    unreaden_mess = unreaden_messages(request.user.username)
    return render(request, 'customer.html', {
        'Items': items,
        # 'Tables': tablesUsers,
        # 'TableRows': tableRows,
        'Suppliers': suppliers,
        "joinedSuppliers": joinedTables,
        'martuni': available,
        "unreaden_messages": unreaden_mess
        })


@customer_required
def tablesByUser(request):
    if request.user.username in ["Գավառ_ավագ","Գավառ_4րդ", "Գավառ_5րդ", "Գ_սարուխան", "Գ_հացառատ2","Գ_գանձակ"]:
        return redirect("gavari_dprocn")
    if request.user.username == 'Օհան':
        return redirect('ohanTables')
    elif request.user.username == 'Կամո':
        return redirect('kamoTables')

    page_number = request.GET.get('page')
    # Joined Tables
    joinedTables = JoinedTables.objects.filter(
        customer=request.user,
        ).order_by('timeOfCreating')  # Reverse the order by '-id'
    joinPaginator = Paginator(joinedTables, 5)  # show 5 joinedTables per page
    join_page_obj = joinPaginator.get_page(page_number)
    reversed_join_page_obj = joinPaginator.get_page(
            joinPaginator.num_pages - join_page_obj.number + 1
        ).__reversed__()  # Reversed join_page_obj
    reversed_join_page_copy = joinPaginator.get_page(
            joinPaginator.num_pages - join_page_obj.number + 1
        ).__reversed__()  # Reversed join_page_obj
    reversed_join_page_for_debt = joinPaginator.get_page(
            joinPaginator.num_pages - join_page_obj.number + 1
        )  # Reversed join_page_obj


    reversed_table_page_obj = []
    for join in reversed_join_page_copy:
        try:
            joins = UserTable.objects.filter(
                user = request.user,
                joinedTable = join,
            )
            for jo in joins:
                reversed_table_page_obj.append(jo)
        except:
            continue
    JoinRows = []
    for tab in reversed_table_page_obj:
        try:
            row =  TableItem.objects.filter(
                customer = request.user,
                table = tab
            )
            for r in row:
                JoinRows.append(r)
        except:
            continue

    # Joined Tables

    single_debt_array = []
    debt_array = []
    for i in reversed_join_page_for_debt:
        try:
            joinedDebt = Debt.objects.get(
                customer = request.user,
                joined = True,
                date = i.dateOfCreating
            )
            theDebt = [str(i.dateOfCreating),joinedDebt.debt,""]
            if joinedDebt.date not in single_debt_array:
                single_debt_array.append(joinedDebt.date)
            try:
                singleDebt = Debt.objects.get(
                    customer = request.user,
                    single=True,
                    date=i.dateOfCreating
                    )
                # if singleDebt.date not in single_debt_array:
                #     single_debt_array.append(singleDebt.date)
                theDebt[2] = singleDebt.debt
            except:
                pass
            debt_array.append(theDebt)
        except:
            continue

    SingleTables = []
    for date in single_debt_array:
        try:
            singleTab = UserTable.objects.get(
                user= request.user,
                singleTable__isnull = False,
                dateOfCreating = date
            )
            SingleTables.append(singleTab)
        except:
            continue

    writng_tables = []
    for date in single_debt_array:
        try:
            writing_tab = UserTable.objects.get(
                user = request.user,
                joinedTable__isnull = True,
                singleTable__isnull = True,
                dateOfCreating = date
            )
            writng_tables.append(writing_tab)
        except:
            continue

    for date in single_debt_array:
        try:
            debt = Debt.objects.get(
                customer = request.user,
                single=False,
                joined=False,
                date=date
            )
            theDebt = [str(date),'Գրենական',debt.debt]
            debt_array.append(theDebt)
        except:
            pass

    SingleRows = []
    for table in writng_tables:
        try:
            row = TableItem.objects.filter(
                customer = request.user,
                table = table,
            )
            for r in row:
                SingleRows.append(r)
        except:
            continue
    for table in SingleTables:
        try:
            row = TableItem.objects.filter(
                customer = request.user,
                table = table,
            )
            for r in row:
                SingleRows.append(r)
        except:
            continue

    # Single Tables
    try:
        weekPaymant = Paymant.objects.get(
            customer = request.user,
            date = single_debt_array[0]
        )
    except:
        weekPaymant = Paymant.objects.none()

    try:
        week_debt = Week_debt.objects.get(
            customer = request.user,
            date = single_debt_array[0]
        )
    except:
        week_debt = Week_debt.objects.none()

    try:
        old_debt = Old_debt.objects.get(
            customer = request.user,
            date = single_debt_array[0]
        )
    except:
        old_debt = Old_debt.objects.none()

    try:
        globalDebt = Global_Debt.objects.filter(customer = request.user).latest('timeOfCreating')
    except:
        globalDebt = Global_Debt.objects.none()

    try:
        defaultDate = single_debt_array[0].strftime("%Y-%m-%d")
    except:
        defaultDate = datetime.now().strftime("%Y-%m-%d")
    is_waiting = len(WaitingForChange.objects.filter(customer=request.user)) != 0

    Old_debts = Old_debt.objects.filter(customer=request.user)

    select_old_debt = []

    for old in Old_debts:
        select_old_debt.append({
                'name': f"{old.date}---{old.until}",
                'value': old.date
            })
    select_old_debt.reverse()
    SingleTables += writng_tables
    return render(request, 'tablesbyUser.html', {
        'table': join_page_obj,
        'defaultDate': defaultDate,
        'tables': reversed_table_page_obj,
        'joins': reversed_join_page_obj,
        # 'Rows': tableRows,
        "SingleRows": SingleRows ,
        "JoinRows": JoinRows ,
        'select_date': select_old_debt,


        # 'singleTables': reversed_single_page_obj,
        'singleTables': SingleTables,
        'joinedDebt': debt_array,
        # 'singleDebt': reversed_single_debt_obj,
        'weekPaymant': weekPaymant,
        'weekDebt': week_debt,
        'oldDebt': old_debt,
        'globalDebt': globalDebt,
        'is_waiting': is_waiting
    })



def gavar_cucak(request, user_id):
    user = User.objects.get(id=user_id)
    page_number = request.GET.get('page')
    # Joined Tables
    joinedTables = JoinedTables.objects.filter(
        customer=User.objects.get(username="171"),
    ).order_by('timeOfCreating')  # Reverse the order by '-id'
    joinPaginator = Paginator(joinedTables, 5)
    join_page_obj = joinPaginator.get_page(page_number)

    reversed_join_page_for_debt = joinPaginator.get_page(
        joinPaginator.num_pages - join_page_obj.number + 1
    )
    debt_array = []
    tables = []
    for i in reversed_join_page_for_debt:
        try:
            tab = SingleTable.objects.get(
                    customer=user,
                    dateOfCreating=i.dateOfCreating
                )
            tables.append(tab)
            debt = Debt.objects.get(
                date=i.dateOfCreating,
                single=True,
                customer=user
            )
            print(debt)
            debt_array.append([str(i.dateOfCreating), "", debt.debt])
        except:
            debt_array.append([str(i.dateOfCreating), "", ""])

    SingleRows = TableItem.objects.filter(customer=user).filter(table__singleTable__in = tables)
    print(SingleRows)
    SingleTables = []
    for i in tables:
        t = UserTable.objects.get(singleTable=i)
        SingleTables.append(t)

    globalDebt = Global_Debt.objects.filter(customer=user).latest('timeOfCreating')
    try:
        week_debt = Week_debt.objects.get(
            customer=user,
            date=debt_array[0][0]
        )
    except:
        week_debt = Week_debt.objects.none()

    try:
        old_debt = Old_debt.objects.get(
            customer=user,
            date=debt_array[0][0]
        )
    except:
        old_debt = Old_debt.objects.none()
    try:
        weekPaymant = Paymant.objects.get(
            customer=user,
            date=debt_array[0][0]
        )
    except:
        weekPaymant = Paymant.objects.none()


    return render(request, "customerTables.html", {
        "customer": user,
        'joinedDebt': debt_array,
        "SingleRows": SingleRows,
        'singleTables': SingleTables,
        'globalDebt': globalDebt,
        'weekDebt': week_debt,
        'oldDebt': old_debt,

        'table': join_page_obj,
        'weekPaymant': weekPaymant,

    })



def gavar_dproc_cucak(request):
    user = request.user
    page_number = request.GET.get('page')
    # Joined Tables
    joinedTables = JoinedTables.objects.filter(
        customer=User.objects.get(username="171"),
    ).order_by('timeOfCreating')  # Reverse the order by '-id'
    joinPaginator = Paginator(joinedTables, 5)
    join_page_obj = joinPaginator.get_page(page_number)

    reversed_join_page_for_debt = joinPaginator.get_page(
        joinPaginator.num_pages - join_page_obj.number + 1
    )
    debt_array = []
    tables = []
    for i in reversed_join_page_for_debt:
        try:
            tab = SingleTable.objects.get(
                    customer=user,
                    dateOfCreating=i.dateOfCreating
                )
            tables.append(tab)
            debt = Debt.objects.get(
                date=i.dateOfCreating,
                single=True,
                customer=user
            )
            print(debt)
            debt_array.append([str(i.dateOfCreating), "", debt.debt])
        except:
            debt_array.append([str(i.dateOfCreating), "", ""])

    SingleRows = TableItem.objects.filter(customer=user).filter(table__singleTable__in = tables)
    print(SingleRows)
    SingleTables = []
    for i in tables:
        t = UserTable.objects.get(singleTable=i)
        SingleTables.append(t)

    globalDebt = Global_Debt.objects.filter(customer=user).latest('timeOfCreating')
    try:
        week_debt = Week_debt.objects.get(
            customer=user,
            date=debt_array[0][0]
        )
    except:
        week_debt = Week_debt.objects.none()

    try:
        old_debt = Old_debt.objects.get(
            customer=user,
            date=debt_array[0][0]
        )
    except:
        old_debt = Old_debt.objects.none()
    try:
        weekPaymant = Paymant.objects.get(
            customer=user,
            date=debt_array[0][0]
        )
    except:
        weekPaymant = Paymant.objects.none()

    is_waiting = len(WaitingForChange.objects.filter(customer=request.user)) != 0
    try:
        defaultDate = debt_array[0][0].strftime("%Y-%m-%d")
    except:
        defaultDate = datetime.now().strftime("%Y-%m-%d")

    select_old_debt = []
    Old_debts = Old_debt.objects.filter(customer=request.user)
    for old in Old_debts:
        select_old_debt.append({
                'name': f"{old.date}---{old.until}",
                'value': old.date
            })
    select_old_debt.reverse()
    print(select_old_debt)

    return render(request, "tablesbyUser.html",{
        "customer": user,
        'joinedDebt': debt_array,
        "SingleRows": SingleRows,
        'singleTables': SingleTables,
        'globalDebt': globalDebt,
        'weekDebt': week_debt,
        'oldDebt': old_debt,

        'table': join_page_obj,
        'weekPaymant': weekPaymant,
        'is_waiting': is_waiting,
        'defaultDate': defaultDate,
        'select_date': select_old_debt
    })



@customer_required
def mistakes(request, table_id):
    # kara vtangavor lini ete idnery hamnknen
    try:
        table = UserTable.objects.get(id = table_id)
        rows = TableItem.objects.filter(table=table)
        context = {
            'table_id': table_id,
            'table': table,
            'rows': rows,
            'is_joined': False,
        }
    except:
        table = JoinedTables.objects.get(id = table_id)
        mid = [TableItem.objects.filter(table = tab) for tab in UserTable.objects.filter(joinedTable = table)]
        rows = []
        for tab in mid:
            for i in tab:
                rows.append(i)
        context = {
            'table_id': table_id,
            'table': table,
            'rows': rows,
            'is_joined': True,
        }
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        us1 = ['Գանձակ', 'Սարուխան']
        us2 = ['Գ.4-րդ', 'Գ.ավագ', 'Արա']
        ohan = User.objects.get(username="Օհան")
        kamo = User.objects.get(username="Կամո")
        for item in data:
            table_item = TableItem.objects.get(id=item["product_id"])
            # if table_item.supplier == "Այլ.ապրանք"։
            #     update_or_create_tmp_value(table_item.product_name, table_item.table.dateOfCreating, table_item.product_count - tochange_item.newCount)
            if table_item.customer in us1:
                us = kamo
            elif table_item.customer in us2:
                us = ohan
            else:
                us = table_item.customer
            # print(table_item.supplier)
            if table_item.table.joinedTable:
                WaitingForChange.objects.create(
                    table_item=table_item,
                    newTotal=item['total_price'],
                    newCount=item['product_count'],
                    customer=table_item.customer,
                    date=table_item.table.joinedTable.dateOfCreating
                )
                try:
                    ordered_Itmes.objects.get(getId=table_item.id)
                    supplier_Mistakes.objects.create(
                        item = table_item,
                        newCount=item['product_count'],
                        oldCount=table_item.product_count,
                        customer=us,
                        supplier= table_item.supplier,
                        date=table_item.table.joinedTable.dateOfCreating
                    )
                except:
                    pass
            else:
                if request.user.username in  ['Էրանոս','Լիճք', 'Մ.1ին','Մ.ավագ', 'Զոլ.2րդ', 'Զոլ.1ին', 'Ծովինար']:
                    try:
                        WaitingForChange.objects.create(
                            table_item=table_item,
                            newTotal=item['total_price'],
                            # oldCount=table_item.product_count,
                            newCount=item['product_count'],
                            customer=table_item.customer,
                            date=table_item.table.singleTable.dateOfCreating
                        )
                    except:
                        WaitingForChange.objects.create(
                            table_item=table_item,
                            newTotal=item['total_price'],
                            # oldCount=table_item.product_count,
                            newCount=item['product_count'],
                            customer=table_item.customer,
                            date=table_item.table.dateOfCreating
                        )
                else:
                    WaitingForChange.objects.create(
                                table_item=table_item,
                                newTotal=item['total_price'],
                                # oldCount=table_item.product_count,
                                newCount=item['product_count'],
                                customer=table_item.customer,
                                date=table_item.table.singleTable.dateOfCreating
                            )
                try:
                    ordered_Itmes.objects.get(getId=table_item.id)
                    supplier_Mistakes.objects.create(
                        item = table_item,
                        newCount=item['product_count'],
                        oldCount=table_item.product_count,
                        customer=us,
                        supplier= table_item.supplier,
                        date=table_item.table.dateOfCreating
                    )
                except:
                    pass
        changeList = WaitingForChange.objects.all()
    return render(request, 'mistakes.html', context)

@customer_required
def change(request):
    if request.user.username == 'Օհան':
        customers = [
        User.objects.get(username='Օհան'), User.objects.get(username='Գ.4-րդ'),
        User.objects.get(username='Գ.ավագ'), User.objects.get(username='Արա')
        ]
        rows = WaitingForChange.objects.filter(customer__in=customers)
        return render(request, 'changes.html', {'rows': rows})
    elif request.user.username == 'Կամո':
        customers = [
        User.objects.get(username='Կամո'),
        User.objects.get(username='Գանձակ'),
        User.objects.get(username='Սարուխան')
        ]
        rows = WaitingForChange.objects.filter(customer__in=customers)
        return render(request, 'changes.html', {'rows': rows})
    rows = WaitingForChange.objects.filter(customer=request.user)
    return render(request, 'changes.html', {'rows': rows})

@login_required
def delChange(request, item_id):
    item = WaitingForChange.objects.get(id=item_id)
    item.delete()
    if request.user.is_customer:
        return HttpResponseRedirect('/account/changes')
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# ******** for supplier

@employee_or_supplier_required
def resetRejectOrEndorse(request, item_id):
    tochange_item = supplier_Mistakes.objects.get(id=item_id)
    tochange_item.endorsed = False
    tochange_item.rejected = False
    tochange_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def delete_sup_Change(request, item_id):
    mistake = supplier_Mistakes.objects.get(id=item_id)
    mistake.rejected = True
    # print(mistake)
    mistake.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def endorse_sup_Change(request, item_id):
    # item = TableItem.objects.get(id = item_id)
    mistake = supplier_Mistakes.objects.get(id=item_id)
    mistake.endorsed = True
    # print(mistake)
    mistake.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
# ******** for supplier




# ******** for employee
def endorse_suppliers_mistake(request, item_id):
    item = TableItem.objects.get(id=item_id)
    mistake = supplier_Mistakes.objects.get(item=item)
    try:
        element = ordered_Itmes.objects.get(getId = item.id)
    except:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    # update_or_create_tmp_value(item.product_name, item.table.dateOfCreating, element.productCount - mistake.newCount)
    element.productCount = mistake.newCount
    element.save()
    mistake.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def reject_suppliers_mistake(request, item_id):
    mistake = supplier_Mistakes.objects.get(id=item_id)
    mistake.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
# ******** for employee

# ========================== Customer End  ===================

# ////////////////////////// Employee Start //////////////////

@employee_required
def employee(request):
    is_waiting = len(WaitingForChange.objects.all()) != 0
    sups = User.objects.filter(is_supplier=True)
    arr = []
    for sup in sups:
        arr.append([sup, len(supplier_Mistakes.objects.filter(supplier=sup)) == 0])

    is_employee = False
    if request.user.username == "Վարդգես":
        is_employee = True
    # for i in TableItem.objects.filter(customer=User.objects.get(username='Կամո')):
        # print(i.supplier, i.product_name)
    return render(request, 'employee.html', {
        'is_waiting': is_waiting,
        'suppliers': arr,
        "is_employee": is_employee
    })


@employee_required
def is_available(request):
    items = ItemsModel.get_all_unique_items()
    return render(request, "summer2024/employee_item_is_avsailable.html", {
        'rows':items
    })

@employee_required
def toggle_availability(request, item_name):
    print(item_name)
    items = ItemsModel.objects.filter(productName=item_name)

    for i in items:
        i.is_available = not i.is_available
        i.save()
    return redirect("is_available")


@employee_required
def otherItems(request):
    # schools = [
    #     '148', '189', '54', '170', '104', '136', '171', '117', '177', '48', '60', '87',
    #     '90', '188', '196', '115', '44','Դավիթ','Օհան','Գ.4-րդ', 'Գ.ավագ', 'Արա','Կամո','Գանձակ', 'Սարուխան','Էրանոս','Լիճք', 'Մ.1ին',
    #     'Մ.ավագ', 'Զոլ.2րդ', 'Զոլ.1ին', 'Ծովինար', "Գավառ_ավագ","Գավառ_4րդ", "Գավառ_5րդ", "Գ_սարուխան", "Գ_հացառատ2","Գ_գանձակ",
    #     ]
    # supplier = User.objects.get(username='Այլ.ապրանք')
    # tableRows = BigTableRows.objects.filter(supplier=supplier)
    # bigTables = BigTable.objects.filter(supplier=supplier)
    is_waiting = len(WaitingForChange.objects.all()) != 0
    # uniq = ItemsModel.uniqueProductNames(None).filter(supplier='Այլ.ապրանք')
    return render(
        request,
        "otherItems.html",
        {
            # 'Products': uniq,
            # 'TableRows': tableRows,
            # 'BigTables': bigTables,
            # 'supplier': supplier,
            # 'schools': schools,
            'is_waiting': is_waiting
        }
                  )


@employee_required
def mainItems(request):
    # schools = [
    #     '148', '189', '54', '170', '104', '136', '171', '117', '177', '48', '60', '87',
    #     '90', '188', '196', '115','44', 'Դավիթ','Օհան','Գ.4-րդ', 'Գ.ավագ', 'Արա','Կամո','Գանձակ', 'Սարուխան','Էրանոս','Լիճք', 'Մ.1ին',
    #     'Մ.ավագ', 'Զոլ.2րդ', 'Զոլ.1ին', 'Ծովինար'
    #     ]
    # uniq = ItemsModel.uniqueProductNames(None).filter(supplier__in=['Արտադրամաս', 'Փուռ','Կիրովական'])
    # suppliers = []
    # for i in ['Արտադրամաս','Փուռ','Կիրովական']:
    #     suppliers.append(User.objects.get(username=i))
    # tableRows = BigTableRows.objects.filter(supplier__in=suppliers)
    # bigTables = BigTable.objects.filter(supplier__in=suppliers)
    is_waiting = len(WaitingForChange.objects.all()) != 0
    return render(
        request,
        "mainItems.html",
        {
            # 'Products': uniq,
            # 'TableRows': tableRows,
            # 'BigTables': bigTables,
            # 'Suppliers': suppliers,
            # 'schools': schools,
            'is_waiting': is_waiting

        }
                  )


@employee_required
def main_items_api(request):
    start_time = time.time()  # Record the start time

    is_employee = False
    if request.user.username == "Վարդգես":
        is_employee = True
    schools = [
        # '148',
        '189', "50",
        # '54',
        '170', '104', '136', '171', '117', '177', '48', '60', '87',
        '90', '188', '196', '115', '44', '52', '163','143','140','154','66','144','Չարբախ_1','106','35',"35_փոքր",'93',"91",
        "134", "38","195", "94", "53","161",
        'Դավիթ','Օհան','Գ.4-րդ', 'Գ.ավագ', 'Արա','Կամո','Գանձակ', 'Սարուխան','Էրանոս','Լիճք', 'Մ.1ին',
        'Մ.ավագ', 'Զոլ.2րդ', 'Զոլ.1ին', 'Ծովինար'
    ]
    uniq = ItemsModel.uniqueProductNames(None).filter(supplier__in=['Արտադրամաս',"Ռաֆո", "Հայկ",'Փուռ','Կիրովական'])
    suppliers = []
    for i in ['Արտադրամաս',"Ռաֆո", "Հայկ",'Փուռ','Կիրովական']:
        suppliers.append(User.objects.get(username=i))
    tableRows = BigTableRows.objects.filter(supplier__in=suppliers)
    bigTables = BigTable.objects.filter(supplier__in=suppliers)
    school_order = {school: i for i, school in enumerate(schools)}
    sorted_columns = sorted(bigTables, key=lambda col: school_order.get(col.user.username, len(schools)))
    # Convert QuerySets to dictionaries

    uniq_data = [item for item in uniq]

    tableRows_data = [
        {
            # "id": item.id,
            "user": item.user.username,
            "supplier_id": item.supplier.id,
            "porductName": item.porduct_name,
            'productCount': item.item.product_count,
            'totalPrice': item.item.total_price if is_employee else 0,
            'table': item.item.table.id,
            "supTotal": item.item.supTotal if is_employee else 0
        } for item in tableRows
    ]
    bigTables_data = [{
            # 'id': item.id,
            'supplier_id': item.supplier_id,
            'user': item.user.username,
            'modifiedDate': item.modifiedDate,
            'table': item.table.id
        } for item in sorted_columns]

    response_data = {
        'Products': uniq_data,
        'TableRows': tableRows_data,
        'BigTables': bigTables_data,
        'Suppliers': [{'id': supplier.id, 'username': supplier.username} for supplier in suppliers],
    }

    # Calculate the time taken
    end_time = time.time()
    execution_time = end_time - start_time
    # print(f"Execution Time: {execution_time} seconds")

    return JsonResponse(response_data, safe=False)

@employee_required
def other_items_api(request):
    start_time = time.time()  # Record the start time

    is_employee = False
    if request.user.username == "Վարդգես":
        is_employee = True

    schools = [
        # '148',
        '189', "50",
        # '54',
        '170', '104', '136', '171', '117', '177', '48', '60', '87',
        '90', '188', '196', '115', '44', '52', '163','143','140','154','66','144','Չարբախ_1','106','35',"35_փոքր",'93',"91",
        "134", "38","195","94", "53","161",
        'Դավիթ','Օհան','Գ.4-րդ', 'Գ.ավագ', 'Արա','Կամո','Գանձակ', 'Սարուխան','Էրանոս','Լիճք', 'Մ.1ին',
        'Մ.ավագ', 'Զոլ.2րդ', 'Զոլ.1ին', 'Ծովինար', "Գավառ_ավագ","Գավառ_4րդ", "Գավառ_5րդ", "Գ_սարուխան", "Գ_հացառատ2","Գ_գանձակ"
        ]
    uniq = ItemsModel.uniqueProductNames(None).filter(supplier__in=['Այլ.ապրանք'])
    suppliers = []
    for i in ['Այլ.ապրանք']:
        suppliers.append(User.objects.get(username=i))
    tableRows = BigTableRows.objects.filter(supplier__in=suppliers)
    bigTables = BigTable.objects.filter(supplier__in=suppliers)
    school_order = {school: i for i, school in enumerate(schools)}
    sorted_columns = sorted(bigTables, key=lambda col: school_order.get(col.user.username, len(schools)))
    # Convert QuerySets to dictionaries

    uniq_data = [item for item in uniq]

    tableRows_data = [
        {
            # "id": item.id,
            "user": item.user.username,
            "supplier_id": item.supplier.id,
            "porductName": item.porduct_name,
            'productCount': item.item.product_count,
            'totalPrice': item.item.total_price if is_employee else 0,
            'table': item.item.table.id,
            "supTotal": item.item.supTotal if is_employee else 0
        } for item in tableRows
    ]
    bigTables_data = [{
            # 'id': item.id,
            'supplier_id': item.supplier_id,
            'user': item.user.username,
            'modifiedDate': item.modifiedDate,
            'table': item.table.id
        } for item in sorted_columns]

    response_data = {
        'Products': uniq_data,
        'TableRows': tableRows_data,
        'BigTables': bigTables_data,
        'Suppliers': [{'id': supplier.id, 'username': supplier.username} for supplier in suppliers],
    }

    # Calculate the time taken
    end_time = time.time()
    execution_time = end_time - start_time
    # print(f"Execution Time: {execution_time} seconds")

    return JsonResponse(response_data, safe=False)





@employee_required
def allCustomers(request):
    allCustomers = []
    # schools = [
    #     '148', '189', '54', '170', '104', '136', '171', '117', '177', '48', '60', '87',
    #     '90', '188', '196', '115', '44', "91", 'Դավիթ','Օհան','Գ.4-րդ', 'Գ.ավագ', 'Արա','Կամո','Գանձակ', 'Սարուխան','Էրանոս','Լիճք', 'Մ.1ին',
    #     'Մ.ավագ', 'Զոլ.2րդ', 'Զոլ.1ին', 'Ծովինար', "Խանութ", "Գավառ_ավագ","Գավառ_4րդ", "Գավառ_5րդ", "Գ_սարուխան", "Գ_հացառատ2","Գ_գանձակ"
    #     ]
    is_employee = False
    if request.user.username == "Վարդգես":
        is_employee = True

    ohan_Users = ['Գ.4-րդ', 'Գ.ավագ', 'Արա']
    kamo_Users = ['Գանձակ', 'Սարուխան']


    for i in schools:
        allCustomers.append(User.objects.get(username=i))
    allSuppliers = User.objects.filter(is_supplier = True)
    globDebts = []
    for cust in allCustomers:
        try:
            if cust.username in ohan_Users or cust.username in kamo_Users or cust.username == "Օհան" or cust.username == "Կամո":
                # latest_global = Global_Debt.objects.filter(customer=cust).latest('timeOfCreating')
                globDebts.append([cust, '---', len(WaitingForChange.objects.filter(customer=cust)) != 0])
                continue
            latest_global = Global_Debt.objects.filter(customer=cust).latest('timeOfCreating')
            globDebts.append([cust, latest_global.debt if is_employee else 0, len(WaitingForChange.objects.filter(customer=cust)) != 0])
            # print(cust.id)
        except:
            globDebts.append([cust, 0, len(WaitingForChange.objects.filter(customer=cust)) != 0])

    ohanDebt = Global_Debt.objects.filter(customer=User.objects.get(username='Օհան')).latest('timeOfCreating').debt
    kamoDebt = Global_Debt.objects.filter(customer=User.objects.get(username='Կամո')).latest('timeOfCreating').debt

    return render(request, 'work.html',{
        'allCustomers':allCustomers,
        'debts': globDebts,
        'allSuppliers': allSuppliers,
        'ohanDebt': ohanDebt if is_employee else 0,
        'kamoDebt': kamoDebt if is_employee else 0,

    })

@employee_or_supplier_required
def endorse(request, user_id):
    page_user = User.objects.get(id=user_id)
    rows = WaitingForChange.objects.filter(customer=page_user)
    ohan_Users = ['Գ.4-րդ', 'Գ.ավագ', 'Արա']
    kamo_Users = ['Գանձակ', 'Սարուխան']
    if page_user.username in ohan_Users and request.user.is_supplier:
        page_user = User.objects.get(username="Օհան")
    elif page_user.username in kamo_Users and request.user.is_supplier:
        page_user = User.objects.get(username="Կամո")
    if request.user.is_supplier:
        new_rows = []
        for i in rows:
            if i.table_item.supplier == request.user:
                new_rows.append(i)
        rows = new_rows.copy()
    return render(request, 'endorse.html', {'rows': rows, 'customer':page_user})

@employee_or_supplier_required
def endorse_supplier(request, user_id):
    if request.user.is_supplier:
        supplier = request.user
    else:
        supplier = User.objects.get(id=user_id)
    mistakes = supplier_Mistakes.objects.filter(
        supplier = supplier
    )

    return render(request, 'supplier_endorse.html', {'rows': mistakes, 'page_user': supplier})


# @employee_or_supplier_required
# def resetRejectOrEndorse(request, item_id):
#     tochange_item = WaitingForChange.objects.get(id=item_id)
#     tochange_item.endorsed = False
#     tochange_item.rejected = False
#     tochange_item.save()
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def get_week_debt_for_debt(debt):
    old_debt = Old_debt.objects.filter(
        customer=debt.customer,
        date__lte=debt.date,
        until__gte=debt.date
    ).first()
    week_debt = Week_debt.objects.get(customer=old_debt.customer, date = old_debt.date)
    return week_debt

def get_old_debt_for_debt(debt):
    old_debt = Old_debt.objects.filter(
        customer=debt.customer,
        date__lte=debt.date,
        until__gte=debt.date
    ).first()
    return old_debt

def changeNext_oldDebt(date, user, debt):
    next_old_date = date + timedelta(days=7)
    try:
        old_debt = Old_debt.objects.get(
            customer = user,
            date = date
        )
        print(debt, 'debt', date)
        old_debt.debt -= debt
        old_debt.save()
        print(date, debt , old_debt.debt , 'old debt succsesfull')
        try:
            week_debt = Week_debt.objects.get(
                customer = user,
                date = date
            )
            week_debt.debt -= debt
            week_debt.save()
            print(date, debt , week_debt.debt , 'week debt succsesfull')
        except:
            pass
        changeNext_oldDebt(next_old_date, user, debt)
    except:
        return
        # return print(date, 'reject')

def format_date_str(date_str):
    date_str = str(date_str)
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    formatted_date = date_obj.strftime('%d.%m.%Y')
    return formatted_date

writing_items_array = ItemsModel.uniqueProductNames("Գրենական")

@employee_or_supplier_required
def endorseChange(request, item_id):
    ohan_Users = ['Գ.4-րդ', 'Գ.ավագ', 'Արա']
    kamo_Users = ['Գանձակ', 'Սարուխան']
    ohan = User.objects.get(username="Օհան")
    kamo = User.objects.get(username="Կամո")
    writing_items_list = []
    for i in writing_items_array:
        writing_items_list.append(i["productName"])
    try:
        item = TableItem.objects.get(id=item_id)
    except:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    # item = TableItem.objects.get(id=item_id)
    tochange_item = WaitingForChange.objects.get(table_item=item)
    prodName = tochange_item.table_item.product_name

    product = ItemsModel.objects.get(customer=item.customer.username, productName=item.product_name)
    sup_price = product.supPrice
    difference = item.total_price - tochange_item.newTotal

    date_format = '%d.%m.%Y'  # Specify the format of the date string


    if item.customer.username in ohan_Users:
        latest_global_debt = Global_Debt.objects.filter(customer=ohan).latest('timeOfCreating')
        Global_Debt.objects.create(
            customer = ohan,
            date = tochange_item.date,
            debt = latest_global_debt.debt - difference,
        )
        if tochange_item.table_item.table.joinedTable:
            tochange_debt = Debt.objects.get(
                date=tochange_item.date,
                customer=tochange_item.customer,
                joined=True,
            )
        else:
            tochange_debt = Debt.objects.get(
                date=tochange_item.date,
                customer=tochange_item.customer,
                single=True,
            )
        ohan_debt = Debt.objects.get(
            date=tochange_item.date,
            customer=ohan,
            joined=True
        )
        try:
            # week_debt = get_week_debt_for_debt(ohan_debt)
            # week_debt.debt -= difference
            # week_debt.save()
            # date_object = datetime.strptime(format_date_str(week_debt.date), date_format)
            # next_week = date_object + timedelta(days=7)
            # changeNext_oldDebt(next_week, week_debt.customer, difference)
            debt_old = get_old_debt_for_debt(ohan_debt)
            debt_old.debt += difference # arajin partqin gumarum u hanum enq nor difference-y
            debt_old.save()
            date_object = datetime.strptime(format_date_str(ohan_debt.date), date_format)
            # next_week = date_object + timedelta(days=7)

            changeNext_oldDebt(date_object, tochange_item.customer, difference)
        except:
            pass
        tochange_debt.debt -= difference
        tochange_debt.save()
        ohan_debt.debt -= difference
        ohan_debt.save()

        item.product_count = tochange_item.newCount
        item.total_price = tochange_item.newTotal
        item.supTotal = tochange_item.newCount * sup_price
        item.save()
        tochange_item.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    elif item.customer.username in kamo_Users:
        latest_global_debt = Global_Debt.objects.filter(customer=kamo).latest('timeOfCreating')
        Global_Debt.objects.create(
            customer = kamo,
            date = tochange_item.date,
            debt = latest_global_debt.debt - difference,
        )
        if tochange_item.table_item.table.joinedTable:
            tochange_debt = Debt.objects.get(
                date=tochange_item.date,
                customer=tochange_item.customer,
                joined=True,
            )
        else:
            tochange_debt = Debt.objects.get(
                date=tochange_item.date,
                customer=tochange_item.customer,
                single=True,
            )
        kamo_debt = Debt.objects.get(
            date=tochange_item.date,
            customer=kamo,
            joined=True
        )
        try:
            # week_debt = get_week_debt_for_debt(kamo_debt)
            # week_debt.debt -= difference
            # week_debt.save()
            # date_object = datetime.strptime(format_date_str(week_debt.date), date_format)
            # next_week = date_object + timedelta(days=7)
            # changeNext_oldDebt(next_week, week_debt.customer, difference)

            debt_old = get_old_debt_for_debt(kamo_debt)
            debt_old.debt += difference # arajin partqin gumarum u hanum enq nor difference-y
            debt_old.save()
            date_object = datetime.strptime(format_date_str(kamo_debt.date), date_format)
            # next_week = date_object + timedelta(days=7)

            changeNext_oldDebt(date_object, tochange_item.customer, difference)

        except:
            pass
        tochange_debt.debt -= difference
        tochange_debt.save()
        kamo_debt.debt -= difference
        kamo_debt.save()

        item.product_count = tochange_item.newCount
        item.total_price = tochange_item.newTotal
        item.supTotal = tochange_item.newCount * sup_price
        item.save()
        tochange_item.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    latest_global_debt = Global_Debt.objects.filter(customer=tochange_item.customer).latest('timeOfCreating')

    if tochange_item.table_item.table.joinedTable:
        tochange_debt = Debt.objects.get(
            date=tochange_item.date,
            customer=tochange_item.customer,
            joined=True,
        )
    else:
        print(writing_items_list, 'grenakan')
        if prodName in writing_items_list:
            try:
                tochange_debt = Debt.objects.get(
                    date=tochange_item.date,
                    customer=tochange_item.customer,
                    single=False,
                    joined=False
                )
            except:
                pass
                # try:
                #     tochange_debt = Debt.objects.get(
                #         date=tochange_item.date,
                #         customer=tochange_item.customer,
                #         single=True,
                #     )
                # except:
                #     print(tochange_item.customer.username, "chka")
        else:
            tochange_debt = Debt.objects.get(
                date=tochange_item.date,
                customer=tochange_item.customer,
                single=True,
            )
    tochange_debt.debt -= difference
    tochange_debt.save()
    try:
        debt_old = get_old_debt_for_debt(tochange_debt)
        debt_old.debt += difference # arajin partqin gumarum u hanum enq nor difference-y
        debt_old.save()
        date_object = datetime.strptime(format_date_str(debt_old.date), date_format)
        # next_week = date_object + timedelta(days=7)

        changeNext_oldDebt(date_object, tochange_item.customer, difference)
    except:
        pass

    glob_debt = Global_Debt.objects.create(
        customer = tochange_item.customer,
        date = tochange_item.date,
        debt = latest_global_debt.debt - difference,
    )
    glob_debt.save()
    latest_global_debt.delete()

    # update_or_create_tmp_value(item.product_name, item.table.dateOfCreating, item.product_count - tochange_item.newCount)

    item.product_count = tochange_item.newCount
    item.total_price = tochange_item.newTotal
    item.supTotal = tochange_item.newCount * sup_price
    item.save()
    tochange_item.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@employee_required
def customerTables(request, user_id):
    user = User.objects.get(id=user_id)
    if user.username in ["Գավառ_ավագ","Գավառ_4րդ", "Գավառ_5րդ", "Գ_սարուխան", "Գ_հացառատ2","Գ_գանձակ"]:
        return redirect("cucak_gavar",user_id)
    page_number = request.GET.get('page')
    # Joined Tables
    joinedTables = JoinedTables.objects.filter(
        customer=user,
    ).order_by('timeOfCreating')  # Reverse the order by '-id'
    joinPaginator = Paginator(joinedTables, 5)  # show 5 joinedTables per page
    join_page_obj = joinPaginator.get_page(page_number)
    reversed_join_page_obj = joinPaginator.get_page(
        joinPaginator.num_pages - join_page_obj.number + 1
    ).__reversed__()  # Reversed join_page_obj
    reversed_join_page_copy = joinPaginator.get_page(
        joinPaginator.num_pages - join_page_obj.number + 1
    ).__reversed__()  # Reversed join_page_obj
    reversed_join_page_for_debt = joinPaginator.get_page(
        joinPaginator.num_pages - join_page_obj.number + 1
    )  # Reversed join_page_obj
    reversed_table_page_obj = []
    for join in reversed_join_page_copy:
        try:
            joins = UserTable.objects.filter(
                user=user,
                joinedTable=join,
            )
            for jo in joins:
                reversed_table_page_obj.append(jo)
        except:
            continue
    JoinRows = []
    for tab in reversed_table_page_obj:
        try:
            row = TableItem.objects.filter(
                customer=user,
                table=tab
            )
            for r in row:
                JoinRows.append(r)
        except:
            continue
    # Joined Tables
    single_debt_array = []
    debt_array = []
    for i in reversed_join_page_for_debt:
        try:
            joinedDebt = Debt.objects.get(
                customer=user,
                joined=True,
                date=i.dateOfCreating
            )
            theDebt = [str(i.dateOfCreating), joinedDebt.debt, ""]
            if joinedDebt.date not in single_debt_array:
                single_debt_array.append(joinedDebt.date)
            try:
                singleDebt = Debt.objects.get(
                    customer=user,
                    single=True,
                    date=i.dateOfCreating
                )
                # if singleDebt.date not in single_debt_array:
                #     single_debt_array.append(singleDebt.date)
                theDebt[2] = singleDebt.debt
            except:
                pass
            debt_array.append(theDebt)
        except:
            continue

    writng_tables = []
    for date in single_debt_array:
        try:
            writing_tab = UserTable.objects.get(
                user = user,
                joinedTable__isnull = True,
                singleTable__isnull = True,
                dateOfCreating = date
            )
            writng_tables.append(writing_tab)
        except:
            continue

    for date in single_debt_array:
        try:
            debt = Debt.objects.get(
                customer = user,
                single=False,
                joined=False,
                date=date
            )
            theDebt = [str(date),'Գրենական',debt.debt]
            debt_array.append(theDebt)
        except:
            pass
    SingleTables = []
    SingleRows = []
    for table in writng_tables:
        try:
            row = TableItem.objects.filter(
                customer = user,
                table = table,
            )
            for r in row:
                SingleRows.append(r)
        except:
            continue
    for date in single_debt_array:
        try:
            singleTab = UserTable.objects.get(
                user=user,
                singleTable__isnull=False,
                dateOfCreating=date
            )
            SingleTables.append(singleTab)
        except:
            continue

    for table in SingleTables:
        try:
            row = TableItem.objects.filter(
                customer=user,
                table=table,
            )
            for r in row:
                SingleRows.append(r)
        except:
            continue
    # Single Tables
    try:
        weekPaymant = Paymant.objects.get(
            customer=user,
            date=single_debt_array[0]
        )
    except:
        weekPaymant = Paymant.objects.none()

    try:
        week_debt = Week_debt.objects.get(
            customer=user,
            date=single_debt_array[0]
        )
    except:
        week_debt = Week_debt.objects.none()

    try:
        old_debt = Old_debt.objects.get(
            customer=user,
            date=single_debt_array[0]
        )
        print(old_debt, "aram")
    except:
        old_debt = Old_debt.objects.none()
        print(single_debt_array[0], 'blya')

    try:
        globalDebt = Global_Debt.objects.filter(customer=user).latest('timeOfCreating')
    except:
        globalDebt = Global_Debt.objects.none()

    try:
        defaultDate = single_debt_array[0].strftime("%Y-%m-%d")
    except:
        defaultDate = datetime.now().strftime("%Y-%m-%d")
    SingleTables += writng_tables
    # print(writing_tables)
    return render(request, 'customerTables.html', {
        'table': join_page_obj,
        'defaultDate': defaultDate,
        'tables': reversed_table_page_obj,
        'joins': reversed_join_page_obj,
        # 'Rows': tableRows,
        "SingleRows": SingleRows,
        "JoinRows": JoinRows,
        # 'singleTables': reversed_single_page_obj,
        'singleTables': SingleTables,
        'joinedDebt': debt_array,
        # 'singleDebt': reversed_single_debt_obj,
        'weekPaymant': weekPaymant,
        'weekDebt': week_debt,
        'oldDebt': old_debt,
        'globalDebt': globalDebt,
        'customer': user
    })


def tables_by_ohan(request):
    page_number = request.GET.get('page')
    # Joined Tables
    ohan_User = User.objects.get(username='Օհան')
    joinedTables = JoinedTables.objects.filter(
        customer=ohan_User,
        ).order_by('timeOfCreating')  # Reverse the order by '-id'

    joinPaginator = Paginator(joinedTables, 5)  # show 5 joinedTables per page
    join_page_obj = joinPaginator.get_page(page_number)
    reversed_join_page_obj = joinPaginator.get_page(
            joinPaginator.num_pages - join_page_obj.number + 1
        ).__reversed__()  # Reversed join_page_obj
    # print(reversed_join_page_obj,"Joined Tables reversed")
    customers = [
        User.objects.get(username='Օհան'), User.objects.get(username='Գ.4-րդ'),
        User.objects.get(username='Գ.ավագ'), User.objects.get(username='Արա')
        ]

    tables = []

    joinedTables_array = []
    for ohan_join in reversed_join_page_obj:
        print(ohan_join,'Ohan join')
        mini_arr = []
        tables.append(ohan_join)
        for join in JoinedTables.objects.filter(dateOfCreating = ohan_join.dateOfCreating, customer__in = customers):
            mini_arr.append(join)
        print(mini_arr)
        joinedTables_array.append(mini_arr)

    # print(joinedTables_array)

    joined_Max = []
    for i in joinedTables_array:
        for j in i:
            joined_Max.append(j)

    # print(joined_Max, "max")

    userTables = UserTable.objects.filter(joinedTable__in = joined_Max)

    userTables_array = []
    for us in userTables:
        userTables_array.append(us)
    print(userTables_array, "user tables")
    suppliers = ['Արտադրամաս','Փուռ','Կիրովական']
    uniq = ItemsModel.productsfor_Customer(ohan_User)
    rows = []
    for joined_arr in joinedTables_array:
        mini_rows = []
        # print(joined_arr)
        for joinedTable in joined_arr:
            table_Rows = []
            for userTable in userTables_array:
                if userTable.joinedTable == joinedTable:
                    for product in uniq:
                        if product.supplier in suppliers:
                            try:
                                if joinedTable.customer.username == 'Օհան':
                                    us = 'ohan'
                                elif joinedTable.customer.username == 'Գ.4-րդ':
                                    us = 'gavar'
                                elif joinedTable.customer.username == 'Գ.ավագ':
                                    us = "avag"
                                elif joinedTable.customer.username == 'Արա':
                                    us = 'ara'
                                r = {
                                    'productName': product.productName,
                                    us: TableItem.objects.get(
                                        table=userTable,
                                        product_name=product.productName,
                                        customer=joinedTable.customer
                                )}
                                table_Rows.append(r)
                            except:
                                pass
            if joinedTable.customer.username == 'Օհան':
                ts = 'ohan'
            elif joinedTable.customer.username == 'Գ.4-րդ':
                ts = 'gavar'
            elif joinedTable.customer.username == 'Գ.ավագ':
                ts = "avag"
            elif joinedTable.customer.username == 'Արա':
                ts = 'ara'
            mini_rows.append({
                'table_name': f'{joinedTable.tableName}',
                ts : table_Rows
                })
        rows.append(mini_rows)
    # print(rows)
    complete_row = []

    for tab in tables:
        mini_comp = []
        ohan_total = 0
        gavar_total = 0
        avag_total = 0
        ara_total = 0
        big_total = 0
        for row in rows:
            # print(row[3]['ohan'])
            if row[3]['table_name'] == tab.tableName:
                for prod in uniq:
                    row_list = []
                    total_of_row = 0
                    row_list.append(prod.productName)
                        # print(ohan)
                    try:

                        for ohan in row[3]['ohan']:
                            if ohan['productName'] == prod.productName:
                                row_list.append(ohan['ohan'])
                                total_of_row += ohan['ohan'].total_price
                                ohan_total += ohan['ohan'].total_price
                                break
                        for gavar in row[2]['gavar']:
                            if gavar['productName'] == prod.productName:
                                row_list.append(gavar['gavar'])
                                total_of_row += gavar['gavar'].total_price
                                gavar_total += gavar['gavar'].total_price
                                break
                        for avag in row[1]['avag']:
                            if avag['productName'] == prod.productName:
                                row_list.append(avag['avag'])
                                total_of_row += avag['avag'].total_price
                                avag_total += avag['avag'].total_price
                                break
                        for ara in row[0]['ara']:
                            if ara['productName'] == prod.productName:
                                row_list.append(ara['ara'])
                                total_of_row += ara['ara'].total_price
                                ara_total += ara['ara'].total_price
                                break
                    except:
                        pass
                    row_list.append(total_of_row)
                    big_total += total_of_row
                    mini_comp.append(row_list)

                # print(mini_comp)
        complete_row.append({f'{tab.tableName}':mini_comp,'last_row': ['Ընդ', ohan_total, gavar_total, avag_total, ara_total, big_total]})

    joineddebt = Debt.objects.filter(
        customer = User.objects.get(username = "Օհան"),
        joined = True
        ).order_by('timeOfCreating')
    joineddebtPaginator = Paginator(joineddebt, 5) #show 5 debts per page of the joined tables
    joineddebt_page_obj = joineddebtPaginator.get_page(page_number)
    reversed_joined_debt_obj = joineddebtPaginator.get_page(
        joineddebtPaginator.num_pages - joineddebt_page_obj.number + 1
    )
    single_debt_array = []
    single_debt_dict = {}

    debt_array = []
    for table in tables[::-1]:
        try:
            debt = Debt.objects.get(date=table.dateOfCreating, customer = ohan_User, joined = True)
            debt_array.append([str(debt.date), debt.debt, ''])
        except:
            debt_array.append([str(table.dateOfCreating), 0, ''])
    # PAYMANT
    try:
        paymant = Paymant.objects.get(
            date = tables[-1].dateOfCreating,
            customer=customers[0]
        )
        total_payments_money = paymant.money
        total_payments_returned = paymant.returned
        total_payments_salary = paymant.salary
    except:
        total_payments_money = 0
        total_payments_returned = 0
        total_payments_salary = 0

    total_global_debt = 0
    try:
        old_debt = Old_debt.objects.get(date = tables[-1].dateOfCreating, customer=customers[0]).debt
    except:
        old_debt = 0

    try:
        new_debt = Week_debt.objects.get(date = tables[-1].dateOfCreating, customer=customers[0]).debt
    except:
        new_debt = 0

    total_global_debt = Global_Debt.objects.filter(customer=customers[0]).latest('timeOfCreating').debt

    is_waiting = WaitingForChange.objects.filter(customer__in=customers).count() != 0
    select_old_debt = []

    Old_debts = Old_debt.objects.filter(customer=customers[0])
    return render(request, 'drivers/tablesBYohan.html', {
        'Tables': tables,
        'CompleteRows': complete_row,
        "table" : join_page_obj,

        'joinedDebt': debt_array,
        'Returned': total_payments_returned,
        'Salary': total_payments_salary,
        'Money': total_payments_money,
        'GlobalDebt': total_global_debt,
        'OldDebt': old_debt,
        'NewDebt': new_debt,
    })

def tables_by_kamo(request):

    page_number = request.GET.get('page')
    # Joined Tables
    kamo_User = User.objects.get(username='Կամո')
    joinedTables = JoinedTables.objects.filter(
        customer=kamo_User,
        ).order_by('timeOfCreating')  # Reverse the order by '-id'
    joinPaginator = Paginator(joinedTables, 5)  # show 5 joinedTables per page
    join_page_obj = joinPaginator.get_page(page_number)
    reversed_join_page_obj = joinPaginator.get_page(
            joinPaginator.num_pages - join_page_obj.number + 1
        ).__reversed__()  # Reversed join_page_obj
    customers = [
        User.objects.get(username='Կամո'),
        User.objects.get(username='Գանձակ'),
        User.objects.get(username='Սարուխան')
        ]

    tables = []

    joinedTables_array = []
    for ohan_join in reversed_join_page_obj:
        mini_arr = []
        tables.append(ohan_join)
        for join in JoinedTables.objects.filter(dateOfCreating = ohan_join.dateOfCreating, customer__in = customers):
            mini_arr.append(join)
        joinedTables_array.append(mini_arr)

    joined_Max = []
    for i in joinedTables_array:
        for j in i:
            joined_Max.append(j)

    userTables = UserTable.objects.filter(joinedTable__in = joined_Max)
    userTables_array = []
    for us in userTables:
        userTables_array.append(us)

    suppliers = ['Արտադրամաս','Փուռ','Կիրովական']
    uniq = ItemsModel.productsfor_Customer(kamo_User)
    rows = []
    for joined_arr in joinedTables_array:
        mini_rows = []
        # print(joined_arr)
        for joinedTable in joined_arr:
            table_Rows = []
            for userTable in userTables_array:
                if userTable.joinedTable == joinedTable:
                    for product in uniq:
                        if product.supplier in suppliers:
                            try:
                                if joinedTable.customer.username == 'Կամո':
                                    us = 'kamo'
                                elif joinedTable.customer.username == 'Գանձակ':
                                    us = 'gandak'
                                elif joinedTable.customer.username == 'Սարուխան':
                                    us = "sarukan"
                                r = {
                                    'productName': product.productName,
                                    us: TableItem.objects.get(
                                        table=userTable,
                                        product_name=product.productName,
                                        customer=joinedTable.customer
                                )}
                                table_Rows.append(r)
                            except:
                                pass
            if joinedTable.customer.username == 'Կամո':
                ts = 'kamo'
            elif joinedTable.customer.username == 'Գանձակ':
                ts = 'gandak'
            elif joinedTable.customer.username == 'Սարուխան':
                ts = "sarukan"
            mini_rows.append({
                'table_name': f'{joinedTable.tableName}',
                ts : table_Rows
                })
        rows.append(mini_rows)

    complete_row = []

    for tab in tables:
        mini_comp = []
        kamo_total = 0
        gandak_total = 0
        sarukan_total = 0
        big_total = 0
        for row in rows:
            # print(row[3]['ohan'])

            if row[2]['table_name'] == tab.tableName:
                for prod in uniq:
                    row_list = []
                    total_of_row = 0
                    row_list.append(prod.productName)
                        # print(ohan)
                    for kamo in row[2]['kamo']:
                        if kamo['productName'] == prod.productName:
                            row_list.append(kamo['kamo'])
                            total_of_row += kamo['kamo'].total_price
                            kamo_total += kamo['kamo'].total_price
                            break
                    for gandak in row[1]['gandak']:
                        if gandak['productName'] == prod.productName:
                            row_list.append(gandak['gandak'])
                            total_of_row += gandak['gandak'].total_price
                            gandak_total += gandak['gandak'].total_price
                            break
                    for sarukan in row[0]['sarukan']:
                        if sarukan['productName'] == prod.productName:
                            row_list.append(sarukan['sarukan'])
                            total_of_row += sarukan['sarukan'].total_price
                            sarukan_total += sarukan['sarukan'].total_price
                            break
                    row_list.append(total_of_row)
                    big_total += total_of_row
                    mini_comp.append(row_list)

                # print(mini_comp)
        complete_row.append({f'{tab.tableName}':mini_comp,'last_row': ['Ընդ', kamo_total, gandak_total, sarukan_total, big_total]})

    joineddebt = Debt.objects.filter(
        customer = User.objects.get(username = "Կամո"),
        joined = True
        ).order_by('timeOfCreating')
    joineddebtPaginator = Paginator(joineddebt, 5) #show 5 debts per page of the joined tables
    joineddebt_page_obj = joineddebtPaginator.get_page(page_number)
    reversed_joined_debt_obj = joineddebtPaginator.get_page(
        joineddebtPaginator.num_pages - joineddebt_page_obj.number + 1
    )

    debt_array = []
    for table in tables[::-1]:
        try:
            debt = Debt.objects.get(date=table.dateOfCreating, customer = kamo_User, joined = True)
            # print(debt)
            debt_array.append([str(debt.date), debt.debt, ''])
            # print('try')
        except:
            # print('except')
            debt_array.append([str(table.dateOfCreating), 0, ''])
    try:
        paymant = Paymant.objects.get(
            date = tables[-1].dateOfCreating,
            customer=customers[0]
        )
        total_payments_money = paymant.money
        total_payments_returned = paymant.returned
        total_payments_salary = paymant.salary
    except:
        total_payments_money = 0
        total_payments_returned = 0
        total_payments_salary = 0

    # single_debt_array = []
    # single_debt_dict = {}
    # for i in reversed_joined_debt_obj:
    #     try:
    #         singleDebt = Debt.objects.filter(
    #             single=True,
    #             date=i.date,
    #             customer__in=customers
    #             )
    #         if singleDebt[0].date not in single_debt_array:
    #             single_debt_array.append(singleDebt[0].date)
    #             single_debt_dict[str(i.date)] = singleDebt.aggregate(sum = Sum('debt'))['sum']
    #     except:
    #         continue
    # debt_array = []
    # for debt in reversed_joined_debt_obj:
    #     joinTable_debt = Debt.objects.filter(
    #         joined = True,
    #         date = debt.date,
    #         customer__in=customers
    #     )
    #     try:
    #         debt_array.append([str(debt.date),joinTable_debt.aggregate(sum = Sum('debt'))['sum'], single_debt_dict[str(debt.date)]])
    #     except:
    #         debt_array.append([str(debt.date),joinTable_debt.aggregate(sum = Sum('debt'))['sum'], ''])
    # try:
    #     total_payments_money = Paymant.objects.get(
    #         date = tables[-1].dateOfCreating,
    #         customer=customers[0]
    #     ).money
    #     total_payments_returned = Paymant.objects.get(
    #         date = tables[-1].dateOfCreating,
    #         customer=customers[0]
    #     ).returned
    #     total_payments_salary = Paymant.objects.get(
    #         date = tables[-1].dateOfCreating,
    #         customer=customers[0]
    #     ).salary
    # except:
    #     total_payments_money = 0
    #     total_payments_returned = 0
    #     total_payments_salary = 0

    total_global_debt = 0
    try:
        old_debt = Old_debt.objects.get(date = tables[-1].dateOfCreating, customer=customers[0]).debt
    except:
        old_debt = 0

    try:
        new_debt = Week_debt.objects.get(date = tables[-1].dateOfCreating, customer=customers[0]).debt
    except:
        new_debt = 0
    total_global_debt = Global_Debt.objects.filter(customer=customers[0]).latest('timeOfCreating').debt
    return render(request, 'drivers/tablesBYkamo.html', {
        'Tables': tables,
        'CompleteRows': complete_row,
        "table" : join_page_obj,

        'joinedDebt': debt_array,
        'Returned': total_payments_returned,
        'Salary': total_payments_salary,
        'Money': total_payments_money,
        'GlobalDebt': total_global_debt,
        'OldDebt': old_debt,
        'NewDebt': new_debt,
    })

def myOrders(request, supplier_id):
    # schools = [
    #     '148', '189', '54', '170', '104', '136', '171', '117', '177', '48', '60', '87',
    #     '90', '188', '196', '115', '44', 'Դավիթ','Օհան','Գ.4-րդ', 'Գ.ավագ', 'Արա','Կամո','Գանձակ', 'Սարուխան','Էրանոս','Լիճք', 'Մ.1ին',
    #     'Մ.ավագ', 'Զոլ.2րդ', 'Զոլ.1ին', 'Ծովինար'
    #     ]
    # theSupplier = User.objects.get(id = supplier_id)
    # orderedProducts_Tables = Ordered_Products_Table.objects.filter(supplierof_Table = theSupplier)
    # paginator = Paginator(orderedProducts_Tables, 2) # show 3 tables per page
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    # uniq = ItemsModel.uniqueProductNames(theSupplier)
    # customers = User.objects.filter(is_customer = True)
    # school_order = {school: i for i, school in enumerate(schools)}
    # arrFromColums = []
    # arrFromOrdTabs = []
    # kamo_User = User.objects.get(username='Կամո')
    # ohan_User = User.objects.get(username='Օհան')

    # for tab in page_obj:
    #     if tab not in arrFromOrdTabs:
    #         arrFromOrdTabs.append(tab)

    # columns_OFtable = Ordered_Products_Column.objects.filter(
    #     supplierof_table = theSupplier
    #     ).filter(
    #         parent_Table__in = arrFromOrdTabs
    #     )

    # for j in columns_OFtable:
    #     if j not in arrFromColums:
    #         arrFromColums.append(j.table)

    # tableRows = (TableItem.objects.filter(supplier_id = supplier_id).filter(
    #     table__in=arrFromColums
    # ) | TableItem.objects.filter(
    #     customer__in = [kamo_User,ohan_User],
    #     table__in=arrFromColums
    # ))

    # sorted_columns = sorted(columns_OFtable, key=lambda col: school_order.get(col.table.user.username, len(schools)))
    theSupplier = User.objects.get(id = supplier_id)
    orderedProducts_Tables = Ordered_Products_Table.objects.filter(supplierof_Table = theSupplier)
    paginator = Paginator(orderedProducts_Tables, 1) # show 3 tables per page
    page_number = request.GET.get('page')
    # print(end-start, tableRows.count())
    return render(request, 'myOrders.html', {
        'supplier': theSupplier,
        'page': page_number or 1
        # 'Tables': page_obj,
        # 'Columns_of_Table': sorted_columns,
        # 'Products': uniq,
        # 'Customers': customers,
        # 'TableRows': tableRows,
    })




@employee_or_supplier_required
def ordered_tables_api(request, supplier_id, page_number):
    # start_time = time.time()  # Record the start time
    # print(page_number, 'api')
    is_employee = False
    if request.user.username == "Վարդգես":
        is_employee = True
    
    schools = [
        # '148',
        '189', "50",
        # '54',
        '170', '104', '136', '171', '117', '177', '48', '60', '87',
        '90', '188', '196', '115', '44', '52', '163','143','140','154','66','144','Չարբախ_1','106','35',"35_փոքր",'93',"91",
        "134", "38","195","94", "53","161",
        'Դավիթ','Օհան','Գ.4-րդ', 'Գ.ավագ', 'Արա','Կամո','Գանձակ', 'Սարուխան','Էրանոս','Լիճք', 'Մ.1ին',
        'Մ.ավագ', 'Զոլ.2րդ', 'Զոլ.1ին', 'Ծովինար', "Գավառ_ավագ","Գավառ_4րդ", "Գավառ_5րդ", "Գ_սարուխան", "Գ_հացառատ2","Գ_գանձակ",#'Խանութ'
    ]
    theSupplier = User.objects.get(id=supplier_id)

    orderedProducts_Tables = Ordered_Products_Table.objects.filter(supplierof_Table=theSupplier)
    paginator = Paginator(orderedProducts_Tables, 2)
    # page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # print(page_number)
    uniq = ItemsModel.uniqueProductNames(theSupplier)
    school_order = {school: i for i, school in enumerate(schools)}
    arrFromColums = []
    arrFromOrdTabs = []

    for tab in page_obj:
        if tab not in arrFromOrdTabs:
            arrFromOrdTabs.append(tab)

    columns_OFtable = Ordered_Products_Column.objects.filter(parentTable__in=arrFromOrdTabs)

    for j in columns_OFtable:
        if j not in arrFromColums:
            arrFromColums.append(j)

    tableRows = ordered_Itmes.objects.filter(parentTable__in=arrFromColums)

    uniq_data = [
        {
            'productName': item["productName"],
            'supPrice': item["supPrice"] if is_employee else 0
        } for item in uniq
    ]
    tableRows_data = [
        {
            'productName': item.productName,
            'productCount': item.productCount,
            'getId': item.getId,
            'parentColumn': item.parentTable.id
        } for item in tableRows
    ]

    columns_data = [
        {
            'column': item.id,
            "customerofTable": item.customerof_table.username,
            "parentTable": item.parentTable.id
        } for item in columns_OFtable
    ]
    sorted_columns_data = sorted(columns_data, key=lambda col: school_order.get(col["customerofTable"], len(schools)))
    tabs = [
        {
            'table': tab.id,
            'date': tab.dateof_Creating
        } for tab in page_obj
    ]

    response_data = {
        'supplier': {'username': theSupplier.username,'id':theSupplier.id},
        # 'Tables': [{'id': tab.id, 'nameof_Table': tab.nameof_Table} for tab in page_obj],
        # 'Columns_of_Table': [{'id': col.id, 'customerof_table': col.customerof_table.username, 'parentTable_id': col.parentTable.id} for col in sorted_columns],
        'Products': uniq_data,
        # 'Customers': [{'id': customer.id, 'username': customer.username} for customer in customers],
        'TableRows': tableRows_data,
        'Columns': sorted_columns_data,
        'Tables': tabs,
        "pagination": {
            "hasPrevious": page_obj.has_previous(),
            "hasNext": page_obj.has_next(),
            "previousPageNumber": page_obj.previous_page_number() if page_obj.has_previous() else None,
            "nextPageNumber": page_obj.next_page_number() if page_obj.has_next() else None,
            "currentPageNumber": page_obj.number,
            "totalPages": paginator.num_pages
        }

    }

    # end_time = time.time()
    # execution_time = end_time - start_time
    # print(f"Execution Time: {execution_time} seconds")

    return JsonResponse(response_data, safe=False)


def create_paymants_for_users(user, date_object):
    try:
        Old_debt.objects.get(
        date=date_object,
        customer=user
        )
    except:
        return 0
    money = 0
    returned = 0
    salary = 0

    try:
        Paymant.objects.get(
            customer=user,
            date = date_object
            )
        # return 0
    except:
        Paymant.objects.create(
            customer=user,
            date = date_object,
            salary = salary,
            returned = returned,
            money = money
            )
    old_debt_object = Old_debt.objects.get(
        date=date_object,
        customer=user
        )
    joined_debts = Debt.objects.filter(
        date__gte=old_debt_object.date,
        date__lte=old_debt_object.until,
        customer=User.objects.get(username="171"),
        joined = True
        )

    counter = 0
    for i in joined_debts:
        counter += 1
    if counter < 5:
        return 0

    old_debt_sum = old_debt_object.debt # week's old detbs
    debts = Debt.objects.filter(date__gte=old_debt_object.date, date__lte=old_debt_object.until, customer=user)
    debt_sum = 0
    for i in debts:
        debt_sum += i.debt
    new_week_debt = old_debt_sum + debt_sum

    try:
        Week_debt.objects.get(
            customer = user,
            date = date_object,
        )
        return 0
    except:
        weekDebt = Week_debt.objects.create(
            customer = user,
            date = date_object,
            debt = new_week_debt
        )
        return 1

@employee_required
def totalPage(request):
    schools = [
        # '148',
        '189',"50",
        # '54',
        '170', '104', '136', '171', '117', '177', '48', '60', '87',
        '90', '188', '196','115', '44', '52','163','143','140','154','66','144','Չարբախ_1','106','35',"35_փոքր",'93',"91",
        "134", "38","195","94", "53","161",
        'Դավիթ','Օհան','Կամո','Էրանոս','Լիճք', 'Մ.1ին',
        'Մ.ավագ', 'Զոլ.2րդ', 'Զոլ.1ին', 'Ծովինար', "Գավառ_ավագ","Գավառ_4րդ", "Գավառ_5րդ", "Գ_սարուխան", "Գ_հացառատ2","Գ_գանձակ",#'Խանութ'
        ]


    page_number = request.GET.get('page')
    joineddebt = JoinedTables.objects.filter(
        customer = User.objects.get(username = 171)
        ).order_by('timeOfCreating')
    joined_table_Paginator = Paginator(joineddebt, 5) #show 5 debts per page of the joined tables
    joined_tables_page = joined_table_Paginator.get_page(page_number)
    reversed_joined_table_obj = joined_table_Paginator.get_page(
        joined_table_Paginator.num_pages - joined_tables_page.number + 1
    )
    date_array = []
    debt_array = []
    ohan_and_kamo_Users = [
        User.objects.get(username='Գ.4-րդ'),
        User.objects.get(username='Գ.ավագ'),
        User.objects.get(username='Արա'),
        User.objects.get(username='Սարուխան'),
        User.objects.get(username='Գանձակ'),
        User.objects.get(username="Խանութ")
    ]
    writing_dbt = 0
    for table in reversed_joined_table_obj:
        try:
            Joined_debts = Debt.objects.filter(
                joined=True,
                date=table.dateOfCreating
            ).exclude(customer__in=ohan_and_kamo_Users)
            Single_debts = Debt.objects.filter(
                single = True,
                date = table.dateOfCreating
            ).exclude(customer__in=ohan_and_kamo_Users)
            Writing_debts = Debt.objects.filter(
                single = False,
                joined = False,
                date = table.dateOfCreating
            ).exclude(customer__in=ohan_and_kamo_Users)
            # for join in Joined_debts:
                # if table.dateOfCreating not in date_array:
            date_array.append(table.dateOfCreating)
            debt_array.append([str(table.dateOfCreating), Joined_debts.aggregate(sum = Sum('debt'))['sum'], Single_debts.aggregate(sum = Sum('debt'))['sum']])
            writing_dbt += Writing_debts.aggregate(sum = Sum('debt'))['sum']
        except:
            continue
    debt_array.append(["Գրենական", "", writing_dbt])
    for school in schools:
        user_obj = User.objects.get(username=school)
        create_paymants_for_users(user_obj, date_array[0])

    try:
        total_payments_money = Paymant.objects.filter(
            date = date_array[0],
        ).aggregate(money=models.Sum('money'))['money']
        total_payments_returned = Paymant.objects.filter(
            date = date_array[0],
        ).aggregate(returned=models.Sum('returned'))['returned']
        total_payments_salary = Paymant.objects.filter(
            date = date_array[0],
        ).aggregate(salary=models.Sum('salary'))['salary']
    except:
        total_payments_money = 0
        total_payments_returned = 0
        total_payments_salary = 0

    # PAYMANT

    customers = User.objects.filter(is_customer=True)
    total_global_debt = 0
    try:
        new_debt = Week_debt.objects.filter(date = date_array[0]).exclude(customer__in=ohan_and_kamo_Users).aggregate(sum = Sum('debt'))['sum']
    except:
        new_debt = 0
    try:
        old_debt = Old_debt.objects.filter(date = date_array[0]).exclude(customer__in=ohan_and_kamo_Users).aggregate(sum = Sum('debt'))['sum']
    except:
        old_debt = 0


    for customer in customers:
        if customer in ohan_and_kamo_Users:
            continue
        try:
            latest_global_debt = Global_Debt.objects.filter(customer=customer).latest('timeOfCreating')
            total_global_debt += latest_global_debt.debt
        except:
            pass
        # debt = Global_Debt.objects.filter(customer=customer).order_by('-timeOfCreating').first()
        # if latest_global_debt:


    paymants = []
    mon = 0
    sal = 0
    ret = 0
    old = 0
    wek = 0
    for name in schools:
        arr = []
        try:
            customer = User.objects.get(username=name)

            arr.append(customer.username)
            try:
                pay = Paymant.objects.get(customer = customer, date=date_array[0])
                mon += pay.money
                sal += pay.salary
                ret += pay.returned
                arr.append(pay.money)
                arr.append(pay.salary)
                arr.append(pay.returned)
            except:
                arr.append('')
                arr.append('')
                arr.append('')

            try:
                old_d = Old_debt.objects.get(customer = customer, date = date_array[0]).debt
                arr.append(old_d)
            except:
                old_d = 0
                arr.append(0)

            try:
                week_d = Week_debt.objects.get(customer = customer, date = date_array[0]).debt
                arr.append(week_d)
            except:
                week_d = 0
                # create_paymants_for_users(customer, date_array[0])
                # week_d = Week_debt.objects.get(customer = customer, date = date_array[0]).debt
                arr.append(0)

            old += old_d
            wek += week_d
            paymants.append(arr)
        except:
            continue
    paymants.append(['Ընդ', mon, sal, ret, old, wek])



    return render(request, 'totalPage.html',{
        'joinedDebt': debt_array,
        'table': joined_tables_page,
        'Returned': total_payments_returned,
        'Salary': total_payments_salary,
        'Money': total_payments_money,
        'GlobalDebt': total_global_debt,
        'OldDebt': old_debt,
        'NewDebt': new_debt,
        'Paymants': paymants
    })

# \\\\\\\\\\\\\\\\\\\\\\\\\\ Employee End   \\\\\\\\\\\\\\\\\\

# ========================== Admin Start    ==================

@admin_required
def admin(request):
    users = User.objects.filter(is_customer=True)
    suppliers = User.objects.filter(is_supplier=True)

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        # print(data)
        customers = data['customers']
        supplier = data['supplier']
        productName = data['productName']
        productPrice = data['productPrice']
        supPrice = data['supPrice']
        # print('post')
        for customer in customers:
            item = ItemsModel(
                customer=customer,
                supplier=supplier,
                productName=productName,
                productPrice=productPrice,
                supPrice=supPrice
            )
            item.save()
            cust = User.objects.get(username = item.customer)
            sup = User.objects.get(username = item.supplier)
            # print(item)
            try:
                big_table = BigTable.objects.get(user=cust, supplier=sup)
                # print(big_table)
                if sup.username == "Այլ.ապրանք":
                    single_table = SingleTable.objects.filter(
                        customer = cust
                        ).latest("timeOfCreating")
                    print(single_table)
                    user_table = UserTable.objects.get(
                        singleTable = single_table
                    )
                    table_item = TableItem(
                        table = user_table,
                        product_name = item.productName,
                        product_price = item.productPrice,
                        customer = cust,
                        supplier = sup,
                        supTotal = 0
                    )
                    table_item.save()
                    print(table_item)
                    big_table_row = BigTableRows(
                        user = cust,
                        supplier = sup,
                        item = table_item,
                        porduct_name = item.productName
                    )
                    # print(big_table_row)
                    big_table_row.save()
                else:
                    joined_table = JoinedTables.objects.filter(
                        customer = cust
                        ).latest("timeOfCreating")

                    user_tables = UserTable.objects.filter(
                        joinedTable = joined_table
                    )
                    # print(user_tables)
                    for user_table in user_tables:
                        tab_i = TableItem.objects.filter(table=user_table).last()
                        if tab_i.supplier != sup:
                            continue
                        table_item = TableItem(
                            table = user_table,
                            product_name = item.productName,
                            product_price = item.productPrice,
                            customer = cust,
                            supplier = sup,
                            supTotal = 0
                        )
                        table_item.save()
                        # print(table_item)
                        big_table_row = BigTableRows(
                            user = cust,
                            supplier = sup,
                            item = table_item,
                            porduct_name = item.productName
                        )
                        big_table_row.save()
                        # print(big_table_row)
            except:
                pass

        return redirect('adminpage')
        # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = ItemAddForm()

    # items = ItemsModel.objects.all()
    uniq = ItemsModel.uniqueProductNames(None)
    # print(uniq)
    return render(request, 'admin.html', {
        # 'Items': items,
        'Users': users,
        'Suppliers': suppliers,
        'Form': form,
        'Uniq': uniq
        })

@admin_required
def cahngeItemsName(request):
    if request.method == 'POST':
        form = ChangeItemsName(request.POST)
        if form.is_valid():
            from_name = form.cleaned_data['fromName']
            to_name = form.cleaned_data['toName']
            # print(from_name, to_name)
            itemsMod = ItemsModel.objects.filter(productName=from_name)
            tableItems = TableItem.objects.filter(product_name=from_name)
            bigtabRows = BigTableRows.objects.filter(porduct_name=from_name)

            for i in itemsMod:
                i.productName = to_name
                i.save()

            for j in tableItems:
                j.product_name = to_name
                j.save()

            for g in bigtabRows:
                g.porduct_name = to_name
                g.save()


            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@admin_required
def delete_item(request, item_id):
    item = get_object_or_404(ItemsModel, id=item_id)
    item.delete()
    # return redirect('adminpage')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@admin_required
def delete_item_all(request, item_id):
    item = get_object_or_404(ItemsModel, id=item_id)
    item.delete()
    # return redirect('productsforall')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@admin_required
def delete_item_byuser(request, item_id):
    item = get_object_or_404(ItemsModel, id=item_id)
    item.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@admin_required
def edit_item(request, item_id):
    customers = User.objects.filter(is_customer=True)
    item = get_object_or_404(ItemsModel, id=item_id)
    suppliers = User.objects.filter(is_supplier = True)
    if request.method == 'POST':
        form = ItemAddForm(request.POST, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            return redirect('adminpage')
            # return redirect(request.META.get('HTTP_REFERER'))
    else:
        form = ItemAddForm(instance=item)
    return render(request, 'edit_item.html', {'form': form,'item':item, 'Users': customers, 'Suppliers': suppliers})

@admin_required
def allCustomersforAdmin(request):
    allCustomers = User.objects.filter(is_customer = True)
    return render(request, 'allCustomersforAdmin.html',{'allCustomers':allCustomers})

@admin_required
def customersProducts(request, user_id):
    customer = User.objects.get(id = user_id)
    Products = ItemsModel.objects.all()
    return render(request, 'customerProducts.html', {'customer': customer, 'products':Products})

@admin_required
def productsForAll(request):
    Products = ItemsModel.objects.filter(customer = 'all')
    return render(request, 'productsForAll.html', {'products': Products})


def debts_by_date(request, date):
    schools = [
        # '148',
        '189', "50",
        # '54',
        '170', '104', '136', '171', '117', '177', '48', '60', '87',
        '90', '188', '196','115','44', '52', '163','143','140','154','66','144','Չարբախ_1','106','35',"35_փոքր",'93',"91",
        "134", "38","195","94", "53","161",
        'Դավիթ','Օհան','Կամո','Էրանոս','Լիճք', 'Մ.1ին',
        'Մ.ավագ', 'Զոլ.2րդ', 'Զոլ.1ին', 'Ծովինար'
    ]
    debts = Debt.objects.filter(date=date)
    data = []
    for name in schools:
        try:
            user = User.objects.get(username = name)
            try:

                join = Debt.objects.get(
                    date=date,
                    customer = user,
                    joined = True
                    )
                single = Debt.objects.get(
                    date=date,
                    customer = user,
                    single = True
                    )
                print(name, 'ok', join.debt)
                data.append(
                    [user.username, join.debt, single.debt]
                )
            except:
                try:
                    join = Debt.objects.get(
                        date=date,
                        customer = user,
                        joined = True
                        )
                    data.append(
                        [user.username, join.debt, '']
                    )
                except:
                    data.append(
                        [user.username, '', '']
                    )
        except:
            print(name, "chok")
            data.append(
                [name, '', '']
            )

    other_schools = ["Գավառ_ավագ","Գավառ_4րդ", "Գավառ_5րդ", "Գ_սարուխան", "Գ_հացառատ2","Գ_գանձակ"]
    for name in other_schools:

        user = User.objects.get(username = name)
        try:
            # join = Debt.objects.get(
            #     date=date,
            #     customer = user,
            #     joined = True
            #     )
            single = Debt.objects.get(
                date=date,
                customer = user,
                single = True
                )
            data.append(
                [user.username, '', single.debt]
            )

        except:
            pass
    # print(data)
    # data = [{'customer': debt.customer.username, 'joined': debt.joined, 'single': debt.single, 'debt': debt.debt} for debt in debts]
    return JsonResponse(data, safe=False)



# ========================== Admin End      ==================

# ///////////////////////// Supplier Start  //////////////////




@supplier_required
def supplier(request):
    # schools = [
    #     '148', '189', '54', '170', '104', '136', '171', '117', '177', '48', '60', '87',
    #     '90', '188', '196', '115','44', 'Դավիթ','Օհան','Գ.4-րդ', 'Գ.ավագ', 'Արա','Կամո','Գանձակ', 'Սարուխան','Էրանոս','Լիճք', 'Մ.1ին',
    #     'Մ.ավագ', 'Զոլ.2րդ', 'Զոլ.1ին', 'Ծովինար'
    #     ]
    # orderedProducts_Tables = Ordered_Products_Table.objects.filter(supplierof_Table = request.user)
    # paginator = Paginator(orderedProducts_Tables, 2) # show 3 tables per page
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    # uniq = ItemsModel.uniqueProductNames(request.user)
    # customers = User.objects.filter(is_customer = True)
    # school_order = {school: i for i, school in enumerate(schools)}
    # arrFromColums = []
    # arrFromOrdTabs = []
    # kamo_User = User.objects.get(username='Կամո')
    # ohan_User = User.objects.get(username='Օհան')

    # for tab in page_obj:
    #     if tab not in arrFromOrdTabs:
    #         arrFromOrdTabs.append(tab)

    # columns_OFtable = Ordered_Products_Column.objects.filter(
    #     supplierof_table = request.user
    #     ).filter(
    #         parent_Table__in = arrFromOrdTabs
    #     )

    # for j in columns_OFtable:
    #     if j not in arrFromColums:
    #         arrFromColums.append(j.table)

    # tableRows = (TableItem.objects.filter(supplier = request.user).filter(
    #     table__in=arrFromColums
    # ) | TableItem.objects.filter(
    #     customer__in = [kamo_User,ohan_User],
    #     table__in=arrFromColums
    # ))

    # sorted_columns = sorted(columns_OFtable, key=lambda col: school_order.get(col.table.user.username, len(schools)))

    # to_change = WaitingForChange.objects.all()
    # to_change_list = []
    # for i in to_change:
    #     to_change_list.append(i.table_item.id)
    # change_List = TableItem.objects.filter(id__in = to_change_list)
    # list_of_change = []
    # for j in change_List:
    #     list_of_change.append(j)

    # print(list_of_change)
    theSupplier = request.user
    page_number = request.GET.get('page')
    changes = supplier_Mistakes.objects.filter(supplier=theSupplier)
    changeList = []
    for c in changes:
        try:
            changeList.append(ordered_Itmes.objects.get(getId = c.item.id))
        except:
            pass
    return render(request, 'supplier.html', {
        'supplier': theSupplier,
        'page': page_number or 1,
        'changeList': changeList
        # 'Tables': page_obj,
        # 'Columns_of_Table': sorted_columns,
        # 'Products': uniq,
        # 'Customers': customers,
        # 'TableRows': tableRows,

    })

@supplier_required
def orderedProducts(request):
    items_list = []
    uniq_lsit = []
    items = ItemsModel.objects.filter(supplier=request.user.username)
    for i in items:
        if i.productName not in uniq_lsit:
            uniq_lsit.append(i.productName)
            items_list.append({'productName': i.productName, 'supPrice': i.supPrice})
    return render(request, 'ordered_Product.html', {'items': items_list})



@employee_required
def writing_items_api(request):
    start_time = time.time()  # Record the start time

    schools = [
        'Էրանոս','Լիճք', 'Մ.1ին',
        'Մ.ավագ', 'Զոլ.2րդ', 'Զոլ.1ին', 'Ծովինար'
    ]
    uniq = ItemsModel.uniqueProductNames(None).filter(supplier__in=["Գրենական"])
    suppliers = []
    for i in ["Գրենական"]:
        suppliers.append(User.objects.get(username=i))
    tableRows = BigTableRows.objects.filter(supplier__in=suppliers)
    bigTables = BigTable.objects.filter(supplier__in=suppliers)
    school_order = {school: i for i, school in enumerate(schools)}
    sorted_columns = sorted(bigTables, key=lambda col: school_order.get(col.user.username, len(schools)))
    # Convert QuerySets to dictionaries

    uniq_data = [item for item in uniq]

    tableRows_data = [
        {
            # "id": item.id,
            "user": item.user.username,
            "supplier_id": item.supplier.id,
            "porductName": item.porduct_name,
            'productCount': item.item.product_count,
            'totalPrice': item.item.total_price,
            'table': item.item.table.id,
            "supTotal": item.item.supTotal
        } for item in tableRows
    ]
    bigTables_data = [{
            # 'id': item.id,
            'supplier_id': item.supplier_id,
            'user': item.user.username,
            'modifiedDate': item.modifiedDate,
            'table': item.table.id
        } for item in sorted_columns]

    response_data = {
        'Products': uniq_data,
        'TableRows': tableRows_data,
        'BigTables': bigTables_data,
        'Suppliers': [{'id': supplier.id, 'username': supplier.username} for supplier in suppliers],
    }

    # Calculate the time taken
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution Time: {execution_time} seconds")

    return JsonResponse(response_data, safe=False)


@employee_required
def product_controll_page(request):
    return 