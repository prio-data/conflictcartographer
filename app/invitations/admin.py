from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from invitations.models import Invitation

# Register your models here.

def makeLink(url, text=None):
    if text is None:
        text = url
    return f"<p><b><a href={url}>{text}</a></b></p>"

class InvitationInline(admin.StackedInline):
    model = Invitation

admin.site.unregister(User)
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = (InvitationInline,)


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
        "status",
        "user_link",
        "referral_link",
    ]

    def status(self,obj):
        return obj.invitation_status()

    def user_link(self,obj):
        url = f"{reverse('admin:index')}auth/user/{obj.user.pk}"
        return format_html(makeLink(url,"Go to user"))
    
    def referral_link(self,obj):
        try:
            url = reverse("referral",args=[obj.refkey])
            link = makeLink(url)
            warning = '<p class="warning">Warning! If you click this, this invitation will be registered as opened (not observable by user)</p>'
            fieldvalue = link + warning
        except:
            fieldvalue = "-"



        return format_html(fieldvalue)

def makeInvitationLink(inv):
    url = f"{reverse('admin:index')}core/invitation/{inv.pk}"
    return f"<p><a href=\"{url}\">{str(inv)}</a></p>"
