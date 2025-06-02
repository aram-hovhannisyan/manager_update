from django.db import models
from account.models import User

class ItemsModel(models.Model):
    customer = models.CharField(max_length=50, null = True)
    supplier = models.CharField(max_length=50, null = True)
    productName = models.CharField(max_length=50)
    productPrice = models.IntegerField()
    supPrice = models.IntegerField(null=True)
    is_available = models.BooleanField(default=True)
    @staticmethod
    def uniqueProductNames(supplier):
        if supplier:
           return ItemsModel.objects.filter(supplier = supplier).values('productName', "supPrice" ,'supplier').distinct()
        return ItemsModel.objects.values('productName', "supPrice", 'supplier').distinct()

    @staticmethod
    def productsfor_Customer(customer):
        custprod = ItemsModel.objects.filter(customer=customer.username)
        custprod_distinct = custprod.values('productName').distinct()
        theProd = (
            ItemsModel.objects.filter(customer=customer.username)
            | ItemsModel.objects.filter(customer="all").exclude(productName__in=custprod_distinct))
        return theProd

    @staticmethod
    def get_all_unique_items():
        return ItemsModel.objects.values('productName',"is_available").distinct()


    def __str__(self) -> str:
        return f'{self.productName}---{self.customer}---{self.supplier}'



class JoinedTables(models.Model):
    tableName = models.CharField(max_length=250, null= True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    dateOfCreating = models.DateField(null=True)
    timeOfCreating = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f">>>{self.customer}---{self.dateOfCreating}"

    class Meta:
        ordering = ["-timeOfCreating"]

class SingleTable(models.Model):
    tableName = models.CharField(max_length=250, null= True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    dateOfCreating = models.DateField(null=True)
    timeOfCreating = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.customer}---{self.dateOfCreating}"
    class Meta:
        ordering = ["-timeOfCreating"]

class UserTable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tableName = models.CharField(max_length=50)
    dateOfCreating = models.DateField(null=True)
    timeOfCreating = models.DateTimeField(auto_now=True, null=True)
    joinedTable = models.ForeignKey(JoinedTables, on_delete=models.CASCADE, null=True)
    singleTable = models.ForeignKey(SingleTable, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ["-timeOfCreating"]

    def __str__(self):
        return f"{self.tableName}-{self.user}---{self.dateOfCreating}---{self.joinedTable}"

class TableItem(models.Model):
    table = models.ForeignKey(UserTable, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=50)
    product_count = models.IntegerField(null=True, default=0)
    product_price = models.IntegerField(null=True)
    total_price = models.IntegerField(null=True,default=0)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    supplier = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='supplier3')
    supTotal = models.IntegerField(null=True)

    def __str__(self) -> str:
        return f'{self.customer}<<<<<<{self.supplier}<<<<{self.product_name}-{self.product_count}--{self.table.tableName}'

class WaitingForChange(models.Model):
    table_item = models.ForeignKey(TableItem, on_delete=models.CASCADE)
    newTotal = models.IntegerField()
    newCount = models.IntegerField()
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    dateofCreating = models.DateTimeField(auto_now=True)
    date = models.DateField()
    endorsed = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.customer.username}---{self.dateofCreating}"

class BigTable(models.Model):
    supplier = models.ForeignKey(User, on_delete=models.CASCADE,related_name='supplier', null = True)
    table = models.ForeignKey(UserTable, on_delete=models.SET_NULL, null = True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null = True)
    modifiedDate = models.DateField(null=True)

    def __str__(self) -> str:
        return f'{self.supplier}---{self.user}---{self.modifiedDate}'

class BigTableRows(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null = True)
    supplier = models.ForeignKey(User, on_delete=models.CASCADE,related_name='supplier1', null = True)
    item = models.ForeignKey(TableItem, on_delete=models.CASCADE, null=True)
    porduct_name = models.CharField(max_length=255, null=True)

    def __str__(self) -> str:
        return f'{self.user}---{self.item.table}---{self.item.product_name}'

class Debt(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    joined = models.BooleanField(default=False)
    single = models.BooleanField(default=False)
    debt = models.IntegerField()
    timeOfCreating = models.DateTimeField(auto_now=True, null=True)
    date = models.DateField(null=True)

    def sumOfEveryUser(user):
        allDebts = Debt.objects.filter(customer = user)
        sum = 0
        for i in allDebts:
            sum += i.debt
        return sum

    def payed(user):
        allDebts = Debt.objects.filter(customer = user)
        payed = 0
        for i in allDebts:
            if i.seen and not i.supplier:
                payed += i.debt
        return payed

    class Meta:
        ordering = ["-timeOfCreating"]

    def __str__(self) -> str:
        return f'{self.customer} - {self.debt} - {self.date}'

class Global_Debt(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    debt = models.IntegerField()
    timeOfCreating = models.DateTimeField(auto_now=True)
    date = models.DateField()

    def __str__(self) -> str:
        return f'{self.customer} -- {self.date} -- {self.debt}'

class Week_debt(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    timeOfCreating = models.DateTimeField(auto_now=True)
    date = models.DateField()
    debt = models.IntegerField()

    def __str__(self):
        return f"{self.customer}---{self.debt}---{self.date}"

class Old_debt(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    timeOfCreating = models.DateTimeField(auto_now=True)
    date = models.DateField()
    debt = models.IntegerField()
    until = models.DateField(null=True)

    def __str__(self) -> str:
        return f"{self.customer.username} --- {self.debt} -- until {self.until}"

class SuppliersProducts(models.Model):

    suplier = models.ForeignKey(User, on_delete=models.CASCADE)
    productName = models.CharField(max_length=100)
    price = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.suplier} {self.productName}'

class Ordered_Products_Table(models.Model):
    nameof_Table = models.CharField(max_length=150)
    supplierof_Table = models.ForeignKey(User, on_delete=models.CASCADE)
    dateof_Creating = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-dateof_Creating"]

    def __str__(self) -> str:
        return f"{self.supplierof_Table}-{self.dateof_Creating.date()}"

class Ordered_Products_Column(models.Model):
    customerof_table = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user')
    parentTable = models.ForeignKey(Ordered_Products_Table, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.parentTable}---{self.customerof_table}"

class ordered_Itmes(models.Model):
    productName = models.CharField(max_length=255)
    productCount = models.IntegerField()
    parentTable = models.ForeignKey(Ordered_Products_Column, on_delete=models.CASCADE)
    getId = models.IntegerField(null=True)

    def __str__(self) -> str:
        return f"{self.parentTable}---{self.productName}---{self.productCount}"

class supplier_Mistakes(models.Model):
    item = models.ForeignKey(TableItem, on_delete=models.CASCADE)
    oldCount = models.IntegerField()
    newCount = models.IntegerField()
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    supplier = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sup')
    date = models.DateField()
    endorsed = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.customer.username}---{self.date}"

class Paymant(models.Model):
    money = models.IntegerField()
    returned = models.IntegerField()
    salary = models.IntegerField()
    timeOfCreating = models.DateTimeField(auto_now=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()

    class Meta:
        ordering = ["-timeOfCreating"]

    def __str__(self):
        return f"{self.customer}---{self.money}---{self.date}"

class Message(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE)
    to_users = models.TextField()
    message = models.TextField()
    seen_by = models.TextField()
    sent = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-sent"]