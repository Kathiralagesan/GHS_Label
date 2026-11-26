# Laboratory GHS & CLP Mixture Label Generator

**A browser-based chemical labeling studio and Python CLI for laboratory solutions and custom mixtures.**

Conceived and developed by **Dr. Kathirvel Alagesan**.

Generate GHS/CLP hazard labels for laboratory buffers, LC-MS mobile phases, and custom chemical mixtures using composition-driven classification, chemical reference data, and vector-based label rendering.

## Key Features

- **Mixture classification:** Supports `% (v/v)`, `% (w/v)`, `% (w/w)`, `M`, and `mM` concentrations.
- **CLP-based evaluation:** Implements applicable EU CLP Annex I generic concentration limits (GCLs), specific concentration limits (SCLs), and pictogram precedence rules.
- **Chemical lookup:** Offline registry of 55+ common laboratory reagents, with optional PubChem lookup by CAS number or chemical name.
- **Label layouts:** Minimal bench labels and full hazard-information layouts with pictograms, signal words, H-codes, and P-codes.
- **Print-ready output:** Calibrated label dimensions, custom sizing, SVG rendering, and 300-DPI PDF export.
- **Batch generation:** Standard laboratory buffer presets, multi-label print queue, and print sheet support.
- **Dual EHS modes:** Strict CLP classification and conservative laboratory precautionary labeling.

## Privacy and Offline Operation

Mixture calculations, classification, SVG rendering, pagination, and PDF generation run locally in the browser.

No application backend is required. Optional PubChem lookups are the only external network requests. Enable **Offline Mode (Disable PubChem)** to prevent external requests and use the built-in registry and cached data.

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
| `index.html` | Main mixture calculator and label studio |
| `GHS_Custom_Solution_Generator.html` | Standalone application |
| `GHS_Labels_Print_Sheet.html` | Batch print sheet studio |
| `ghs_mixture_cli.py` | Python CLI and SVG generator |
| `generate_ghs_labels.py` | Batch preset label generator |
| `official_ghs_icons/` | GHS pictogram SVGs |
| `labels_svg_*/` | Pre-generated labels by layout and EHS mode |

## Regulatory Scope

Designed primarily for laboratory secondary-container labeling.

Classification depends on the accuracy of the composition and chemical data provided. PubChem information should be verified against applicable regulatory sources.

Generated labels do not replace supplier SDSs or complete legally compliant CLP labels where required. Conservative EHS mode provides supplementary laboratory precautions and is not a substitute for regulatory classification.

## Data and Attribution

- **Regulatory framework:** EU CLP Regulation (EC) No 1272/2008
- **Chemical data:** Built-in registry and optional NCBI PubChem PUG-REST / PUG-View integration
- **Pictograms:** UNECE GHS Rev. 10 vector artwork (adapted from public-domain UNECE / Wikimedia Commons / [`artofpilgrim/labels`](https://github.com/artofpilgrim/labels))

## License

Released under the [MIT License](LICENSE).

**Author:** Dr. Kathirvel Alagesan
