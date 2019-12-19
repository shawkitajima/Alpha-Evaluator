from django.shortcuts import render, redirect
import os
import requests
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from .models import Company, Performance


def home(request):
  return HttpResponse('<h1>Hello /ᐠ｡‸｡ᐟ\ﾉ</h1>')

def my_stocks(request):
  return HttpResponse('Congrats on logging in')


def company_detail(request, company_id):
  company = Company.objects.get(id=company_id)
  news = fetchNews(company.ticker)
  return render(request, 'detail.html', {
    'news': news,
    'company': company
  })

def fetchNews(ticker):
    response = requests.get(f'https://finnhub.io/api/v1/news/{ticker}?token=bnp91cnrh5re75ftjav0')
    arr = response.json()
    final = []
    for obj in arr:
        date = str(obj['datetime'])
        date = int(date[:10])
        date = datetime.fromtimestamp(date).strftime('%Y-%m-%d')
        final.append({
            'date': date,
            'headline': obj['headline'],
            'image': obj['image'],
            'source': obj['source']
        })
    return final

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)