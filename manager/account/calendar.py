# views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from storage.models import Non_Working_Days
from django.views.decorators.csrf import csrf_exempt
import json

from tables.models import (JoinedTables, Debt)
from account.models import (User)

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
def non_working_days_view(request):
    if request.method == 'POST':
        selected_date = request.POST.get('selected_date')
        if selected_date:
            # Avoid duplicates
            Non_Working_Days.objects.get_or_create(day=selected_date)
            for i in schools:
                JoinedTables.objects.create(
                    tableName = i + selected_date,
                    customer = User.objects.get(username=i),
                    dateOfCreating = selected_date
                )
                Debt.objects.create(
                    customer = User.objects.get(username=i),
                    joined = True,
                    debt = 0,
                    date = selected_date,
                )

            print(selected_date)
        return redirect('calendar')  # reload the page

    # Send non-working days to frontend
    days = Non_Working_Days.objects.values_list('day', flat=True)
    non_working_days = [d.strftime('%Y-%m-%d') for d in days]
    print(non_working_days)
    context = {
        'non_working_days': json.dumps(non_working_days),
    }
    return render(request, 'calendar_form.html', context)
