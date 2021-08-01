import copy

from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
import pandas as pd
from .forms import UploadFileForm, form_validation_error
from django.http import JsonResponse
import json

DATA_FILE = '/Users/weilixu/PycharmProjects/wbcusa/wbcplatform/static/datasets/TIEQ_2021_weekdays_timestamped.csv';

# Create your views here.
@method_decorator(login_required(login_url='accounts/login/'), name='dispatch')
class DashboardView(View):

    def get(self, request):
        if 'setting' not in request.GET:
            return render(request, "platform/dashboard.html")

        setting_str = request.GET['setting']
        setting = json.loads(setting_str)
        if setting['app'] == 'hourlydata':
            # retrieve hourly data
            keys = setting['keys'] # key should be a list, so add []
            start = setting['start'] # start date
            end = setting['end'] # end_date
            # process data - need to replace this later with data from database
            real_keys = temp_data_map(keys)
            if setting['visual'] == 'scatter_3d':
                data = temp_read_data_for_3d(open(DATA_FILE, 'r'), real_keys, start, end)
                return JsonResponse({'status': 'success', 'data': data, 'keys': real_keys})
            elif setting['visual'] == 'distribution':
                data = temp_read_data_for_dist(open(DATA_FILE, 'r'), real_keys, start, end)
                return JsonResponse({'status': 'success', 'data': data, 'keys': real_keys})
            elif setting['visual'] == 'multiline':
                data = temp_read_data_for_3d(open(DATA_FILE, 'r'), real_keys, start, end)
                return JsonResponse({'status': 'success', 'data': data, 'keys': real_keys})
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

# return a json list - data, min, max
# assume, only one key is selected.
def temp_read_data_for_dist(file, keys, start, end):
    df = select_subset_keys_times(file, keys, start, end)
    min = df[keys[0]].min()
    max = df[keys[0]].max()
    df_obj = dict()
    df_obj['data'] = df.to_json(orient='records', date_format='iso')
    df_obj['min'] = min
    df_obj['max'] = max
    return df_obj

def temp_read_data_for_3d(file, keys, start, end):
    df = select_subset_keys_times(file, keys, start, end)
    return df.to_json(orient='records', date_format='iso')


def select_subset_keys_times(file, keys, start, end):
    df = pd.read_csv(file)
    # subset data with keys
    # need to add DateTime as the basic parameter
    data_key = copy.deepcopy(keys)
    data_key.append('DateTime')
    df_sub = df[data_key]

    # set time limit
    df_sub['DateTime'] = pd.to_datetime(df_sub['DateTime'])
    mask = (df_sub['DateTime'] > '6/22/2021  12:00:00 AM') & (df_sub['DateTime'] <= '6/22/2021  1:00:00 AM')

    # select the sub data
    df_sub_sub = df_sub.loc[mask]
    return df_sub_sub


def temp_data_map(keys):
    real_keys = []
    for key in keys:
        if key == 'ambient_temp':
            real_keys.append('Ambient temperature')
        elif key == 'zone_temp':
            real_keys.append('Zone temperature')
        elif key == 'fan_speed':
            real_keys.append('Fan speed')
        elif key == 'internal_gain':
            real_keys.append('Internal gains')
        elif key == 'hvac_power':
            real_keys.append('HVAC power')
        else:
            real_keys.append('Solar Radiation')
    return real_keys