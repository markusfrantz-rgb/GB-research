# Projektstatus — GBS & IgA-brist Kunskapsdatabas

> Senast uppdaterad: 2026-03-24

## Fas: Live / Aktiv forskning

Kunskapsdatabasen är online och funktionell. Fokus nu är att utöka forskningen och förfina innehållet baserat på klinisk utveckling.

## Vad som finns

### Forskningsdokument (9 st, 245 chunks, ~250 referenser)

| # | Dokument | Område | Status |
|---|----------|--------|--------|
| 1 | `01-GBS/GBS_Comprehensive_Review.md` | GBS fullständig översikt (patofys, diagnostik, behandling, prognos) | Komplett |
| 2 | `01-GBS/Recurrent_and_Severe_GBS.md` | Recidiverande GBS, fulminant GBS, A-CIDP-differentiering | Komplett |
| 3 | `01-GBS/Severe_GBS_ICU_Management.md` | IVA-vård, ventilator, autonom dysfunktion, prognos, rehab | Komplett |
| 4 | `02-IgA-deficiency/Selective_IgA_Deficiency_Comprehensive_Review.md` | IgA-brist fullständig översikt | Komplett |
| 5 | `02-IgA-deficiency/IgA_Deficiency_SCIG_IVIg_Safety.md` | Gamanorm-tolerans, IVIg-säkerhet, svenska produkter | Komplett |
| 6 | `03-GBS-and-IgA-deficiency/GBS_IgA_Deficiency_Combined_Review.md` | Kombinationen: behandlingsalgoritm, IgA-säkra terapier | Komplett |
| 7 | `04-related-autoimmune/GBS-IgAD-Autoimmune-Conditions-Research.md` | Relaterade autoimmuna tillstånd, delade mekanismer | Komplett |
| 8 | `05-treatment-resistance/Refractory_GBS_Comprehensive_Research.md` | Refraktär GBS, SID-GBS, komplementhämmare | Komplett |
| 9 | `05-treatment-resistance/PE_Refractory_GBS_Treatment_Options.md` | PE-refraktär GBS, efgartigimod, imlifidase, svenska möjligheter | Komplett |

### Infrastruktur

| Komponent | Status | Detaljer |
|-----------|--------|----------|
| RAG-system | Live | ChromaDB + Gemini embeddings, 245 chunks |
| Webb (Flask) | Live | Sök, fråga, dokument-vy |
| Auth | Live | ACCESS_CODE via env var |
| Rate limiting | Live | 10 frågor/min, 30 sökningar/min per IP |
| Railway deploy | Live | Auto-deploy vid git push |
| Domän | Railway default | `gb-research-production.up.railway.app` |
| Egen domän | Ej konfigurerad | Väntar på domänval |

## Klinisk kontext

Markus fru Madeleine:
- 53 år, recidiverande GBS (första episod vid 16 års ålder)
- Känd selektiv IgA-brist, tolererat Gamanorm (SCIG)
- Insjuknade fredag 2026-03-21, IVA/respirator inom timmar
- Nära total förlamning
- Fått 3 plasmaferesesessioner utan förväntat svar
- Koagulopati utvecklad → trakeostomi uppskjuten
- Status per 2026-03-24: avvaktar vidare behandlingsbeslut

## Möjliga nästa steg

### Forskning
- [ ] Uppdatera med Madeleines kliniska utveckling (anonymiserat om publiceras)
- [ ] Fördjupa kring efgartigimod off-label-protokoll i Sverige
- [ ] Hansa Biopharma compassionate use — resultat av kontakt
- [ ] Tanruprubart EMA-status — bevaka
- [ ] Nya fallrapporter GBS + IgA-brist (löpande PubMed-bevakning)
- [ ] CIDP-differentiering: fördjupa diagnostiska biomarkörer

### Teknik
- [ ] Egen domän (subdomän under paraplydomän)
- [ ] Sökresultat: förbättra rendering av tabeller i expanderade chunks
- [ ] Lösenordsskydd per användare (om fler behöver individuell access)
- [ ] Exportfunktion: generera PDF av Q&A-svar med källor

### Innehåll
- [ ] Översätt KUNSKAPSBASEN.md till engelska (parallellversion)
- [ ] Lägg till dokument om rehabilitering efter svår GBS
- [ ] Lägg till dokument om psykologiskt stöd för närstående

## Ändringslogg

| Datum | Vad |
|-------|-----|
| 2026-03-24 | Initial release: 5 forskningsdokument, RAG, lokal webbsida |
| 2026-03-24 | Utökad: +4 dokument (recidiverande GBS, IVA, SCIG/IVIg-säkerhet, PE-refraktär) |
| 2026-03-24 | Deploy till Railway, auth, rate limiting, klickbara källor |
