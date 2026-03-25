# Projektstatus — GBS & IgA-brist Kunskapsdatabas

> Senast uppdaterad: 2026-03-25 (kväll, slutlig)

## Fas: Live / Aktiv forskning

Kunskapsdatabasen är online och funktionell. Fokus nu är att utöka forskningen och förfina innehållet baserat på klinisk utveckling.

## Vad som finns

### Forskningsdokument (16 st, ~480 referenser)

| # | Dokument | Område | Status |
|---|----------|--------|--------|
| 1 | `01-GBS/GBS_Comprehensive_Review.md` | GBS fullständig översikt (patofys, diagnostik, behandling, prognos) | Komplett |
| 2 | `01-GBS/Recurrent_and_Severe_GBS.md` | Recidiverande GBS, fulminant GBS, A-CIDP-differentiering, **SCIG-utsättning och recidiv** | Komplett |
| 3 | `01-GBS/Severe_GBS_ICU_Management.md` | IVA-vård, ventilator, autonom dysfunktion, prognos, rehab | Komplett |
| 4 | `02-IgA-deficiency/Selective_IgA_Deficiency_Comprehensive_Review.md` | IgA-brist fullständig översikt | Komplett |
| 5 | `02-IgA-deficiency/IgA_Deficiency_SCIG_IVIg_Safety.md` | Gamanorm-tolerans, IVIg-säkerhet, svenska produkter | Komplett |
| 6 | `03-GBS-and-IgA-deficiency/GBS_IgA_Deficiency_Combined_Review.md` | Kombinationen: behandlingsalgoritm, IgA-säkra terapier | Komplett |
| 7 | `04-related-autoimmune/GBS-IgAD-Autoimmune-Conditions-Research.md` | Relaterade autoimmuna tillstånd, delade mekanismer | Komplett |
| 8 | `04-related-autoimmune/Hashimoto-IgAD-GBS-Autoimmune-Cluster.md` | Autoimmunt kluster, levotyroxin vid IVA, **levotyroxin-dosjustering som trigger**, T3 och nervregeneration | Komplett |
| 9 | `05-treatment-resistance/Refractory_GBS_Comprehensive_Research.md` | Refraktär GBS, SID-GBS, komplementhämmare | Komplett |
| 10 | `05-treatment-resistance/PE_Refractory_GBS_Treatment_Options.md` | PE-refraktär GBS, efgartigimod, imlifidase, svenska möjligheter | Komplett |
| 11 | `05-treatment-resistance/PE_Coagulopathy_and_Thromboprophylaxis_in_GBS.md` | PE-koagulopati, fibrinogen, DVT-profylax, trakeostomi-timing | Komplett |
| 12 | `05-treatment-resistance/Sequential_Combined_Therapy_After_PE_Failure.md` | Sekventiell terapi, **efgartigimod off-label i Sverige (praktisk väg)**, timing, interaktioner | Komplett |
| 13 | `05-treatment-resistance/Complete_PE_Failure_Protocol_and_Decision_Algorithm.md` | PE-svikt efter 5 sessioner, beslutsalgoritm, biomarkörer under sedering, NfL-monitorering | Komplett |
| 14 | `06-monitoring-prognosis/GBS_Prognostic_Monitoring_Comprehensive_Review.md` | Prognostisk monitorering: biomarkörer, kliniska skalor, elektrofysiologi, IVA-protokoll | Komplett |
| 15 | `07-acute-icu-protocols/Post_Tracheostomy_Care_GBS_Dysautonomia.md` | Post-trakeostomivård: sugningsprotokoll, vagolytika, BP-hantering, autonom storm, **mortalitetsdata (6% vs 2%)**, monitorering | Komplett |
| 16 | `07-acute-icu-protocols/Ventilator_Weaning_GBS_Protocol.md` | **Respiratoravvänjning: FVC/NIF-trösklar, SBT-protokoll, decannulation, reintubationsrisk, långtidsutfall** | Komplett |

### Utskrivbart kliniskt dokument

| Dokument | Beskrivning |
|----------|-------------|
| `Case_Madeleine_Fragor_och_Fynd.md` | Utskrivbar fallsammanfattning med patientprofil, 19 frågor till neurolog/IVA-läkare, evidenstabeller. Åtkomlig via `/doc/Case_Madeleine_Fragor_och_Fynd.md` |

### Infrastruktur

