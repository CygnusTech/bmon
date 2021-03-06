from django.conf.urls import include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('bmsapp.urls')),
]

admin.site.site_title = 'BMON Admin'
admin.site.site_header = 'BMON Administration'
admin.site.index_title = 'Site Administration'
