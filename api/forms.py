from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm
from django.core.exceptions import ValidationError
from django import forms
from django.utils.translation import gettext_lazy as _
from api.models import User, Product, ProductInfo, Category, Shop, ConfirmEmailToken


class ConfirmAccountForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = ConfirmEmailToken
        fields = [
            'email',
            'key',
        ]


class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    shop = forms.ModelChoiceField(queryset=Shop.objects.all())
    product = forms.ModelChoiceField(queryset=Product.objects.all())

    class Meta:
        model = ProductInfo
        fields = [
            'category',
            'product',
            'shop',
    ]


class RegistrationForm(UserCreationForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Password confirmation'), widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'username',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active',)
