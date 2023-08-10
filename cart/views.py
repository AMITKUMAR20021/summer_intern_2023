from django.http import JsonResponse
from .models import TemperatureReading, PulseReading, ECGReading
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render ,redirect

@csrf_exempt
def temperature_data(request):
    if request.method == 'POST':
        temperature = request.POST.get('temperature')
        reading = TemperatureReading(temperature=float(temperature))
        reading.save()

        # Delete excess records
        total_readings = TemperatureReading.objects.count()
        if total_readings > 40:
            excess_ids = TemperatureReading.objects.order_by('-time')[40:].values_list('id', flat=True)
            TemperatureReading.objects.filter(id__in=excess_ids).delete()

        return JsonResponse({'status': 'ok'}, status=201)
    else:
        return JsonResponse({'status': 'not ok'}, status=400)


@csrf_exempt
def pulse_data(request):
    if request.method == 'POST':
        pulse = request.POST.get('pulse')
        reading = PulseReading(pulse=float(pulse))
        reading.save()

        # Delete excess records
        total_readings = PulseReading.objects.count()
        if total_readings > 40:
            excess_ids = PulseReading.objects.order_by('-time')[40:].values_list('id', flat=True)
            PulseReading.objects.filter(id__in=excess_ids).delete()

        return JsonResponse({'status': 'ok'}, status=201)
    else:
        return JsonResponse({'status': 'not ok'}, status=400)


@csrf_exempt
def ecg_data(request):
    if request.method == 'POST':
        ecg = request.POST.get('ecg')
        reading = ECGReading(ecg_data=ecg)
        reading.save()

        # Delete excess records
        total_readings = ECGReading.objects.count()
        if total_readings > 40:
            excess_ids = ECGReading.objects.order_by('-time')[40:].values_list('id', flat=True)
            ECGReading.objects.filter(id__in=excess_ids).delete()

        return JsonResponse({'status': 'ok'}, status=201)
    else:
        return JsonResponse({'status': 'not ok'}, status=400)


def cart(request):
    temperature_readings = TemperatureReading.objects.all().order_by('-time')
    pulse_readings = PulseReading.objects.all().order_by('-time')
    ecg_readings = ECGReading.objects.all().order_by('-time')

    return render(request, 'cart.html', {'temperature_readings': temperature_readings, 'pulse_readings': pulse_readings, 'ecg_readings': ecg_readings})