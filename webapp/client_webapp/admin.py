from django.contrib import admin
from .models import ProviderModel, SelectionParam, McpServerConfig


# Register your models here.

@admin.register(ProviderModel)
class ProviderModelSetting(admin.ModelAdmin):
    pass

@admin.register(SelectionParam)
class SelectionParamSetting(admin.ModelAdmin):
    def has_add_permission(self, request):
        """Di questo ModelAdmin è permessa una sola istanza."""
        return not SelectionParam.objects.exists()


@admin.register(McpServerConfig)
class McpServerConfigSetting(admin.ModelAdmin):
    # TODO support for multi mcp servers
    def has_add_permission(self, request):
        """Di questo ModelAdmin è permessa una sola istanza."""
        return not McpServerConfig.objects.exists()