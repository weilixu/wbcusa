from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
import pandas as pd
from .forms import UploadFileForm, form_validation_error
from django.http import JsonResponse

# Create your views here.
@method_decorator(login_required(login_url='accounts/login/'), name='dispatch')
class DashboardView(View):

    def get(self, request):
        return render(request, "platform/dashboard.html")

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            data = temp_read_data(request.FILES['file'])
            # context = {'status': 'success', 'data': data}
            return JsonResponse({'status': 'success', 'data': data})
        return redirect('dashboard')

def temp_read_data(file):
    # Open a csv reader called DictReader
    df = pd.read_csv(file)
    out = df.to_json()
    return out
