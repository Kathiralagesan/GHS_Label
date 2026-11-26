# Laboratory GHS & CLP Mixture Label Generator

**A browser-based chemical labeling studio and Python CLI for laboratory solutions and custom mixtures.**

Conceived and developed by **Dr. Kathirvel Alagesan**.

Generate GHS/CLP hazard labels for laboratory buffers, LC-MS mobile phases, and custom chemical mixtures using composition-driven classification, chemical reference data, and vector-based label rendering.

## Regulatory Scope and Limitations

- **Intended use:** Designed primarily for laboratory secondary-container labeling.
- **Data dependency:** Calculated classifications depend on the accuracy and completeness of the user-entered composition and chemical reference data.
- **PubChem verification:** Optional PubChem lookups retrieve available GHS hazard information (pictograms, signal words, and hazard/precautionary statements) as a reference and should be verified against applicable regulatory sources.
- **Not a legal substitute:** Generated labels do not replace supplier Safety Data Sheets (SDSs) or complete legally compliant CLP labels where required. **Conservative EHS mode** provides supplementary laboratory precautions and is not a substitute for regulatory classification.

## Key Features

- **Mixture classification:** Supports `% (v/v)`, `% (w/v)`, `% (w/w)`, `M`, and `mM` concentrations.
- **CLP-based evaluation:** Implements applicable EU CLP Annex I generic concentration limits (GCLs), specific concentration limits (SCLs), and Article 26 pictogram precedence rules.
- **Chemical lookup:** Offline registry of 55+ common laboratory reagents, with optional PubChem lookup by CAS number or chemical name.
- **Label layouts:** Minimal bench labels (`DATE PREPARED`, `PREPARED BY`, `NOTES`) and full hazard-information layouts with pictograms, signal words, H-codes, and P-codes.
- **Print-ready output:** Calibrated label dimensions (`45 × 25 mm` to `100 × 60 mm` plus custom sizes), SVG rendering, anti-clip A4/Letter pagination, and 300-DPI PDF export.
- **Batch generation:** 38 standard laboratory buffer presets, multi-label print queue, and print sheet support.
- **Dual EHS modes:** Strict CLP classification and conservative laboratory precautionary labeling.

## Classification Methodology and Limitations

- **Molarity-to-concentration conversion:** Molar (`M`) and millimolar (`mM`) inputs are converted to mass concentration (`% w/v`, g per 100 mL) using each component's molecular weight (`MW`). For custom or unresolved compounds without a known `MW`, a default placeholder of `100 g/mol` is used unless specified.
- **Percentage units and density:** Inputs in `% (v/v)`, `% (w/v)`, and `% (w/w)` are evaluated directly against the numeric CLP concentration thresholds without separate density-based volume-to-mass conversion (effectively approximating dilute aqueous density ≈ 1 g/mL when comparing `% w/v` or `% v/v` against `% w/w` cutoffs).
- **Additive vs. individual cutoffs:** Components are evaluated against component-specific SCLs/GCLs and Article 26 pictogram precedence rules; complex physical hazards (e.g., flash-point testing of mixed organic/aqueous phases) are not experimentally measured and should be verified when exact flash-point boundaries apply.

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

```bash
python3 ghs_mixture_cli.py \
  --comp "6 M GdnHCl, 50 mM Tris, 10 mM TCEP, 40 mM CAA" \
  --title "Proteomics Lysis Buffer" \
  --style minimal \
  --width-mm 80 --height-mm 45 \
  --out lysis_buffer_label.svg
```

**Generate a label using CAS numbers:**

```bash
python3 ghs_mixture_cli.py \
  --comp "80% 75-05-8, 0.1% 64-18-6" \
  --title "LC-MS Mobile Phase B" \
  --out lcms_buffer_b.svg
```

## Repository Structure

| File / Directory | Description |
|---|---|
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
