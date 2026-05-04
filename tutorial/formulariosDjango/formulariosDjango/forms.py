from django import forms

class ComentarioForm(forms.Form):
    name = forms.CharField(label="escribe tu nombre", help_text="100 chars max")
    url = forms.URLField(label="tu sitio web", required=False)
    comment = forms.CharField()


class ContactForm(forms.Form):
    name = forms.CharField(
        label="escribe tu nombre",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(
        label="email",
        max_length="50",
        widget=forms.EmailInput(attrs={'class': 'form-control'}))
    message = forms.CharField(
        label="di algo",
        widget=forms.Textarea(attrs={'class': 'form-control'}))
    
    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name != "manuel":
            raise forms.ValidationError("El valor manuel es el único que puedes poner")
        else:
            return name