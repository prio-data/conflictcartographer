from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from invitations.models import Invitation
from api.models import Profile

# Register your models here.

def makeLink(url, text=None):
    if text is None:
        text = url
    return f"<p><b><a href={url}>{text}</a></b></p>"

class ProfileInline(admin.StackedInline):
    model = Profile 

admin.site.unregister(User)
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = (
            ProfileInline,
        )

@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    exclude = [
        "user",
        "refkey",
        "reached",
        "opened",
        "registered",
    ]

    readonly_fields =[
        "referral_link",
    ]
    
    def referral_link(self,obj):
        try:
            url = reverse("referral",args=[obj.refkey])
            link = makeLink(url)
            fieldvalue = link
        except:
            fieldvalue = "-"



        return format_html(fieldvalue)

def makeInvitationLink(inv):
    url = f"{reverse('admin:index')}core/invitation/{inv.pk}"
    return f"<p><a href=\"{url}\">{str(inv)}</a></p>"
