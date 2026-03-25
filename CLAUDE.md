# GBS & IgA-brist — Kunskapsdatabas

> **Start here.** Läs detta innan du gör något annat i projektet.

## Vad är detta?

En RAG-driven medicinsk kunskapsdatabas om Guillain-Barré syndrom (GBS) i kombination med selektiv IgA-brist. Databasen är byggd för neurologer och intensivvårdsläkare som beslutsunderlag.

**Live:** https://gbs.ragbase.org (custom domain) | https://gb-research-production.up.railway.app (Railway default)
**Åtkomstkod:** Satt som `ACCESS_CODE` i Railway env vars.
**Paraplydomän:** `ragbase.org` (Namecheap) — framtida databaser läggs som subdomäner (t.ex. `brew.ragbase.org`)

## Varför finns det?

Markus fru Madeleine (52 år) insjuknade akut i svår recidiverande GBS (första episoden vid 16 års ålder) i mars 2026. Hon har känd selektiv IgA-brist. Ingen publicerad guideline täcker denna kombination specifikt. Databasen samlar all tillgänglig evidens för att ge behandlande läkare bästa möjliga underlag.

## Tech stack

| Komponent | Teknologi |
|-----------|-----------|
| Kunskapsbas | 9 markdown-dokument, ~250 peer-reviewed referenser |
| Vektordatabas | ChromaDB (lokal, filbaserad) |
| Embeddings | Gemini `gemini-embedding-001` (768d) |
| LLM (Q&A) | Gemini `gemini-2.5-flash` |
| Webb | Flask + gunicorn |
| Hosting | Railway (Docker) |
| Repo | GitHub: `markusfrantz-rgb/GB-research` |

## Projektstruktur

```
GB-research/
├── CLAUDE.md                ← DU ÄR HÄR
├── PROJECT_STATUS.md        ← Nuvarande status
├── KUNSKAPSBASEN.md         ← Intro-sidan som visas på webben
│
├── 01-GBS/                  ← GBS-forskning (3 dokument)
├── 02-IgA-deficiency/       ← IgA-brist-forskning (2 dokument)
├── 03-GBS-and-IgA-deficiency/ ← Kombinationen (1 dokument, nyckeldokument)
├── 04-related-autoimmune/   ← Relaterade autoimmuna tillstånd (2 dokument)
├── 05-treatment-resistance/ ← Refraktär GBS, nya terapier, koagulopati, sekventiell terapi, PE-svikt-protokoll (5 dokument)
├── 06-monitoring-prognosis/ ← Prognostisk monitorering, biomarkörer, neuroprognostikering, EGRIS, beslutspunkter (1 dokument)
├── 07-acute-icu-protocols/  ← Akuta IVA-protokoll: post-trakeostomivård, dysautonomi, respiratoravvänjning (2 dokument)
├── sources/fulltext/        ← Källbibliotek: 12 PDF + 10 textfiler (22 fulltexter)
├── Tillgang_till_medicinska_kallor.md ← Komplett artikelöversikt med status
├── metadata/                ← Index och källregister
│
├── rag/                     ← RAG-systemet (Python)
│   ├── config.py            ← Konfiguration
│   ├── chunker.py           ← Markdown-medveten hierarkisk chunkning
│   ├── ingest.py            ← Dokument → embeddings → ChromaDB
│   ├── search.py            ← Semantisk sökning
│   ├── qa.py                ← RAG Q&A med Gemini
│   └── cli.py               ← CLI (ingest/search/ask/stats)
│
├── web/                     ← Webbgränssnitt (Flask)
│   ├── app.py               ← Routes, auth, rate limiting
│   ├── templates/           ← HTML (index, login, document)
│   └── static/style.css     ← Styling
│
├── Dockerfile               ← Produktion (Railway)
├── start.sh                 ← Startup: indexera → starta server
├── requirements.txt
└── .env                     ← GOOGLE_API_KEY (gitignored)
```

## Säkerhet & drift

- **Åtkomstkod:** Sätts via `ACCESS_CODE` i Railway env vars. Session-baserad (giltig tills webbläsaren stängs).
- **Rate limiting:** 10 frågor/min, 30 sökningar/min per IP. Konfigurerbart via `RATE_LIMIT_ASK` och `RATE_LIMIT_SEARCH` env vars.
- **API-nyckel:** `GOOGLE_API_KEY` i Railway env vars (Gemini, för embeddings + LLM).
- **SECRET_KEY:** Flask session-nyckel, default hårdkodad — bör sättas som env var i produktion.
- **Railway env vars som MÅSTE finnas:** `GOOGLE_API_KEY`, `ACCESS_CODE`.
- **OBS:** Env vars måste finnas som Service Variables på rätt service i Railway (inte projekt- eller environment-nivå). Verifiera med loggraden `[ENV] ACCESS_CODE is: SET` vid deploy.

