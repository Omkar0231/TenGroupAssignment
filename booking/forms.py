from django import forms


class CSVUploadForm(forms.Form):
    MEMBER_INFO = "member_info"
    INVENTORY = "inventory"

    choices = (
        (MEMBER_INFO, "Member Info"),
        (INVENTORY, "Inventory")
    )
    file = forms.FileField(
        label="Upload CSV File",
        widget=forms.ClearableFileInput(attrs={"accept": ".csv"})
    )
    model = forms.ChoiceField(choices=choices, help_text="Select the Table to insert data.")
