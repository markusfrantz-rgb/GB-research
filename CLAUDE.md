# GBS & IgA-brist — Kunskapsdatabas

> **Start here.** Läs detta innan du gör något annat i projektet.

## Vad är detta?

En RAG-driven medicinsk kunskapsdatabas om Guillain-Barré syndrom (GBS) i kombination med selektiv IgA-brist. Databasen är byggd för neurologer och intensivvårdsläkare som beslutsunderlag.

**Live:** https://gbs.ragbase.org (custom domain) | https://gb-research-production.up.railway.app (Railway default)
**Åtkomstkod:** Satt som `ACCESS_CODE` i Railway env vars.
**Paraplydomän:** `ragbase.org` (Namecheap) — framtida databaser läggs som subdomäner (t.ex. `brew.ragbase.org`)

## Varför finns det?

Markus fru Madeleine (53 år) insjuknade akut i svår recidiverande GBS (första episoden vid 16 års ålder) i mars 2026. Hon har känd selektiv IgA-brist. Ingen publicerad guideline täcker denna kombination specifikt. Databasen samlar all tillgänglig evidens för att ge behandlande läkare bästa möjliga underlag.

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
├── 05-treatment-resistance/ ← Refraktär GBS, nya terapier, koagulopati, sekventiell terapi (4 dokument)
├── 06-monitoring-prognosis/ ← Prognostisk monitorering, biomarkörer, IVA-protokoll (1 dokument)
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
3. Kolla om det finns nya instruktioner eller prioriteringar
4. Om forskning ska utökas: lägg till md-filer i rätt mapp, kör `python -m rag ingest --reindex -v`
5. Om kod ändras: `git push` triggar automatisk Railway-deploy
6. Uppdatera `PROJECT_STATUS.md` efter avslutat arbete

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
