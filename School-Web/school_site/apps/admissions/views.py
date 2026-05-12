from django.shortcuts import render
from .models import AdmissionBrochure, Job, ZhongKaoFAQ


def brochures(request):
    brochures = AdmissionBrochure.objects.filter(is_active=True)
    return render(request, 'admissions/brochures.html', {'brochures': brochures})


def jobs(request):
    jobs = Job.objects.filter(is_active=True)
    return render(request, 'admissions/jobs.html', {'jobs': jobs})


def zhongkao_faq(request):
    faqs = ZhongKaoFAQ.objects.all()
    return render(request, 'admissions/zhongkao_faq.html', {'faqs': faqs})