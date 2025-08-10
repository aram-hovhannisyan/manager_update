from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

from .models import (
    ItemsModel,
    TableItem,
    UserTable,
    BigTable,
    Debt,
    Ordered_Products_Column,
    Ordered_Products_Table,
    JoinedTables,
    SingleTable,
    Paymant,
    Global_Debt,
    Week_debt,
    Old_debt,
    BigTableRows,
    ordered_Itmes
)
from account.models import User

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json

# from datetime import timedelta
from datetime import datetime, timedelta

from django.shortcuts import redirect

from account.forms import PaymantForm

from storage.models import Tmp_Elements_Values, Storage_Element
from storage.views import update_or_create_tmp_value
# Create your views here.

yerevan_schools = [
    # '148',
    '44',
    '171', '136',
    '177', '48',
    '87', '93',
    '117', '188',
    '90', '60',
    '104', '170',
    # '54',
    '189',"94", "50",
    'Դավիթ', '115', '96', '196', '52',
    '163','143','140','154','66','144','Չարբախ_1',
    '106','35','93', "91","35_փոքր", "38" ,
    # "Խանութ",
    # "196_փոքր",
    # "110", "38" "27",
    "134", "195", "53","161",
]

def home(request):
    User = request.user
    Items = ItemsModel.objects.all()

    return render(request, 'tables/home.html', {'Items': Items, 'user': User})


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

def create_global_debt(date, user, total):
    try:
        latest_global_debt = Global_Debt.objects.filter(customer=user).latest('timeOfCreating')
        newGlobalDebt = Global_Debt.objects.create(
            customer = user,
            date = date,
            debt = latest_global_debt.debt + total,

        )
    except:
        newGlobalDebt = Global_Debt.objects.create(
            customer = user,
            date = date,
            debt = total
        )

def create_debt(date, user, total, joined = False):
    if joined:
        Debt.objects.create(
            customer = user,
            joined = True,
            debt = total,
            date = date,
        )
    else:
        Debt.objects.create(
            customer = user,
            single = True,
            debt = total,
            date = date
        )

