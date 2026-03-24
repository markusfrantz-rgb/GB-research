---
doc_type: reference
date: 2026-03-24
status: active
---

# GBS-IgA Research Knowledge Base -- Index

*Knowledge base for RAG-powered research on Guillain-Barre Syndrome, IgA Deficiency, and related autoimmune conditions.*

---

## Knowledge Base Structure

### 01-GBS/ -- Guillain-Barre Syndrome
Core research on GBS covering all aspects from pathophysiology to emerging treatments.

| Document | Description | Sections |
|----------|-------------|----------|
| [GBS_Comprehensive_Review.md](../01-GBS/GBS_Comprehensive_Review.md) | Complete evidence-based review of GBS | Pathophysiology, Epidemiology, Diagnosis, Treatment, Prognosis, Refractory GBS, Recent Advances |

**Key topics covered:**
- All GBS subtypes (AIDP, AMAN, AMSAN, Miller Fisher, PCB, panneurofascin)
- Molecular mimicry and ganglioside antibody table
- Brighton criteria, electrodiagnostic criteria
- IVIg and PE protocols with Cochrane evidence
- mEGOS and EGRIS prognostic scoring
- T-cell autoimmunity discovery (Sukenikova et al., Nature 2024)

---

### 02-IgA-deficiency/ -- Selective IgA Deficiency
Comprehensive review of IgA deficiency including the critical IVIg complication risk.

| Document | Description | Sections |
|----------|-------------|----------|
| [Selective_IgA_Deficiency_Comprehensive_Review.md](../02-IgA-deficiency/Selective_IgA_Deficiency_Comprehensive_Review.md) | Complete evidence-based review of SIgAD | Pathophysiology, Genetics, Epidemiology, Diagnosis, Clinical Manifestations, Treatment, IVIg Complications, Autoimmune Comorbidities |

**Key topics covered:**
- B-cell differentiation defects, HLA 8.1 ancestral haplotype
- GWAS findings (PVT1, ATG13-AMBRA1, AHI1, CLEC16A, IFIH1)
- TACI mutations and CVID spectrum relationship
- Anti-IgA antibodies: prevalence, types, anaphylaxis mechanisms
- IgA-depleted IVIg products and safety protocols
- Autoimmune comorbidity mapping (15+ conditions)

---

### 03-GBS-and-IgA-deficiency/ -- The Critical Combination
The central document addressing the treatment dilemma when GBS and IgA deficiency co-occur.

| Document | Description | Sections |
|----------|-------------|----------|
| [GBS_IgA_Deficiency_Combined_Review.md](../03-GBS-and-IgA-deficiency/GBS_IgA_Deficiency_Combined_Review.md) | Combined clinical review with decision framework | Treatment Dilemma, Anti-IgA Risk, IgA-Depleted Products, PE as Alternative, Clinical Algorithm, Treatment Resistance, Emerging IgA-Safe Therapies, Shared Mechanisms |

**Key topics covered:**
- Clinical decision algorithm for GBS + IgA deficiency
- GAMMAGARD LIQUID ERC (FDA approved June 2025, available Jan 2026)
- IgA content comparison table for all IVIg products
- All emerging IgA-safe therapies (tanruprubart, efgartigimod, imlifidase)
- Evidence quality assessment table
- Research gaps and priorities

---

### 04-related-autoimmune/ -- Related Autoimmune Conditions
Mapping of autoimmune conditions connected to GBS, IgA deficiency, or both.

| Document | Description | Sections |
|----------|-------------|----------|
| [GBS-IgAD-Autoimmune-Conditions-Research.md](../04-related-autoimmune/GBS-IgAD-Autoimmune-Conditions-Research.md) | Autoimmune comorbidity research | GBS-Associated, IgA-Associated, Overlapping Conditions, Immune Dysregulation Spectrum, Molecular Mechanisms, Clinical Implications |

**Key topics covered:**
- 6 overlapping conditions (SLE, T1D, thyroid disease, IBD, celiac, RA)
- Shared HLA-B8/DR3/DQ2 haplotype associations
- Molecular mimicry across conditions
- Complement and cytokine pathway overlap
- Clinical implications for treatment decisions

---

### 05-treatment-resistance/ -- Refractory GBS and Emerging Therapies
Detailed evidence on treatment-resistant GBS and the therapy pipeline.

| Document | Description | Sections |
|----------|-------------|----------|
| [Refractory_GBS_Comprehensive_Research.md](../05-treatment-resistance/Refractory_GBS_Comprehensive_Research.md) | Complete refractory GBS research | TRF Definition, Second-Line Treatments, Clinical Trials, Biomarkers, Special Populations, Guidelines, Emerging Therapies |

**Key topics covered:**
- SID-GBS trial results (second IVIg course futility)
- Tanruprubart Phase 3 positive results (OR 2.4, p=0.0058)
- Imlifidase Phase 2 results (walking 6 weeks sooner)
- Efgartigimod case reports and ongoing Phase 2
- NfL, delta-IgG, and complement biomarkers
- 2023 EAN/PNS guideline recommendations

---

## Quick Reference: Key Clinical Findings

### Most Important Treatment Facts
1. **IVIg and PE are equivalent** for GBS (Level 1 evidence)
2. **Second IVIg course does NOT help** and increases adverse events (SID-GBS trial)
3. **Anti-IgA anaphylaxis risk is lower than traditionally believed** (Rachid & Bonilla 2012)
4. **GAMMAGARD LIQUID ERC** is the first ready-to-use low-IgA liquid IVIg (<=2 mcg/mL, available US Jan 2026)
5. **Tanruprubart (ANX005)** is the first drug with positive Phase 3 results in GBS -- and it's IgA-safe
6. **All emerging therapies** (tanruprubart, efgartigimod, imlifidase) are IgA-safe (monoclonal antibodies/enzymes)

### For the GBS + IgA Deficiency Patient
- **First choice**: Plasmapheresis (avoids IgA entirely)
- **If PE unavailable**: IgA-depleted IVIg with precautions
- **If refractory**: Tanruprubart or efgartigimod (IgA-safe, no immunoglobulin content)
- **Never**: Second IVIg course, combined PE+IVIg, or corticosteroids alone

---

## Citation Statistics

| Document | Number of References | Evidence Levels |
|----------|---------------------|-----------------|
| GBS Comprehensive Review | 54 | RCTs, Cochrane reviews, guidelines |
| IgA Deficiency Review | 37 | GWAS, systematic reviews, guidelines |
| Combined GBS+IgA Review | 26 | Cochrane reviews, Phase 3 trials, systematic reviews |
| Autoimmune Conditions | 44 | Systematic reviews, meta-analyses, case series |
| Refractory GBS Research | 29 | RCTs, Phase 2/3 trials, guidelines |
| **Total unique references** | **~150+** | |

---

## RAG Integration Notes

This knowledge base is structured for optimal chunking by the brewmaster RAG system:
- All documents use H2 (`##`) and H3 (`###`) headings for hierarchical chunking
- Each document has YAML frontmatter with `doc_type: research`, `date`, and `status: active`
- Tables are used extensively for structured data (treatment comparisons, evidence levels)
- Clinical decision algorithms use code blocks for complex logic flows
- Cross-references between documents use relative links

### Recommended brewmaster configuration:
```typescript
const INDEX_PATHS = [
  'docs/research/GBS-IgA',  // or wherever this is placed in brewmaster
];
```

### Chunking expectations:
- ~800 token chunks aligned on H2/H3 boundaries
- Each chunk will be prefixed with document title for context
- Evidence tables will chunk as complete units
- Decision algorithms will chunk as complete units
