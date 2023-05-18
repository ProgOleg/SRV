from django import forms

from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from srvbd import models


# ***__Добавление клиента__***
class PersonCreate(forms.ModelForm):
    class Meta:
        model = models.Person
        fields = ["first_name", "last_name", "patronymic_name", "tell", "addres", "email", "role", "discount"]

        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите имя",
                }
            ),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите фамилию"}),
            "patronymic_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите отчество"}),
            "tell": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Введите номер телефона", "value": "+380"}
            ),
            "addres": forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите адрес"}),
            "email": forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите email"}),
            "role": forms.Select(attrs={"class": "form-control", "id": "role"}),
            "discount": forms.NumberInput(attrs={"class": "form-control", "id": "discount", "max": 100, "min": 0}),
        }

    def clean_tell(self):
        new_tell = self.cleaned_data["tell"]
        s = "+38"
        if new_tell[:3] != s and len(new_tell) == 10:
            new_tell = s + new_tell
        if len(new_tell) != 13:
            raise ValidationError("Не допустимое кол-во символов")
        for i in new_tell:
            if i == "+":
                continue
            try:
                int(i)
            except ValueError:
                raise ValidationError("Номер не должен состоять из букв!")
        return new_tell

    def clean_first_name(self):
        c = self.cleaned_data["first_name"]
        c = c.lower().capitalize()
        return c

    def clean_last_name(self):
        c = self.cleaned_data["last_name"]
        c = c.lower().capitalize()
        return c

    def clean_patronymic_name(self):
        c = self.cleaned_data["patronymic_name"]
        c = c.lower().capitalize()
        return c

    def clean_discount(self):
        discount = self.cleaned_data["discount"]
        if discount > 100 or discount < 0:
            raise ValidationError("Не больше 100, не меньше 0!")
        return discount


# ***__Добавление поставщика__***
class ShipperCreate(forms.ModelForm):
    class Meta:
        model = models.Shipper
        fields = [
            "first_name",
            "last_name",
            "patronymic_name",
            "specification",
        ]

        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите имя",
                }
            ),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите фамилию"}),
            "patronymic_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите отчество"}),
            "specification": forms.Textarea(attrs={"class": "form-control", "placeholder": "Введите описание"}),
        }

    def clean_first_name(self):
        c = self.cleaned_data["first_name"]
        c = c.lower().capitalize()
        return c

    def clean_last_name(self):
        c = self.cleaned_data["last_name"]
        c = c.lower().capitalize()
        return c

    def clean_patronymic_name(self):
        c = self.cleaned_data["patronymic_name"]
        c = c.lower().capitalize()
        return c


# ***__Добавление запчастей в справочник__***
class AddPart(forms.ModelForm):
    part_num = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите партномер", "name": "bvz"}),
        initial=""
    )

    class Meta:
        model = models.SparPart
        fields = ["name", "part_num", "specification"]

        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Введите наименование", "name": "bvz"}
            ),
            "specification": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Введите описание", "rows": "4"}
            )
        }


# ***__Добавленгие типа запчасти__***
class AddTypeSparPart(forms.ModelForm):
    class Meta:
        model = models.TypeSparPart
        fields = ["type_spar_part"]

        widgets = {
            "type_spar_part": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Введите наименование", "name": "type_spar_part"}
            )
        }

    def clean_type_spar_part(self):
        obj = self.cleaned_data["type_spar_part"]
        obj = obj.lower().capitalize()

        return obj


# ***__Добавление типа устройства__***
class AddTypeAppliances(forms.ModelForm):
    class Meta:
        model = models.TypeAppliances
        fields = ["type_appliances"]

        widgets = {
            "type_appliances": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Введите наименование", "name": "type_appliances"}
            )
        }

    def clean_type_appliances(self):
        obj = self.cleaned_data["type_appliances"]
        obj = obj.lower().capitalize()
        return obj


