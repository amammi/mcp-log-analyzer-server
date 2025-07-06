from django.db import models

# Create your models here.
class ProviderModel(models.Model):
    model_provider_id = models.TextField(primary_key=True, choices=[("OPENAI", "OpenAI"), ("OLLAMA", "Ollama (Local LLM server)")])
    model_name = models.CharField(default="gpt-4.1-mini")
    api_key = models.CharField(default="ollama")
    base_url = models.URLField(blank=True, default=None)

    def __str__(self):
        return f"{self.model_provider_id} - {self.model_name}"



class SelectionParam(models.Model):
    provider_selection = models.ForeignKey(ProviderModel, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.provider_selection}"