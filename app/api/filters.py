from datetime import datetime

# These functions take a queryset and apply a filter.

# ================================================
# Only return active projects
# Admins are excempt
def active(queryset,request):
    now = datetime.now()
    if not request.user.is_staff:
        queryset = queryset.filter(
            startdate__lt = now, 
            enddate__gt = now) 
    return queryset