# ***__Добавление производителя__***
class AddManufacturer(forms.ModelForm):
    class Meta:
        model = models.Manufacturer
        fields = ["manufacturer"]

        widgets = {
            "manufacturer": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Введите наименование", "name": "manufacturer"}
            )
        }

    def clean_manufacturer(self):
        obj = self.cleaned_data["manufacturer"]
        obj = obj.lower().capitalize()
        return obj


# ***__Создание прихода__***


class CreateIncom(forms.ModelForm):
    class Meta:
        model = models.Incoming
        fields = ["incoming_date", "ship", "currency"]
        widgets = {
            "incoming_date": forms.DateInput(
                attrs={
                    "class": "form-control ",
                    "id": "datepicker",
                    "placeholder": "Укажите дату прихода",
                }
            ),
            "ship": forms.Select(attrs={"class": "form-control"}),
            "currency": forms.Select(attrs={"class": "form-control"}),
        }


# ***__Создание прихода и добавление запчастей на склад__***!!!ЖЕСТКО ЗАКОДИРОВАНЫЕ УРЛЫ В ДАТА АТРИБУТЕ!!!
class IncomInfoShipper(forms.Form):
    attachment_appliances = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "list": "attachment_appliances",
                "class": "form-control",
                "data-ajax_url": "/ajax_tools_select_applience/",
            }
        ),
    )
    attachment_part = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "list": "attachment_part",
                "class": "form-control",
                "data-ajax_url": "/ajax_tools_select_type_sparpart/",
            }
        ),
    )
    attachment_manufacturer = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "list": "attachment_manufacturer",
                "class": "form-control",
                "data-ajax_url": "/ajax_tools_select_manufacturer/",
            }
        ),
    )


class AddDeviceForm(forms.ModelForm):
    class Meta:
        model = models.Device
        fields = ["mod", "pnc"]
        widgets = {
            "mod": forms.TextInput(attrs={"class": "form-control"}),
            "pnc": forms.TextInput(attrs={"class": "form-control"}),
        }


class SelectManufacturTypeAppliances(forms.Form):

    type_appliances = forms.CharField(
        widget=forms.TextInput(attrs={"list": "type_appliances", "class": "form-control "})
    )
    manufacturer = forms.CharField(widget=forms.TextInput(attrs={"list": "manufacturer", "class": "form-control "}))


class FilterDetail(forms.Form):

    name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "name",
                "maxlength": "50",
            }
        ),
    )
    specification = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "specification",
                "maxlength": "50",
            }
        ),
    )
    part_num = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "part_num",
                "maxlength": "50",
            }
        ),
    )


class ExchangeRatesForm(forms.ModelForm):
    class Meta:
        model = models.ExchangeRates
        fields = ["exchange_rates"]
        widgets = {
            "exchange_rates": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Укажите курс 'EUR'", "step": "0.01", "value": "0.00"}
            )
        }

    def clean_exchange_rates(self):
        data = self.cleaned_data["exchange_rates"]
        if float(data) < 1:
            self.add_error(error="курс не может быть меньше еденицы", field="exchange_rates")
        return data


class AuthUserForm(AuthenticationForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "password")


class MatSaleObjChangeQuantity(forms.Form):

    quantity = forms.FloatField(required=False, widget=forms.NumberInput(attrs={}))

    def clean_quantity(self):
        data = self.cleaned_data["quantity"]
        if len(str(data)) == 0:
            raise ValidationError("Значение не должно быть пустым", code="invalid")
        if data <= 0:
            raise ValidationError(("Значение не должно быть отрицательным или 0",), code="invalid")
        return round(data, 2)


class MatSaleObjChangeSalePrice(forms.Form):

    sale_price = forms.FloatField(required=False, widget=forms.NumberInput(attrs={}))

    def clean_sale_price(self):

        data = self.cleaned_data["sale_price"]
        if len(str(data)) == 0:
            raise ValidationError("Значение не должно быть пустым", code="invalid")
        if data <= 0:
            raise ValidationError("Значение не должно быть отрицательным или 0", code="invalid")
        return round(data, 2)
