import os
import django
from datetime import datetime
# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'manager.settings')
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()

from tables.models import ItemsModel, JoinedTables, SingleTable, Debt, Old_debt, BigTable, UserTable, Global_Debt, BigTableRows, TableItem, Week_debt
# dateOfCreating
def create_items():

    # user = User.objects.get(username = "Կամո")
    # name = user.username

    may_1st = datetime(year=2025, month=1, day=10)
    may_2nd = datetime(year=2025, month=1, day=10)
    for username in ['50']:
        user = User.objects.get(username=username)
        aa = JoinedTables.objects.filter(
        customer = user,
        dateOfCreating = may_2nd
        )
        print(may_1st)
        aa.update(timeOfCreating = may_1st)
        # aa.save()
        # print(aa)
        # table.timeOfCreating = may_1st


    # debts = SingleTable.objects.filter(dateOfCreating="2024-01-07")

    # debts = UserTable.objects.filter(singleTable__isnull = False, dateOfCreating = "2024-01-07")
    # for i in debts:
    #     i.dateOfCreating = "2025-01-07"
    #     i.save()
    #     print(i.dateOfCreating)
    # old_debts = Old_debt.objects.filter(date="2024-01-06")
    # for i in old_debts:
    #     i.until = "2025-01-11"
    #     i.date = "2025-01-06"
    #     i.save()
        # i.until.replace(year = 2025)
        # i.date.replace(year = 2025)
        # print(i.until)
        # i.save()
        # print(i)

    # date = "2024-01-07"
    # join = Debt.objects.get(
    #     date=date,
    #     customer = user,
    #     # joined = True
    #     )
    # single = Debt.objects.get(
    #     date=date,
    #     customer = user,
    #     single = True
    #     )
    # print(join)
    # print(name, 'ok', join.debt)

    # customer = User.objects.get(username="161")
    # items = ItemsModel.objects.filter(productName__in=["ԲեբիՖոքս"])
    # for i in items:
    #     i.productPrice = 250
    #     print(i)
    #     i.save()
    # users = User.objects.all()
    # for i in users:
    #     try:
    #         latest_global_debt = Global_Debt.objects.filter(customer=i).latest('timeOfCreating')

    #         Old_debt.objects.create(
    #                 customer = i,
    #                 debt = latest_global_debt.debt,
    #                 date = "2024-01-06",
    #                 until = "2024-01-11"

    #             )
    #         JoinedTables.objects.create(
    #                 customer = i,
    #                 tableName = i.username + "06",
    #                 dateOfCreating = "2024-01-06"
    #             )

    #         Debt.objects.create(
    #                 customer = i,
    #                 joined = True,
    #                 debt = 0,
    #                 date = "2024-01-06"
    #             )
    #     except:
    #         pass
    # products = ItemsModel.objects.filter(customer="106")
    # for i in products:
        # ItemsModel.objects.create(
        #         customer='161',
        #         supplier=i.supplier,
        #         productName=i.productName,
        #         productPrice=i.productPrice,
        #         supPrice=i.supPrice,
        #         is_available = i.is_available
        #     )
    # items = ItemsModel.objects.filter(productName='խաչ.մեծ')
    # debt = Debt.objects.filter(customer=User.objects.get(username="Չարբախ_1"), date="2024-11-29", joined=True)
    # for i in debt:
    #     print(i.customer, "Partq", i.debt, "Jam", i.timeOfCreating)
    # for i in items:
    #     # if i.customer in ['177', '60', '134']:
    #     #     print(i.customer, i.productPrice)
    #     #     continue
    #     if i.customer in ['91', '53', '115']:
    #         i.productPrice = 120
    #         i.save()
    #         print(i.customer, i.productPrice)
    #         continue
        # i.productPrice = 150
        # i.save()

        # ItemsModel.objects.create(
        #         customer='53',
        #         supplier=i.supplier,
        #         productName=i.productName,
        #         productPrice=i.productPrice,
        #         supPrice=i.supPrice,
        #         is_available = i.is_available
        #     )
    # for i in products:
    #     print(i.customer, i.productPrice, i.supPrice)
    #     i.supPrice = 75
    #     i.save()

    # all_week_debts = Week_debt.objects.filter(date="2024-10-28")
    # for i in all_week_debts:
    #     try:
    #         old_debt = Old_debt.objects.get(customer=i.customer, date="2024-11-04")
    #         i.debt = old_debt.debt
    #         i.save()
    #     except:
    #         pass
    #     print(old_debt)
    # ohan_and_kamo_Users = [
    #     User.objects.get(username='Գ.4-րդ'),
    #     # User.objects.get(username='Գ.ավագ'),
    #     # User.objects.get(username='Արա'),
    #     # User.objects.get(username='Սարուխան'),
    #     # User.objects.get(username='Գանձակ'),
    #     # User.objects.get(username="Օհան"),
    #     # User.objects.get(username="Կամո")
    # ]
    # user_tables = UserTable.objects.filter(user__in=ohan_and_kamo_Users, dateOfCreating="2024-10-28")
    # for i in user_tables:
    #     items = TableItem.objects.filter(table=i)
    #     for j in items:
    #         j.product_count = 0
    #         j.save()
    #         print(j)
    # for i in user_tables:
    #     # i.dateOfCreating = "2024-10-28"
    #     # i.save()
    #     Table
    #     print(i)

    # customers = User.objects.filter(is_customer=True)
    # total_global_debt = 0
    # for customer in customers:
    #     if customer in ohan_and_kamo_Users:
    #         continue
    #     try:
    #         latest_global_debt = Global_Debt.objects.filter(customer=customer).latest('timeOfCreating')
    #         total_global_debt += latest_global_debt.debt
    #     except:
    #         pass
    # print(total_global_debt)
    # for user in User.objects.filter(is_customer=True):
    #     try:
    #         latest_global_debt = Global_Debt.objects.filter(customer=user).latest('timeOfCreating')
    #         print(latest_global_debt.customer, latest_global_debt.debt)
    #     except:
    #         pass
    # for i in all_week_debts:
    #     print(i)
    # for i in all_week_debts:
    #     try:
    #         old_debt = Old_debt.objects.get(customer=i.customer, date="2024-10-21")
    #         old_debt.debt = i.debt
    #         old_debt.save()
    #         print(f"successfully updated {i.customer}'s debt")
    #     except:
    #         print(i.customer, "There is no Old debt!!!!!")
        # i.customer =
        # print(i)
    # all_customers = Wee
    # for i in items:
        # i.delete()
    # for i in items:
    #     for j in ItemsModel.objects.filter(productName=i.productName):
    #         j.is_available = i.is_available
    #         j.save()
    # for i in items:
    #     ItemsModel.objects.create(
    #             customer='94',
    #             supplier=i.supplier,
    #             productName=i.productName,
    #             productPrice=i.productPrice,
    #             supPrice=i.supPrice,
    #             is_available = i.is_available
    #         )

    # debts = Debt.objects.filter()
    # items = ItemsModel.objects.filter(customer="171")
    # for i in items:
    #     ItemsModel.objects.create(
    #             customer='50',
    #             supplier=i.supplier,
    #             productName=i.productName,
    #             productPrice=i.productPrice,
    #             supPrice=i.supPrice,
    #             is_available = i.is_available
    #         )

    # for i in items:
    #     print(i)
    #     i.productPrice = 250
    #     i.save()
    # items = ItemsModel.objects.filter(supplier="Գրենական",customer="Մ.1ին")

    # for i in items:
    #     ItemsModel.objects.create(
    #             customer='Չարբախ_1',
    #             supplier=i.supplier,
    #             productName=i.productName,
    #             productPrice=i.productPrice,
    #             supPrice=i.supPrice
    #         )
        # print(i.productName)

    # print("done")
    # tab_items1 = ItemsModel.objects.filter(customer="60")
    # tab_items2 = ItemsModel.objects.filter(customer="110")

    # for i, j in zip(tab_items1, tab_items2):
    #     j.productPrice = i.productPrice
    #     j.save()

    # may_1st = datetime(year=2024, month=4, day=24)
    # for username in ['117']:
    #     user = User.objects.get(username=username)

    #     # table.timeOfCreating = may_1st
    #     # table.save()
    #     # print(table.timeOfCreating for table in table)
    #     JoinedTables.objects.create(
    #         tableName = username+"06,01",
    #         customer = user,
    #         dateOfCreating = may_1st,
    #         timeOfCreating = may_1st
    #         )
    #     table = JoinedTables.objects.filter(customer = user, dateOfCreating = may_1st).update(timeOfCreating = may_1st)
    #     Debt.objects.create(
    #         customer = user,
    #         joined = True,
    #         single = False,
    #         debt = 0,
    #         timeOfCreating = may_1st,
    #         date = may_1st
    #         )
    #     print(user)

    # for i in tab_items1:
    #     i.delete()
    # for i in tab_items2:
    #     ItemsModel.objects.create(
    #             customer='110',
    #             supplier=i.supplier,
    #             productName=i.productName,
    #             productPrice=i.productPrice,
    #             supPrice=i.supPrice
    #         )
    # items = ItemsModel.objects.filter(customer="177")
    # items = Debt.objects.filter(date__in=["2024-03-26", "2024-03-25"])
    # items = BigTable.objects.filter(modifiedDate__in=["2024-03-26", "2024-03-25"])
    # items1 = JoinedTables.objects.filter(dateOfCreating="2024-03-26")
    # for i in items:
    #     i.modifiedDate = "2024-04-01"
    #     i.save()
    #     print(i)
    # items2 = SingleTable.objects.filter(dateOfCreating="2024-03-26")
    # for i in items2:
    #     i.dateOfCreating = "2024-04-01"
    #     i.save()
    #     print(i)
    # items3 = Old_debt.objects.filter(date__in=["2024-04-01", "2024-03-26", "2024-03-25"])
    # for i in items3:
    #     i.date = "2024-04-01"
    #     i.until = "2024-04-06"
    #     i.save()
    #     print(i)
    # for i in tab_items:
    #     i.delete()
    # for i in items:
    #     i.delete()
    # customers = User.objects.all()
    # items = ItemsModel.objects.filter(productName="հոթ-դոգ պանիր")
    # items = ItemsModel.objects.filter(customer="115")
    # users = User.objects.all()
    # pur = User.objects.get(username="Փուռ")
    # kir = User.objects.get(username="Կիրովական")
    # items = ItemsModel.objects.filter(productName="Նագետս")
    # btr_items = BigTableRows.objects.filter(porduct_name__in = ["Բրաունի", "Cake Up", "Mr.Donut", "ԾամոնMentos", "ԱպաչիՊեչենի", "CocaCola05"])
    # print(BigTable.objects.filter(supplier=kir).count())
    # c = 0
    # for i in items:
    #     i.supPrice = 230
    #     i.productPrice = 350
    #     i.save()
        # i.productPrice = 450
    # for i in items:
    #     i.delete()
        # print(i.productName, i.customer, i.productPrice)
        # i.supPrice = 120
        # i.save()
        # c+=1
        # print(i.user.username ,i.porduct_name + "a",)
    # print(c)
    # counter = 0
    # for i in users:
    #     btr_items =  BigTableRows.objects.filter(supplier=kir, user=i)
    #     counter = 0
    #     for j in btr_items:
    #         if str(j.item.table.dateOfCreating) == "2024-01-24":
    #             counter += 1
    #         # print(j.supplier, j)
    #     if counter != 0:
    #         print(counter, i)
    # print(counter)
    # items_ = ItemsModel.objects.filter(supplier="Այլ.ապրանք",customer="148")
    # for i in items:
    #     i.supplier = 'Կիրովական'
    #     i.supPrice = 75
    #     i.save()
    # items = ItemsModel.objects.filter(productName="Բարնի")
    # for i in items:
    #     print(i)
    #     i.productPrice = 200
    #     # i.supplier = 'Փուռ'
    #     # i.supPrice = 60
    #     i.save()
    # items = ItemsModel.objects.filter(productName='խաչ.մեծ')
    # for i in items:
    #     i.supplier = 'Կիրովական'
    #     print(i.customer, i.productName)
    #     # i.supPrice = 110
    #     i.save()
    # items = ItemsModel.objects.filter(productName="Երշիկ")
    # for i in items:
    #     # i.supplier = "Փուռ"
    #     # i.save()
    #     ItemsModel.objects.create(
    #             customer='91',
    #             supplier=i.supplier,
    #             productName=i.productName,
    #             productPrice=i.productPrice,
    #             supPrice=i.supPrice
    #         )

    # for i in items:
    #     ItemsModel.objects.create(
    #             customer='134',
    #             supplier=i.supplier,
    #             productName=i.productName,
    #             productPrice=i.productPrice,
    #             supPrice=i.supPrice
    #         )

    # for i in items:
    #     ItemsModel.objects.create(
    #             customer='38',
    #             supplier=i.supplier,
    #             productName=i.productName,
    #             productPrice=i.productPrice,
    #             supPrice=i.supPrice
    #         )
    # for i in items:
    #     ItemsModel.objects.create(
    #             customer='Գ_հացառատ2',
    #             supplier=i.supplier,
    #             productName=i.productName,
    #             productPrice=i.productPirce,
    #             supPrice=i.supPrice
    #         )
    # for i in items:
    #     ItemsModel.objects.create(
    #             customer='Գ_սարուխան',
    #             supplier=i.supplier,
    #             productName=i.productName,
    #             productPrice=i.productPirce,
    #             supPrice=i.supPrice
    #         )
    # for i in items:
    #     ItemsModel.objects.create(
    #             customer='Գավառ_ավագ',
    #             supplier=i.supplier,
    #             productName=i.productName,
    #             productPrice=i.productPirce,
    #             supPrice=i.supPrice
    #         )

    # for i in items:
    #     ItemsModel.objects.create(
    #             customer='Գավառ_4րդ',
    #             supplier=i.supplier,
    #             productName=i.productName,
    #             productPrice=i.productPirce,
    #             supPrice=i.supPrice
    #         )
    # for i in items:
    #     ItemsModel.objects.create(
    #             customer='Գավառ_5րդ',
    #             supplier=i.supplier,
    #             productName=i.productName,
    #             productPrice=i.productPirce,
    #             supPrice=i.supPrice
    #         )
    # for i in items:
    #     ItemsModel.objects.create(
    #             customer='93',
    #             supplier=i.supplier,
    #             productName=i.productName,
    #             productPrice=i.supPrice,
    #             supPrice=i.supPrice
    #         )
    # joins = JoinedTables.objects.filter(dateOfCreating ="2023-10-23")
    # # print(joins)
    # singles = SingleTable.objects.filter(dateOfCreating ="2023-10-23")
    # usTabs = UserTable.objects.filter(dateOfCreating ="2023-10-23")
    # debts = Debt.objects.filter(date = "2023-10-23")
    # olds = Old_debt.objects.filter(date = "2023-10-23")
    # bigs = BigTable.objects.filter(modifiedDate = "2023-10-23")
    # for i in joins:
    #     i.dateOfCreating = "2023-10-30"
    #     i.save()
    # for i in singles:
    #     i.dateOfCreating = "2023-10-30"
    #     i.save()

    # for i in usTabs:
    #     i.dateOfCreating = "2023-10-30"
    #     i.save()

    # for i in debts:
    #     i.date = "2023-10-30"
    #     i.save()

    # for i in olds:
    #     i.date = "2023-10-30"
    #     i.save()

    # for i in bigs:
    #     i.modifiedDate = "2023-10-30"
    #     i.save()
    # customers = ['all']
    # suppliers = ['Կիրովական', 'Արտադրամաս', 'Այլ․ապրանք']

    # for i in range(1, 21):
    #     item = ItemsModel.objects.create(
    #         customer=customers[0],
    #         supplier=suppliers[0]                 for j in range(4):
    #                 item = ItemsModel.objects.create(
    #                     customer=customer.username,
    #                     supplier=suppliers[i % 2].username,
    #                     productName=f'Joined Item {i}{j}-{customer}',
    #                     productPrice=j * 10
    #                 ),
    #         productName=f'item{i}',
    #         productPrice=i * 10
    #     )
    #     item.save()
    # for j in range(1, 11):
    #     item = ItemsModel.objects.create(
    #         customer=customers[0],
    #         supplier=suppliers[2],
    #         productName=f'Ապրանք{j}',
    #         productPrice=j * 30
    #     )
    # users = ['115']
    # items = ItemsModel.objects.filter(customer="148", supplier='Այլ.ապրանք')
    # for username in users:
    #     for i in items:
    #         ItemsModel.objects.create(
    #                 customer = username,
    #                 productPrice = i.productPrice,
    #                 productName = i.productName,
    #                 supPrice = i.supPrice,
    #                 supplier = i.supplier
    #             )
    # items = {"ԲուլկիՉամիչ": 70, "Քլաբ սենդ": 175}
    # for i in items:
    #     for j in ItemsModel.objects.filter(productName=i):
    #         j.supPrice = items[i]
    #         j.save()
    print('Items created successfully!')

# Call the create_items() function
create_items()
