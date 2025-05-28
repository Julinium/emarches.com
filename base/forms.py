from django import forms
from portal.models import Profile

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'company', 'avatar', 'ice', 'date_est', 'city', 'country', 'sector', 
            'role', 'phone', 'email', 'whatsapp', 'faximili', 'website', 'note', 
            ]
        widgets = {
            'note': forms.Textarea(attrs={'rows': 3, }),
        }
