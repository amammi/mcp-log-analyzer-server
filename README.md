# AI Log Analyzer
###### Analisi intelligente dei log container

<div align="center">
    <img src="/webapp/static/logo_v3.png" alt="" width="500" style="display: block; margin: 0 auto"/>
</div>

<div>

Questo repository contiene il codice sorgente del progetto finale del corso di Programmazione Python del primo modulo del master <strong>"Applied Artificial Intelligence"</strong>.
</div>

## Descrizione del progetto
<div>
Il progetto punta alla costruzione di un Proof of Concept che riesca, dato il nome di un container docker, ad analizzare i log
su diversi livelli dell'applicazione che vive dentro quel container attraverso l'utilizzo degli LLM e del protocollo MCP.


Il progetto si compone di 3 moduli:

- **mcp_server**: con all'interno il codice sorgente del server MCP che permette l'estrazione dei log dai container docker. Per costruire tale server MCP è stata utilizzata la libreria Python FastMCP.
- **app**: una piccola FastAPI app costruita per generare log che alcuni dei tools presenti nel server MCP dovranno estrarre su tre livelli:
  - INFO
  - DEBUG
  - ERROR
- **webapp**: una webapp Django con un frontend in React che funge da client verso l'utente finale, che sfrutta la combinazione LLM + MCP server per l'analisi dei log dei container Docker.
</div>

## Requisiti di sistema

<div>
I requisiti che il sistema deve avere per far partire il progetto sono:

- Docker
- Docker compose
- WSL (se il progetto verrà fatto partire con Windows come OS)
</div>

## Build del progetto
<div>
Una volta soddisfatti i requisiti di sistema e clonato questo repository, sarà necessario 
fare la build delle immagini docker di tutti e tre moduli e successivamente avviare i relativi container docker.
</div>


<div>

Per fare entrambe le cose (build + run), sarà necessario posizionarsi nella root del progetto (la medesima di questo file README.md)
e lanciare il comando:
</div>

<div>

<code>docker compose up -d </code>
</div>

<div>

Si avvierà la fase di build delle immagini e successivamente la fase di start dei vari container.
Una volta fatto, l'infrastruttura dei container sarà pronta per poter essere utilizzata. 
</div>

## Getting started

Una volta avviata l'infrastruttura dei vari container, la situazione sarà la seguente:

- **mcp_server**: sarà attiva e in ascolto sulla porta 8080
- **application**: sarà attiva e in ascolto sulla porta 8050
- **django_webapp**: sarà attiva e in ascolto sulla porta 8000

Per prima cosa, poiché dovremo poter fare le analisi dei log del container **application**,
si dovranno generare tali log. A tal proposito, dunque, sarà necessario fare delle richieste su 2 endpoint differenti:

- GET /greet: genera log di livello INFO e DEBUG
- POST /operations: genera log di livello INFO, DEBUG ed ERROR (simulati)

Per chiamare questi endpoint basterà farlo, anche con body vuoto, attraverso curl oppure tool come Postman o Insomnia.

Una volta generati i log con varie chiamate, possiamo cominciare ad utilizzare
la **django_webapp**.

## Configurazione Applicazione

Prima di utilizzare il client vanno, nell'ordine, settate 2 configurazioni nel pannello di amministrazione dell'applicazione:

1. Collegarsi all'indirizzo <code>http://localhost:8000/</code> e nella pagina iniziale, come si vede dalla figura, cliccare il tasto
"Impostazioni". Si verrà reindirizzati al pannello di amministrazione dell'applicazione dove al primo accesso verranno chieste le credenziali
   (se non sono state cambiate in fase di build nel docker-compose file, user e password sono admin:admin)

<div align="center">
    <img src="/docs/assets/GoToSettings.png" alt="" width="500" style="display: block; margin: 0 auto"/>
</div>

2. Aggingere un **Provider Model**: Per aggiungere un Provider Model, cliccare su "Add" nel menu a sinistra accanto alla relativa voce. 
Possibile scelta tra 3 diversi provider come Ollama, OpenAI e Anthropic. Di seguito 
viene riportato l'esempio per OpenAI

<div align="center">
    <img src="/docs/assets/AddProviderModel.png" alt="" width="500" style="display: block; margin: 0 auto"/>
</div>

Per ogni provider model sarà necessario esplicitare:

- il **provider**
- il **modello** di quel provider da utilizzare
- la relativa **API key** (lasciare anche "ollama" che appare di default se il provider scelto è Ollama)
- se si seleziona Ollama come provider bisogna valorizzare obbligatoriamente il campo **base url** con l'indirizzo del server ollama remoto, diversamente, 
per gli altri provider questo campo non è necessario.
- il flag **is_active** per attivare quel provider per l'intera applicazione

3. Configurare i dati dell'MCP server: Per aggiungere un MCP Server Config, cliccare su "Add" nel menu a sinistra accanto alla relativa voce.

<div align="center">
    <img src="/docs/assets/AddMCPServerConfig.png" alt="" width="500" style="display: block; margin: 0 auto"/>
</div>

In questa schermata è necessario esplicitare un nome e l'url al quale è raggiungibile il nostro MCP Server.
Nel nostro caso, sarà necessario inserire l'indirizzo <code>http://host.docker.internal:8080</code>

## Utilizzo del client

Terminata la configurazione, è ora possibile utilizzare il client. Per far ciò, se si è all'interno del pannello di amministrazione dell'applicazione si potrà cliccare direttamente nella voce di menu "**View Site**",
altrimenti basterà collegarsi all'indirizzo <code>http://localhost:8000/</code> ed in questo modo si verrà reindirizzati alla seguente schermata:

<div align="center">
    <img src="/docs/assets/homepage.png" alt="" width="500" style="display: block; margin: 0 auto"/>
</div>

Notiamo subito in alto a destra il numero dei container attivi ed la voce "Impostazioni" vista in precedenza per accedere al pannello di amministrazione, 
poi, proseguendo verso il basso, abbiamo l'area di sinistra dove sono presenti le info da selezionare per l'analisi dei log come:

- Nome del container da analizzare
- Log level

A destra invece troveremo la risposta del nostro LLM, dopo aver utilizzato gli opportuni tool del server MCP. 
Di seguito un breve video sul funzionamento:




[demo.webm](https://github.com/user-attachments/assets/34ae9f4e-3362-4678-a2a6-bbff58313c03)



