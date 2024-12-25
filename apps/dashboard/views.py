from http import HTTPStatus

from django.shortcuts import render

# Create your views here.


def dashboard(request):
    return render(
        request=request,
        template_name="dashboard/pages/dashboard.html",
        status=HTTPStatus.OK,
        context={
            "user_info": {
                "name": "Mickey Mouse",
                "email": "teste@test.com",
                "phone": "123456789",
            },
        },
    )
