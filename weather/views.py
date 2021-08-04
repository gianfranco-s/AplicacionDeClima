import requests
from django.shortcuts import render, redirect
from requests.models import ContentDecodingError
from .models import City
from .forms import CityForm

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=33aa691b24e49630c8a740405a9b40b0'

    err_msg = ''
    message = ''
    message_class = ''
    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()
            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'No existe la ciudad!'
            else:
                err_msg = 'Ya existe la ciudad en la base de datos!'
        
        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'Ciudad agregada.'
            message_class = 'is-success'
    

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:

        r = requests.get(url.format(city)).json()
        # print(r.text)  # Imprime a Terminal, y me permite determinar los datos que tiene r

        city_weather = {
            'city' : city.name,                          # Viene de la app que estoy creando
            'temperature' : r['main']['temp'],      # Busqué el item "main", que es un diccionario, y dentro de él, "temp"
            'description' : r['weather'][0]['description'],        # "weather" es una lista de un elemento (por eso agarro el elemento [0])
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)


    print(weather_data)

    context = {
        'weather_data' : weather_data ,
        'form' : form,
        'message':message,
        'message_class':message_class
    }

    return render(request, 'weather/weather.html',context)

def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')