from django.shortcuts import render, redirect
from django.views import View
from .forms import ComandoForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Comando


class CommandListView(LoginRequiredMixin, View):
    template_name =  "comando.html"

    def get(self, request):
        executed_commands = Comando.objects.filter(ejecutado=True).order_by("-fecha_y_hora")
        not_executed_commands = Comando.objects.filter(ejecutado=False).order_by("fecha_y_hora")
        context = {
            "executed_commands": executed_commands,
            "not_executed_commands": not_executed_commands

        }
        return render(request, self.template_name, context)
    


class NewCommandView(LoginRequiredMixin, View):
    template_name =  "comando.html"
    form = ComandoForm

    def get(self, request):
        context = {
            "form" : self.form()
        }        
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Command successfully added")
            return redirect("lista-comando")
        else:
            messages.warning(request, "Error processing your request")
            return render(request, self.template_name, {"form": form})

class CommandEditView(LoginRequiredMixin, View):
    template_name = "comando_edit.html"
    form = ComandoForm
    
    def get(self,request, cmd_id):
        self.cmd = Comando.objects.get(id=cmd_id)
        form = self.form(instance=self.cmd)
        context = {
            "form": form,
            "comando": self.cmd
        }
        return render(request, self.template_name, context)
    
    def post(self, request, cmd_id):
        submit_value = request.POST.get('submit_value')
        self.cmd = Comando.objects.get(id=cmd_id)
        form = self.form(request.POST, instance=self.cmd)
        
        if submit_value == 'update':
            return self.handle_update(form)
        elif submit_value == 'delete':
            return self.handle_delete(self.cmd)

        return redirect("lista-comando")

    def handle_update(self, form):
        if form.is_valid():
            form.save()
            messages.success(self.request, "Command successfully updated")
            return redirect("lista-comando")
        else:
            return self.form_invalid(form)

    def handle_delete(self, cmd):
        cmd.delete()
        messages.success(self.request, "Command successfully deleted")
        return redirect("lista-comando")

    def form_invalid(self, form):
        messages.error(self.request, "There was an error processing your request")
        return render(self.request, self.template_name, {'form': form,
                                                         "comando": self.cmd})