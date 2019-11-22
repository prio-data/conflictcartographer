from django.contrib import admin
from core.models import Invitation, Cohort
from django.urls import reverse
from django.utils.html import format_html

# Register your models here.

def makeLink(url, text=None):
    if text is None:
        text = url
    return f"<p><b><a href={url}>{text}</a></b></p>"

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

@admin.register(Cohort)
class CohortAdmin(admin.ModelAdmin):
    readonly_fields = [
        "stamp",
        "number_of_invitations",     
        "invitations_registered",
        "invitations_reached",
        "invitations_opened",
        "cohort_invitation_links"
    ]

    def cohort_invitations(self,obj):
        return obj.invitations.all()

    def cohort_invitation_links(self,obj):
        invitations = self.cohort_invitations(obj)
        links = "\n".join([makeInvitationLink(i) for i in invitations])
        return format_html(links)

    def number_of_invitations(self,obj):
        return len(self.cohort_invitations(obj))

    def invitations_reached(self,obj):
        return sum([i.reached for i in self.cohort_invitations(obj)])

    def invitations_opened(self,obj):
        return sum([i.opened for i in self.cohort_invitations(obj)]) 

    def invitations_registered(self,obj):
        return sum([i.registered for i in self.cohort_invitations(obj)])
