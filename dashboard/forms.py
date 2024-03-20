from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Employee, Team, Task


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
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control"},
        )
    )

    class Meta(UserCreationForm.Meta):
        model = Employee
        fields = UserCreationForm.Meta.fields + ("role", "team")


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"

    def __init__(self, team=None, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        if team:
            self.fields["assigned_to"].queryset = team.members.all()

        for field_name, field in self.fields.items():
            if field_name not in ["assigned_to", "is_completed"]:
                field.widget.attrs.update({"class": "form-control"})

    assigned_to = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    type = forms.ChoiceField(
        label="Type",
        choices=Task.Type.choices,
        required=True
    )

    is_completed = forms.CheckboxInput(
    )

    deadline = forms.DateTimeField(
        label="Deadline",
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        required=False
    )


class SearchForm(forms.Form):
    search_key = forms.CharField(
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
