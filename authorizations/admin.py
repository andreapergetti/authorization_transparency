import json

from django.contrib import admin
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncDay
from django.http import JsonResponse
from django.urls import path

from authorizations.models import Authorizations


# Register your models here.
class AuthorizationsAdmin(admin.ModelAdmin):
    fields = ('issuer', 'server', 'client', 'start_validity', 'expiration_time')
    list_display = ('issuer', 'server', 'client', 'start_validity', 'expiration_time')
    search_fields = ['issuer__user__username', 'server', 'client', 'start_validity', 'expiration_time']


class MyAuthorizations(Authorizations):
    class Meta:
        proxy = True


class AuthorizationReleaseAdmin(admin.ModelAdmin):
#    AuthorizationsAdmin):
    fields = ('issuer', 'server', 'client', 'start_validity', 'expiration_time')
    list_display = ('issuer', 'server', 'client', 'start_validity', 'expiration_time')
    ordering = ('-start_validity',)

    def changelist_view(self, request, extra_context=None):
        # Aggregate new subscribers per day
        chart_data = (
            Authorizations.objects.annotate(date=TruncDay("start_validity")).values("date").annotate(
                y=Count("id")).order_by("-date")
        )

        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}

        # Call the superclass changelist_view to render the page
        print(extra_context)
        return super().changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        extra_urls = [
            path("chart_data/", self.admin_site.admin_view(self.chart_data_endpoint))
        ]
        # NOTE! Our custom urls have to go before the default urls, because they
        # default ones match anything.
        return extra_urls + urls

    # JSON endpoint for generating chart data that is used for dynamic loading
    # via JS.
    def chart_data_endpoint(self, request):
        chart_data = self.chart_data()
        return JsonResponse(list(chart_data), safe=False)

    def chart_data(self):
        return (
            Authorizations.objects.annotate(date=TruncDay("start_validity"))
                .values("date")
                .annotate(y=Count("id"))
                .order_by("-date")
        )


#admin.site.register(Authorizations, AuthorizationsAdmin)
#admin.site.register(MyAuthorizations, AuthorizationReleaseAdmin)
admin.site.register(Authorizations, AuthorizationReleaseAdmin)