@login_required
@csrf_exempt
def save_table_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)['data']
        table_name = json.loads(request.body)['table_name']
        total = json.loads(request.body)['total-sum']
        date = json.loads(request.body)['date']
        joinedTables = User.objects.filter(is_supplier=True, username__in=["Կիրովական", "Արտադրամաս", "Փուռ"])
        items = ItemsModel.productsfor_Customer(request.user)
        # date = "2025-03-31"
        # date = "2024-01-07"
        if len(table_name) == 1:
            try:
                SingleTable.objects.get(
                    customer=request.user,
                    dateOfCreating=date
                )
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            except:
                pass
        else:
            if request.user.username in ["Գավառ_ավագ","Գավառ_4րդ", "Գավառ_5րդ", "Գ_սարուխան", "Գ_հացառատ2","Գ_գանձակ"]:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            try:
                JoinedTables.objects.get(
                    customer=request.user,
                    dateOfCreating=date
                )
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            except:
                pass



        if len(table_name) == 1 and request.user.username != "27":#"Խանութ":
            Create_old_debt(date=date, user=request.user)
        try:
            SingleTable.objects.get(dateOfCreating = date, customer = request.user)
        except:
            Create_old_debt(date=date, user=request.user)

        create_global_debt(date=date, user=request.user, total=total)

        if len(table_name) == 1 and request.user.username != "27": #"Խանութ":
            singleTabUsr = User.objects.filter(is_supplier=True).exclude(username__in=joinedTables.values('username'))
            mainTable = SingleTable.objects.create(
                tableName = table_name,
                customer = request.user,
                dateOfCreating = date
                )
            for join, tabNam in zip(singleTabUsr, table_name):
                table = UserTable.objects.create(
                    user = request.user,
                    tableName = tabNam,
                    singleTable = mainTable,
                    dateOfCreating = date
                )
                for row in data:
                    if row['productCount'] == '':
                        row['productCount'] = 0
                    update_or_create_tmp_value(row['productName'], date, -int(row['productCount']))

                    supTot = items.get(productName=row['productName']).supPrice * int(row['productCount'])
                    table_item = TableItem.objects.create(
                        table=table,
                        product_name=row['productName'],
                        product_count=row["productCount"],
                        product_price=row['productPrice'],
                        total_price=row['totalPrice'],
                        customer = request.user,
                        supplier = join,
                        supTotal=supTot
                    )
                    table_item.save()

                    try:
                        big_tab = BigTableRows.objects.get(
                            user=request.user,
                            supplier=join,
                            porduct_name=row['productName']
                            )
                        big_tab.item = table_item
                        big_tab.save()
                    except BigTableRows.DoesNotExist:
                        # Create a new BigTableRows object since it doesn't exist for the user and supplier.
                        big_tab = BigTableRows.objects.create(
                            user=request.user,
                            supplier=join,
                            item=table_item,
                            porduct_name=row['productName']
                            )
                        big_tab.save()

                try:
                    bigtable = BigTable.objects.get(supplier=join, user=request.user)
                    bigtable.table = table
                    bigtable.modifiedDate = date
                    bigtable.save()
                except BigTable.DoesNotExist:
                    bigtable = BigTable.objects.create(
                        supplier=join,
                        table=table,
                        user=request.user,
                        modifiedDate=date
                        )
            create_debt(date=date, user=request.user, total=total, joined = False)

            return JsonResponse({'message': 'Table data saved successfully'})
        
        if request.user.username == "27":#"Խանութ":
            table_name.insert(0, 1)
            table_name.insert(1, 1)

        mainTable = JoinedTables.objects.create(
            tableName = table_name,
            customer = request.user,
            dateOfCreating = date
            )
        counter = 0
        for join, tabNam in zip(joinedTables, table_name):
            counter += 1
            if request.user.username in yerevan_schools and counter == 1:
                continue
            if request.user.username == "27" and counter == 2: #'Խանութ'
                # print('xanut')
                continue
            table = UserTable.objects.create(
                user = request.user,
                tableName = tabNam,
                joinedTable = mainTable,
                dateOfCreating = date
            )
            for row in data:
                if row['supplier'] == join.username:
                    if row['productCount'] == '':
                        row['productCount'] = 0
                    supTot = items.get(productName=row['productName']).supPrice * int(row['productCount'])
                    table_item = TableItem.objects.create(
                        table=table,
                        product_name=row['productName'],
                        product_count=row["productCount"],
                        product_price=row['productPrice'],
                        total_price=row['totalPrice'],
                        customer = request.user,
                        supplier = join,
                        supTotal=supTot
                    )
                    table_item.save()

                    try:
                        big_tab = BigTableRows.objects.get(
                            user=request.user,
                            supplier=join,
                            porduct_name=row['productName']
                            )
                        big_tab.item = table_item
                        big_tab.save()
                    except BigTableRows.DoesNotExist:
                        # Create a new BigTableRows object since it doesn't exist for the user and supplier.
                        big_tab = BigTableRows.objects.create(
                            user=request.user,
                            supplier=join,
                            item=table_item,
                            porduct_name=row['productName']
                            )
                        big_tab.save()

            try:
                bigtable = BigTable.objects.get(supplier=join, user=request.user)
                bigtable.table = table
                bigtable.modifiedDate = date
                bigtable.save()
            except BigTable.DoesNotExist:
                bigtable = BigTable.objects.create(
                    supplier=join,
                    table=table,
                    user=request.user,
                    modifiedDate=date
                    )

        create_debt(date=date, user=request.user, total=total, joined=True)
        

        return JsonResponse({'message': 'Table data saved successfully'})
        # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def changeNext_oldDebt(date, user, debt):
    next_old_date = date + timedelta(days=7)
    try:
        old_debt = Old_debt.objects.get(
            customer = user,
            date = date
        )
        old_debt.debt -= debt
        old_debt.save()
        # print(date, 'old debt succsesfull')
        try:
            week_debt = Week_debt.objects.get(
                customer = user,
                date = date
            )
            week_debt.debt -= debt
            week_debt.save()
            # print(date, 'week debt succsesfull')
        except:
            pass
        changeNext_oldDebt(next_old_date, user, debt)
    except:
        return
        # return print(date, 'reject')


def get_debts_between_old_dates(old_date, customer):
    old_debt = Old_debt.objects.get(date=old_date,customer=customer)
    debts = Debt.objects.filter(date__gte=old_debt.date, date__lte=old_debt.until, customer=customer)
    debt_sum = 0
    for i in debts:
        debt_sum += i.debt
    return debt_sum


def Paymant_View(request):
    if request.method == 'POST':
        money = int(request.POST.get('money') or 0)
        returned = int(request.POST.get('returned') or 0)
        salary = int(request.POST.get('salary') or 0)
        date = request.POST.get('date')
        date_format = '%d.%m.%Y'  # Specify the format of the date string

        date_object = datetime.strptime(date, date_format)

        try:
            paymant = Paymant.objects.get(
                customer=request.user,
                date = date_object
                )
            paymant.salary += salary
            paymant.returned += returned
            paymant.money += money
            paymant.save()
        except:
            paymant = Paymant.objects.create(
                customer=request.user,
                date = date_object,
                salary = salary,
                returned = returned,
                money = money
                )
        old_debt_object = Old_debt.objects.get(
            date=date_object,
            customer=request.user
            )
        old_debt_sum = old_debt_object.debt # week's old detbs
        paymant_sum = money + returned + salary # paymant sum
        all_week_debt_sum = get_debts_between_old_dates(date_object, request.user) # weeks's debts sum
        new_week_debt = old_debt_sum + all_week_debt_sum - paymant_sum

        try:
            weekDebt = Week_debt.objects.get(
                customer = request.user,
                date = date_object,
            )
            weekDebt.debt -= paymant_sum # changed 12/17/20223
            weekDebt.save()
        except:
            weekDebt = Week_debt.objects.create(
                customer = request.user,
                date = date_object,
                debt = new_week_debt
            )
        next_date_obj = date_object + timedelta(days=7)

        changeNext_oldDebt(next_date_obj, request.user, paymant_sum)

        global_debt = Global_Debt.objects.filter(
            customer = request.user
            ).latest('timeOfCreating')
        new_global_debt = global_debt.debt - paymant_sum

        gloabalDebt = Global_Debt.objects.create(
            customer = request.user,
            debt = new_global_debt,
            date = date_object
        )

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return redirect('tablesbyuser')



