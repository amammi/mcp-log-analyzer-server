from django.contrib import admin
from .models import ProviderModel, SelectionParam, McpServerConfig


# Register your models here.

class LogAnalyzerAdminSite(admin.AdminSite):
    site_header = "AI Log Analyzer"
    site_title = "AILA Admin Panel"
    index_title = "AI Log Analyzer Admin Panel"
    site_url = "/client"
    index_template = "admin/index.html"
    app_index_template = "admin/app_index.html"


admin_site = LogAnalyzerAdminSite(name="AI Log Analyzer")


class ProviderModelSetting(admin.ModelAdmin):
    pass

class SelectionParamSetting(admin.ModelAdmin):
    def has_add_permission(self, request):
        """Di questo ModelAdmin è permessa una sola istanza."""
        return not SelectionParam.objects.exists()


class McpServerConfigSetting(admin.ModelAdmin):
    # TODO support for multi mcp servers
    def has_add_permission(self, request):
        """Di questo ModelAdmin è permessa una sola istanza."""
        return not McpServerConfig.objects.exists()


admin_site.register(ProviderModel, ProviderModelSetting)
admin_site.register(SelectionParam, SelectionParamSetting)
admin_site.register(McpServerConfig, McpServerConfigSetting)