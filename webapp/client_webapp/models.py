from django.db import models

# Create your models here.
class ProviderModel(models.Model):
    model_provider_id = models.TextField(primary_key=True, choices=[("OPENAI", "OpenAI"), ("OLLAMA", "Ollama (Private LLM server)"), ("ANTHROPIC", "Anthropic")])
    model_name = models.CharField(default="gpt-4.1-mini")
    api_key = models.CharField(default="ollama")
    base_url = models.URLField(blank=True, default=None)

    def __str__(self):
        return f"{self.model_provider_id} - {self.model_name}"


class McpServerConfig(models.Model):
    name = models.CharField(default=None)
    base_url = models.URLField(default="http://127.0.0.1:8000")
    connection_type = models.CharField(choices=[("sse", "Sse")], default="sse")

    def __str__(self):
        return self.name


class SelectionParam(models.Model):
    provider_selection = models.ForeignKey(ProviderModel, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.provider_selection}"