def get_next_working_day():
    today = datetime.today()
    if today.weekday() == 5:
        today += timedelta(days=2)
    elif today.weekday() == 4:
        today += timedelta(days=3)
    else:
        today += timedelta(days=1)
    return today


def sendOrder(request):
    if request.method == "POST":
        data = json.loads(request.body)
        # print(data)
        # return HttpResponseRedirect('/')
        # suplier_id = data['supplier_id']
        orderedTableName = data['nameOftable']
        customers = User.objects.filter(is_customer = True)
        supplier = User.objects.get(username = data['sup_name'])
        pTable = Ordered_Products_Table.objects.create(
            nameof_Table = orderedTableName,
            supplierof_Table = supplier,
        )
        pTable.save()

        next_working_day = get_next_working_day().date()
        # next_working_day = datetime(2025, 3, 31).date()
        for cust in customers:
            try:
                # print(next_working_day)
                # print(supplier.username)
                custBigTable = BigTable.objects.get(
                    supplier = supplier,
                    user = cust
                )
                # print(next_working_day)
                # print(custBigTable.modifiedDate)
                print(supplier.username)
                if supplier.username == 'Այլ.ապրանք':
                    if custBigTable.modifiedDate == next_working_day:
                        # print(cust.username)
                        column = Ordered_Products_Column.objects.create(
                            customerof_table = cust,
                            parentTable = pTable
                        )
                        items = BigTableRows.objects.filter(user = cust,supplier = supplier)
                    for j in items:
                        it = ordered_Itmes.objects.create(
                            productName = j.item.product_name,
                            productCount = j.item.product_count,
                            parentTable = column,
                            getId = j.item.id
                        )
                        it.save()
                    else:
                        continue
                else:
                    column = Ordered_Products_Column.objects.create(
                        customerof_table = cust,
                        parentTable = pTable
                    )
                    items = BigTableRows.objects.filter(user = cust,supplier = supplier)
                    for j in items:
                        it = ordered_Itmes.objects.create(
                            productName = j.item.product_name,
                            productCount = j.item.product_count,
                            parentTable = column,
                            getId = j.item.id
                        )
                        it.save()
            except:
                print('order sending error')
                continue
    return redirect('employee')




def writing_save(request):
    if request.method == "POST":
        data = json.loads(request.body)['data']
        table_name = json.loads(request.body)['table_name']
        total = json.loads(request.body)['total-sum']
        date = json.loads(request.body)['date']
        items = ItemsModel.productsfor_Customer(request.user)
        latest_global_debt = Global_Debt.objects.filter(customer=request.user).latest('timeOfCreating')

        global_debt = Global_Debt.objects.create(
            customer = request.user,
            date = date,
            debt = latest_global_debt.debt + total,
        )
        global_debt.save()
        print(global_debt)
        supp = User.objects.get(username = 'Գրենական')

        table = UserTable.objects.create(
            user = request.user,
            tableName = table_name[0:len(table_name)//2],
            dateOfCreating = date
        )
        table.save()
        for row in data:
            if row['productCount'] == '':
                row['productCount'] = 0
            supTot = items.get(productName=row['productName']).supPrice * int(row['productCount'])
            table_item = TableItem.objects.create(
                table=table,
                product_name=row['productName'],
                product_count=row["productCount"],
                product_price=row['productPrice'],
                total_price=row['totalPrice'],
                customer = request.user,
                supplier = supp,
                supTotal=supTot
            )
            table_item.save()

            try:
                big_tab = BigTableRows.objects.get(
                    user=request.user,
                    supplier=supp,
                    porduct_name=row['productName']
                    )
                big_tab.item = table_item
                big_tab.save()
            except BigTableRows.DoesNotExist:
                big_tab = BigTableRows.objects.create(
                    user=request.user,
                    supplier=supp,
                    item=table_item,
                    porduct_name=row['productName']
                    )
                big_tab.save()

        try:
            bigtable = BigTable.objects.get(
                supplier=supp,
                user=request.user
                )
            bigtable.table = table
            bigtable.modifiedDate = date
            bigtable.save()
        except:
            bigtable = BigTable.objects.create(
                supplier=supp,
                table=table,
                user=request.user,
                modifiedDate=date
                )
            bigtable.save()
        debt = Debt.objects.create(
            customer = request.user,
            single = False,
            joined = False,
            debt = total,
            date = date
        )
        debt.save()
        print('table has created succesfully')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def writing_table(request):
    items = ItemsModel.objects.filter(supplier='Գրենական', customer=request.user.username)
    return render(request, 'writing/customer_writing.html', {
        "Items": items,
    })


def writing_big_tables(request):
    return render(request, 'writing/writing_bigTables.html', {})

