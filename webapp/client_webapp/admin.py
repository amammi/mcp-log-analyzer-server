from django.contrib import admin
from .models import ProviderModel, McpServerConfig


# Register your models here.

class LogAnalyzerAdminSite(admin.AdminSite):
    site_url = "/"
    site_header = "AI Log Analyzer"
    site_title = "AILA Admin Panel"
    index_template = "admin/index.html"
    index_title = "AI Log Analyzer Admin Panel"
    app_index_template = "admin/app_index.html"



admin_site = LogAnalyzerAdminSite(name="AI Log Analyzer")


class ProviderModelSetting(admin.ModelAdmin):

    list_per_page = 10
    list_display = ['model_provider_id', 'model_name', 'is_active']
    search_fields = ['model_provider_id', 'model_name', 'is_active']

    pass


class McpServerConfigSetting(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['name', 'base_url', 'connection_type']
    search_fields = ['name']
    # TODO support for multi mcp servers
    def has_add_permission(self, request):
        """Di questo ModelAdmin è permessa una sola istanza."""
        return not McpServerConfig.objects.exists()


admin_site.register(ProviderModel, ProviderModelSetting)
admin_site.register(McpServerConfig, McpServerConfigSetting)