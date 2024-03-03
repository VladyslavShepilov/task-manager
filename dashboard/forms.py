from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Employee, Team


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))


class EmployeeCreateForm(UserCreationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"}
        )
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"}
        )
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"}
        )
    )
    password2 = forms.CharField(
        label="Password check",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password check",
                   "class": "form-control"}
        )
    )
    role = forms.ChoiceField(
        label="Role",
        choices=Employee.Role.choices,
        widget=forms.Select(
            attrs={
                "class": "form-control"}
        )
    )
    team = forms.ModelChoiceField(
        label="Team",
        queryset=Team.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control"}
        )
    )

    class Meta(UserCreationForm.Meta):
        model = Employee
        fields = UserCreationForm.Meta.fields + ("role", "team")


class EmployeeSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search",
                "autocomplete": "off"
            }
        ),
    )
