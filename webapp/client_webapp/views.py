from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from client.agent import LogAnalyzerAgentWrapper

import json
import time
import docker

from client_webapp.models import SelectionParam


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
        
        agent = LogAnalyzerAgentWrapper()

        if not SelectionParam.objects.exists():
            return JsonResponse({'error': 'Non esiste una selezione del LLM nel pannello di admin.'}, status=400)

        selected_provider = SelectionParam.objects.filter(is_active=True)
        if not selected_provider.exists():
            return JsonResponse({'error': 'La selezione del LLM non è attiva. Attivarla dal pannello di admin. '}, status=400)

        selected_provider = selected_provider.first()
        result = agent.analyze(provider=selected_provider.provider_selection.model_provider_id.lower().strip(),
                      model=selected_provider.provider_selection.model_name.strip(),
                      container_name=container,
                      log_level_choice=log_level.upper())
        
        return JsonResponse({
            'success': True,
            'result': result,
            'container': container,
            'log_level': log_level
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Dati JSON non validi'}, status=400)
    except Exception as e:
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

def analyze_container_logs(container, log_level):
    """Funzione per analizzare i log (da sostituire con vera AI)"""
    
    # Mock responses per ogni log level
    mock_responses = {
        'error': f"""Analisi dei log di errore per {container}:
        
🔍 **Rilevati 12 errori critici nelle ultime 24 ore**

**Errori più frequenti:**
• Database connection timeout (8 occorrenze)
• Memory allocation failure (3 occorrenze)  
• API rate limit exceeded (1 occorrenza)

**Raccomandazioni:**
• Ottimizzare le query del database per ridurre i timeout
• Aumentare la memoria allocata al container
• Implementare retry logic per le chiamate API

**Impatto stimato:** Alto - possibili interruzioni del servizio""",

        'warn': f"""Analisi dei warning per {container}:
        
⚠️ **Identificati 45 warning nelle ultime 24 ore**

**Warning principali:**
• Slow query detected (23 occorrenze)
• High memory usage (15 occorrenze)
• Deprecated API usage (7 occorrenze)

**Raccomandazioni:**
• Ottimizzare le query lente identificate
• Monitorare l'utilizzo della memoria
• Aggiornare le chiamate API deprecate

**Impatto stimato:** Medio - performance degradate""",

        'info': f"""Analisi dei log informativi per {container}:
        
ℹ️ **Processati 1,247 log informativi nelle ultime 24 ore**

**Attività principali:**
• User authentication (456 eventi)
• API requests processed (523 eventi)
• Database transactions (268 eventi)

**Statistiche:**
• Uptime: 99.8%
• Response time medio: 245ms
• Throughput: 52 req/min

**Stato generale:** Ottimale""",

        'debug': f"""Analisi dei log di debug per {container}:
        
🐛 **Elaborati 2,891 log di debug nelle ultime 24 ore**

**Debug info principali:**
• Function execution traces (1,234 eventi)
• Variable state changes (891 eventi)
• Cache operations (766 eventi)

**Insight tecnici:**
• Cache hit rate: 87.3%
• Average function execution: 15ms
• Memory cleanup frequency: ogni 30min

**Stato sistema:** Stabile""",

        'all': f"""Analisi completa dei log per {container}:
        
📊 **Panoramica generale delle ultime 24 ore**

**Distribuzione log:**
• Error: 12 (0.3%)
• Warning: 45 (1.1%) 
• Info: 1,247 (30.2%)
• Debug: 2,891 (68.4%)

**Metriche chiave:**
• Availability: 99.8%
• Error rate: 0.3%
• Performance: Ottimale
• Sicurezza: Nessun alert

**Raccomandazioni prioritarie:**
1. Risolvere i timeout del database
2. Ottimizzare le query lente
3. Monitorare l'utilizzo memoria

**Stato complessivo:** 🟢 Buono"""
    }
    
    return mock_responses.get(log_level, mock_responses['all'])