## Sessionschecklista

1. Läs `CLAUDE.md` (denna fil)
2. Läs `PROJECT_STATUS.md` för aktuellt läge
3. Läs sprint-minnet (i Claude memory) för nästa sessions prioriteringar
4. **Fråga Markus om klinisk uppdatering** — det styr allt annat
5. Utför arbete (se arbetsflöde nedan)
6. Uppdatera `PROJECT_STATUS.md` + sprint-minne efter avslutat arbete

## Arbetsflöde — så här arbetar vi

Varje session följer samma mönster. **Allt ska vara i ordning när sessionen avslutas.**

### Steg 1: Klinisk uppdatering
Fråga Markus vad som hänt. Uppdatera:
- `PROJECT_STATUS.md` → klinisk tidslinje
- `KUNSKAPSBASEN.md` → aktuellt förlopp
- `Case_Madeleine_Fragor_och_Fynd.md` → status + nya frågor

### Steg 2: Nya artiklar
Om Markus har nya PDF:er (Downloads, sjukhusbibliotek, läkarvänner):
1. Identifiera artikeln (pdftotext, kolla titel/författare/PMID)
2. Kopiera till `sources/fulltext/` med namnkonvention: `Författare_År_Ämne_PMCID.pdf`
3. Extrahera fulltext via NCBI API om möjligt (`.txt`-fil)
4. Uppdatera `Tillgang_till_medicinska_kallor.md` med ny artikel + status
5. Integrera relevant data i forskningsdokumenten (01-07-mapparna)

### Steg 3: Uppdatera forskningsdokument
Om klinisk utveckling kräver det (ny behandling, nytt provsvar, ny komplikation):
1. Skapa nytt dokument i rätt mapp, ELLER uppdatera befintligt
2. Följ formatkonventioner: YAML-frontmatter, H1-titel, H2-sektioner med TOC
3. Evidensgradering `*[Level X]*` vid varje åtgärdbar rekommendation
4. PMID vid varje nyckelreferens
5. Korsreferera till relaterade dokument

### Steg 4: Reindexera RAG
```bash
source .venv/bin/activate
python -m rag ingest --reindex -v
```
Verifiera: rätt antal dokument, nya chunks inkluderade.

### Steg 5: Synkronisera "Om databasen"
`KUNSKAPSBASEN.md` är landningssidan — den MÅSTE spegla verkligheten:
- Rätt antal dokument och referenser
- Alla dokument listade med korrekta länkar (`/doc/XX-mapp/filnamn.md`)
- Aktuell klinisk status
- Artikelöversikten länkad (`/doc/Tillgang_till_medicinska_kallor.md`)

### Steg 6: Commit + Deploy
```bash
git add [specifika filer]
git commit -m "Beskrivande meddelande"
git push  # Triggar Railway auto-deploy
```

### Steg 7: Dokumentera för nästa session
- Uppdatera `PROJECT_STATUS.md` med ändringslogg
- Uppdatera sprint-minne i Claude memory med:
  - Madeleines senaste status
  - Vad som gjorts
  - Vad som bör göras härnäst
  - Öppna kliniska frågor

### Formatkonventioner (forskningsdokument)

```yaml
---
doc_type: research
date: 2026-03-25
status: active
---
```
- **Titlar:** H1 (`#`), sektioner H2 (`##`) med numrerad TOC, undersektioner H3+
- **Evidens:** `*[Level 1 — Cochrane/RCT]*` till `*[Level 5 — expertutlåtande]*` inline
- **Citeringar:** `> **Citation:** Författare. Titel. *Journal*. År. PMID: XXXXX`
- **Tabeller:** Markdown pipe-tabeller med klinisk data
- **Beslutalgoritmer:** Code blocks med if/then-logik
- **Språk:** Engelska i forskningsdokument, svenska i kliniska dokument och UI

## Viktiga kommandon

```bash
# Aktivera miljö
source .venv/bin/activate

# Indexera om (efter nya/ändrade dokument)
python -m rag ingest --reindex -v

# Lokal webbserver
python web/app.py

# Sök / fråga via CLI
python -m rag search "query"
python -m rag ask "fråga"

# Deploy
git push  # Railway bygger automatiskt
```

## Länkar till djupare dokumentation

- **Forskningsinnehåll:** `metadata/index.md` — fullständigt index över alla dokument och vad de täcker
- **Källregister:** `metadata/source-registry.md` — alla ~250 referenser organiserade efter typ
- **Intro/landningssida:** `KUNSKAPSBASEN.md` — den text som visas på webben
