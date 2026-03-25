# Projektstatus — GBS & IgA-brist Kunskapsdatabas

> Senast uppdaterad: 2026-03-25 (eftermiddag)

## Fas: Live / Aktiv forskning

Kunskapsdatabasen är online och funktionell. Fokus nu är att utöka forskningen och förfina innehållet baserat på klinisk utveckling.

## Vad som finns

### Forskningsdokument (13 st, ~330 chunks, ~400 referenser)

| # | Dokument | Område | Status |
|---|----------|--------|--------|
| 1 | `01-GBS/GBS_Comprehensive_Review.md` | GBS fullständig översikt (patofys, diagnostik, behandling, prognos) | Komplett |
| 2 | `01-GBS/Recurrent_and_Severe_GBS.md` | Recidiverande GBS, fulminant GBS, A-CIDP-differentiering | Komplett |
| 3 | `01-GBS/Severe_GBS_ICU_Management.md` | IVA-vård, ventilator, autonom dysfunktion, prognos, rehab | Komplett |
| 4 | `02-IgA-deficiency/Selective_IgA_Deficiency_Comprehensive_Review.md` | IgA-brist fullständig översikt | Komplett |
| 5 | `02-IgA-deficiency/IgA_Deficiency_SCIG_IVIg_Safety.md` | Gamanorm-tolerans, IVIg-säkerhet, svenska produkter | Komplett |
| 6 | `03-GBS-and-IgA-deficiency/GBS_IgA_Deficiency_Combined_Review.md` | Kombinationen: behandlingsalgoritm, IgA-säkra terapier | Komplett |
| 7 | `04-related-autoimmune/GBS-IgAD-Autoimmune-Conditions-Research.md` | Relaterade autoimmuna tillstånd, delade mekanismer | Komplett |
| 8 | `04-related-autoimmune/Hashimoto-IgAD-GBS-Autoimmune-Cluster.md` | Trippelt autoimmunt kluster: Hashimotos + IgA-brist + GBS, levotyroxin vid IVA, sköldkörtel & nervåterhämtning | Komplett |
| 9 | `05-treatment-resistance/Refractory_GBS_Comprehensive_Research.md` | Refraktär GBS, SID-GBS, komplementhämmare | Komplett |
| 10 | `05-treatment-resistance/PE_Refractory_GBS_Treatment_Options.md` | PE-refraktär GBS, efgartigimod, imlifidase, svenska möjligheter | Komplett |
| 11 | `05-treatment-resistance/PE_Coagulopathy_and_Thromboprophylaxis_in_GBS.md` | PE-koagulopati, fibrinogen, DVT-profylax, trakeostomi-timing, blödning/trombos-balans | Komplett |
| 12 | `05-treatment-resistance/Sequential_Combined_Therapy_After_PE_Failure.md` | Sekventiell terapi: PE→IVIg→efgartigimod/imlifidase timing, interaktioner, beslutsstöd | Komplett |
| 13 | `06-monitoring-prognosis/GBS_Prognostic_Monitoring_Comprehensive_Review.md` | Prognostisk monitorering: biomarkörer, kliniska skalor, elektrofysiologi, behandlingssvar, IVA-protokoll | Komplett |

### Infrastruktur

| Komponent | Status | Detaljer |
|-----------|--------|----------|
| RAG-system | Live | ChromaDB + Gemini embeddings, 245 chunks |
| Webb (Flask) | Live | Sök, fråga, dokument-vy |
| Auth | Live | ACCESS_CODE via env var |
| Rate limiting | Live | 10 frågor/min, 30 sökningar/min per IP |
| Railway deploy | Live | Auto-deploy vid git push |
| Domän (Railway) | Live | `gb-research-production.up.railway.app` |
| Domän (custom) | Live (DNS propagerar) | `gbs.ragbase.org` — CNAME → `kwv21e29.up.railway.app` |
| Paraplydomän | Registrerad | `ragbase.org` (Namecheap, Auto-Renew, exp 2027-03-24) |
| Åtkomstkod | Live | `ACCESS_CODE` env var, session-baserad (giltig tills browser stängs) |

## Klinisk kontext

Markus fru Madeleine:
- 53 år, recidiverande GBS (första episod vid 16 års ålder, ~37 år sedan)
- Känd selektiv IgA-brist, tidigare behandlad med Gamanorm SCIG (~2020–2023, utsatt ca 2023)
- Levotyroxin för sköldkörteln (troligen Hashimotos tyreoidit — autoimmun hypotyreos)
- **Autoimmunt kluster:** GBS + selektiv IgA-brist + autoimmun sköldkörtelsjukdom (HLA-8.1-haplotyp-association)
- Insjuknade fredag 2026-03-21, IVA/respirator inom timmar
- Nära total förlamning
- Fått 3 plasmaferesesessioner utan förväntat svar
- Koagulopati utvecklad → trakeostomi uppskjuten
- MR hjärna 2026-03-23: normal
- CT huvud 2026-03-24 kväll: utförd pga anisokori (V > H) + koagulopati — inväntar svar
- Djupt sederad. Kommunikation vid lättare sedering: svag höger ögonblinkning (ja), svag höger axel (nej)
- Obstruktiv sömnapné (hemmabehandling: inhalator + nässpray)
- Ospecificerad födoämnesallergi, pollenallergi (antihistamin året runt)
- **Diagnostiska luckor per 2026-03-25:** Elektrofysiologi (NCS/EMG), gangliosid-antikroppar, anti-IgA-antikroppar, NfL, TSH/fT4/fT3 — ej utförda/skickade
- Status per 2026-03-25: avvaktar vidare behandlingsbeslut

