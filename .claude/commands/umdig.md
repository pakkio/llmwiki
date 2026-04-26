---
name: umdig
description: Skill unificato per contenuti salahzar.com. Concatena salahzar v5, newsal v6, antipattern-filter e research-to-salahzar in un flusso operativo unico. Attivare per qualsiasi articolo, analisi o pezzo per il blog — dalla ricerca alla pubblicazione.
metadata:
  version: 1.2.0
  category: Content Pipeline (unified)
  language: Italian
  author: Salahzar Stenvaag / Claudio Pacchiega
  chains: salahzar v5.0, newsal v6.0, newsal-antipattern-filter v1.0, research-to-salahzar v1.0
  changelog: |
    v1.2.0 - Aggiornamento:
             - Livello 3: regola esplicita sull'inciampo di registro (posizione, non frequenza)
             - Livello 3: modulo incipit con esempi buoni/cattivi
             - Livello 1: nota operativa su step separati per research estesa
             - Livello 5: warning esplicito su fonti italiane di nicchia pre-2018
    v1.1.0 - Aggiornamento:
             - Antipattern autopromozione LinkedIn (esteso e sistematizzato)
             - Antipattern tic dichiarativi (annunciare invece di fare)
             - Protocollo riferimenti finali con verifica link obbligatoria
    v1.0.0 - Prima versione unificata:
             - Architettura a 5 livelli (decisione → research → materiale → scrittura → revisione)
             - Eliminazione ridondanze tra i 4 skill originali
             - Materiale biografico/esperienziale centralizzato
             - Check bloccanti unificati (6 da newsal v6 + 20 antipattern)
             - Pipeline research integrata
---
 
# UMDIG v1.1
## Skill Unificato per Contenuti Salahzar
 
---
 
## LIVELLO 0 — PRIMA DI APRIRE L'EDITOR
 
Tre domande. Se ne fallisci due, non scrivere.
 
**1. Sai qualcosa di nuovo?**
Non "ho letto articoli". Hai *fatto* qualcosa? Hai dati diretti, codice fallito, ore in aula?
Esempio sbagliato: "L'AI trasformerà l'educazione"
Esempio giusto: "2015: Second Life in aula. 2024: ChatGPT in aula. Prima domanda identica."
 
**2. Qualcun altro l'ha già detto meglio?**
Se stai per scrivere l'ennesimo "l'AI cambierà tutto", fermati. Cosa aggiungi tu?
 
**3. Stai razionalizzando uno sfogo?**
Test: se ti mostrassero dati contrari, cambieresti idea o difenderesti la tesi? Se la seconda — non scrivere.
 
**Quarta (bloccante assoluta):** Il tema richiede competenze che non hai? → studia o taci.
 
---
 
## LIVELLO 1 — RESEARCH (se parti da URL o topic)
 
*Salta al Livello 2 se hai già il materiale.*
 
### 1a. Raccolta fonti
 
**Tool priority:**
1. `fetch` MCP — sempre prima scelta, accesso più libero
2. `web_fetch` — fallback se fetch MCP blocca
3. `web_search` — per topic senza URL (query 3-5 parole, poi fetch dei risultati)
Per ogni URL: estrai titolo, tesi, dati citati, fonti secondarie. Annota anche **cosa non dice** — i silenzi sono dati.
 
Per topic: almeno 3 fonti, di cui 1 primaria (paper/report/dati ufficiali) e 1 controcorrente rispetto alla tesi mainstream.
 
### 1b. Critica filologica delle fonti
 
Ogni fonte è un manoscritto con un'agenda. Applicare:
 
| Operazione | Domanda pratica |
|---|---|
| **Agenda del testo** | Chi ha scritto e perché? Quale interesse ha? |
| **Lectio difficilior** | Cosa l'articolo evita? Cosa è troppo liscio? |
| **Interpolazione** | Dati senza fonte primaria = aggiunta spuria del copista |
| **Normalizzazione** | Cosa ha appiattito rispetto alla realtà complessa? |
| **Stemma codicum** | Dove divergono due fonti sullo stesso fatto? |
 
**Check anti-fuffa per ogni dato:**
- Ha fonte primaria verificabile? Se no → qualificare come "secondo X" o cercare fonte
- La fonte dice *esattamente* quello che l'articolo dice? → verificare
- Esiste dato contrario non citato? → cercarlo attivamente
### 1c. Domanda bloccante pre-scrittura
 
