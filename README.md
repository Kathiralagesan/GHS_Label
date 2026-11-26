# Laboratory GHS & CLP Mixture Label Generator

**A browser-based chemical labeling studio and Python CLI for laboratory solutions and custom mixtures.**

[**https://kathiralagesan.github.io/GHS_Label/**](https://kathiralagesan.github.io/GHS_Label/)

Conceived and developed by **Dr. Kathirvel Alagesan**.

Generate GHS/CLP hazard labels for laboratory buffers, LC-MS mobile phases, and custom chemical mixtures using composition-driven screening, chemical reference data, and vector-based label rendering.

## Regulatory Scope and Limitations

- **Intended use (screening suggestion):** Designed primarily for laboratory secondary-container labeling. All generated classifications and labels are **automated screening suggestions**, not legally authoritative hazard determinations.
- **Verify against official documents:** Users must verify all chemical identities, concentrations, pictograms, signal words, and hazard/precautionary statements against official supplier **Safety Data Sheets (SDS)** and applicable **institutional or laboratory EHS practices** before affixing labels to containers.
- **Data dependency:** Calculated classifications depend on the accuracy and completeness of the user-entered composition and chemical reference data.
- **PubChem verification:** Optional PubChem lookups retrieve available GHS hazard information (pictograms, signal words, and hazard/precautionary statements) as a reference and must be verified against applicable regulatory sources.
- **Not a legal substitute:** Generated labels do not replace supplier SDSs or complete legally compliant CLP labels where required. **Conservative EHS mode** provides supplementary laboratory precautions and is not a substitute for regulatory classification.

## Key Features

- **Mixture classification:** Supports `% (v/v)`, `% (w/v)`, `% (w/w)`, `M`, and `mM` concentrations.
- **CLP-based evaluation:** Applies implemented EU CLP Annex I classification criteria, generic and specific concentration limits (GCLs/SCLs), and Article 26 pictogram precedence rules.
- **Chemical lookup:** Offline registry of 55+ common laboratory reagents, with optional PubChem lookup by CAS number or chemical name.
- **Label layouts:** Minimal bench labels (`DATE PREPARED`, `PREPARED BY`, `NOTES`) and full hazard-information layouts with pictograms, signal words, H-codes, and P-codes.
- **Print-ready output:** Calibrated label dimensions (`45 × 25 mm` to `100 × 60 mm` plus custom sizes), vector SVG rendering, A4/Letter print-sheet pagination with clipping safeguards, and 300-DPI rasterized PDF export.
- **Batch generation:** 38 standard laboratory buffer presets, multi-label print queue, and print sheet support.
- **Dual EHS modes:** Strict CLP classification and conservative laboratory precautionary labeling.

## Classification Methodology and Limitations

- **Molarity-to-concentration conversion:** Molar (`M`) and millimolar (`mM`) inputs are converted to mass concentration (`% w/v`, g per 100 mL) using each component's verified molecular weight (`MW`). Compounds without a verified `MW` are flagged as **unresolved** in the calculation dossier and excluded from molar contribution calculations until a verified `MW` from the supplier SDS is provided.
- **Percentage units and density (approximate screening):** Inputs in `% (v/v)`, `% (w/v)`, and `% (w/w)` are compared directly against numeric CLP concentration thresholds without separate density-based volume-to-mass conversion. Because these concentration units are not interchangeable, results for mixtures specified in `% (v/v)` or `% (w/v)` should be treated as **approximate screening** rather than definitive CLP classification, and verified against supplier SDSs and institutional EHS rules.
- **Physical and mixture hazards:** Components are evaluated against implemented component-level SCLs/GCLs and Article 26 pictogram precedence rules; complex physical hazards (e.g., flash-point testing of mixed organic/aqueous phases) are not experimentally measured and must be verified per laboratory safety protocols.

## Privacy and Offline Operation

The browser application performs mixture calculations, hazard classification, SVG rendering, pagination, and PDF generation locally. No application backend or server-side processing is required.

Optional chemical lookups use the NCBI PubChem API (`pubchem.ncbi.nlm.nih.gov`) and represent the only external network requests. Enable **Offline Mode (Disable PubChem)** in the UI to disable all external requests and restrict lookups to the built-in registry and local browser cache.

## Quick Start

### Browser

Open `index.html` or `GHS_Custom_Solution_Generator.html` in any modern browser. No server or installation is required.

### GitHub Pages

Deploy the repository from the `main` branch and root directory using **Settings → Pages → Deploy from a branch**.

## Python CLI

The standalone SVG generator requires Python 3 and the standard library.

**Generate a proteomics buffer label:**

``` bash
python3 ghs_mixture_cli.py \
  --comp "6 M GdnHCl, 50 mM Tris, 10 mM TCEP, 40 mM CAA" \
  --title "Proteomics Lysis Buffer" \
  --style minimal \
  --width-mm 80 --height-mm 45 \
  --out lysis_buffer_label.svg
```

**Generate a label using CAS numbers:**

``` bash
python3 ghs_mixture_cli.py \
  --comp "80% 75-05-8, 0.1% 64-18-6" \
  --title "LC-MS Mobile Phase B" \
  --out lcms_buffer_b.svg
```

## Repository Structure

| File / Directory | Description |
|----|----|
| `index.html` | Primary mixture calculator and label studio |
| `GHS_Custom_Solution_Generator.html` | Standalone web application |
| `GHS_Labels_Print_Sheet.html` | Batch print sheet studio |
| `ghs_mixture_cli.py` | Python CLI and SVG generator |
| `generate_ghs_labels.py` | Batch preset label generator |
| `official_ghs_icons/` | GHS pictogram SVGs |
| `labels_svg_*/` | Pre-generated labels by layout and EHS mode |

## Data and Attribution

- **Regulatory framework:** EU CLP Regulation (EC) No 1272/2008
- **Chemical data:** Built-in offline registry and optional NCBI PubChem PUG-REST / PUG-View integration
- **Pictograms:** UNECE GHS Rev. 10 vector artwork (adapted from public-domain UNECE / Wikimedia Commons / [`artofpilgrim/labels`](https://github.com/artofpilgrim/labels))

## License

Released under the [MIT License](LICENSE).

**Author:** Dr. Kathirvel Alagesan
