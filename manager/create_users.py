import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'manager.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

from django.contrib.auth.hashers import make_password

def change_password(username, new_password):
    try:
        user = User.objects.get(username=username)
        user.password = make_password(new_password)
        user.save()
        return True, "Password changed successfully."
    except User.DoesNotExist:
        return False, "User does not exist."

# print(change_password("93", "48pass8563"))
# print(change_password("35", "4835pass8563"))
# customers = ["148", "189", "54", "170", "104", "Էրանոս", "Լիճք", "Մ․ավագ",
#             "Մ.1ին", "Զոլ.1ին", "Զոլ.2րդ", "Ծովինար",
            # 'Գ.5-րդ', 'Գ.4-րդ', 'Հացառատ8', 'Գ․ավագ', 'Հացառատ2', 'Գանձակ', 'Սարուխան',
#             '60', '90', '188', '93', '48', '136', '44', '117', '87', '177', '171'
#             ]
customers = [
    # 'Արման',
    # 'Կամո',
    # 'Օհան',
    # "Արա"
    # '96',
    # '115',
    # 'Դավիթ'
    # '44'
    # '52'
    # '163',
    # '143',
    # '140',
    # '154',
    # '66',
    # '144',
    # '99'
    # 'Խանութ',
    # '106',
    # '35',
    # '93'
    # "35_փոքր"
    # "Գ_գանձակ",
    # "Գ_հացառատ2",
    # "Գ_սարուխան",
    # "Գավառ_ավագ",
    # "Գավառ_4րդ",
    # "Գավառ_5րդ"
    # "196_փոքր"
    # "91"
    # "110",
    # "38",
    # "27"
    # "134"
]
customersPasswords = [
    # 'arman145632',
    # 'kamo526987',
    # 'ohan489637',
    # "ara14689752"
    # '96pass2032',
    # 'pass155aa',
    # 'dav789456'
    # 'pass52word834',
    # '163pass25',
    # '143word33',
    # '140123jhk',
    # '154vrt123',
    # '66wer417a',
    # '144qwerty1',
    # '99asdfg12',
    # 'xanut4785'
    # 'passw4561',
    # 'passw8795',
    # 'passw3640'
    # "poqrpass35"
    # "gav545pass",
    # "pass236sa2",
    # "gavar1235a",
    # "pass89gava",
    # "369gavar1p",
    # "pass45word"
    # "passwordof196"
    # "91password",
    # "110password",
    # "38password",
    # "password27"
    # "134password"
]
# customersPasswords = [
#     '148password1234', "189password5678",
#     "54password1478", "170password2369",
#     "104password2589", "eranospassword3258",
#     "lijqpassword6547", "mavagpassword4569",
#     "m1inpassword9654", "zol1inpassword7428",
#     "zol2rdpassword9426", "tovinarpassword1463",
#     "g5password", 'g4password', 'hac8password',
#     "gavagpassword", 'hac2password', 'gandzpassword',
#     'sarpassword', '60pass1234', '90pass2345',
#     '188password', '93pass1478', '48pass8563', '136password', '44password14',
#     '117password', '87pass1258', '177pass1937', '171password6852'
# ]

# customersPasswords = [
#     '148password1234', "189password5678",
#     "54password1478", "170password2369",
#     "104password2589", "eranospassword3258",
#     "lijqpassword6547", "mavagpassword4569",
#     "m1inpassword9654", "zol1inpassword7428",
#     "zol2rdpassword9426", "tovinarpassword1463"
#                     ]
# admins = ['Վակուլ']

# superusers = ['aram']

# suppliers = ['Կիրովական', 'Արտադամաս']
# suppliers = ['Արտադամաս']

def create_users():
    pass
    # aram_admin = User.objects.create_superuser(username = 'aram', password= 'aramhovhannisyan')
    # aram_admin.save()

    # Create an admin user
    # admin_user = User.objects.create_user(username='Վակուլ', password='vakulpassword1236')
    # admin_user.is_admin = True
    # admin_user.save()

    # Create a customer user
    # customers = ["195"]
    # customersPasswords = ["pass195word12"]
    # customers = ["94"]
    # customersPasswords = ["pass94word12"]
    # customers = ["53"]
    # customersPasswords = ["pass53word53"]
    # customers = ["161"]
    # customersPasswords = ["pass161word53"]

    customers = ["50"]
    customersPasswords = ["pass50word53"]
    for customer, password in zip(customers, customersPasswords):
        print(customer,'---', password)
        customer_user = User.objects.create_user(username=customer, password=password)
        customer_user.is_customer = True
        customer_user.save()

    # supplier_user = User.objects.create_user(username='Գրենական', password='grenakan5864')
    # supplier_user.is_supplier = True
    # supplier_user.save()



    # Create an employee user
    # employee_user = User.objects.create_user(username='Վարդգես', password='vardgespassword1234')
    # employee_user.is_employee = True
    # employee_user.save()

    # # Create a supplier user
    # supplier_user = User.objects.create_user(username='Արտադրամաս', password='artadramas1258')
    # supplier_user.is_supplier = True
    # supplier_user.save()

    # supplier_user = User.objects.create_user(username='Փուռ', password='gavarpur5973')
    # supplier_user.is_supplier = True
    # supplier_user.save()

    # supplier_user = User.objects.create_user(username='Կիրովական', password='kirovakanpassword4569')
    # supplier_user.is_supplier = True
    # supplier_user.save()

    # supplier_user = User.objects.create_user(username='Այլ.ապրանք', password='aylapranqpassword1793')
    # supplier_user.is_supplier = True
    # supplier_user.save()

create_users()
