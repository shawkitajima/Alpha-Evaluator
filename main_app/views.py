from django.shortcuts import render, redirect
import os
import requests
from datetime import datetime
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from .models import Company, Performance


def home(request):
 return render(request, 'home.html')

@login_required
def my_stocks(request):
  return render(request, 'my_stocks.html')

@login_required
def company_search(request):
  ticker = request.POST['ticker']
  return redirect('detail', ticker=ticker)


def company_detail(request, ticker):
  news = fetchNews(ticker)
  prices = fetchPrices(ticker)
  info = fetchInfo(ticker)
  return render(request, 'detail.html', {
    'news': news,
    'prices': prices,
    'info': info
  })

def fetchPrices(ticker):
    API_KEY = os.environ['ALPHA_KEY']
    response = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&outputsize=full&apikey={API_KEY}')
    obj = response.json()
    days = obj['Time Series (Daily)']
    arr = []
    for key, val in days.items():
        arr.append(
            {
                'date': key,
                'close': val['4. close']
            }
        )
    return arr

def fetchNews(ticker):
    API_KEY = os.environ['FINN_KEY']
    response = requests.get(f'https://finnhub.io/api/v1/news/{ticker}?token={API_KEY}')
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


def fetchInfo(ticker):
    API_KEY = os.environ['FINN_KEY']
    response = requests.get(f'https://finnhub.io/api/v1/stock/profile?symbol={ticker}&token={API_KEY}')
    obj = response.json()
    info = {
        'address': obj['address'],
        'city': obj['city'],
        'description': obj['description'],
        'exchange': obj['exchange'],
        'name': obj['name'],
        'weburl': obj['weburl'],
        'state': obj['state'],
        'phone': obj['phone']
    }
    return info

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('my_stocks')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)
