from datetime import datetime
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from app.decorators import already_loggedin
from app.forms import *
from app.commons.common_services import *
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from app.forms import RegisterUserForm, LoginForm
from app.models import DXVLLogs, SearchKeyWords
from django.utils.timezone import make_aware
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.templatetags.static import static
from xhtml2pdf import pisa
from django.utils.formats import number_format
from django.utils import timezone
from django.views.generic import View, CreateView, DeleteView, UpdateView

class SearchKeywordsView(View):
    template_name = 'keywords.html'
    
    def get(self, request):
        context = {}
        context['search_keywords'] = SearchKeyWords.objects.all().order_by('-date_added')
        return render(request, self.template_name,context)

class AddSearchKeywordsView(CreateView):
    template_name = 'form_templates/add_form.html'
    model = SearchKeyWords
    form_class = SearchKeywordForm
    success_url = reverse_lazy('search_keywords')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_form'] = SearchKeywordForm()
        return context

    def form_valid(self, form):
        messages.error(self.request, "You have successfully added search keyword for advertisement.",extra_tags="primary")
        response = super().form_valid(form)
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, "Error search keyword advertisement information.", extra_tags="danger")
        return super().form_invalid(form)

class UpdateSearchKeywordView(UpdateView):
    pk_url_kwarg = 'pk'
    model = SearchKeyWords
    form_class = SearchKeywordForm
    template_name = 'form_templates/edit_form.html'
    success_url = reverse_lazy('search_keywords')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['edit_form'] = context.pop('form')
        return context

    def form_valid(self, form):
        messages.error(self.request, "You have successfully updated search keyword.", extra_tags="primary")
        response = super().form_valid(form)
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, "Error while updating search keyword.", extra_tags="danger")
        return super().form_invalid(form)

class DeleteSearchKeywordView(DeleteView):
    pk_url_kwarg = 'pk'
    model = SearchKeyWords
    template_name = 'form_templates/delete_form.html'
    success_url = reverse_lazy('search_keywords')
    
    def form_valid(self, form):
        messages.error(self.request, "You have successfully deleted search keyword.", extra_tags="primary")
        response = super().form_valid(form)
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, "Error while deleting search keyword.", extra_tags="danger")
        return super().form_invalid(form)


@already_loggedin
def login_page_view(request):
    context = {}
    form = LoginForm()
    if request.method == "POST":
        login_form = LoginForm(request.POST)

        check_user = DXVLUsers.objects.get(
            username=request.POST.get("username")
        )

        
        if check_user.is_active == False:
            context["login_form"] = form
            context["error"] = "Your account is still inactive, please try again later."
            return render(request, "login.html", context)
        
        if login_form.is_valid():
            user = authenticate(
                username=login_form.cleaned_data["username"],
                password=login_form.cleaned_data["password"],
            )

            if user is not None:
                login(request, user)
                return redirect(reverse_lazy("dashboard"))
            else:
                context["error"] = "Invalid username or password, please try again."

    context["login_form"] = form
    return render(request, "login.html", context)


@already_loggedin
def register_page_view(request):
    context = {}
    form = RegisterUserForm()
    if request.method == "POST":
        register_form = RegisterUserForm(request.POST)

        if register_form.is_valid():
            register_form.save()
            return redirect(reverse_lazy("login"))
        else:
            context["error"] = "Please check your input, registration failed try again."

    context["register_form"] = form
    return render(request, "register.html", context)


def signout(request):
    logout(request)
    return redirect(reverse_lazy("login"))


@login_required(login_url=reverse_lazy("login"))
def generate_billing_statement(request):
    if request.method == "POST":
        start_date_str = request.POST.get('range_from')
        end_date_str = request.POST.get('range_to')
        account_name = request.POST.get('account_name')

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

            start_date = timezone.make_aware(start_date)
            end_date = timezone.make_aware(end_date.replace(hour=23, minute=59, second=59, microsecond=999999))

        except ValueError:
            return HttpResponse("Invalid date format. Please use YYYY-MM-DD.", status=400)

        query_advertisement = Advertisements.objects.get(
            advertisement_id=request.POST.get('ad_id')
        )

        query_logs = DXVLLogs.objects.filter(
            advertisement=query_advertisement.advertisement_name,
            date_aired__range=(start_date, end_date),
        )

        total_cost = number_format((query_logs.count() * float(query_advertisement.advertisement_price)), force_grouping=True)

        first_record = query_logs.first()
        last_record = query_logs.last()

        header_img_url = request.build_absolute_uri(static("assets/img/billing_header.png"))
        footer_img_url = request.build_absolute_uri(static("assets/img/billing_footer.png"))
        current_date = datetime.now().strftime("%B %d, %Y")
        billing_range = f"{first_record.date_aired.strftime('%B %d')} to {last_record.date_aired.strftime('%B %d, %Y')}"

        context = {
            "account_name": f"{account_name}",
            "current_date": f"{current_date}",
            "particulars": f"{str(int(query_advertisement.advertisement_price))}-seconder radio plug",
            "date_range": f"{billing_range}",
            "total": f"P {total_cost}",
            'header_img_header': header_img_url,
            'header_img_footer': footer_img_url
        }

        html_content = render_to_string("pdf_template/billing_statement.html", context)

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="DXVL_Billing_Statement_{account_name}_{current_date}.pdf"'
        pisa_status = pisa.CreatePDF(html_content, dest=response)

        if pisa_status.err:
            return HttpResponse("Error generating PDF", status=500)

        return response
    else:
        return HttpResponse("Invalid request method.", status=405)