**"Ho qualcosa da aggiungere che le fonti non hanno?"**
- Sì → procedi con quel materiale come aggancio principale
- No → scrivi una nota breve, non un articolo
- Parzialmente → scrivi solo la parte verificabile, qualifica il resto
> **Nota operativa**: per articoli che richiedono research estesa, eseguire Livello 1 e Livello 2 separatamente. Presentare il materiale raccolto e attendere conferma prima di procedere con il Livello 3. Questo evita che la stesura dimentichi i vincoli di revisione del Livello 4.
 
---
 
## LIVELLO 2 — MATERIALE SALAHZAR
 
Prima di scrivere: quale materiale esperienziale è attivabile?
 
### Matrice di attivazione
 
| Topic | Materiale disponibile |
|---|---|
| AI in education | INDIRE 2011-2018: 1400h, "Copieranno?", curva 15/20/65, gap policy/pratica |
| Hype tecnologico | edu3d/Second Life: cicli completi 2007→oggi, stesso entusiasmo, stesso oblio |
| Metaverso / spatial computing | Second Life (stesso concetto, nome aggiornato) |
| LLM, bias, allucinazioni | Nexus NPC: interpolazione in atto, turing test falliti in produzione |
| Normalizzazione culturale AI | Filologia: copista che normalizza = modello che appiattisce — metodo isomorfo |
| Tool AI pratici, RAG, embedding | Codice fallito: NER su italiano, RAG fragile su edge case, 12 framework testati |
| Sovranità digitale, governance | Diari ucronici: pensiero critico, storie alternative |
| Automazione del lavoro | Fantozzi (1975) come dato antropologico avant la lettre |
 
### Regola sull'esperienza come dato
 
**Mai**: "Con la mia esperienza pluriennale..." → tono CV
**Sempre**: "Dal 2011 al 2018, stessa domanda in ogni aula. 'Copieranno?'" → osservazione documentabile
 
L'esperienza entra nel testo come **dato verificabile**, non come credenziale.
 
### Autopromozione LinkedIn — lista nera estesa
 
Il CV-speak classico ("con la mia esperienza pluriennale") è ovvio. Più subdola è l'autopromozione in stile LinkedIn, che finge di parlare del mondo mentre parla di sé.
 
**Pattern da eliminare:**
 
| Forma | Problema | Alternativa |
|---|---|---|
| "Ho avuto il privilegio di lavorare con..." | Gratitudine performativa | Descrivi cosa hai visto, non che eri lì |
| "Sono orgoglioso di annunciare..." | Comunicato stampa di sé stessi | Non appartiene a un articolo |
| "La mia passione per X mi ha portato a..." | Branded storytelling | Parti dal fenomeno, non da te |
| "Ho dedicato anni a capire..." | Sacrificio come credenziale | Cosa hai capito? Quello conta |
| "Come qualcuno che lavora in questo spazio..." | "Spazio" è già LinkedIn-speak | Vai diretto al punto |
| "Sono entusiasta di condividere..." | Entusiasmo prefabbricato | Non condividere entusiasmo, condividi contenuto |
| "Questo mi ha insegnato che..." | Morale della favola personale | La lezione deve emergere dal dato, non essere dichiarata |
| Foto-mentale: "seduto in prima fila a..." | Name-dropping posizionale | Irrilevante se non aggiunge contesto |
 
**Regola pratica**: se una frase potrebbe stare su un profilo LinkedIn senza sembrare fuori posto → non appartiene a salahzar.com.
 
**Test rapido**: sostituisci il tuo nome con quello di chiunque. La frase regge? Allora non stai dicendo niente di tuo — stai solo occupando spazio.
 
### Cinema e cultura — funzionale, non decorativo
 
**Intellettuale**: Fellini, Antonioni, De Sica, Rossellini, Pasolini
**Popolare**: Fantozzi, Troisi, Benigni, Verdone, Virzì, Muccino
**Contemporaneo**: Sorrentino, Garrone, Rohrwacher
 
Regola: usa quello che *spiega* qualcosa che senza non sarebbe chiaro. Se rimuovi il riferimento e il paragrafo regge uguale → era decorazione, toglilo.
 
