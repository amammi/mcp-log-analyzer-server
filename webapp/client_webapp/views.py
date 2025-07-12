import pathlib

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from client.agent import LogAnalyzerAgentWrapper
from client_webapp.models import McpServerConfig, ProviderModel

import json
import docker
import logging

from client_webapp.utils import create_analysis_pdf

logger = logging.getLogger(__name__)

# Create your views here.
def index(request: HttpRequest):
    return HttpResponse("Index works!")


def log_analyzer_view(request):
    """Vista principale per l'analizzatore log"""
    return render(request, 'client_webapp/index.html')

@csrf_exempt
@require_http_methods(["POST"])
def analyze_logs_api(request):
    """API endpoint per l'analisi dei log"""
    try:
        data = json.loads(request.body)
        container = data.get('container')
        log_level = data.get('log_level')
        
        if not container or not log_level:
            return JsonResponse({'error': 'Container e log level sono obbligatori'}, status=400)

        mcp_servers = McpServerConfig.objects.all()
        selected_provider = ProviderModel.objects.filter(is_active=True)

        if not mcp_servers or len(mcp_servers) == 0:
            return JsonResponse({'error': 'La configurazione dei server MCP è obbligatoria.'}, status=400)

        if not ProviderModel.objects.exists():
            return JsonResponse({'error': 'Non esiste un provider di modelli LLM nel pannello di admin.'}, status=400)

        if not selected_provider.exists():
            return JsonResponse({'error': 'La selezione del LLM non è attiva. Attivarla dal pannello di admin. '},
                                status=400)

        agent = LogAnalyzerAgentWrapper(mcp_servers=list(mcp_servers))

        selected_provider = selected_provider.first()
        result = agent.analyze(provider=selected_provider.model_provider_id.lower().strip(),
                      model=selected_provider.model_name.strip(),
                      container_name=container,
                      log_level_choice=log_level.upper(),
                      api_key=selected_provider.api_key.strip(),
                      base_url=selected_provider.base_url)
        
        return JsonResponse({
            'success': True,
            'result': result,
            'container': container,
            'log_level': log_level
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Dati richiesta non validi'}, status=400)
    except Exception as e:
        logger.exception(e, exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)

def get_active_containers(request):
    """API per ottenere i container attivi"""
    try:
        client = docker.from_env()
        containers = []
        for container in client.containers.list():
            containers.append({
                'id': container.name,
                'name': container.name,
                'status': 'running'})
        return JsonResponse({'containers': containers})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def generate_report(request: HttpRequest):
    try:
        data = json.loads(request.body)
        container = data.get('container_name')
        log_level = data.get('log_level')
        ai_response = data.get('ai_response')

        logo_path = pathlib.Path('./static/logo_v3.png')
        report_bytes = create_analysis_pdf(container_name=container, log_level=log_level, ai_response=ai_response, logo_path=f"{logo_path.absolute()}")

        return HttpResponse(report_bytes, content_type="application/pdf", status=200, headers={'content-disposition': f'attachment; filename="report-{log_level}-{container}.pdf"', 'content-length': str(len(report_bytes))})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Dati richiesta non validi'}, status=400)
    except Exception as e:
        logger.exception(e, exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)