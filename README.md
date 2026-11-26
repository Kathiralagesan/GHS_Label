# Laboratory GHS Pictogram & Mixture Label Studio

**Conceived & Developed by Dr. Kathirvel Alagesan**

A 100% client-side, zero-backend web application and Python CLI tool for generating **Globally Harmonized System (GHS) / EU CLP Regulation (EC) No 1272/2008** chemical safety labels for laboratory buffers, mobile phases, and custom multi-component mixtures.

---

## ✨ Key Features

- **Composition-Driven CLP Mixture Engine**: Enter any solution recipe in `% (v/v)`, `% (w/v)`, `% (w/w)`, `M (mol/L)`, or `mM (mmol/L)` (e.g., `80% ACN, 0.1% FA` or `6 M GdnHCl, 50 mM Tris, 10 mM TCEP, 40 mM CAA`). Molarities are automatically converted to `% (w/v)` via Molecular Weight ($\text{MW}$) and evaluated against EU CLP Annex I Generic Concentration Limits (GCLs), Annex VI Specific Concentration Limits (SCLs), and Article 26 Pictogram Precedence rules.
- **CAS Number Search & Live NCBI PubChem Lookup (115M+ Compounds)**:
  - **Instant Offline Registry**: Built-in database of 55+ common biochemistry, proteomics, LC-MS, and molecular biology reagents indexed by CAS number, name, formula, and abbreviation.
  - **Live PubChem PUG-REST & PUG-View Integration**: Enter any CAS number not in the offline table to automatically resolve its Compound ID (CID), Molecular Weight, official GHS Pictograms (`GHS01`–`GHS09`), Signal Word, and H/P-codes directly in the browser, with automatic `localStorage` caching.
- **Minimal & Full Regulatory Layouts**:
  - **Minimal Bench Layout (Default)**: Clean, high-legibility secondary container label displaying the solution name, composition, Signal Word banner, official UNECE vector GHS diamond pictograms, and three write-in/pre-fillable fields (`DATE PREPARED`, `PREPARED BY`, `NOTES`).
  - **Full Regulatory Layout**: Includes full Hazard Statements (`H-codes`) and Precautionary Statements (`P-codes`).
- **Calibrated Physical Print Sizes (`mm` / `inches`)**:
  - **Large Bottle (500–1000 mL GL45)**: `100 × 60 mm` (`3.94" × 2.36"`)
  - **Medium Bottle (250–500 mL)**: `80 × 45 mm` (`3.15" × 1.77"`)
  - **Small Bottle / 50 mL Falcon Tube**: `60 × 35 mm` (`2.36" × 1.38"`)
  - **Mini / 15 mL Tube / Vial**: `45 × 25 mm` (`1.77" × 0.98"`)
  - **Custom Dimensions**: Any user-specified `Width × Height (mm)`.
- **Dual EHS Modes**: Switch between **Strict CLP Regulatory Mixture Cutoffs** (e.g., Formic Acid SCL $\ge 2\%$, TFA GCL $\ge 1\%$) and **Conservative Lab EHS Policy Mode** (displays precautionary acid/corrosive pictograms on all dilute acid/base buffers).

---

## 🚀 Quick Start (Browser & GitHub Pages)

1. **Local Use**: Double-click `index.html` (or `GHS_Custom_Solution_Generator.html`) to open the studio in any modern browser. No server or installation is required.
2. **GitHub Pages Deployment**:
   - Push this repository to GitHub.
   - In your GitHub repository, go to **Settings → Pages → Build and deployment**, select **Deploy from a branch** (`main` / `/ (root)`), and save.
   - Your studio will be live at `https://<your-username>.github.io/<repo-name>/`.

---

## 🖥️ Command-Line Interface (Python CLI)

Generate standalone vector `.svg` labels directly from the terminal using `ghs_mixture_cli.py` (requires only standard Python 3):

```bash
# Generate a minimal 80x45 mm label from chemical names or abbreviations
python3 ghs_mixture_cli.py \
  --comp "6 M GdnHCl, 50 mM Tris, 10 mM TCEP, 40 mM CAA" \
  --title "Proteomics Lysis Buffer" \
  --style minimal \
  --width-mm 80 --height-mm 45 \
  --out lysis_buffer_label.svg

# Generate a label directly from CAS numbers
python3 ghs_mixture_cli.py \
  --comp "80% 75-05-8, 0.1% 64-18-6" \
  --title "LC-MS Mobile Phase B" \
  --out lcms_buffer_b.svg
```

---

## 📁 Repository Structure

- `index.html` / `GHS_Custom_Solution_Generator.html` — Flagship editorial web application (Universal Mixture Calculator, Live PubChem CAS Lookup, 18 Standard Presets, and Multi-Label Print Sheet Queue).
- `GHS_Labels_Print_Sheet.html` — Dedicated 18-buffer batch print sheet studio.
- `ghs_mixture_cli.py` — Command-line mixture GHS calculator and SVG generator.
- `generate_ghs_labels.py` — Batch generator for the 18 preset LC-MS & solvent labels.
- `official_ghs_icons/` — Official UNECE vector SVG pictograms (`GHS01.svg`–`GHS09.svg`).
- `labels_svg_minimal_regulatory/` & `labels_svg_minimal_ehs/` — Individual minimal vector SVG labels for the 18 standard buffers.
- `labels_svg_regulatory/` & `labels_svg_conservative_ehs/` — Individual full-text vector SVG labels for the 18 standard buffers.

---

## 📜 Attribution & License

- **Author & Credit**: Conceived and developed by **Dr. Kathirvel Alagesan**.
- **Pictogram Artwork**: Official UNECE GHS Rev. 10 vector pictograms (adapted from public-domain UNECE / Wikimedia Commons / [`artofpilgrim/labels`](https://github.com/artofpilgrim/labels)).
- **Chemical Data**: Harmonised classifications per EU CLP Regulation (EC) No 1272/2008 Annex VI and live lookups via NCBI PubChem PUG-REST / PUG-View APIs.
- **License**: Released under the [MIT License](LICENSE).