**Classici latini**: funzionali (*lectio difficilior*, Seneca su volontà e algoritmi), mai per impressionare.
 
---
 
## LIVELLO 3 — SCRITTURA (newsal v6)
 
### Struttura anti-NYT
 
**Non fare** (five-paragraph essay mascherato):
```
## Il problema
## L'evidenza
## L'analogia
## La soluzione
## Conclusione
```
 
**Fare** (flusso italiano — accumulo, digressione, contrappunto, ritorno):
```
[Apertura concreta — scena, dato, paradosso — non annuncio di tesi]
[Sviluppo con deviazione interna — transizione dentro il flusso, non titolino]
[Momento di autocritica o incertezza reale]
[Ritorno all'immagine iniziale, angolazione diversa]
[Momento basso — una parola, registro parlato — il testo inciampa]
[Chiusa che rilancia o resta sospesa — mai che chiude e ribadisce]
```
 
**Test struttura**: togli tutti i titolini e separatori. Il flusso regge? Se no, il problema non sono i titolini — è che il testo non ha flusso.
 
### Varianza di registro (obbligo)
 
Almeno un momento basso ogni 500-800 parole. Non volgarità — registro parlato che interrompe il tono medio-alto.
 
Esempi funzionanti:
- "Vabbè." — dopo autocritica, chiude e riapre
- "Boh." — ammissione di incertezza senza scuse
- "Non è granché." — giudizio secco invece di analisi elaborata
- "Funziona? Più o meno." — abbassa la retorica
> **Regola di posizione**: l'inciampo funziona *dopo* un momento di tensione o densità accumulata. Inserito a freddo, diventa macchietta. La caduta di registro ha bisogno di altezza da cui cadere — costruisci prima, poi inciampa.
 
**Test acustico**: leggi ad alta voce. Se il tono è uniforme per due paragrafi consecutivi, hai un problema.
 
### Incipit — le prime tre righe
 
L'incipit è il punto di cedimento più frequente. Gli LLM producono per default due tipi di apertura, entrambi da eliminare:
 
- **Scena cinematografica finta**: "Era il 2015, nelle aule italiane risuonava una domanda..." → artificioso, non vissuto
- **Statistica decontestualizzata**: "Il 67% degli insegnanti afferma che..." → inizio da comunicato stampa
**Aperture che funzionano per Salahzar:**
 
| Tipo | Esempio |
|---|---|
| Dato diretto e concreto | "Dal 2011 al 2018, prima domanda invariabile in ogni aula INDIRE: 'Copieranno?'" |
| Paradosso osservato | "Second Life era morto. Il metaverso è il nome del funerale con buffet." |
| Frammento di codice o log reale | "ValueError: list index out of range. Era il mio quarto framework NER in sei mesi." |
| Domanda non retorica | "Cosa cambia, esattamente, tra un NPC che interpola e un modello che allucinava?" |
 
**Regola**: l'incipit deve sapere *già qualcosa* — non annunciare che lo scoprirà. Se le prime tre righe potrebbero stare all'inizio di qualsiasi articolo sullo stesso tema, riscrivi.
 
### Autocritica strutturale
 
Il testo deve poter mordere sé stesso. Se stai scrivendo contro la normalizzazione e il pezzo ha struttura da editoriale americano, il medium contraddice il messaggio.
 
Prima di finalizzare: *la forma di questo testo contraddice quello che dice?*
 
### Lunghezza target
 
600-1200 parole per articolo blog standard. Oltre 1200: giustificare.
 
---
 
## LIVELLO 4 — REVISIONE FINALE
 
### Check bloccanti v6 (tutti e 6 — se ne fallisci uno, riscrivi)
 
1. **Anglicismi**: zero residui sostituibili (`framework` ok, `insight` no, `deploy` → rilasciare)
2. **Autopromozione**: zero frasi da CV (esperienza come dato, non credenziale)
3. **Claim**: ogni fatto ha fonte verificata o è qualificato come "nella mia esperienza" / "osservazione locale"
4. **Parallelo culturale**: almeno 1 che spiega, non decora
5. **Struttura**: flusso continuo — titolini rimossi, testo regge ancora?
6. **Registro**: almeno 1 momento basso / inciampo nel ritmo
### 20 antipattern da eliminare (scansione rapida)
 
