from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Task, UserProfile

User = get_user_model()


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "assigned_to",
            "priority",
            "status",
            "due_date",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Prepare project plan",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Add task details...",
                }
            ),
            "assigned_to": forms.Select(
                attrs={"class": "form-select"}
            ),
            "priority": forms.Select(
                attrs={"class": "form-select"}
            ),
            "status": forms.Select(
                attrs={"class": "form-select"}
            ),
            "due_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["assigned_to"].queryset = (
            User.objects.filter(is_active=True)
            .order_by("first_name", "username")
        )

        for field in self.fields.values():
            if not field.widget.attrs.get("class"):
                field.widget.attrs["class"] = "form-control"


class MemberCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
    )

    last_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "autocomplete": "email",
            }
        )
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
        )
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "autocomplete": "username",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs["class"] = (
            "form-control"
        )

        self.fields["password1"].widget.attrs.update(
            {
                "class": "form-control",
                "autocomplete": "new-password",
            }
        )

        self.fields["password2"].widget.attrs.update(
            {
                "class": "form-control",
                "autocomplete": "new-password",
            }
        )

    def clean_email(self):
        email = self.cleaned_data["email"].strip()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "An account with this email address already exists."
            )

        return email

    def save(self, commit=True):
        user = super().save(commit=False)

        user.email = self.cleaned_data["email"].strip()
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data.get("last_name", "")

        if commit:
            user.save()

            profile, _ = UserProfile.objects.get_or_create(
                user=user
            )
            profile.role = UserProfile.Role.MEMBER
            profile.save()

        return user


class EmailOrUsernameAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Email address or username",
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Enter your email or username",
                "autocomplete": "username",
                "autofocus": True,
            }
        ),
    )

    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Enter your password",
                "autocomplete": "current-password",
            }
        ),
    )

    def clean_username(self):
        value = self.cleaned_data["username"].strip()

        # Support login with either an email address or username.
        if "@" in value:
            user = User.objects.filter(
                email__iexact=value
            ).first()

            if user:
                return user.get_username()

        return value


class StatusUpdateForm(forms.Form):
    status = forms.ChoiceField(
        choices=Task.Status.choices,
        widget=forms.Select(
            attrs={"class": "form-select form-select-sm"}
        ),
    )