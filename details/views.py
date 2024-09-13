from django.shortcuts import render, redirect
from .models import Restaurant
from .forms import RestaurantForm

def add_restaurant(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('restaurant_list')
    else:
        form = RestaurantForm()
    return render(request, 'details/add_restaurant.html', {'form': form})

def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'details/restaurant_list.html', {'details': restaurants})