| Komponent | Status | Detaljer |
|-----------|--------|----------|
| RAG-system | Live | ChromaDB + Gemini embeddings, 7 indexerade mappar |
| Webb (Flask) | Live | Sök, fråga, dokument-vy, case-baserad landningssida |
| Auth | Live | ACCESS_CODE via env var, session-baserad |
| Rate limiting | Live | 10 frågor/min, 30 sökningar/min per IP |
| Railway deploy | Live | Auto-deploy vid git push |
| Domän (custom) | Live | `gbs.ragbase.org` |
| Paraplydomän | Registrerad | `ragbase.org` (Namecheap, exp 2027-03-24) |

## Klinisk kontext — Madeleine

### Profil

| | |
|---|---|
| **Ålder** | 53 år |
| **Diagnoser** | Recidiverande GBS (1:a episod vid 16, ~37 år sedan), selektiv IgA-brist, Hashimotos tyreoidit, obstruktiv sömnapné, ospecificerad födoämnesallergi, pollenallergi |
| **Autoimmunt kluster** | GBS + IgA-brist + Hashimotos — MAS typ 3 (HLA-B8/DR3/DQ2) |
| **Aktuella läkemedel** | Levotyroxin (dosjusterad 2-3 v före insjuknande, **inga uppföljningsprover**), luftrörsvidgande inhalator + nässpray, antihistamin |
| **Tidigare läkemedel** | Gamanorm SCIG (IgA-brist, ~2020–2023, **utsatt ca 2023**) |

### Aktuellt förlopp (2026-03-21 → 2026-03-25)

| Datum | Händelse |
|-------|---------|
| 2026-03-21 (fre) | Akut insjuknande, IVA/respirator inom timmar, nära total förlamning |
| 2026-03-21–24 | 3 PE-sessioner utan kliniskt svar |
| 2026-03-23 | MR hjärna: **normal** |
| 2026-03-24 kväll | CT huvud: **normal** (inga blödningstecken). Anisokori = autonom dysfunktion. |
| 2026-03-25 fm | Trakeostomi genomförd (~kl 12). Feber 38,1°C. Autonom dysfunktion bekräftad (BP-instabilitet, anisokori). |
| 2026-03-25 em | Sedering lättad för att bedöma spontanandning (diafragmafunktion). Levotyroxin ges. Luftrörsvidgande insatt. Allergimedel pågår. |
| 2026-03-26 (plan) | PE session 4 planerad. 2 sessioner kvar av 5. |

### Kommunikation

Vid lättare sederingsdjup: svag höger ögonblinkning (ja), svag höger axel/deltoideus (nej).

### Post-trakeostomi (2026-03-25 em)

Sedering lättas för att bedöma spontanandningsförmåga. Första indikationen på diafragmafunktion och djupet av den motoriska påverkan.

### Diagnostiska luckor (per 2026-03-25)

| Test | Status | Varför det behövs |
|------|--------|--------------------|
| Elektrofysiologi (NCS/EMG) | **Ej utförd** | Subtypning (AIDP/AMAN/AMSAN), prognos |
| Gangliosid-antikroppar | **Ej skickade** | Subtypning, behandlingsval |
| Anti-IgA-antikroppar (IgE + IgG) | **Ej skickade** | IVIg-säkerhet |
| Anti-NF155/NF186 | **Ej skickade** | A-CIDP-differentiering |
| Serum-NfL | **Ej taget** | Prognos, axonal skada, behandlingssvar under sedering |
| TSH, fT4, fT3 | **Ej kontrollerade sedan inläggning** | Sköldkörtelstatus okänd pga dosjustering utan uppföljning |
| CSF IL-8 | **Ej taget** | GBS vs CIDP (96,7% specificitet) |

### Hypoteser att utreda

1. **SCIG-utsättning som bidragande faktor**: Stabil under ~3 år på Gamanorm, recidiv ~2 år efter utsättning. Mönstret påminner om CIDP-dependency. Oavsett om R-GBS eller A-CIDP bör SCIG återinsättas efter akutfasen.
2. **Levotyroxin-dosjustering som trigger**: Dos ändrad 2-3 v före insjuknande, inga uppföljningsprover. TSH-instabilitet kan driva Th1/Th17-polarisering via DC-aktivering. Tidslinjen matchar GBS-triggerlatens (1-4 veckor).
3. **R-GBS vs A-CIDP**: 37-årsintervall talar starkt för R-GBS (Kuitwaard 2009). Men SCIG-utsättningens roll och behandlingsrespons kan tala för A-CIDP. Diagnostik behövs (NCS, CSF IL-8, anti-NF155).