**Retorici/strutturali:**
1. *Correctio* — "Non X, ma Y" → falsa profondità senza aggiunta
2. *Hedging compulsivo* — "vale la pena notare", "in un certo senso", "per certi versi" → o lo dici o non lo dici
3. *Apertura sycofantica* — "Ottima domanda!", "Assolutamente!" → taglia, inizia dalla risposta
4. *Throat-clearing* — "Prima di entrare nel merito..." → entra al primo rigo
5. *Resumptive parroting* — ripetere la domanda prima di risponderle
6. *Transizioni formulaiche* — "Entriamo nel vivo", "Analizziamo insieme" → le transizioni avvengono dentro il flusso
7. *Cataphoric teasing* — "Ed è qui che diventa interessante..." → se è interessante, dillo e basta
**Lessicali:**
8. *Intensificatori vuoti* — "davvero", "veramente", "incredibilmente" dove non misurano nulla
9. *Metacommento* — "È un problema complesso" → affrontalo, non commentarne la difficoltà
10. *Both-sidesing* — "Ci sono punti validi su entrambi i lati" → se hai opinione, dilla
11. *Caveat non richiesto* — "Tuttavia, è importante notare..." → integralo nel ragionamento o taglia
12. *Esaustività compulsiva* — ogni angolo/eccezione/caso limite → scegli, non inventariare
13. *Magic triple* — "veloce, affidabile e scalabile" → se sono due, dì due
14. *Synonym stacking* — "robusto, completo ed esauriente" → uno basta, il più preciso
15. *Faux profundity* — "In fin dei conti", "Alla radice", "Fondamentalmente" → taglia il cappello
16. *Pivot to positivity* — chiusa ottimista indipendentemente dal contenuto → chiudi onestamente
17. *Inspirational summary* — "In definitiva, si tratta di trovare quello che funziona per te" → zero
18. *LLM-signature vocabulary* — esplorare (nel senso di analizzare), paesaggio (settore), navigare (gestire), sfumato, multifaccettato, sottolinea, promuovere → tasso < 1/3 della norma umana
19. *Compulsive listing* — bullet point su qualcosa che la prosa gestirebbe meglio
20. *Excessive bolding* — grassetto ogni terza frase → massimo 2-3 per testo
 
**Tic dichiarativi — annunciare invece di fare:**
 
Categoria separata perché particolarmente frequente negli output LLM e nei pezzi scritti in fretta. Il principio: se stai per *descrivere* quello che farai, fallo e basta.
 
| Tic dichiarativo | Cosa fare invece |
|---|---|
| "Vorrei ora esaminare..." | Esamina. |
| "Vale la pena soffermarsi su..." | Soffermati. |
| "Permettimi di spiegare..." | Spiega. |
| "Cercherò di chiarire..." | Chiarisci. |
| "A questo punto è utile ricordare che..." | Ricorda direttamente. |
| "Passiamo ora a considerare..." | Considera. |
| "È necessario fare un passo indietro e..." | Fai il passo indietro. |
| "Per rispondere a questa domanda, dobbiamo prima..." | Rispondi. |
| "Proviamo a capire insieme perché..." | Spiega perché. |
| "Mi sembra importante sottolineare che..." | Sottolinea, senza dirlo. |
 
**Regola**: ogni volta che stai per scrivere un verbo che descrive l'azione invece di compierla, cancella l'annuncio e fai l'azione. Il lettore non ha bisogno di sapere che stai per spiegare qualcosa — ha bisogno della spiegazione.
 
### Tre domande finali (invariate)
 
1. **È onesto?** Hai scritto quello che pensi davvero? Hai omesso dati contrari?
2. **È interessante?** Continueresti dopo il secondo paragrafo?
3. **È necessario?** Qualcuno ne trarrà vantaggio, o stai riempiendo il web di rumore?
Se ne fallisci due: probabilmente il pezzo non doveva esistere.
 
---
 
## LIVELLO 5 — RIFERIMENTI FINALI E VERIFICA CLAIM
 
Ogni articolo per salahzar.com termina con una sezione **Riferimenti** obbligatoria se contiene dati, statistiche, studi o affermazioni verificabili. Non è una bibliografia accademica — è una lista operativa che permette al lettore di controllare.
 
### Formato standard
 
```
**Riferimenti**
 
[1] Autore/Ente, *Titolo*, Anno. Nota sintetica sul dato rilevante.
URL: https://...  ← link diretto alla fonte, non alla homepage
```
 
