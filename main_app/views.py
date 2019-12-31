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
  companies = Company.objects.filter(user=request.user)
  tickers = []
  for company in companies:
    API_KEY = os.environ['FINN_KEY']
    response = requests.get(f'https://finnhub.io/api/v1/quote?symbol={company.ticker}&token={API_KEY}')
    obj = response.json()
    tickers.append(
      {
        'id': company.id,
        'name': company.name,
        'ticker': company.ticker,
        'price': obj['c'],
      }
    )
  return render(request, 'my_stocks.html', {'watchList': tickers})

@login_required
def company_delete(request, company_id):
  Company.objects.filter(id=company_id).delete()
  return redirect('my_stocks')

@login_required
def company_search(request):
  ticker = request.POST['ticker']
  return redirect('detail', ticker=ticker)


def company_detail(request, ticker):
  news = fetchNews(ticker)
  prices = fetchPrices(ticker)
  prices.reverse()
  info = fetchInfo(ticker)
  return render(request, 'detail.html', {
    'news': news,
    'prices': prices,
    'info': info,
    'ticker': ticker
  })

def company_add(request):
  company = Company(
    ticker=request.POST['ticker'],
    name=request.POST['name'],
    user=request.user
  )
  company.save()
  return redirect('detail', ticker=request.POST['ticker'])

def add_performance(request):
  performance = Performance(
    ticker = request.POST['ticker'],
    buy = request.POST['buy'],
    sell = request.POST['sell'],
    user =  request.user.id
  )
  performance.save()
  return redirect('playground', ticker=request.POST['ticker'])


def fetchPrices(ticker):
    API_KEY = os.environ['ALPHA_KEY']
    response = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={ticker}&outputsize=full&apikey={API_KEY}')
    obj = response.json()
    days = obj['Time Series (Daily)']
    arr = []
    for key, val in days.items():
      date = str(datetime.strptime(key, '%Y-%M-%d'))
      arr.append(
          {
              'date': date,
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
            'source': obj['source'],
            'url': obj['url'],
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