## Möjliga nästa steg

### Forskning — öppna uppgifter
- [ ] Uppdatera med Madeleines kliniska utveckling (anonymiserat om publiceras)
- [ ] Hansa Biopharma compassionate use — resultat av kontakt
- [ ] Tanruprubart EMA-status — bevaka
- [ ] Nya fallrapporter GBS + IgA-brist (löpande PubMed-bevakning)

### Forskning — genomförda denna session (2026-03-25)
- [x] PE-koagulopati: fibrinogendepletion, monitorering, ersättningsprotokoll (38 ref)
- [x] DVT/PE-profylax vid immobiliserad GBS (incidens, LMWH, IPC)
- [x] Trakeostomi-timing vid koagulopati (tröskelvärden, korrektion)
- [x] Sekventiell terapi: PE→IVIg→efgartigimod/imlifidase timing och interaktioner
- [x] Efgartigimod off-label i Sverige: regulatorisk väg, sjukhusapotek, argenx-kontakt, tidsram, kostnad
- [x] Hashimotos + IgA-brist + GBS autoimmunt kluster (48 ref)
- [x] Levotyroxin-dosjustering som potentiell GBS-trigger (biologisk rimlighet, tidslinjeanalys)
- [x] PE avlägsnar levotyroxin — doseringsprotokoll (ge EFTER PE, monitorera TSH)
- [x] Prognostisk monitorering: NfL, mEGOS, EGRIS, NCS, IVA-protokoll (27 ref)
- [x] Komplett PE-svikt-protokoll efter 5 sessioner: definition, beslutsalgoritm, biomarkörer under sedering (20 ref)
- [x] Post-trakeostomivård vid svår dysautonomi: sugningsprotokoll, vagolytika, BP-hantering, autonom storm (21 ref)
- [x] SCIG-utsättning och GBS-recidiv: immunmodulering, CIDP-parallell, rebound, diagnostiska implikationer
- [x] Case-baserad landningssida med patientprofil och evidenspresentation
- [x] Utskrivbart kliniskt sammanfattningsdokument (19 frågor + evidenstabeller)
- [x] RAG-konfiguration: alla 7 mappar indexerade

### Teknik
- [x] Custom domän `gbs.ragbase.org`
- [x] RAG indexerar alla 7 mappar (01-07)
- [ ] Sökresultat: förbättra rendering av tabeller i expanderade chunks
- [ ] Lösenordsskydd per användare (om fler behöver individuell access)
- [ ] Exportfunktion: generera PDF av Q&A-svar med källor

### Innehåll — Fas 2 (pausad, tas efter akutfasen)
- [ ] Rehabilitering efter svår GBS (evidensbaserade protokoll, tidslinjer, milstolpar)
- [ ] Fatigue, kronisk smärta och livskvalitet långsiktigt
- [ ] Psykologiskt stöd: PICS, IVA-delirium, anhörigstöd
- [ ] Kommunikationsstrategier vid locked-in/ventilator
- [ ] Översätt KUNSKAPSBASEN.md till engelska (parallellversion)

### Kvalitetssäkring — att tänka på
- [ ] Verifiera specifika doser/tröskelvärden mot originalartiklar (se disclaimer nedan)
- [ ] Kontrollera att kontaktuppgifter (argenx, Hansa) fortfarande är aktuella
- [ ] Korrigera författarattribution i 5 referenser (Martin-Aguilar→van Tilburg, Kohle→Altmann, Nagaoka→Thomma, Haupt 2011 ej hittad, Qiu 2022 ej hittad) — PMIDs stämmer, innehåll korrekt, men förstaförfattare fel
- [x] Lägga till PMID-nummer för nyckelreferenser (genomfört 2026-03-25, ~30 PMIDs tillagda)
- [x] Evidensgradering (Level 1-5) vid nyckelrekommendationer (genomfört 2026-03-25, 10 dokument annoterade)

## Disclaimer om evidenskvalitet

Databasen är en strukturerad litteraturöversikt baserad på ~450 peer-reviewed källor (PubMed, Cochrane Library, ClinicalTrials.gov). Den har **inte genomgått formell peer review**. Specifika siffror (doser, tröskelvärden, p-värden) bör verifieras mot originalartiklarna. Kontaktuppgifter kan ha ändrats. Regulatorisk information (efgartigimod off-label i Sverige) baseras på publicerade riktlinjer och kan behöva verifieras med Läkemedelsverket eller sjukhusapotek.

