from django.shortcuts import render
from .models import Storage_Element, Tmp_Elements_Values
from account.mydecorators import (
    employee_required
)

from django.http import JsonResponse
from django.http import HttpResponseRedirect

import json

from tables.models import ItemsModel


def update_or_create_tmp_value(element_name, date, new_val):
    try:
        element = Storage_Element.objects.get(element_name=element_name)
        refresh_storage_element(element.id, element.count + new_val)
    except Storage_Element.DoesNotExist:
        return {"error": "Element with that name not found"}
     
    # try:
    #     # print("Tmp Element Exists!!!")
    #     obj = Tmp_Elements_Values.objects.get(element=element, date=date)
    #     obj.tmp_val += new_val
    #     obj.save()
    #     created = False
    # except:
    #     # print("new Tmp Element created!!!")
    #     obj = Tmp_Elements_Values.objects.create(
    #         element=element,
    #         date=date,
    #         tmp_val=element.count + new_val
    #     )
    #     created = True

    # return {
    #     "status": "created" if created else "updated",
    #     "value": obj.tmp_val
    # }

@employee_required
def edit_elements(request, element_id):
    if request.method == "POST":
        data = json.loads(request.body)
        new_count = data.get("element_name")
        print(new_count)
        obj = Storage_Element.objects.get(id=element_id)
        obj.count = new_count
        obj.save()
        return JsonResponse({"status": "ok"})
    return JsonResponse({"error": "invalid method"}, status=405)


def refresh_storage_element(element_id, new_count):
    obj = Storage_Element.objects.get(id=element_id)
    obj.count = new_count
    obj.save()


def confirm_tmp_val(request, tmp_el_id):
    tmp_val_obj = Tmp_Elements_Values.objects.get(id=tmp_el_id)
    element = tmp_val_obj.element

    element.count = tmp_val_obj.tmp_val
    element.save()

    tmp_val_obj.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# 0 - ayl 1 kir 2 - pur 3 - art
@employee_required
def register_elements(request):
    elements_of_storage = Storage_Element.objects.filter(supplier_id = 0)
    uniq1 = ItemsModel.uniqueProductNames('Այլ.ապրանք')
    uniq2 = ItemsModel.get_all_unique_items()
    mylist = [i["productName"] for i in uniq1]
    # for i in uniq2:
    #     if i["productName"] in mylist:
            
    #         item = Storage_Element.objects.create(
    #             element_name = i["productName"],
    #             is_available = i["is_available"]
    #         )
    #         print(item)
    tmp_vals = Tmp_Elements_Values.objects.all()
    
    return render(request, 'storage/reg.html', {
       "elements": elements_of_storage,
       "tmp_values" : tmp_vals
    })  