**Regole:**
- Massimo una riga di nota per riferimento — il testo ha già spiegato il contesto
- Link alla pagina specifica, non al sito (es. `/en/topics/bees` non `efsa.europa.eu`)
- Se il link è un PDF, specificarlo: `[PDF]`
- Se la fonte è a pagamento o richiede login, annotarlo: `[paywall]`
- Dati da fonti secondarie (giornali che citano ISTAT): verificare la fonte primaria e citare quella, non il giornale
### Procedura di verifica prima di pubblicare
 
Per ogni claim con numero o dato specifico nel testo:
 
**1. Verifica esistenza fonte**
Usare `fetch` MCP o `web_search` per confermare che la fonte esiste e dice quello che il testo afferma.
 
**2. Verifica corrispondenza esatta**
La fonte dice *esattamente* quella cifra, in quel contesto? Attenzione a:
- Dati aggregati spacciati come dati specifici ("il 42% degli italiani" vs "il 42% dell'acqua nelle reti")
- Anni diversi (dato 2020 citato come attuale)
- Campioni diversi (studio su 100 persone citato come dato nazionale)
**3. Verifica link funzionante**
Fare un fetch del link prima di includerlo. Link rotti o reindirizzati a homepage → cercare URL aggiornato o sostituire con fonte equivalente.
 
**4. Qualifica se non verificabile**
Se il dato non è verificabile con certezza:
- Fonte secondaria affidabile: "secondo [testata], citando [ente]..."
- Osservazione personale: "nella mia esperienza con X casi..."
- Stima: "stima approssimativa basata su Y"
Mai lasciare un dato nudo senza qualifica quando la fonte non è verificabile.
 
### Claim che NON richiedono riferimento
 
- Affermazioni di senso comune verificabili da chiunque
- Osservazioni personali esplicitamente qualificate come tali
- Paralleli culturali (Fantozzi, Seneca) — sono interpretazioni, non fatti
- Giudizi critici chiaramente espressi come opinione
### Segnali di allarme
 
- Cifre tonde (70%, 50%, "la metà") senza fonte → probabilmente stimate, qualificare
- "Secondo studi recenti" senza titolo → non pubblicare finché non hai il titolo
- Dati da comunicati stampa aziendali → cercare conferma indipendente
- Statistiche pre-2020 su AI/tech → verificare se ancora valide
- **Fonti italiane di nicchia pre-2018** (INDIRE, MIUR, rapporti regionali, atti convegni) → rischio allucinazione alto: gli LLM costruiscono citazioni plausibili piuttosto che ammettere l'assenza. Verificare sempre con `fetch` prima di includere. Se non verificabile, qualificare esplicitamente come "nella mia esperienza diretta" o "osservazione non documentata pubblicamente".
| Bannato | Usa invece |
|---|---|
| "AI non è X ma Y" | Affronta direttamente con dato |
| "È importante notare che" | Vai al punto |
| "In primo/secondo/terzo luogo" | Flusso naturale |
| "Con la mia esperienza pluriennale" | "Dal 2011 al 2018, stessa domanda" |
| "Come esperto del settore" | Osservazione concreta |
| "Navigare il futuro" | Gestire / affrontare |
| "Sfide e opportunità" | Taglia e scegli una |
| "Ecosistema AI" | Il settore / il campo / i modelli |
| "In definitiva" / "In fin dei conti" | Chiudi senza cappello |
| insight, deploy, performance | osservazione, rilasciare, prestazioni |
 
---
 
## QUANDO NON USARE QUESTO SKILL
 
- Tutorial tecnici step-by-step (serve chiarezza, non ironia archeologica)
- Documentazione API o codice (serve precisione, non teatralità)
- Email di lavoro (serve brevità, non paralleli culturali)
- Quando l'editor dice "è troppo denso"
## QUANDO USARLO AL 100%
 
- Qualsiasi articolo per salahzar.com
- Analisi AI/education/tech con nome sotto
- Newsletter e pezzi di opinione
- Ogni volta che parti da URL/topic e vuoi un pezzo finito
---
 
*Principio guida (newsal v6): se il pezzo è troppo liscio, ha già normalizzato qualcosa che valeva la pena tenere. Lectio difficilior potior.*
 