## Ändringslogg

| Datum | Vad |
|-------|-----|
| 2026-03-24 | Initial release: 5 forskningsdokument, RAG, lokal webbsida |
| 2026-03-24 | Utökad: +4 dokument (recidiverande GBS, IVA, SCIG/IVIg-säkerhet, PE-refraktär) |
| 2026-03-24 | Deploy till Railway, auth, rate limiting, klickbara källor |
| 2026-03-24 | Dokumentation färdigställd (CLAUDE.md, PROJECT_STATUS.md) |
| 2026-03-25 | Custom domain `gbs.ragbase.org` konfigurerad. Auth verifierad. |
| 2026-03-25 | +4 nya dokument: PE-koagulopati (38 ref), sekventiell terapi, Hashimoto-kluster (48 ref), prognostisk monitorering (27 ref). Totalt 13 dok. |
| 2026-03-25 | KUNSKAPSBASEN.md omstrukturerad till case-baserat format med patientprofil, metodsektion, disclaimer. |
| 2026-03-25 | Utskrivbart kliniskt dokument: `Case_Madeleine_Fragor_och_Fynd.md` (19 frågor + evidenstabeller). |
| 2026-03-25 | Gamanorm korrigerat: tidigare läkemedel (utsatt ~2023), ej aktuellt. |
| 2026-03-25 | Kliniska uppdateringar: CT normal, trakeostomi genomförd, autonom dysfunktion bekräftad, PE återupptas, levotyroxin ges. |
| 2026-03-25 | +2 nya dokument: Komplett PE-svikt-protokoll (20 ref), post-trakeostomi dysautonomi-vård (21 ref). Ny mapp `07-acute-icu-protocols/`. Totalt 15 dok. |
| 2026-03-25 | Efgartigimod off-label i Sverige: praktisk tillgångsväg tillagd (regulatorisk väg, argenx-kontakt, sjukhusapotek, tidsram, kostnad, doseringsprotokoll). |
| 2026-03-25 | Levotyroxin-dosjustering som potentiell GBS-trigger: ny sektion med biologisk mekanism (T3→DC→Th1/Th17), tidslinjeanalys, PE-levotyroxin-interaktion (5 nya ref). |
| 2026-03-25 | SCIG-utsättning och GBS-recidiv: ny sektion med immunmodulering, CIDP-parallell (PATH-studien), rebound-evidens, R-GBS vs A-CIDP diagnostisk implikation, rekommendation om SCIG-återinsättning. |
| 2026-03-25 | RAG konfigurerad för alla 7 mappar (01-07). Totalt 15 dokument, ~450 referenser. |
| 2026-03-25 | Klinisk uppdatering: trakeostomi genomförd, sedering lättad för spontanandningstest, PE4 planerad 2026-03-26. |
| 2026-03-25 | Evidensgradering (Level 1-5) tillagd i 10 dokument. Evidensskala-legend tillagd i KUNSKAPSBASEN.md. |
| 2026-03-25 | ~30 PMID-nummer tillagda vid nyckelreferenser (behandlingsrekommendationer, tröskelvärden, doseringsprotokoll). |
| 2026-03-25 | Författarkorrigeringar: Martin-Aguilar→van Tilburg, Kohle→Altmann, Nagaoka→Thomma, Stolk→Mahmoud, SID-GBS PMID korrigerat. |
| 2026-03-25 | Nytt dokument: `07-acute-icu-protocols/Ventilator_Weaning_GBS_Protocol.md` — respiratoravvänjning, FVC/NIF-trösklar, SBT-protokoll, decannulation, 7 referenser. |
| 2026-03-25 | Dysautonomi-doc uppdaterat: mortalitet 6% vs 2% (Chakraborty), incidenstal från 2 kohorter, weaning-korsreferens. |
| 2026-03-25 | Prognostik-doc uppdaterat: neuroprognostikering (Busl GRADE), EGRIS validering (n=1500), strukturerade beslutspunkter dag 7/14/28. |
| 2026-03-25 | Källbibliotek: 22 fulltexter hämtade (12 PDF + 10 text), 30 artiklar kartlagda. `sources/fulltext/` + `Tillgang_till_medicinska_kallor.md`. |
| 2026-03-25 | RAG reindexerad: 16 dokument, 391 chunks. Deploy till gbs.ragbase.org. |
