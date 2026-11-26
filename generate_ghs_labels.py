#!/usr/bin/env python3
"""
Generates individual GHS-compliant SVG labels (both Minimal and Full layouts,
in both CLP Regulatory and Conservative Lab EHS modes) and an interactive/printable
HTML Label Studio with exact physical print sizes (mm / inches).
"""

import json
from pathlib import Path

BASE_DIR = Path("/Users/u_alagesan/Documents/GHS Label")
SVG_REG_DIR = BASE_DIR / "labels_svg_regulatory"
SVG_EHS_DIR = BASE_DIR / "labels_svg_conservative_ehs"
SVG_MIN_REG_DIR = BASE_DIR / "labels_svg_minimal_regulatory"
SVG_MIN_EHS_DIR = BASE_DIR / "labels_svg_minimal_ehs"

for d in [SVG_REG_DIR, SVG_EHS_DIR, SVG_MIN_REG_DIR, SVG_MIN_EHS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

GHS_SYMBOLS_INNER = json.loads((BASE_DIR / "official_ghs_symbols.json").read_text(encoding="utf-8"))


def render_ghs_diamond_svg(code: str, x: float, y: float, size: float) -> str:
    sym = GHS_SYMBOLS_INNER[code]
    vb, inner = sym["viewBox"], sym["svg"]
    return f'<svg x="{x:.1f}" y="{y:.1f}" width="{size:.1f}" height="{size:.1f}" viewBox="{vb}">{inner}</svg>'


LABELS_DATA = [
    {
        "id": "01_TFA_1pct",
        "group": "Group 1: Aqueous Acid Buffers (TFA / FA)",
        "title": "TFA, 1%",
        "subtitle": "1% (v/v) Trifluoroacetic Acid in Water",
        "cas": "CAS: 76-05-1 (TFA) | 7732-18-5 (H₂O)",
        "composition": "1% Trifluoroacetic acid, 99% Ultrapure Water (pH ~ 1.1)",
        "reg_pictograms": ["GHS07"],
        "reg_signal": "WARNING",
        "reg_h_statements": ["H315: Causes skin irritation (CLP GCL: 1% ≤ C < 5%).", "H319: Causes serious eye irritation (CLP GCL: 1% ≤ C < 3%)."],
        "reg_p_statements": ["P264: Wash skin thoroughly after handling.", "P280: Wear protective gloves and eye/face protection.", "P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes."],
        "reg_note": "CLP GCL 1–3%: Irritant (GHS07). Note: pH < 2; use GHS05 if strict extreme-pH rule applies.",
        "ehs_pictograms": ["GHS05", "GHS07"],
        "ehs_signal": "DANGER",
        "ehs_h_statements": ["H314: Causes severe skin burns and eye damage (Extreme pH ≤ 2 rule).", "H318: Causes serious eye damage."],
        "ehs_p_statements": ["P260: Do not breathe mist or vapours.", "P280: Wear protective gloves, lab coat, and eye/face protection.", "P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes."]
    },
    {
        "id": "02_TFA_0.1pct",
        "group": "Group 1: Aqueous Acid Buffers (TFA / FA)",
        "title": "TFA, 0.1%",
        "subtitle": "0.1% (v/v) Trifluoroacetic Acid in Water",
        "cas": "CAS: 76-05-1 (TFA) | 7732-18-5 (H₂O)",
        "composition": "0.1% Trifluoroacetic acid, 99.9% Ultrapure Water (pH ~ 2.0)",
        "reg_pictograms": [],
        "reg_signal": "NO SIGNAL WORD",
        "reg_h_statements": ["Not a hazardous mixture according to GHS / CLP (< 1% Generic Concentration Limit).", "EUH210: Safety data sheet available on request."],
        "reg_p_statements": ["P280: Wear standard laboratory eye protection and gloves.", "Avoid contact with eyes and prolonged skin contact (dilute acidic buffer, pH ~ 2.0)."],
        "reg_note": "Below 1% CLP GCL cutoff (no mandatory GHS pictogram). Switch to Lab EHS Mode for GHS07.",
        "ehs_pictograms": ["GHS07"],
        "ehs_signal": "WARNING",
        "ehs_h_statements": ["H315/H319 (Precautionary EHS): Dilute strong acid solution (pH ~ 2.0); may irritate eyes/skin."],
        "ehs_p_statements": ["P280: Wear protective gloves and eye protection.", "P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes."]
    },
    {
        "id": "03_FA_1pct",
        "group": "Group 1: Aqueous Acid Buffers (TFA / FA)",
        "title": "FA, 1%",
        "subtitle": "1% (v/v) Formic Acid in Water",
        "cas": "CAS: 64-18-6 (Formic Acid) | 7732-18-5 (H₂O)",
        "composition": "1% Formic acid, 99% Ultrapure Water (pH ~ 2.2)",
        "reg_pictograms": [],
        "reg_signal": "NO SIGNAL WORD",
        "reg_h_statements": ["Not a hazardous mixture under CLP Annex VI Specific Concentration Limit (SCL for FA is ≥ 2%).", "EUH210: Safety data sheet available on request."],
        "reg_p_statements": ["P280: Wear standard laboratory gloves and safety glasses.", "Wash hands after handling; avoid eye contact (dilute organic acid, pH ~ 2.2)."],
        "reg_note": "Formic acid CLP Annex VI SCL for Skin/Eye Irrit. 2 is 2% ≤ C < 10%. At 1%, no pictogram is required.",
        "ehs_pictograms": ["GHS07"],
        "ehs_signal": "WARNING",
        "ehs_h_statements": ["H315/H319 (Precautionary EHS): Contains 1% Formic Acid; may cause mild skin/eye irritation."],
        "ehs_p_statements": ["P280: Wear protective gloves and eye protection.", "P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes."]
    },
    {
        "id": "04_FA_0.1pct",
        "group": "Group 1: Aqueous Acid Buffers (TFA / FA)",
        "title": "FA, 0.1%",
        "subtitle": "0.1% (v/v) Formic Acid in Water",
        "cas": "CAS: 64-18-6 (Formic Acid) | 7732-18-5 (H₂O)",
        "composition": "0.1% Formic acid, 99.9% Ultrapure Water (pH ~ 2.7)",
        "reg_pictograms": [],
        "reg_signal": "NO SIGNAL WORD",
        "reg_h_statements": ["Not a hazardous substance or mixture according to GHS / CLP (< 2% SCL for Formic Acid)."],
        "reg_p_statements": ["Handle in accordance with good industrial hygiene and laboratory safety practice.", "P280: Wear standard eye protection and nitrile gloves."],
        "reg_note": "Well below 2% CLP SCL cutoff. Non-hazardous aqueous LC-MS mobile phase A.",
        "ehs_pictograms": ["GHS07"],
        "ehs_signal": "WARNING",
        "ehs_h_statements": ["Precautionary Lab EHS Label: Contains 0.1% Formic Acid (dilute acidic buffer, pH ~ 2.7)."],
        "ehs_p_statements": ["P280: Wear protective gloves and eye protection.", "P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes."]
    },
    {
        "id": "05_1pct_TFA_80pct_ACN",
        "group": "Group 2: 80% Acetonitrile (ACN) + Acid Buffers",
        "title": "1% TFA, 80% ACN",
        "subtitle": "1% TFA, 80% Acetonitrile in Water",
        "cas": "CAS: 75-05-8 (ACN) | 76-05-1 (TFA) | 7732-18-5 (H₂O)",
        "composition": "80% Acetonitrile, 1% Trifluoroacetic acid, 19% Water",
        "reg_pictograms": ["GHS02", "GHS07"],
        "reg_signal": "DANGER",
        "reg_h_statements": ["H225: Highly flammable liquid and vapour.", "H302+H312+H332: Harmful if swallowed, in contact with skin, or if inhaled.", "H315: Causes skin irritation (1% TFA). H319: Causes serious eye irritation."],
        "reg_p_statements": ["P210: Keep away from heat, hot surfaces, sparks, open flames. No smoking.", "P280: Wear protective gloves, protective clothing, eye/face protection.", "P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes."],
        "reg_note": "Classified by 80% ACN (Flam. Liq. 2, Acute Tox. 4, Eye Irrit. 2) + 1% TFA (Skin Irrit. 2).",
        "ehs_pictograms": ["GHS02", "GHS05", "GHS07"],
        "ehs_signal": "DANGER",
        "ehs_h_statements": ["H225: Highly flammable liquid and vapour.", "H302+H312+H332: Harmful if swallowed, in contact with skin, or if inhaled.", "H314: Causes severe skin burns and eye damage (1% TFA conservative EHS)."],
        "ehs_p_statements": ["P210: Keep away from heat, sparks, open flames. No smoking.", "P260: Do not breathe vapours. P280: Wear gloves, lab coat, eye protection.", "P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes."]
    },
    {
        "id": "06_0.1pct_TFA_80pct_ACN",
        "group": "Group 2: 80% Acetonitrile (ACN) + Acid Buffers",
        "title": "0.1% TFA, 80% ACN",
        "subtitle": "0.1% TFA, 80% Acetonitrile in Water",
        "cas": "CAS: 75-05-8 (ACN) | 76-05-1 (TFA) | 7732-18-5 (H₂O)",
        "composition": "80% Acetonitrile, 0.1% Trifluoroacetic acid, 19.9% Water",
        "reg_pictograms": ["GHS02", "GHS07"],
        "reg_signal": "DANGER",
        "reg_h_statements": ["H225: Highly flammable liquid and vapour.", "H302+H312+H332: Harmful if swallowed, in contact with skin, or if inhaled.", "H319: Causes serious eye irritation."],
        "reg_p_statements": ["P210: Keep away from heat, hot surfaces, sparks, open flames. No smoking.", "P261: Avoid breathing vapours. P280: Wear protective gloves and eye protection.", "P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes."],
        "reg_note": "Hazards governed by 80% Acetonitrile (GHS02 + GHS07, Danger).",
        "ehs_pictograms": ["GHS02", "GHS07"],
        "ehs_signal": "DANGER",
        "ehs_h_statements": ["H225: Highly flammable liquid and vapour.", "H302+H312+H332: Harmful if swallowed, in contact with skin, or if inhaled.", "H319: Causes serious eye irritation (contains 0.1% TFA acid modifier)."],
        "ehs_p_statements": ["P210: Keep away from heat, hot surfaces, sparks, open flames. No smoking.", "P261: Avoid breathing vapours. P280: Wear protective gloves and eye protection.", "P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes."]
    },
    {
        "id": "07_1pct_FA_80pct_ACN",
        "group": "Group 2: 80% Acetonitrile (ACN) + Acid Buffers",
        "title": "1% FA, 80% ACN",
        "subtitle": "1% Formic Acid, 80% Acetonitrile in Water",
        "cas": "CAS: 75-05-8 (ACN) | 64-18-6 (FA) | 7732-18-5 (H₂O)",
        "composition": "80% Acetonitrile, 1% Formic acid, 19% Water",
        "reg_pictograms": ["GHS02", "GHS07"],
        "reg_signal": "DANGER",
        "reg_h_statements": ["H225: Highly flammable liquid and vapour.", "H302+H312+H332: Harmful if swallowed, in contact with skin, or if inhaled.", "H319: Causes serious eye irritation."],
        "reg_p_statements": ["P210: Keep away from heat, hot surfaces, sparks, open flames. No smoking.", "P261: Avoid breathing vapours. P280: Wear protective gloves and eye protection.", "P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes."],
        "reg_note": "Hazards governed by 80% Acetonitrile (GHS02 + GHS07, Danger).",
        "ehs_pictograms": ["GHS02", "GHS07"],
        "ehs_signal": "DANGER",
        "ehs_h_statements": ["H225: Highly flammable liquid and vapour.", "H302+H312+H332: Harmful if swallowed, in contact with skin, or if inhaled.", "H315/H319: Causes serious eye and mild skin irritation (contains 1% Formic Acid)."],
        "ehs_p_statements": ["P210: Keep away from heat, hot surfaces, sparks, open flames. No smoking.", "P261: Avoid breathing vapours. P280: Wear protective gloves and eye protection.", "P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes."]
    },
    {
        "id": "08_0.1pct_FA_80pct_ACN",
        "group": "Group 2: 80% Acetonitrile (ACN) + Acid Buffers",
        "title": "0.1% FA, 80% ACN",
        "subtitle": "0.1% Formic Acid, 80% Acetonitrile in Water",
        "cas": "CAS: 75-05-8 (ACN) | 64-18-6 (FA) | 7732-18-5 (H₂O)",
        "composition": "80% Acetonitrile, 0.1% Formic acid, 19.9% Water",
        "reg_pictograms": ["GHS02", "GHS07"],
        "reg_signal": "DANGER",
        "reg_h_statements": ["H225: Highly flammable liquid and vapour.", "H302+H312+H332: Harmful if swallowed, in contact with skin, or if inhaled.", "H319: Causes serious eye irritation."],
        "reg_p_statements": ["P210: Keep away from heat, hot surfaces, sparks, open flames. No smoking.", "P261: Avoid breathing vapours. P280: Wear protective gloves and eye protection.", "P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes."],
        "reg_note": "Corrected '80% CAN' typo to '80% ACN'. Governed by 80% Acetonitrile (GHS02 + GHS07).",
        "ehs_pictograms": ["GHS02", "GHS07"],
        "ehs_signal": "DANGER",
        "ehs_h_statements": ["H225: Highly flammable liquid and vapour.", "H302+H312+H332: Harmful if swallowed, in contact with skin, or if inhaled.", "H319: Causes serious eye irritation (contains 0.1% Formic Acid)."],
        "ehs_p_statements": ["P210: Keep away from heat, hot surfaces, sparks, open flames. No smoking.", "P261: Avoid breathing vapours. P280: Wear protective gloves and eye protection.", "P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes."]
    },
    {
        "id": "09_10pct_DMSO_1pct_TFA",
        "group": "Group 3: 10% DMSO + Acid Buffers",
        "title": "10% DMSO + 1% TFA",
        "subtitle": "10% Dimethyl Sulfoxide, 1% TFA in Water",
        "cas": "CAS: 67-68-5 (DMSO) | 76-05-1 (TFA) | 7732-18-5 (H₂O)",
        "composition": "10% DMSO, 1% Trifluoroacetic acid, 89% Water",
        "reg_pictograms": ["GHS07"],
        "reg_signal": "WARNING",
        "reg_h_statements": ["H315: Causes skin irritation (1% TFA ≥ 1% CLP GCL).", "H319: Causes serious eye irritation.", "Advisory: Contains 10% DMSO — accelerates skin absorption of dissolved solutes."],
        "reg_p_statements": ["P264: Wash skin thoroughly after handling.", "P280: Wear chemical-resistant gloves (butyl/nitrile) and eye protection.", "P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes."],
        "reg_note": "DMSO is not GHS-classified; 1% TFA triggers Skin/Eye Irrit. 2 (GHS07).",
        "ehs_pictograms": ["GHS05", "GHS07"],
        "ehs_signal": "DANGER",
        "ehs_h_statements": ["H314: Causes severe skin burns and eye damage (1% TFA extreme pH ≤ 2).", "Advisory: Contains 10% DMSO — enhances dermal penetration of acid/solutes."],
        "ehs_p_statements": ["P260: Do not breathe mist/vapours. P280: Wear gloves, lab coat, eye protection.", "P303+P361+P353: IF ON SKIN: Take off contaminated clothing. Rinse skin with water."]
    },
    {
        "id": "10_10pct_DMSO_0.1pct_TFA",
        "group": "Group 3: 10% DMSO + Acid Buffers",
        "title": "10% DMSO + 0.1% TFA",
        "subtitle": "10% Dimethyl Sulfoxide, 0.1% TFA in Water",
        "cas": "CAS: 67-68-5 (DMSO) | 76-05-1 (TFA) | 7732-18-5 (H₂O)",
        "composition": "10% DMSO, 0.1% Trifluoroacetic acid, 89.9% Water",
        "reg_pictograms": [],
        "reg_signal": "NO SIGNAL WORD",
        "reg_h_statements": ["Not a hazardous mixture according to GHS / CLP (DMSO not classified; TFA < 1% GCL).", "Advisory: Contains 10% DMSO (facilitates skin penetration) and dilute acid (pH ~ 2.0)."],
        "reg_p_statements": ["P280: Wear protective gloves and safety glasses.", "Avoid skin and eye contact; wash hands thoroughly after handling."],
        "reg_note": "Below GHS concentration cutoffs. Switch to Lab EHS Mode if precautionary GHS07 is desired.",
        "ehs_pictograms": ["GHS07"],
        "ehs_signal": "WARNING",
        "ehs_h_statements": ["H315/H319 (Precautionary EHS): Acidic DMSO buffer (pH ~ 2.0); may irritate eyes and skin.", "Advisory: 10% DMSO promotes dermal absorption."],
        "ehs_p_statements": ["P280: Wear protective gloves and eye protection.", "P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes."]
    },
    {
        "id": "11_10pct_DMSO_1pct_FA",
        "group": "Group 3: 10% DMSO + Acid Buffers",
        "title": "10% DMSO + 1% FA",
        "subtitle": "10% Dimethyl Sulfoxide, 1% Formic Acid in Water",
        "cas": "CAS: 67-68-5 (DMSO) | 64-18-6 (FA) | 7732-18-5 (H₂O)",
        "composition": "10% DMSO, 1% Formic acid, 89% Water",
        "reg_pictograms": [],
        "reg_signal": "NO SIGNAL WORD",
        "reg_h_statements": ["Not a hazardous mixture according to GHS / CLP (DMSO not classified; FA < 2% SCL).", "Advisory: Contains 10% DMSO (enhances skin absorption) and 1% Formic Acid (pH ~ 2.2)."],
        "reg_p_statements": ["P280: Wear protective gloves and safety glasses.", "Avoid contact with skin and eyes; rinse immediately with water if contact occurs."],
        "reg_note": "1% Formic Acid is below the 2% CLP Annex VI SCL; DMSO is non-classified under GHS.",
        "ehs_pictograms": ["GHS07"],
        "ehs_signal": "WARNING",
        "ehs_h_statements": ["H315/H319 (Precautionary EHS): Contains 1% Formic Acid + 10% DMSO; may irritate eyes/skin.", "Advisory: 10% DMSO promotes dermal penetration."],
        "ehs_p_statements": ["P280: Wear protective gloves and eye protection.", "P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes."]
    },
    {
        "id": "12_10pct_DMSO_0.1pct_FA",
        "group": "Group 3: 10% DMSO + Acid Buffers",
        "title": "10% DMSO + 0.1% FA",
        "subtitle": "10% Dimethyl Sulfoxide, 0.1% Formic Acid in Water",
        "cas": "CAS: 67-68-5 (DMSO) | 64-18-6 (FA) | 7732-18-5 (H₂O)",
        "composition": "10% DMSO, 0.1% Formic acid, 89.9% Water",
        "reg_pictograms": [],
        "reg_signal": "NO SIGNAL WORD",
        "reg_h_statements": ["Not a hazardous mixture according to GHS / CLP (DMSO not classified; FA < 2% SCL).", "Advisory: Contains 10% DMSO (facilitates skin absorption) and 0.1% Formic Acid."],
        "reg_p_statements": ["P280: Wear standard laboratory gloves and eye protection.", "Wash skin after contact."],
        "reg_note": "Included for the 4th DMSO buffer slot (0.1% FA counterpart to 1% FA).",
        "ehs_pictograms": ["GHS07"],
        "ehs_signal": "WARNING",
        "ehs_h_statements": ["Precautionary Lab EHS Label: Contains 10% DMSO + 0.1% Formic Acid (pH ~ 2.7).", "Advisory: 10% DMSO can carry dissolved compounds across skin."],
        "ehs_p_statements": ["P280: Wear protective gloves and eye protection.", "P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes."]
    },
    {
        "id": "13_100pct_ACN",
        "group": "Group 4: Pure Solvents & Reagents",
        "title": "100% ACN",
        "subtitle": "Acetonitrile (100%, Anhydrous / HPLC-MS Grade)",
        "cas": "CAS: 75-05-8 | EC: 200-835-2 | Formula: CH₃CN",
        "composition": "100% Acetonitrile (Methyl cyanide), MW 41.05 g/mol",
        "reg_pictograms": ["GHS02", "GHS07"],
        "reg_signal": "DANGER",
        "reg_h_statements": ["H225: Highly flammable liquid and vapour.", "H302+H312+H332: Harmful if swallowed, in contact with skin, or if inhaled.", "H319: Causes serious eye irritation."],
        "reg_p_statements": ["P210: Keep away from heat, hot surfaces, sparks, open flames. No smoking.", "P280: Wear protective gloves, protective clothing, eye/face protection.", "P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes.", "P403+P233: Store in a well-ventilated place. Keep container tightly closed."],
        "reg_note": "Harmonised CLP Annex VI classification (Index 608-001-00-3).",
        "ehs_pictograms": ["GHS02", "GHS07"],
        "ehs_signal": "DANGER",
        "ehs_h_statements": ["H225: Highly flammable liquid and vapour.", "H302+H312+H332: Harmful if swallowed, in contact with skin, or if inhaled.", "H319: Causes serious eye irritation."],
        "ehs_p_statements": ["P210: Keep away from heat, hot surfaces, sparks, open flames. No smoking.", "P280: Wear protective gloves, protective clothing, eye/face protection.", "P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes.", "P403+P233: Store in a well-ventilated place. Keep container tightly closed."]
    },
    {
        "id": "14_Acetonitrile",
        "group": "Group 4: Pure Solvents & Reagents",
        "title": "Acetonitrile",
        "subtitle": "Pure Acetonitrile (CH₃CN, 100%)",
        "cas": "CAS: 75-05-8 | EC: 200-835-2 | Index: 608-001-00-3",
        "composition": "Acetonitrile (100%), MW 41.05 g/mol",
        "reg_pictograms": ["GHS02", "GHS07"],
        "reg_signal": "DANGER",
        "reg_h_statements": ["H225: Highly flammable liquid and vapour.", "H302+H312+H332: Harmful if swallowed, in contact with skin, or if inhaled.", "H319: Causes serious eye irritation."],
        "reg_p_statements": ["P210: Keep away from heat, hot surfaces, sparks, open flames. No smoking.", "P280: Wear protective gloves, protective clothing, eye/face protection.", "P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes.", "P403+P233: Store in a well-ventilated place. Keep container tightly closed."],
        "reg_note": "Harmonised CLP Annex VI classification (Index 608-001-00-3).",
        "ehs_pictograms": ["GHS02", "GHS07"],
        "ehs_signal": "DANGER",
        "ehs_h_statements": ["H225: Highly flammable liquid and vapour.", "H302+H312+H332: Harmful if swallowed, in contact with skin, or if inhaled.", "H319: Causes serious eye irritation."],
        "ehs_p_statements": ["P210: Keep away from heat, hot surfaces, sparks, open flames. No smoking.", "P280: Wear protective gloves, protective clothing, eye/face protection.", "P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes.", "P403+P233: Store in a well-ventilated place. Keep container tightly closed."]
    },
    {
        "id": "15_Ethanol",
        "group": "Group 4: Pure Solvents & Reagents",
        "title": "Ethanol",
        "subtitle": "Ethyl Alcohol (C₂H₅OH, ≥ 96–100%)",
        "cas": "CAS: 64-17-5 | EC: 200-578-6 | Index: 603-002-00-5",
        "composition": "Ethanol (Ethyl alcohol), MW 46.07 g/mol",
        "reg_pictograms": ["GHS02", "GHS07"],
        "reg_signal": "DANGER",
        "reg_h_statements": ["H225: Highly flammable liquid and vapour.", "H319: Causes serious eye irritation (CLP SCL ≥ 50%)."],
        "reg_p_statements": ["P210: Keep away from heat, hot surfaces, sparks, open flames. No smoking.", "P233: Keep container tightly closed. P280: Wear eye protection and gloves.", "P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes.", "P403+P235: Store in a well-ventilated place. Keep cool."],
        "reg_note": "Flam. Liq. 2 (H225, GHS02) + Eye Irrit. 2 (H319, GHS07 at ≥ 50%).",
        "ehs_pictograms": ["GHS02", "GHS07"],
        "ehs_signal": "DANGER",
        "ehs_h_statements": ["H225: Highly flammable liquid and vapour.", "H319: Causes serious eye irritation."],
        "ehs_p_statements": ["P210: Keep away from heat, hot surfaces, sparks, open flames. No smoking.", "P233: Keep container tightly closed. P280: Wear eye protection and gloves.", "P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes.", "P403+P235: Store in a well-ventilated place. Keep cool."]
    },
    {
        "id": "16_Methanol",
        "group": "Group 4: Pure Solvents & Reagents",
        "title": "Methanol",
        "subtitle": "Methyl Alcohol (CH₃OH, 100%)",
        "cas": "CAS: 67-56-1 | EC: 200-659-6 | Index: 603-001-00-X",
        "composition": "Methanol (Methyl alcohol), MW 32.04 g/mol",
        "reg_pictograms": ["GHS02", "GHS06", "GHS08"],
        "reg_signal": "DANGER",
        "reg_h_statements": ["H225: Highly flammable liquid and vapour.", "H301+H311+H331: Toxic if swallowed, in contact with skin, or if inhaled.", "H370: Causes damage to organs (eyes / optic nerve, central nervous system)."],
        "reg_p_statements": ["P210: Keep away from heat, sparks, open flames. No smoking.", "P260: Do not breathe vapours. P280: Wear protective gloves, clothing, eye protection.", "P301+P310: IF SWALLOWED: Immediately call a POISON CENTER or doctor.", "P308+P311: IF exposed or concerned: Call a POISON CENTER or doctor."],
        "reg_note": "Harmonised CLP Annex VI: Flam. Liq. 2 (GHS02), Acute Tox. 3 (GHS06), STOT SE 1 (GHS08).",
        "ehs_pictograms": ["GHS02", "GHS06", "GHS08"],
        "ehs_signal": "DANGER",
        "ehs_h_statements": ["H225: Highly flammable liquid and vapour.", "H301+H311+H331: Toxic if swallowed, in contact with skin, or if inhaled.", "H370: Causes damage to organs (eyes / optic nerve, central nervous system)."],
        "ehs_p_statements": ["P210: Keep away from heat, sparks, open flames. No smoking.", "P260: Do not breathe vapours. P280: Wear protective gloves, clothing, eye protection.", "P301+P310: IF SWALLOWED: Immediately call a POISON CENTER or doctor.", "P308+P311: IF exposed or concerned: Call a POISON CENTER or doctor."]
    },
    {
        "id": "17_Isopropanol",
        "group": "Group 4: Pure Solvents & Reagents",
        "title": "Isopropanol",
        "subtitle": "2-Propanol / Isopropyl Alcohol (C₃H₈O)",
        "cas": "CAS: 67-63-0 | EC: 200-661-7 | Index: 603-117-00-0",
        "composition": "Isopropanol (2-Propanol / IPA), MW 60.10 g/mol",
        "reg_pictograms": ["GHS02", "GHS07"],
        "reg_signal": "DANGER",
        "reg_h_statements": ["H225: Highly flammable liquid and vapour.", "H319: Causes serious eye irritation.", "H336: May cause drowsiness or dizziness."],
        "reg_p_statements": ["P210: Keep away from heat, hot surfaces, sparks, open flames. No smoking.", "P261: Avoid breathing vapours. P280: Wear protective gloves and eye protection.", "P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes.", "P403+P233: Store in a well-ventilated place. Keep container tightly closed."],
        "reg_note": "Harmonised CLP Annex VI: Flam. Liq. 2 (GHS02), Eye Irrit. 2 & STOT SE 3 (GHS07).",
        "ehs_pictograms": ["GHS02", "GHS07"],
        "ehs_signal": "DANGER",
        "ehs_h_statements": ["H225: Highly flammable liquid and vapour.", "H319: Causes serious eye irritation.", "H336: May cause drowsiness or dizziness."],
        "ehs_p_statements": ["P210: Keep away from heat, hot surfaces, sparks, open flames. No smoking.", "P261: Avoid breathing vapours. P280: Wear protective gloves and eye protection.", "P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes.", "P403+P233: Store in a well-ventilated place. Keep container tightly closed."]
    },
    {
        "id": "18_Cellulose",
        "group": "Group 4: Pure Solvents & Reagents",
        "title": "Cellulose",
        "subtitle": "Microcrystalline / Powder Cellulose ((C₆H₁₀O₅)ₙ)",
        "cas": "CAS: 9004-34-6 | EC: 232-674-9",
        "composition": "Cellulose, 100% Solid / Powder",
        "reg_pictograms": [],
        "reg_signal": "NON-HAZARDOUS",
        "reg_h_statements": ["Not a hazardous substance or mixture according to Regulation (EC) No 1272/2008 (CLP) / GHS.", "Advisory: May form combustible dust concentrations in air if dispersed as fine powder."],
        "reg_p_statements": ["Avoid breathing dust. Minimize dust generation and accumulation.", "Store tightly closed in a dry, well-ventilated area."],
        "reg_note": "Exempt from GHS hazard pictograms.",
        "ehs_pictograms": [],
        "ehs_signal": "NON-HAZARDOUS",
        "ehs_h_statements": ["Not a hazardous substance or mixture according to Regulation (EC) No 1272/2008 (CLP) / GHS.", "Advisory: Avoid creating airborne dust; use dust mask if handling large quantities."],
        "ehs_p_statements": ["Avoid breathing dust. Minimize dust generation and accumulation.", "Store tightly closed in a dry, well-ventilated area."]
    }
]


def xml_escape(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def wrap_text(text: str, max_chars: int = 58) -> list:
    words = text.split()
    lines, cur, cur_len = [], [], 0
    for w in words:
        if cur_len + len(w) + (1 if cur else 0) <= max_chars:
            cur.append(w)
            cur_len += len(w) + (1 if len(cur) > 1 else 0)
        else:
            lines.append(" ".join(cur))
            cur, cur_len = [w], len(w)
    if cur:
        lines.append(" ".join(cur))
    return lines


def generate_minimal_label_svg(item: dict, mode: str = "reg", width_mm: float = 80.0, height_mm: float = 45.0) -> str:
    """
    Generates a clean, Minimal GHS SVG label (NO Hazard/Precautionary statements):
    Contains Title, Subtitle/Composition, Signal Word, GHS Diamond Pictogram(s),
    and 3 clean fields: DATE PREPARED, PREPARED BY, NOTES.
    """
    pictos = item["reg_pictograms"] if mode == "reg" else item["ehs_pictograms"]
    signal = item["reg_signal"] if mode == "reg" else item["ehs_signal"]

    if signal == "DANGER":
        sig_bg = "#d90000"
    elif "WARNING" in signal:
        sig_bg = "#d97706"
    else:
        sig_bg = "#16a34a"

    picto_parts = []
    # Left Pictogram Zone in 480x270 viewBox: x=12..218, y=76..256 (width=206, height=180)
    if len(pictos) == 1:
        picto_parts.append(render_ghs_diamond_svg(pictos[0], 56, 86, 118))
        picto_parts.append(
            f'<text x="115" y="224" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="11" font-weight="bold" fill="#334155">{xml_escape(GHS_SYMBOLS_INNER[pictos[0]]["name"])}</text>'
        )
    elif len(pictos) == 2:
        picto_parts.append(render_ghs_diamond_svg(pictos[0], 18, 96, 94))
        picto_parts.append(render_ghs_diamond_svg(pictos[1], 116, 96, 94))
        picto_parts.append(
            f'<text x="115" y="216" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="11" font-weight="bold" fill="#334155">{" + ".join(pictos)}</text>'
        )
    elif len(pictos) >= 3:
        picto_parts.append(render_ghs_diamond_svg(pictos[0], 74, 80, 82))
        picto_parts.append(render_ghs_diamond_svg(pictos[1], 24, 142, 82))
        picto_parts.append(render_ghs_diamond_svg(pictos[2], 124, 142, 82))
        picto_parts.append(
            f'<text x="115" y="242" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="10.5" font-weight="bold" fill="#334155">{" + ".join(pictos[:3])}</text>'
        )
    else:
        picto_parts.append("""
        <rect x="34" y="112" width="162" height="92" rx="10" fill="#f0fdf4" stroke="#16a34a" stroke-width="2" stroke-dasharray="5,3"/>
        <circle cx="115" cy="142" r="16" fill="#16a34a"/>
        <path d="M108 142 L113.5 147.5 L123 137" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
        <text x="115" y="176" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="11.5" font-weight="bold" fill="#15803d">NO GHS PICTOGRAM</text>
        <text x="115" y="191" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="9.5" fill="#166534">Below CLP Cutoff / Non-Haz</text>
        """)

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 270" width="{width_mm}mm" height="{height_mm}mm">
  <!-- Outer Card & Border -->
  <rect x="2" y="2" width="476" height="266" rx="10" fill="#ffffff" stroke="#0f172a" stroke-width="2.5"/>
  <!-- Top Signal Color Bar -->
  <path d="M 12 3.5 L 468 3.5 C 473 3.5 476.5 7 476.5 12 L 476.5 13 L 3.5 13 L 3.5 12 C 3.5 7 7 3.5 12 3.5 Z" fill="{sig_bg}"/>

  <!-- Header Section -->
  <text x="16" y="40" font-family="Arial, Helvetica, sans-serif" font-size="23" font-weight="900" fill="#0f172a">{xml_escape(item["title"])}</text>
  <text x="16" y="58" font-family="Arial, Helvetica, sans-serif" font-size="11" font-weight="bold" fill="#334155">{xml_escape(item["subtitle"])}</text>

  <!-- Signal Word Banner (Top Right) -->
  <rect x="332" y="20" width="134" height="32" rx="6" fill="{sig_bg}"/>
  <text x="399" y="41" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="13.5" font-weight="900" letter-spacing="0.8" fill="#ffffff">{xml_escape(signal)}</text>

  <!-- Divider -->
  <line x1="12" y1="70" x2="468" y2="70" stroke="#cbd5e1" stroke-width="1.5"/>

  <!-- Left Pictogram Zone -->
  <rect x="12" y="78" width="206" height="178" rx="8" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1.2"/>
  {''.join(picto_parts)}

  <!-- Right Simple Metadata Fields: DATE PREPARED, PREPARED BY, NOTES -->
  <rect x="228" y="78" width="238" height="53" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.2"/>
  <text x="238" y="94" font-family="Arial, Helvetica, sans-serif" font-size="9.5" font-weight="800" fill="#475569">DATE PREPARED:</text>
  <line x1="238" y1="121" x2="454" y2="121" stroke="#cbd5e1" stroke-width="1.2"/>

  <rect x="228" y="140" width="238" height="53" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.2"/>
  <text x="238" y="156" font-family="Arial, Helvetica, sans-serif" font-size="9.5" font-weight="800" fill="#475569">PREPARED BY:</text>
  <line x1="238" y1="183" x2="454" y2="183" stroke="#cbd5e1" stroke-width="1.2"/>

  <rect x="228" y="203" width="238" height="53" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.2"/>
  <text x="238" y="219" font-family="Arial, Helvetica, sans-serif" font-size="9.5" font-weight="800" fill="#475569">NOTES:</text>
  <line x1="238" y1="246" x2="454" y2="246" stroke="#cbd5e1" stroke-width="1.2"/>
</svg>""".strip()


def generate_full_label_svg(item: dict, mode: str = "reg", width_mm: float = 100.0, height_mm: float = 60.0) -> str:
    pictos = item["reg_pictograms"] if mode == "reg" else item["ehs_pictograms"]
    signal = item["reg_signal"] if mode == "reg" else item["ehs_signal"]
    h_stmts = item["reg_h_statements"] if mode == "reg" else item["ehs_h_statements"]
    p_stmts = item["reg_p_statements"] if mode == "reg" else item["ehs_p_statements"]

    if signal == "DANGER":
        sig_bg = "#d90000"
    elif "WARNING" in signal:
        sig_bg = "#d97706"
    else:
        sig_bg = "#16a34a"

    picto_svg_parts = []
    if len(pictos) == 1:
        picto_svg_parts.append(render_ghs_diamond_svg(pictos[0], 30, 108, 96))
        picto_svg_parts.append(f'<text x="78" y="218" text-anchor="middle" font-family="Arial, sans-serif" font-size="9.5" font-weight="bold" fill="#374151">{GHS_SYMBOLS_INNER[pictos[0]]["name"]}</text>')
    elif len(pictos) == 2:
        picto_svg_parts.append(render_ghs_diamond_svg(pictos[0], 8, 114, 72))
        picto_svg_parts.append(render_ghs_diamond_svg(pictos[1], 76, 114, 72))
        picto_svg_parts.append(f'<text x="78" y="206" text-anchor="middle" font-family="Arial, sans-serif" font-size="9.5" font-weight="bold" fill="#374151">{" + ".join(pictos)}</text>')
    elif len(pictos) == 3:
        picto_svg_parts.append(render_ghs_diamond_svg(pictos[0], 45, 88, 66))
        picto_svg_parts.append(render_ghs_diamond_svg(pictos[1], 11, 142, 66))
        picto_svg_parts.append(render_ghs_diamond_svg(pictos[2], 79, 142, 66))
        picto_svg_parts.append(f'<text x="78" y="220" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" font-weight="bold" fill="#374151">{" + ".join(pictos)}</text>')
    else:
        picto_svg_parts.append("""
        <rect x="20" y="115" width="116" height="72" rx="8" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.8" stroke-dasharray="4,3"/>
        <circle cx="78" cy="140" r="13" fill="#16a34a"/>
        <path d="M72 140 L76.5 144.5 L85 135.5" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>
        <text x="78" y="166" text-anchor="middle" font-family="Arial, sans-serif" font-size="9.5" font-weight="bold" fill="#15803d">NO GHS PICTOGRAM</text>
        <text x="78" y="178" text-anchor="middle" font-family="Arial, sans-serif" font-size="8.2" fill="#166534">Below CLP Cutoff / Non-Haz</text>
        """)

    text_elements = []
    y_cursor = 96
    text_elements.append(f'<text x="166" y="{y_cursor}" font-family="Arial, sans-serif" font-size="9.5" font-weight="bold" fill="#991b1b">HAZARD STATEMENTS:</text>')
    y_cursor += 12
    for stmt in h_stmts:
        for line in wrap_text(stmt, 58):
            if y_cursor < 178:
                text_elements.append(f'<text x="166" y="{y_cursor}" font-family="Arial, sans-serif" font-size="8.8" fill="#111827">{xml_escape(line)}</text>')
                y_cursor += 11.2
    y_cursor = max(y_cursor + 4, 174)
    text_elements.append(f'<text x="166" y="{y_cursor}" font-family="Arial, sans-serif" font-size="9.5" font-weight="bold" fill="#1e40af">PRECAUTIONARY STATEMENTS:</text>')
    y_cursor += 12
    for stmt in p_stmts:
        for line in wrap_text(stmt, 58):
            if y_cursor < 252:
                text_elements.append(f'<text x="166" y="{y_cursor}" font-family="Arial, sans-serif" font-size="8.6" fill="#1f2937">{xml_escape(line)}</text>')
                y_cursor += 11.0

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 330" width="{width_mm}mm" height="{height_mm}mm">
  <rect x="2" y="2" width="516" height="326" rx="10" fill="#ffffff" stroke="#111827" stroke-width="2.5"/>
  <path d="M 12 3.5 L 508 3.5 C 513 3.5 516.5 7 516.5 12 L 516.5 13 L 3.5 13 L 3.5 12 C 3.5 7 7 3.5 12 3.5 Z" fill="{sig_bg}"/>
  <text x="16" y="37" font-family="Arial, sans-serif" font-size="21" font-weight="900" fill="#0f172a">{xml_escape(item["title"])}</text>
  <text x="16" y="53" font-family="Arial, sans-serif" font-size="10.5" font-weight="bold" fill="#334155">{xml_escape(item["subtitle"])}</text>
  <text x="16" y="66" font-family="Arial, sans-serif" font-size="8.8" fill="#64748b">{xml_escape(item["cas"])}  •  {xml_escape(item["composition"])}</text>
  <rect x="374" y="19" width="132" height="28" rx="5" fill="{sig_bg}"/>
  <text x="440" y="37" text-anchor="middle" font-family="Arial, sans-serif" font-size="13" font-weight="900" letter-spacing="0.8" fill="#ffffff">{xml_escape(signal)}</text>
  <line x1="12" y1="74" x2="508" y2="74" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="10" y="80" width="144" height="170" rx="6" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1"/>
  {''.join(picto_svg_parts)}
  {''.join(text_elements)}
  <line x1="12" y1="256" x2="508" y2="256" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="12" y="263" width="158" height="53" rx="4" fill="#f8fafc" stroke="#94a3b8" stroke-width="1"/>
  <text x="18" y="276" font-family="Arial, sans-serif" font-size="8" font-weight="bold" fill="#475569">DATE PREPARED:</text>
  <line x1="18" y1="304" x2="160" y2="304" stroke="#cbd5e1" stroke-width="1"/>
  <rect x="178" y="263" width="158" height="53" rx="4" fill="#f8fafc" stroke="#94a3b8" stroke-width="1"/>
  <text x="184" y="276" font-family="Arial, sans-serif" font-size="8" font-weight="bold" fill="#475569">PREPARED BY:</text>
  <line x1="184" y1="304" x2="326" y2="304" stroke="#cbd5e1" stroke-width="1"/>
  <rect x="344" y="263" width="164" height="53" rx="4" fill="#f8fafc" stroke="#94a3b8" stroke-width="1"/>
  <text x="350" y="276" font-family="Arial, sans-serif" font-size="8" font-weight="bold" fill="#475569">NOTES:</text>
  <line x1="350" y1="304" x2="498" y2="304" stroke="#cbd5e1" stroke-width="1"/>
</svg>""".strip()


for item in LABELS_DATA:
    (SVG_MIN_REG_DIR / f"{item['id']}.svg").write_text(generate_minimal_label_svg(item, mode="reg"), encoding="utf-8")
    (SVG_MIN_EHS_DIR / f"{item['id']}.svg").write_text(generate_minimal_label_svg(item, mode="ehs"), encoding="utf-8")
    (SVG_REG_DIR / f"{item['id']}.svg").write_text(generate_full_label_svg(item, mode="reg"), encoding="utf-8")
    (SVG_EHS_DIR / f"{item['id']}.svg").write_text(generate_full_label_svg(item, mode="ehs"), encoding="utf-8")

print(f"Generated 18 Minimal SVG labels in {SVG_MIN_REG_DIR} and {SVG_MIN_EHS_DIR}")
print(f"Generated 18 Full SVG labels in {SVG_REG_DIR} and {SVG_EHS_DIR}")


labels_json_str = json.dumps(LABELS_DATA, ensure_ascii=False, indent=2)
symbols_json_str = json.dumps(GHS_SYMBOLS_INNER, ensure_ascii=False, indent=2)

HTML_STUDIO = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>GHS Buffer &amp; Solvent Labels — Minimal &amp; Full Print Studio</title>
  <style id="dynamicPrintStyle"></style>
  <style>
    :root {{
      --bg: #f1f5f9;
      --text: #0f172a;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      padding: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
    }}
    .toolbar {{
      position: sticky;
      top: 0;
      z-index: 50;
      background: #0f172a;
      color: #fff;
      padding: 14px 24px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }}
    .toolbar-top {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      max-width: 1320px;
      margin: 0 auto;
    }}
    .toolbar h1 {{ margin: 0; font-size: 18px; font-weight: 800; }}
    .toolbar p {{ margin: 2px 0 0; font-size: 12px; color: #94a3b8; }}
    .controls-bar {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px 14px;
      align-items: center;
      max-width: 1320px;
      margin: 12px auto 0;
      padding-top: 12px;
      border-top: 1px solid #334155;
      font-size: 12.5px;
    }}
    .control-group {{
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .control-group label {{ color: #cbd5e1; font-weight: 600; }}
    .control-group input, .control-group select {{
      background: #1e293b;
      color: #fff;
      border: 1px solid #475569;
      border-radius: 6px;
      padding: 5px 8px;
      font-size: 12.5px;
    }}
    .btn {{
      cursor: pointer;
      border: none;
      border-radius: 6px;
      padding: 8px 14px;
      font-size: 12.5px;
      font-weight: 700;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }}
    .btn-primary {{ background: #2563eb; color: #fff; }}
    .btn-primary:hover {{ background: #1d4ed8; }}
    .container {{
      max-width: 1320px;
      margin: 20px auto 48px;
      padding: 0 20px;
    }}
    .size-info-banner {{
      background: #fff;
      border-left: 4px solid #2563eb;
      border-radius: 8px;
      padding: 10px 16px;
      margin-bottom: 18px;
      font-size: 12.5px;
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 10px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }}
    .labels-grid {{
      display: flex;
      flex-wrap: wrap;
      gap: 16px;
    }}
    .label-wrapper {{
      background: #fff;
      border-radius: 10px;
      padding: 10px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.07);
      border: 1px solid #e2e8f0;
      display: flex;
      flex-direction: column;
      gap: 6px;
      width: calc(50% - 8px);
    }}
    .label-actions {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 11.5px;
      color: #64748b;
    }}
    .label-actions button {{
      cursor: pointer;
      background: #f1f5f9;
      border: 1px solid #cbd5e1;
      border-radius: 5px;
      padding: 3px 8px;
      font-size: 11px;
      font-weight: 600;
      color: #1e293b;
    }}
    .svg-holder svg {{
      width: 100%;
      height: auto;
      display: block;
    }}

    @media print {{
      body {{ background: #fff; }}
      .toolbar, .size-info-banner, .label-actions {{ display: none !important; }}
      .container {{ max-width: 100%; margin: 0; padding: 0; }}
      .labels-grid {{
        display: flex;
        flex-wrap: wrap;
        gap: 4mm;
      }}
      .label-wrapper {{
        box-shadow: none;
        border: none;
        padding: 0;
        page-break-inside: avoid;
        break-inside: avoid;
      }}
      .label-wrapper.hidden-print {{
        display: none !important;
      }}
    }}
  </style>
</head>
<body>
  <div class="toolbar">
    <div class="toolbar-top">
      <div>
        <h1>GHS Individual Buffer &amp; Solvent Label Studio (18 Labels)</h1>
        <p>Minimal &amp; Full Layouts • Exact Physical Millimeter / Inch Print Sizes</p>
      </div>
      <div>
        <button class="btn btn-primary" onclick="window.print()">🖨️ Print All at Selected Physical Size</button>
      </div>
    </div>
    <div class="controls-bar">
      <div class="control-group">
        <label for="layoutSelect">Label Style:</label>
        <select id="layoutSelect" onchange="renderAll()">
          <option value="minimal" selected>✨ Minimal (Pictogram + Date Prepared / Prepared By / Notes)</option>
          <option value="full">📋 Full Detailed (with Hazard &amp; Precautionary Statements)</option>
        </select>
      </div>
      <div class="control-group">
        <label for="sizePreset">Print Size:</label>
        <select id="sizePreset" onchange="onSizePresetChange()">
          <option value="100x60">Large Bottle: 100 × 60 mm (3.94" × 2.36") — 2/row</option>
          <option value="80x45" selected>Medium Bottle: 80 × 45 mm (3.15" × 1.77") — 2/row</option>
          <option value="60x35">Small Bottle / 50 mL Falcon: 60 × 35 mm (2.36" × 1.38") — 3/row</option>
          <option value="45x25">Mini 15 mL Tube / Vial: 45 × 25 mm (1.77" × 0.98") — 4/row</option>
          <option value="custom">Custom Dimensions (mm)...</option>
        </select>
      </div>
      <div class="control-group" id="customDimGroup" style="display:none;">
        <label>W×H (mm):</label>
        <input type="number" id="customW" value="80" min="20" max="200" style="width:58px;" oninput="renderAll()" />
        <span>×</span>
        <input type="number" id="customH" value="45" min="15" max="150" style="width:58px;" oninput="renderAll()" />
      </div>
      <div class="control-group">
        <label for="modeSelect">GHS Mode:</label>
        <select id="modeSelect" onchange="renderAll()">
          <option value="reg">CLP Regulatory Cutoffs</option>
          <option value="ehs">Conservative Lab EHS (All Dilute Acids Show Pictogram)</option>
        </select>
      </div>
      <div class="control-group">
        <label for="prepDate">Date Prepared:</label>
        <input type="text" id="prepDate" placeholder="e.g. 2026-11-26" oninput="renderAll()" style="width:105px;" />
      </div>
      <div class="control-group">
        <label for="prepBy">Prepared By:</label>
        <input type="text" id="prepBy" placeholder="Initials / Name" oninput="renderAll()" style="width:100px;" />
      </div>
      <div class="control-group">
        <label for="notesInput">Notes:</label>
        <input type="text" id="notesInput" placeholder="e.g. RT / Exp 6 mo" oninput="renderAll()" style="width:120px;" />
      </div>
    </div>
  </div>

  <div class="container">
    <div id="sizeBanner" class="size-info-banner"></div>
    <div id="labelsGrid" class="labels-grid"></div>
  </div>

  <script>
    const LABELS = {labels_json_str};
    const SYMBOLS = {symbols_json_str};

    function esc(s) {{
      return String(s || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
    }}

    function getPhysicalDims() {{
      const preset = document.getElementById('sizePreset').value;
      if (preset === 'custom') {{
        const w = parseFloat(document.getElementById('customW').value) || 80;
        const h = parseFloat(document.getElementById('customH').value) || 45;
        return {{ w, h }};
      }}
      const [w, h] = preset.split('x').map(Number);
      return {{ w, h }};
    }}

    function onSizePresetChange() {{
      const preset = document.getElementById('sizePreset').value;
      document.getElementById('customDimGroup').style.display = preset === 'custom' ? 'flex' : 'none';
      if (preset !== 'custom') {{
        const [w, h] = preset.split('x').map(Number);
        document.getElementById('customW').value = w;
        document.getElementById('customH').value = h;
      }}
      renderAll();
    }}

    function renderDiamond(code, x, y, size) {{
      const sym = SYMBOLS[code];
      return `<svg x="${{x.toFixed(1)}}" y="${{y.toFixed(1)}}" width="${{size.toFixed(1)}}" height="${{size.toFixed(1)}}" viewBox="${{sym.viewBox}}">${{sym.svg}}</svg>`;
    }}

    function wrapText(text, maxChars = 58) {{
      const words = String(text).split(/\\s+/);
      const lines = [];
      let cur = [], curLen = 0;
      for (const w of words) {{
        if (curLen + w.length + (cur.length ? 1 : 0) <= maxChars) {{ cur.push(w); curLen += w.length + (cur.length > 1 ? 1 : 0); }}
        else {{ lines.push(cur.join(' ')); cur = [w]; curLen = w.length; }}
      }}
      if (cur.length) lines.push(cur.join(' '));
      return lines;
    }}

    function buildMinimalSVG(item, mode, meta, dims) {{
      const pictos = mode === 'reg' ? item.reg_pictograms : item.ehs_pictograms;
      const signal = mode === 'reg' ? item.reg_signal : item.ehs_signal;
      let sigBg = '#16a34a';
      if (signal === 'DANGER') sigBg = '#d90000';
      else if (signal.includes('WARNING')) sigBg = '#d97706';

      let pictoParts = [];
      if (pictos.length === 1) {{
        pictoParts.push(renderDiamond(pictos[0], 56, 86, 118));
        pictoParts.push(`<text x="115" y="224" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#334155">${{esc(SYMBOLS[pictos[0]].name)}}</text>`);
      }} else if (pictos.length === 2) {{
        pictoParts.push(renderDiamond(pictos[0], 18, 96, 94));
        pictoParts.push(renderDiamond(pictos[1], 116, 96, 94));
        pictoParts.push(`<text x="115" y="216" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#334155">${{pictos.join(' + ')}}</text>`);
      }} else if (pictos.length >= 3) {{
        pictoParts.push(renderDiamond(pictos[0], 74, 80, 82));
        pictoParts.push(renderDiamond(pictos[1], 24, 142, 82));
        pictoParts.push(renderDiamond(pictos[2], 124, 142, 82));
        pictoParts.push(`<text x="115" y="242" text-anchor="middle" font-family="Arial, sans-serif" font-size="10.5" font-weight="bold" fill="#334155">${{pictos.slice(0,3).join(' + ')}}</text>`);
      }} else {{
        pictoParts.push(`
          <rect x="34" y="112" width="162" height="92" rx="10" fill="#f0fdf4" stroke="#16a34a" stroke-width="2" stroke-dasharray="5,3"/>
          <circle cx="115" cy="142" r="16" fill="#16a34a"/>
          <path d="M108 142 L113.5 147.5 L123 137" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
          <text x="115" y="176" text-anchor="middle" font-family="Arial, sans-serif" font-size="11.5" font-weight="bold" fill="#15803d">NO GHS PICTOGRAM</text>
          <text x="115" y="191" text-anchor="middle" font-family="Arial, sans-serif" font-size="9.5" fill="#166534">Below CLP Cutoff / Non-Haz</text>
        `);
      }}

      return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 270" width="${{dims.w}}mm" height="${{dims.h}}mm">
        <rect x="2" y="2" width="476" height="266" rx="10" fill="#ffffff" stroke="#0f172a" stroke-width="2.5"/>
        <path d="M 12 3.5 L 468 3.5 C 473 3.5 476.5 7 476.5 12 L 476.5 13 L 3.5 13 L 3.5 12 C 3.5 7 7 3.5 12 3.5 Z" fill="${{sigBg}}"/>
        <text x="16" y="40" font-family="Arial, sans-serif" font-size="23" font-weight="900" fill="#0f172a">${{esc(item.title)}}</text>
        <text x="16" y="58" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#334155">${{esc(item.subtitle)}}</text>

        <rect x="332" y="20" width="134" height="32" rx="6" fill="${{sigBg}}"/>
        <text x="399" y="41" text-anchor="middle" font-family="Arial, sans-serif" font-size="13.5" font-weight="900" letter-spacing="0.8" fill="#ffffff">${{esc(signal)}}</text>

        <line x1="12" y1="70" x2="468" y2="70" stroke="#cbd5e1" stroke-width="1.5"/>
        <rect x="12" y="78" width="206" height="178" rx="8" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1.2"/>
        ${{pictoParts.join('')}}

        <rect x="228" y="78" width="238" height="53" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.2"/>
        <text x="238" y="94" font-family="Arial, sans-serif" font-size="9.5" font-weight="800" fill="#475569">DATE PREPARED:</text>
        <text x="238" y="116" font-family="Arial, sans-serif" font-size="13" font-weight="bold" fill="#0f172a">${{esc(meta.prepDate)}}</text>
        <line x1="238" y1="121" x2="454" y2="121" stroke="#cbd5e1" stroke-width="1.2"/>

        <rect x="228" y="140" width="238" height="53" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.2"/>
        <text x="238" y="156" font-family="Arial, sans-serif" font-size="9.5" font-weight="800" fill="#475569">PREPARED BY:</text>
        <text x="238" y="178" font-family="Arial, sans-serif" font-size="13" font-weight="bold" fill="#0f172a">${{esc(meta.prepBy)}}</text>
        <line x1="238" y1="183" x2="454" y2="183" stroke="#cbd5e1" stroke-width="1.2"/>

        <rect x="228" y="203" width="238" height="53" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.2"/>
        <text x="238" y="219" font-family="Arial, sans-serif" font-size="9.5" font-weight="800" fill="#475569">NOTES:</text>
        <text x="238" y="241" font-family="Arial, sans-serif" font-size="13" font-weight="bold" fill="#0f172a">${{esc(meta.notes)}}</text>
        <line x1="238" y1="246" x2="454" y2="246" stroke="#cbd5e1" stroke-width="1.2"/>
      </svg>`;
    }}

    function buildFullSVG(item, mode, meta, dims) {{
      const pictos = mode === 'reg' ? item.reg_pictograms : item.ehs_pictograms;
      const signal = mode === 'reg' ? item.reg_signal : item.ehs_signal;
      const hStmts = mode === 'reg' ? item.reg_h_statements : item.ehs_h_statements;
      const pStmts = mode === 'reg' ? item.reg_p_statements : item.ehs_p_statements;

      let sigBg = '#16a34a';
      if (signal === 'DANGER') sigBg = '#d90000';
      else if (signal.includes('WARNING')) sigBg = '#d97706';

      let pictoParts = [];
      if (pictos.length === 1) {{
        pictoParts.push(renderDiamond(pictos[0], 30, 108, 96));
        pictoParts.push(`<text x="78" y="218" text-anchor="middle" font-family="Arial, sans-serif" font-size="9.5" font-weight="bold" fill="#374151">${{esc(SYMBOLS[pictos[0]].name)}}</text>`);
      }} else if (pictos.length === 2) {{
        pictoParts.push(renderDiamond(pictos[0], 8, 114, 72));
        pictoParts.push(renderDiamond(pictos[1], 76, 114, 72));
        pictoParts.push(`<text x="78" y="206" text-anchor="middle" font-family="Arial, sans-serif" font-size="9.5" font-weight="bold" fill="#374151">${{pictos.join(' + ')}}</text>`);
      }} else if (pictos.length === 3) {{
        pictoParts.push(renderDiamond(pictos[0], 45, 88, 66));
        pictoParts.push(renderDiamond(pictos[1], 11, 142, 66));
        pictoParts.push(renderDiamond(pictos[2], 79, 142, 66));
        pictoParts.push(`<text x="78" y="220" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" font-weight="bold" fill="#374151">${{pictos.join(' + ')}}</text>`);
      }} else {{
        pictoParts.push(`
          <rect x="20" y="115" width="116" height="72" rx="8" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.8" stroke-dasharray="4,3"/>
          <circle cx="78" cy="140" r="13" fill="#16a34a"/>
          <path d="M72 140 L76.5 144.5 L85 135.5" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>
          <text x="78" y="166" text-anchor="middle" font-family="Arial, sans-serif" font-size="9.5" font-weight="bold" fill="#15803d">NO GHS PICTOGRAM</text>
          <text x="78" y="178" text-anchor="middle" font-family="Arial, sans-serif" font-size="8.2" fill="#166534">Below CLP Cutoff / Non-Haz</text>
        `);
      }}

      let textEls = [], y = 96;
      textEls.push(`<text x="166" y="${{y}}" font-family="Arial, sans-serif" font-size="9.5" font-weight="bold" fill="#991b1b">HAZARD STATEMENTS:</text>`);
      y += 12;
      for (const st of hStmts) {{
        for (const ln of wrapText(st, 58)) {{
          if (y < 178) {{ textEls.push(`<text x="166" y="${{y}}" font-family="Arial, sans-serif" font-size="8.8" fill="#111827">${{esc(ln)}}</text>`); y += 11.2; }}
        }}
      }}
      y = Math.max(y + 4, 174);
      textEls.push(`<text x="166" y="${{y}}" font-family="Arial, sans-serif" font-size="9.5" font-weight="bold" fill="#1e40af">PRECAUTIONARY STATEMENTS:</text>`);
      y += 12;
      for (const st of pStmts) {{
        for (const ln of wrapText(st, 58)) {{
          if (y < 252) {{ textEls.push(`<text x="166" y="${{y}}" font-family="Arial, sans-serif" font-size="8.6" fill="#1f2937">${{esc(ln)}}</text>`); y += 11.0; }}
        }}
      }}

      return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 330" width="${{dims.w}}mm" height="${{dims.h}}mm">
        <rect x="2" y="2" width="516" height="326" rx="10" fill="#ffffff" stroke="#111827" stroke-width="2.5"/>
        <path d="M 12 3.5 L 508 3.5 C 513 3.5 516.5 7 516.5 12 L 516.5 13 L 3.5 13 L 3.5 12 C 3.5 7 7 3.5 12 3.5 Z" fill="${{sigBg}}"/>
        <text x="16" y="37" font-family="Arial, sans-serif" font-size="21" font-weight="900" fill="#0f172a">${{esc(item.title)}}</text>
        <text x="16" y="53" font-family="Arial, sans-serif" font-size="10.5" font-weight="bold" fill="#334155">${{esc(item.subtitle)}}</text>
        <text x="16" y="66" font-family="Arial, sans-serif" font-size="8.8" fill="#64748b">${{esc(item.cas)}}  •  ${{esc(item.composition)}}</text>

        <rect x="374" y="19" width="132" height="28" rx="5" fill="${{sigBg}}"/>
        <text x="440" y="37" text-anchor="middle" font-family="Arial, sans-serif" font-size="13" font-weight="900" letter-spacing="0.8" fill="#ffffff">${{esc(signal)}}</text>

        <line x1="12" y1="74" x2="508" y2="74" stroke="#cbd5e1" stroke-width="1.5"/>
        <rect x="10" y="80" width="144" height="170" rx="6" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1"/>
        ${{pictoParts.join('')}}
        ${{textEls.join('')}}

        <line x1="12" y1="256" x2="508" y2="256" stroke="#cbd5e1" stroke-width="1.5"/>
        <rect x="12" y="263" width="158" height="53" rx="4" fill="#f8fafc" stroke="#94a3b8" stroke-width="1"/>
        <text x="18" y="276" font-family="Arial, sans-serif" font-size="8" font-weight="bold" fill="#475569">DATE PREPARED:</text>
        <text x="18" y="298" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#0f172a">${{esc(meta.prepDate)}}</text>
        <line x1="18" y1="304" x2="160" y2="304" stroke="#cbd5e1" stroke-width="1"/>

        <rect x="178" y="263" width="158" height="53" rx="4" fill="#f8fafc" stroke="#94a3b8" stroke-width="1"/>
        <text x="184" y="276" font-family="Arial, sans-serif" font-size="8" font-weight="bold" fill="#475569">PREPARED BY:</text>
        <text x="184" y="298" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#0f172a">${{esc(meta.prepBy)}}</text>
        <line x1="184" y1="304" x2="326" y2="304" stroke="#cbd5e1" stroke-width="1"/>

        <rect x="344" y="263" width="164" height="53" rx="4" fill="#f8fafc" stroke="#94a3b8" stroke-width="1"/>
        <text x="350" y="276" font-family="Arial, sans-serif" font-size="8" font-weight="bold" fill="#475569">NOTES:</text>
        <text x="350" y="298" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#0f172a">${{esc(meta.notes)}}</text>
        <line x1="350" y1="304" x2="498" y2="304" stroke="#cbd5e1" stroke-width="1"/>
      </svg>`;
    }}

    function buildSVG(item, layout, mode, meta, dims) {{
      return layout === 'minimal'
        ? buildMinimalSVG(item, mode, meta, dims)
        : buildFullSVG(item, mode, meta, dims);
    }}

    function downloadSVG(id) {{
      const layout = document.getElementById('layoutSelect').value;
      const mode = document.getElementById('modeSelect').value;
      const dims = getPhysicalDims();
      const item = LABELS.find(x => x.id === id);
      const meta = {{
        prepDate: document.getElementById('prepDate').value,
        prepBy: document.getElementById('prepBy').value,
        notes: document.getElementById('notesInput').value,
      }};
      const svg = '<?xml version="1.0" encoding="UTF-8"?>\\n' + buildSVG(item, layout, mode, meta, dims);
      const blob = new Blob([svg], {{type: 'image/svg+xml;charset=utf-8'}});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${{item.id}}_${{layout}}_${{dims.w}}x${{dims.h}}mm.svg`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }}

    function printSingle(id) {{
      const cards = document.querySelectorAll('.label-wrapper');
      cards.forEach(c => {{
        if (c.dataset.id !== id) c.classList.add('hidden-print');
        else c.classList.remove('hidden-print');
      }});
      window.print();
      cards.forEach(c => c.classList.remove('hidden-print'));
    }}

    function renderAll() {{
      const layout = document.getElementById('layoutSelect').value;
      const mode = document.getElementById('modeSelect').value;
      const dims = getPhysicalDims();
      const inW = (dims.w / 25.4).toFixed(2);
      const inH = (dims.h / 25.4).toFixed(2);
      const meta = {{
        prepDate: document.getElementById('prepDate').value,
        prepBy: document.getElementById('prepBy').value,
        notes: document.getElementById('notesInput').value,
      }};

      // Enforce exact physical millimeter print dimensions in @media print
      document.getElementById('dynamicPrintStyle').textContent = `
        @media print {{
          .label-wrapper {{
            width: ${{dims.w}}mm !important;
            height: ${{dims.h}}mm !important;
          }}
          .svg-holder svg {{
            width: ${{dims.w}}mm !important;
            height: ${{dims.h}}mm !important;
          }}
        }}
      `;

      document.getElementById('sizeBanner').innerHTML = `
        <div>
          <strong>Active Physical Print Size:</strong> <span style="color:#1d4ed8; font-weight:800;">${{dims.w}} mm × ${{dims.h}} mm (${{inW}}" × ${{inH}}")</span>
          &nbsp;•&nbsp; <strong>Style:</strong> ${{layout === 'minimal' ? 'Minimal (Pictogram + Date Prepared / Prepared By / Notes)' : 'Full Detailed (with H/P Statements)'}}
        </div>
        <div style="color:#64748b;">Tip: Set printer scale to <strong>100% (Actual Size)</strong> in the browser print dialog for exact millimeter output.</div>
      `;

      const cols = dims.w <= 50 ? 4 : (dims.w <= 65 ? 3 : 2);
      const colWidthCalc = cols === 4 ? 'calc(25% - 12px)' : (cols === 3 ? 'calc(33.333% - 11px)' : 'calc(50% - 8px)');

      const grid = document.getElementById('labelsGrid');
      grid.innerHTML = LABELS.map((item, idx) => {{
        const svg = buildSVG(item, layout, mode, meta, dims);
        return `<div class="label-wrapper" data-id="${{item.id}}" style="width:${{colWidthCalc}};">
          <div class="label-actions">
            <span><strong>#${{idx + 1}} ${{esc(item.title)}}</strong> • ${{dims.w}}×${{dims.h}} mm</span>
            <div style="display:flex; gap:6px;">
              <button onclick="printSingle('${{item.id}}')">🖨️ Print (${{dims.w}}×${{dims.h}}mm)</button>
              <button onclick="downloadSVG('${{item.id}}')">⬇️ SVG</button>
            </div>
          </div>
          <div class="svg-holder">${{svg}}</div>
        </div>`;
      }}).join('');
    }}

    renderAll();
  </script>
</body>
</html>
"""

html_path = BASE_DIR / "GHS_Labels_Print_Sheet.html"
html_path.write_text(HTML_STUDIO, encoding="utf-8")
print(f"Updated interactive printable HTML sheet at {html_path}")
