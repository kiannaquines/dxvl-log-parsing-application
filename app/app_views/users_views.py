from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from app.models import DXVLUsers
from django.contrib.auth.decorators import login_required
from app.commons.common_services import all_objects_only,pagination
from django.views.generic import UpdateView,DeleteView, CreateView
from django.urls import reverse_lazy
from app.forms import EditUserForm,RegisterUserForm
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required(login_url=reverse_lazy('login'))
def users(request):
    context = {}
    users_list = all_objects_only(DXVLUsers.objects,'username','email','first_name','last_name','date_joined')
    page_obj = pagination(users_list,request.GET.get('page'),10)
    context['users_obj'] = page_obj
    return render(request,"users.html",context)

class NewUserView(LoginRequiredMixin, CreateView):
    template_name = 'form_templates/add_form.html'
    model = DXVLUsers
    form_class = RegisterUserForm
    success_url = reverse_lazy('users')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_form'] = context.pop('form')
        return context
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response  = super().form_valid(form)
        return response

class EditUserView(LoginRequiredMixin, UpdateView):
    template_name = 'form_templates/edit_form.html'
    model = DXVLUsers
    pk_url_kwarg = 'pk'
    form_class = EditUserForm
    success_url = reverse_lazy('users')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['edit_form'] = context.pop('form')
        return context
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_valid(form)
        return response
    
class DeleteUserView(LoginRequiredMixin, DeleteView):
    template_name = 'form_templates/delete_form.html'
    model = DXVLUsers
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('users')

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_valid(form)
        return response