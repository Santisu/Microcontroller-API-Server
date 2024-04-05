from datetime import timedelta
from django.utils import timezone
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from app_api.models import Peticion
from app_user.forms import LoginForm
from microcontroller_server.settings import USUARIO_CONTROLADOR


# Create your views here.
class IndexView(View):
    template_name = 'index.html'
    def get(self, request):
        last_microcontroller_query = Peticion.objects.filter(user=USUARIO_CONTROLADOR).last()
        time_left = self.time_difference(last_microcontroller_query.fecha_y_hora)
        context = {
            "last_microcontroller_query": last_microcontroller_query,
            "minutes": time_left[1],
            "seconds": time_left[2],
        }
        
        return render(request, self.template_name, context)
    
    def time_difference(self, last_query_time):
        current_time = timezone.now()
        next_time = last_query_time + timedelta(minutes=15)
        time_left = next_time - current_time
        return str(time_left).split(":")
    

class LoginView(View):
    """Login view"""

    form = LoginForm
    template = 'login.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse('index'))  # Redirige al index
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form()
        context = {'form' : form}
        return render(request, self.template, context)
    
    def post(self, request):
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            context = {"error": "User not found or wrong password",
                       'form': self.form()}
            return render(request, 'login.html', context)
        else:
            login(request, user)
            return redirect('lista-comando')
        
@login_required
def logout_view(request):
    """Logout view"""
    logout(request)
    return redirect('login')