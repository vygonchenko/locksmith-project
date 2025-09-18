# core/views.py
from django.shortcuts import render
from django.http import JsonResponse
from .forms import CallbackForm
from .models import CallbackRequest
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def home(request):
    form = CallbackForm()
    if request.method == 'POST':
        form = CallbackForm(request.POST)
        if form.is_valid():
            callback = CallbackRequest.objects.create(
                name=form.cleaned_data['name'],
                phone=form.cleaned_data['phone'],
                preferred_time=form.cleaned_data['time'],
                message=form.cleaned_data['message']
            )
            # Отправка email уведомления
            send_callback_email(callback)
            return render(request, 'home.html', {'form': form, 'success': True})
    return render(request, 'home.html', {'form': form})

def callback_view(request):
    if request.method == 'POST':
        form = CallbackForm(request.POST)
        if form.is_valid():
            callback = CallbackRequest.objects.create(
                name=form.cleaned_data['name'],
                phone=form.cleaned_data['phone'],
                preferred_time=form.cleaned_data['time'],
                message=form.cleaned_data['message']
            )
            # Отправка email уведомления
            send_callback_email(callback)
            return JsonResponse({'success': True, 'message': 'Спасибо! Мы свяжемся с вами в ближайшее время.'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = CallbackForm()
        return render(request, 'core/callback.html', {'form': form})

def send_callback_email(callback):
    """Отправка email уведомления о новой заявке"""
    subject = f'Новая заявка на звонок от {callback.name}'
    context = {
        'name': callback.name,
        'phone': callback.phone,
        'preferred_time': callback.preferred_time,
        'message': callback.message
    }
    message = render_to_string('email/callback_notification.html', context)
    
    send_mail(
        subject,
        'Пожалуйста, свяжитесь с клиентом в указанное время.',
        settings.DEFAULT_FROM_EMAIL,
        ['vygonchenko@gmail.com'],  # Укажите ваш email
        html_message=message,
        fail_silently=False,
    )