## Möjliga nästa steg

### Forskning
- [ ] Uppdatera med Madeleines kliniska utveckling (anonymiserat om publiceras)
- [ ] Fördjupa kring efgartigimod off-label-protokoll i Sverige
- [ ] Hansa Biopharma compassionate use — resultat av kontakt
- [ ] Tanruprubart EMA-status — bevaka
- [ ] Nya fallrapporter GBS + IgA-brist (löpande PubMed-bevakning)
- [ ] CIDP-differentiering: fördjupa diagnostiska biomarkörer
- [x] Sekventiell terapi: PE→IVIg→efgartigimod/imlifidase timing och interaktioner
- [x] Hashimotos + IgA-brist + GBS autoimmunt kluster (TSH-recidivdata, levotyroxin IVA)
- [x] Prognostisk monitorering: NfL, mEGOS, EGRIS, NCS, IVA-protokoll
- [x] Case-baserad landningssida med patientprofil och evidenspresentation
- [x] Utskrivbart kliniskt sammanfattningsdokument (Case_Madeleine_Fragor_och_Fynd.md)
- [x] PE-koagulopati: fibrinogendepletion, monitorering, ersättningsprotokoll
- [x] DVT/PE-profylax vid immobiliserad GBS (incidens, LMWH, IPC)
- [x] Trakeostomi-timing vid koagulopati (tröskelvärden, korrektion)
- [x] Antikoagulationsbeslut vid samtidig koagulopati och immobilisering

### Teknik
- [x] Egen domän — `gbs.ragbase.org` (DNS propagerar, bör vara klart 2026-03-25 morgon)
- [ ] Sökresultat: förbättra rendering av tabeller i expanderade chunks
- [ ] Lösenordsskydd per användare (om fler behöver individuell access)
- [ ] Exportfunktion: generera PDF av Q&A-svar med källor

### Innehåll
- [ ] Översätt KUNSKAPSBASEN.md till engelska (parallellversion)
- [ ] **Fas 2 — Rehabilitering & livskvalitet** (pausad, tas efter akutfasen):
  - [ ] Rehabilitering efter svår GBS (evidensbaserade protokoll, tidslinjer, milstolpar)
  - [ ] Fatigue, kronisk smärta och livskvalitet långsiktigt
  - [ ] Psykologiskt stöd: PICS, IVA-delirium, anhörigstöd
  - [ ] Kommunikationsstrategier vid locked-in/ventilator

## Ändringslogg

| Datum | Vad |
|-------|-----|
| 2026-03-24 | Initial release: 5 forskningsdokument, RAG, lokal webbsida |
| 2026-03-24 | Utökad: +4 dokument (recidiverande GBS, IVA, SCIG/IVIg-säkerhet, PE-refraktär) |
| 2026-03-24 | Deploy till Railway, auth, rate limiting, klickbara källor |
| 2026-03-24 | Snabblänkar till nyckeldokument, CLAUDE.md + PROJECT_STATUS.md dokumentation |
| 2026-03-25 | Auth verifierad och fungerande. Env var-felsökning dokumenterad. |
| 2026-03-25 | Custom domain `gbs.ragbase.org` konfigurerad (Namecheap DNS + Railway). Paraplydomän `ragbase.org` registrerad. |
| 2026-03-25 | Nyckeldokument-länktabell och deep-links från introsidan. Dokumentation färdigställd (CLAUDE.md, PROJECT_STATUS.md). |
| 2026-03-25 | Nytt dokument: PE-koagulopati och trombosprofylax vid GBS (38 referenser). Täcker fibrinogendepletion, lab-monitorering, DVT-profylax, trakeostomi-timing, antikoagulationsbeslut. |
| 2026-03-25 | Nytt dokument: Prognostisk monitorering vid akut GBS (27 referenser). NfL, mEGOS/EGRIS, NCS-timing, IVA-protokoll. |
| 2026-03-25 | Nytt dokument: Sekventiell/kombinerad terapi efter PE-svikt. PE→IVIg timing, PE→efgartigimod (24-48h), imlifidase fördel vid koagulopati, beslutsstödsalgoritm. |
| 2026-03-25 | Nytt dokument: Hashimotos-IgA-brist-GBS autoimmunt kluster (48 referenser). TSH >3.87 som riskfaktor för GBS-recidiv, levotyroxin vid IVA, T3 och nervregeneration. |
| 2026-03-25 | Utökad klinisk kontext: Madeleines fullständiga profil inkl. Hashimotos, sömnapné, allergier, anisokori, CT-huvud, sederingsgrad. |
| 2026-03-25 | Totalt nu: 13 forskningsdokument, ~400 referenser. Fas 2 (rehab/livskvalitet) dokumenterad som framtida steg. |
