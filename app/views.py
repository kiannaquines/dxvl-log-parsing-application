from django.http import HttpResponse
from django.shortcuts import render
from app.decorators import already_loggedin
from app.forms import *
from app.commons.common_services import *
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from app.forms import RegisterUserForm, LoginForm


@already_loggedin
def login_page_view(request):
    context = {}
    form = LoginForm()
    if request.method == "POST":
        login_form = LoginForm(request.POST)

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


from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static


@login_required(login_url=reverse_lazy("login"))
def generate_billing_statement(request):
    if request.method == "POST":
        from xhtml2pdf import pisa
        from django.template.loader import render_to_string
        header_img_url = request.build_absolute_uri(static("assets/img/billing_header.png"))
        footer_img_url = request.build_absolute_uri(static("assets/img/billing_footer.png"))
        context = {
            "billing_details": [
                {
                    "particulars": "60-seconder radio plug",
                    "cost_per_hour": "5,500/Month",
                    "date_range": "May 01 to August 17, 2024",
                    "total": "P 18,210.00",
                },
            ],
            'header_img_header': header_img_url,
            'header_img_footer': footer_img_url
        }

        html_content = render_to_string("pdf_template/billing_statement.html", context)
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="billing_statement.pdf"'
        pisa_status = pisa.CreatePDF(html_content, dest=response)
        if pisa_status.err:
            return HttpResponse("Error generating PDF", status=500)

        return response
