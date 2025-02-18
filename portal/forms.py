from django import forms

class InstallForm(forms.Form): 
    netbox_url = forms.CharField(max_length=80, initial='http://192.168.3.105:8080/')
    netbox_api_token = forms.CharField(max_length=120, initial='0123456789abcdef0123456789abcdef01234567')
    vlan_id = forms.IntegerField(initial=802)
    vlan_name = forms.CharField(max_length=80, initial='net2d-lab')
    prefix4 = forms.CharField(max_length=120, initial='192.168.3.0/24')
    prefix6 = forms.CharField(max_length=120, initial='2001:db8:cafe::/64')
    device_name = forms.CharField(max_length=120, initial='sw-lab-01')
    device_address4 = forms.CharField(max_length=120, initial='192.168.3.196/24')
    device_address6 = forms.CharField(max_length=120, initial='2001:db8:cafe::196/64')
    