# AI Log Analyzer
###### Analisi intelligente dei log container

<div >
    <img src="/webapp/static/logo_v3.png" alt="drawing" width="500" style="display: block; margin: 0 auto"/>
</div>

<div>

Questo repository contiene il codice sorgente del progetto finale del corso di Programmazione Python del primo modulo del master <strong>"Applied Artificial Intelligence"</strong>.
</div>

## Descrizione del progetto
<div>

Il progetto si compone di 3 moduli:

- **mcp_server**: con all'interno il codice sorgente del server MCP che permette l'estrazione dei log dai container docker. Per costruire tale server MCP è stata utilizzata la libreria Python FastMCP.
- **app**: una piccola FastAPI app costruita per generare log che alcuni dei tools presenti nel server dovranno estrarre su tre livelli:
  - INFO
  - DEBUG
  - ERROR
- **webapp**: una webapp Django con un frontend in React che funge da client verso l'utente finale, che sfrutta la combinazione LLM + MCP server per l'analisi dei log.
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

Per farlo, sarà necessario posizionarsi nella root del progetto (la medesima di questo file README.md)
e lanciare il comando:
</div>

<div>

<code>docker compose -d up </code>
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

## Configurazione Django



