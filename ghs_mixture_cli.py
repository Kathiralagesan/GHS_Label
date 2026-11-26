#!/usr/bin/env python3
"""
Universal Composition-Based GHS Solution Label Generator (CLI + Standalone Web App Builder)
Calculates GHS/CLP mixture classifications, pictograms (GHS01-GHS09), signal words,
H-statements, and P-statements for any solution composition (% v/v, % w/v, % w/w, M, mM).
"""

import argparse
import json
import re
import sys
from pathlib import Path

BASE_DIR = Path("/Users/u_alagesan/Documents/GHS Label")

# All 9 Official UNECE GHS Pictogram Vector Inner Symbols (100x100 viewBox inside red diamond)
GHS_SYMBOLS_ALL = json.loads((BASE_DIR / "official_ghs_symbols.json").read_text(encoding="utf-8"))

CHEM_DB = [
    # --- ACIDS ---
    {
        "key": "TFA",
        "name": "Trifluoroacetic Acid (TFA)",
        "aliases": ["tfa", "trifluoroacetic acid", "cf3cooh"],
        "category": "Acids",
        "cas": "76-05-1",
        "formula": "CF₃COOH",
        "mw": 114.02,
        "corr_1_min": 5.0, "eye_1_min": 3.0, "skin_2_min": 1.0, "eye_2_min": 1.0,
        "extreme_ph_min": 0.8, "ehs_irrit_min": 0.05,
        "acute_4_min": 25.0, "acute_h_cat4": "H332: Harmful if inhaled.",
        "p_Codes": ["P260: Do not breathe mist/vapours.", "P280: Wear protective gloves and eye/face protection.", "P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes."]
    },
    {
        "key": "FA",
        "name": "Formic Acid (FA)",
        "aliases": ["fa", "formic acid", "hcooh", "methanoic acid"],
        "category": "Acids",
        "cas": "64-18-6",
        "formula": "HCOOH",
        "mw": 46.03,
        "flam_min_cat3": 85.0,
        "corr_1_min": 10.0, "eye_1_min": 10.0, "skin_2_min": 2.0, "eye_2_min": 2.0,  # CLP Annex VI SCL
        "ehs_irrit_min": 0.05,
        "acute_3_min": 25.0, "acute_4_min": 10.0,
        "acute_h_cat3": "H331: Toxic if inhaled. H302: Harmful if swallowed.",
        "acute_h_cat4": "H302+H332: Harmful if swallowed or inhaled.",
        "p_Codes": ["P260: Do not breathe mist/vapours.", "P280: Wear protective gloves and eye/face protection.", "P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes."]
    },
    {
        "key": "AcOH",
        "name": "Acetic Acid (Glacial / AcOH)",
        "aliases": ["acoh", "acetic acid", "hac", "glacial acetic acid", "ch3cooh", "ethanoic acid"],
        "category": "Acids",
        "cas": "64-19-7",
        "formula": "CH₃COOH",
        "mw": 60.05,
        "flam_min_cat3": 80.0,
        "corr_1_min": 25.0, "eye_1_min": 25.0, "skin_2_min": 10.0, "eye_2_min": 10.0,  # CLP Annex VI SCL
        "ehs_irrit_min": 0.5,
        "p_Codes": ["P280: Wear protective gloves and eye/face protection.", "P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes."]
    },
    {
        "key": "HCl",
        "name": "Hydrochloric Acid (HCl)",
        "aliases": ["hcl", "hydrochloric acid"],
        "category": "Acids",
        "cas": "7647-01-0",
        "formula": "HCl",
        "mw": 36.46,
        "corr_1_min": 25.0, "eye_1_min": 25.0, "skin_2_min": 10.0, "eye_2_min": 10.0,  # CLP Annex VI SCL
        "extreme_ph_min": 0.4, "ehs_irrit_min": 0.05,
        "stot_3_min": 10.0, "stot_3_h": "H335: May cause respiratory irritation.",
        "p_Codes": ["P260: Do not breathe mist/vapours.", "P280: Wear protective gloves, clothing, and eye/face protection.", "P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes."]
    },
    {
        "key": "H2SO4",
        "name": "Sulfuric Acid (H₂SO₄)",
        "aliases": ["h2so4", "sulfuric acid", "sulphuric acid"],
        "category": "Acids",
        "cas": "7664-93-9",
        "formula": "H₂SO₄",
        "mw": 98.08,
        "corr_1_min": 15.0, "eye_1_min": 15.0, "skin_2_min": 5.0, "eye_2_min": 5.0,  # CLP Annex VI SCL
        "extreme_ph_min": 0.5, "ehs_irrit_min": 0.05,
        "p_Codes": ["P260: Do not breathe mist/vapours.", "P280: Wear protective gloves, lab coat, and eye/face protection.", "P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes."]
    },
    {
        "key": "HNO3",
        "name": "Nitric Acid (HNO₃)",
        "aliases": ["hno3", "nitric acid"],
        "category": "Acids",
        "cas": "7697-37-2",
        "formula": "HNO₃",
        "mw": 63.01,
        "ox_min": 65.0,
        "corr_1_min": 5.0, "eye_1_min": 3.0, "skin_2_min": 1.0, "eye_2_min": 1.0,
        "extreme_ph_min": 0.5, "ehs_irrit_min": 0.05,
        "acute_3_min": 15.0, "acute_h_cat3": "H331: Toxic if inhaled.",
        "p_Codes": ["P260: Do not breathe vapours.", "P280: Wear protective gloves, clothing, and face protection.", "P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes."]
    },
    {
        "key": "H3PO4",
        "name": "Phosphoric Acid (H₃PO₄)",
        "aliases": ["h3po4", "phosphoric acid", "orthophosphoric acid"],
        "category": "Acids",
        "cas": "7664-38-2",
        "formula": "H₃PO₄",
        "mw": 98.00,
        "corr_1_min": 25.0, "eye_1_min": 25.0, "skin_2_min": 10.0, "eye_2_min": 10.0,  # CLP Annex VI SCL
        "extreme_ph_min": 1.0, "ehs_irrit_min": 0.1,
        "p_Codes": ["P280: Wear protective gloves and eye/face protection.", "P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes."]
    },
    {
        "key": "TCA",
        "name": "Trichloroacetic Acid (TCA)",
        "aliases": ["tca", "trichloroacetic acid", "ccl3cooh"],
        "category": "Acids",
        "cas": "76-03-9",
        "formula": "CCl₃COOH",
        "mw": 163.38,
        "corr_1_min": 5.0, "eye_1_min": 3.0, "skin_2_min": 1.0, "eye_2_min": 1.0,
        "stot_3_min": 1.0, "stot_3_h": "H335: May cause respiratory irritation.",
        "aquat_min": 2.5,
        "extreme_ph_min": 1.0, "ehs_irrit_min": 0.1,
        "p_Codes": ["P260: Do not breathe dust or mist.", "P273: Avoid release to the environment.", "P280: Wear protective gloves and eye/face protection."]
    },
    {
        "key": "CitricAcid",
        "name": "Citric Acid",
        "aliases": ["citric acid", "citrate"],
        "category": "Acids",
        "cas": "77-92-9",
        "formula": "C₆H₈O₇",
        "mw": 192.12,
        "eye_2_min": 10.0, "stot_3_min": 20.0, "stot_3_h": "H335: May cause respiratory irritation.",
        "p_Codes": ["P280: Wear eye protection and protective gloves.", "P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes."]
    },
    {
        "key": "BoricAcid",
        "name": "Boric Acid",
        "aliases": ["boric acid", "h3bo3"],
        "category": "Acids",
        "cas": "10043-35-3",
        "formula": "H₃BO₃",
        "mw": 61.83,
        "stot_1_min": 0.3,  # Repr. 1B CLP GCL >= 0.3%
        "stot_h": "H360FD: May damage fertility. May damage the unborn child (Repr. 1B ≥ 0.3%).",
        "p_Codes": ["P201: Obtain special instructions before use.", "P280: Wear protective gloves, protective clothing, and eye protection.", "P308+P313: IF exposed or concerned: Get medical advice/attention."]
    },

    # --- BASES ---
    {
        "key": "NaOH",
        "name": "Sodium Hydroxide (NaOH)",
        "aliases": ["naoh", "sodium hydroxide"],
        "category": "Bases",
        "cas": "1310-73-2",
        "formula": "NaOH",
        "mw": 40.00,
        "corr_1_min": 2.0, "eye_1_min": 2.0, "skin_2_min": 0.5, "eye_2_min": 0.5,  # CLP Annex VI SCL
        "extreme_ph_min": 0.2, "ehs_irrit_min": 0.05,
        "p_Codes": ["P260: Do not breathe dust or mist.", "P280: Wear protective gloves, protective clothing, and eye/face protection.", "P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes."]
    },
    {
        "key": "KOH",
        "name": "Potassium Hydroxide (KOH)",
        "aliases": ["koh", "potassium hydroxide"],
        "category": "Bases",
        "cas": "1310-58-3",
        "formula": "KOH",
        "mw": 56.11,
        "corr_1_min": 2.0, "eye_1_min": 2.0, "skin_2_min": 0.5, "eye_2_min": 0.5,  # CLP Annex VI SCL
        "acute_4_min": 15.0, "acute_h_cat4": "H302: Harmful if swallowed.",
        "extreme_ph_min": 0.2, "ehs_irrit_min": 0.05,
        "p_Codes": ["P280: Wear protective gloves, protective clothing, and eye/face protection.", "P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes."]
    },
    {
        "key": "NH4OH",
        "name": "Ammonium Hydroxide / Ammonia (NH₄OH)",
        "aliases": ["nh4oh", "ammonium hydroxide", "ammonia", "nh3"],
        "category": "Bases",
        "cas": "1336-21-6",
        "formula": "NH₄OH",
        "mw": 35.05,
        "corr_1_min": 5.0, "eye_1_min": 3.0, "skin_2_min": 1.0, "eye_2_min": 1.0,
        "stot_3_min": 5.0, "stot_3_h": "H335: May cause respiratory irritation.",
        "aquat_min": 25.0,
        "ehs_irrit_min": 0.1,
        "p_Codes": ["P261: Avoid breathing vapours.", "P280: Wear protective gloves and eye/face protection.", "P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes."]
    },
    {
        "key": "TEA",
        "name": "Triethylamine (TEA)",
        "aliases": ["tea", "triethylamine", "et3n"],
        "category": "Bases",
        "cas": "121-44-8",
        "formula": "(C₂H₅)₃N",
        "mw": 101.19,
        "flam_min_cat2": 15.0, "flam_min_cat3": 5.0,
        "corr_1_min": 5.0, "eye_1_min": 1.0, "skin_2_min": 1.0, "eye_2_min": 0.5,
        "acute_3_min": 15.0, "acute_4_min": 3.0,
        "acute_h_cat3": "H311+H331: Toxic in contact with skin or if inhaled. H302: Harmful if swallowed.",
        "acute_h_cat4": "H302+H312+H332: Harmful if swallowed, in contact with skin, or if inhaled.",
        "stot_3_min": 1.0, "stot_3_h": "H335: May cause respiratory irritation.",
        "ehs_irrit_min": 0.05,
        "p_Codes": ["P210: Keep away from heat, sparks, open flames.", "P260: Do not breathe vapours.", "P280: Wear protective gloves, clothing, and eye/face protection."]
    },

    # --- ORGANIC SOLVENTS ---
    {
        "key": "ACN",
        "name": "Acetonitrile (ACN)",
        "aliases": ["acn", "can", "acetonitrile", "mecn", "ch3cn", "methyl cyanide"],
        "category": "Organic Solvents",
        "cas": "75-05-8",
        "formula": "CH₃CN",
        "mw": 41.05,
        "flam_min_cat2": 15.0, "flam_min_cat3": 5.0,
        "acute_4_min": 20.0, "acute_h_cat4": "H302+H312+H332: Harmful if swallowed, in contact with skin, or if inhaled.",
        "eye_2_min": 10.0,
        "ehs_irrit_min": 5.0,
        "p_Codes": ["P210: Keep away from heat, hot surfaces, sparks, open flames. No smoking.", "P280: Wear protective gloves, protective clothing, and eye/face protection.", "P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes."]
    },
    {
        "key": "Methanol",
        "name": "Methanol (MeOH)",
        "aliases": ["methanol", "meoh", "ch3oh", "methyl alcohol"],
        "category": "Organic Solvents",
        "cas": "67-56-1",
        "formula": "CH₃OH",
        "mw": 32.04,
        "flam_min_cat2": 20.0, "flam_min_cat3": 8.0,
        "acute_3_min": 10.0, "acute_4_min": 3.0,
        "acute_h_cat3": "H301+H311+H331: Toxic if swallowed, in contact with skin, or if inhaled.",
        "acute_h_cat4": "H302+H312+H332: Harmful if swallowed, in contact with skin, or if inhaled.",
        "stot_1_min": 10.0, "stot_2_min": 3.0,  # CLP Annex VI SCL for Methanol: >=10% STOT SE 1, 3-10% STOT SE 2
        "stot_h": "H370: Causes damage to organs (eyes / optic nerve, central nervous system).",
        "stot_2_h": "H371: May cause damage to organs (eyes / optic nerve, central nervous system).",
        "p_Codes": ["P210: Keep away from heat, sparks, open flames. No smoking.", "P260: Do not breathe vapours.", "P280: Wear protective gloves, protective clothing, and eye protection.", "P301+P310: IF SWALLOWED: Immediately call a POISON CENTER or doctor."]
    },
    {
        "key": "Ethanol",
        "name": "Ethanol (EtOH)",
        "aliases": ["ethanol", "etoh", "c2h5oh", "ethyl alcohol"],
        "category": "Organic Solvents",
        "cas": "64-17-5",
        "formula": "C₂H₅OH",
        "mw": 46.07,
        "flam_min_cat2": 50.0, "flam_min_cat3": 12.0,
        "eye_2_min": 50.0,  # ECHA REACH SCL for Ethanol Eye Irrit. 2 >= 50%
        "p_Codes": ["P210: Keep away from heat, hot surfaces, sparks, open flames. No smoking.", "P233: Keep container tightly closed.", "P280: Wear eye protection and protective gloves.", "P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes."]
    },
    {
        "key": "Isopropanol",
        "name": "Isopropanol (2-Propanol / IPA)",
        "aliases": ["isopropanol", "ipa", "2-propanol", "isopropyl alcohol"],
        "category": "Organic Solvents",
        "cas": "67-63-0",
        "formula": "C₃H₈O",
        "mw": 60.10,
        "flam_min_cat2": 30.0, "flam_min_cat3": 10.0,
        "eye_2_min": 10.0,
        "stot_3_min": 20.0, "stot_3_h": "H336: May cause drowsiness or dizziness.",
        "p_Codes": ["P210: Keep away from heat, hot surfaces, sparks, open flames. No smoking.", "P261: Avoid breathing vapours.", "P280: Wear protective gloves and eye protection.", "P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes."]
    },
    {
        "key": "DMSO",
        "name": "Dimethyl Sulfoxide (DMSO)",
        "aliases": ["dmso", "dimethyl sulfoxide", "dimethylsulfoxide"],
        "category": "Organic Solvents",
        "cas": "67-68-5",
        "formula": "(CH₃)₂SO",
        "mw": 78.13,
        "advisory": "Contains DMSO — readily penetrates skin and can carry dissolved compounds across the dermal barrier.",
        "p_Codes": ["P280: Wear chemical-resistant gloves (butyl/nitrile) and eye protection.", "Avoid skin and eye contact; wash hands thoroughly after handling."]
    },
    {
        "key": "Acetone",
        "name": "Acetone",
        "aliases": ["acetone", "2-propanone"],
        "category": "Organic Solvents",
        "cas": "67-64-1",
        "formula": "C₃H₆O",
        "mw": 58.08,
        "flam_min_cat2": 15.0, "flam_min_cat3": 5.0,
        "eye_2_min": 10.0,
        "stot_3_min": 20.0, "stot_3_h": "H336: May cause drowsiness or dizziness.",
        "p_Codes": ["P210: Keep away from heat, hot surfaces, sparks, open flames. No smoking.", "P261: Avoid breathing vapours.", "P280: Wear protective gloves and eye protection."]
    },
    {
        "key": "DMF",
        "name": "N,N-Dimethylformamide (DMF)",
        "aliases": ["dmf", "dimethylformamide"],
        "category": "Organic Solvents",
        "cas": "68-12-2",
        "formula": "C₃H₇NO",
        "mw": 73.09,
        "flam_min_cat3": 50.0,
        "acute_4_min": 20.0, "acute_h_cat4": "H312+H332: Harmful in contact with skin or if inhaled.",
        "eye_2_min": 10.0,
        "stot_1_min": 0.3,  # Repr. 1B H360D >= 0.3%
        "stot_h": "H360D: May damage the unborn child (Repr. 1B).",
        "p_Codes": ["P201: Obtain special instructions before use.", "P210: Keep away from heat, sparks, open flames.", "P280: Wear protective gloves, clothing, and eye protection.", "P308+P313: IF exposed or concerned: Get medical advice/attention."]
    },
    {
        "key": "THF",
        "name": "Tetrahydrofuran (THF)",
        "aliases": ["thf", "tetrahydrofuran"],
        "category": "Organic Solvents",
        "cas": "109-99-9",
        "formula": "C₄H₈O",
        "mw": 72.11,
        "flam_min_cat2": 10.0, "flam_min_cat3": 3.0,
        "acute_4_min": 25.0, "acute_h_cat4": "H302: Harmful if swallowed.",
        "eye_2_min": 25.0,
        "stot_2_min": 1.0, "stot_2_h": "H351: Suspected of causing cancer (Carc. 2).",
        "stot_3_min": 25.0, "stot_3_h": "H335: May cause respiratory irritation.",
        "advisory": "EUH019: May form explosive peroxides.",
        "p_Codes": ["P210: Keep away from heat, sparks, open flames. No smoking.", "P280: Wear protective gloves, clothing, and eye protection."]
    },
    {
        "key": "Chloroform",
        "name": "Chloroform (CHCl₃)",
        "aliases": ["chloroform", "chcl3", "trichloromethane"],
        "category": "Organic Solvents",
        "cas": "67-66-3",
        "formula": "CHCl₃",
        "mw": 119.38,
        "acute_3_min": 20.0, "acute_4_min": 5.0,
        "acute_h_cat3": "H331: Toxic if inhaled. H302: Harmful if swallowed.",
        "acute_h_cat4": "H302+H332: Harmful if swallowed or inhaled.",
        "skin_2_min": 10.0, "eye_2_min": 10.0,
        "stot_1_min": 1.0,
        "stot_h": "H351: Suspected of causing cancer. H361d: Suspected of damaging the unborn child. H372: Causes damage to organs through prolonged or repeated exposure.",
        "p_Codes": ["P260: Do not breathe vapours.", "P280: Wear protective gloves, clothing, and eye/face protection.", "P308+P313: IF exposed or concerned: Get medical advice/attention."]
    },
    {
        "key": "DCM",
        "name": "Dichloromethane (DCM)",
        "aliases": ["dcm", "dichloromethane", "ch2cl2", "methylene chloride"],
        "category": "Organic Solvents",
        "cas": "75-09-2",
        "formula": "CH₂Cl₂",
        "mw": 84.93,
        "skin_2_min": 10.0, "eye_2_min": 10.0,
        "stot_2_min": 1.0, "stot_2_h": "H351: Suspected of causing cancer (Carc. 2).",
        "stot_3_min": 20.0, "stot_3_h": "H336: May cause drowsiness or dizziness.",
        "p_Codes": ["P261: Avoid breathing vapours.", "P280: Wear protective gloves, protective clothing, and eye protection."]
    },
    {
        "key": "Phenol",
        "name": "Phenol",
        "aliases": ["phenol", "carbolic acid"],
        "category": "Organic Solvents",
        "cas": "108-95-2",
        "formula": "C₆H₅OH",
        "mw": 94.11,
        "corr_1_min": 3.0, "eye_1_min": 3.0, "skin_2_min": 1.0, "eye_2_min": 1.0,  # CLP Annex VI SCL
        "acute_3_min": 10.0, "acute_4_min": 2.0,
        "acute_h_cat3": "H301+H311+H331: Toxic if swallowed, in contact with skin, or if inhaled.",
        "acute_h_cat4": "H302+H312+H332: Harmful if swallowed, in contact with skin, or if inhaled.",
        "stot_2_min": 1.0, "stot_2_h": "H341: Suspected of causing genetic defects (Muta. 2). H373: May cause damage to organs through prolonged exposure.",
        "p_Codes": ["P260: Do not breathe mist/vapours.", "P280: Wear protective gloves, clothing, and eye/face protection.", "P301+P310: IF SWALLOWED: Immediately call a POISON CENTER or doctor."]
    },

    # --- CHAOTROPES, DETERGENTS & DENATURANTS ---
    {
        "key": "Urea",
        "name": "Urea",
        "aliases": ["urea", "carbamide"],
        "category": "Chaotropes & Detergents",
        "cas": "57-13-6",
        "formula": "CH₄N₂O",
        "mw": 60.06,
        "p_Codes": ["P280: Wear standard laboratory gloves and eye protection."]
    },
    {
        "key": "Thiourea",
        "name": "Thiourea",
        "aliases": ["thiourea"],
        "category": "Chaotropes & Detergents",
        "cas": "62-56-6",
        "formula": "CH₄N₂S",
        "mw": 76.12,
        "acute_4_min": 25.0, "acute_h_cat4": "H302: Harmful if swallowed.",
        "stot_2_min": 1.0, "stot_2_h": "H351: Suspected of causing cancer (Carc. 2). H361d: Suspected of damaging the unborn child.",
        "aquat_min": 25.0,
        "p_Codes": ["P201: Obtain special instructions before use.", "P273: Avoid release to the environment.", "P280: Wear protective gloves, clothing, and eye protection."]
    },
    {
        "key": "GdnHCl",
        "name": "Guanidine Hydrochloride (GdnHCl)",
        "aliases": ["gdnhcl", "guhcl", "guanidine hcl", "guanidine hydrochloride", "guanidinium chloride"],
        "category": "Chaotropes & Detergents",
        "cas": "50-01-1",
        "formula": "CH₅N₃·HCl",
        "mw": 95.53,
        "acute_4_min": 25.0, "acute_h_cat4": "H302+H332: Harmful if swallowed or if inhaled.",
        "skin_2_min": 10.0, "eye_2_min": 10.0,
        "ehs_irrit_min": 1.0,
        "p_Codes": ["P261: Avoid breathing dust or mist.", "P280: Wear protective gloves and eye protection.", "P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes."]
    },
    {
        "key": "GITC",
        "name": "Guanidine Thiocyanate (GITC)",
        "aliases": ["gitc", "guanidine thiocyanate", "guanidinium thiocyanate", "gdnscn"],
        "category": "Chaotropes & Detergents",
        "cas": "593-84-0",
        "formula": "C₂H₆N₄S",
        "mw": 118.16,
        "corr_1_min": 5.0, "eye_1_min": 3.0, "skin_2_min": 1.0, "eye_2_min": 1.0,
        "acute_4_min": 20.0, "acute_h_cat4": "H302+H312+H332: Harmful if swallowed, in contact with skin, or if inhaled.",
        "advisory": "EUH032: Contact with acids liberates very toxic gas (HCN). Do NOT mix with bleach or acids!",
        "p_Codes": ["P260: Do not breathe dust or mist.", "P280: Wear protective gloves, clothing, and eye/face protection.", "P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes."]
    },
    {
        "key": "SDS",
        "name": "Sodium Dodecyl Sulfate (SDS)",
        "aliases": ["sds", "sodium dodecyl sulfate", "sodium lauryl sulfate", "sls"],
        "category": "Chaotropes & Detergents",
        "cas": "151-21-3",
        "formula": "C₁₂H₂₅NaO₄S",
        "mw": 288.38,
        "eye_1_min": 20.0, "skin_2_min": 10.0, "eye_2_min": 10.0,  # ECHA REACH SCL for SDS aqueous solutions
        "acute_4_min": 25.0, "acute_h_cat4": "H302+H332: Harmful if swallowed or inhaled (dust).",
        "ehs_irrit_min": 0.5,
        "p_Codes": ["P261: Avoid breathing dust/mist.", "P280: Wear protective gloves and eye protection.", "P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes."]
    },
    {
        "key": "TritonX100",
        "name": "Triton X-100",
        "aliases": ["triton x-100", "triton x100", "tx-100", "triton"],
        "category": "Chaotropes & Detergents",
        "cas": "9002-93-1",
        "formula": "C₁₄H₂₂O(C₂H₄O)ₙ",
        "mw": 647.0,
        "eye_1_min": 3.0, "skin_2_min": 10.0, "eye_2_min": 1.0,
        "acute_4_min": 25.0, "acute_h_cat4": "H302: Harmful if swallowed.",
        "aquat_min": 2.5,
        "ehs_irrit_min": 0.1,
        "p_Codes": ["P273: Avoid release to the environment.", "P280: Wear protective gloves and eye/face protection.", "P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes."]
    },
    {
        "key": "Tween20",
        "name": "Tween-20 (Polysorbate 20)",
        "aliases": ["tween-20", "tween 20", "polysorbate 20"],
        "category": "Chaotropes & Detergents",
        "cas": "9005-64-5",
        "formula": "C₅₈H₁₁₄O₂₆",
        "mw": 1227.54,
        "p_Codes": ["P280: Wear standard laboratory gloves and eye protection."]
    },
    {
        "key": "SDC",
        "name": "Sodium Deoxycholate (SDC)",
        "aliases": ["sdc", "sodium deoxycholate", "deoxycholate"],
        "category": "Chaotropes & Detergents",
        "cas": "302-95-4",
        "formula": "C₂₄H₃₉NaO₄",
        "mw": 414.55,
        "acute_4_min": 25.0, "acute_h_cat4": "H302: Harmful if swallowed.",
        "stot_3_min": 20.0, "stot_3_h": "H335: May cause respiratory irritation.",
        "ehs_irrit_min": 1.0,
        "p_Codes": ["P261: Avoid breathing dust.", "P280: Wear protective gloves and eye protection."]
    },

    # --- BUFFERS & SALTS ---
    {
        "key": "Tris",
        "name": "Tris (Tromethamine / Tris-HCl)",
        "aliases": ["tris", "tris-hcl", "tris base", "trizma", "tromethamine"],
        "category": "Buffers & Salts",
        "cas": "77-86-1",
        "formula": "C₄H₁₁NO₃",
        "mw": 121.14,
        "p_Codes": ["P280: Wear standard laboratory gloves and eye protection."]
    },
    {
        "key": "HEPES",
        "name": "HEPES",
        "aliases": ["hepes"],
        "category": "Buffers & Salts",
        "cas": "7365-45-9",
        "formula": "C₈H₁₈N₂O₄S",
        "mw": 238.30,
        "p_Codes": ["P280: Wear standard laboratory gloves and eye protection."]
    },
    {
        "key": "MES",
        "name": "MES Buffer",
        "aliases": ["mes"],
        "category": "Buffers & Salts",
        "cas": "4432-31-9",
        "formula": "C₆H₁₃NO₄S",
        "mw": 195.24,
        "p_Codes": ["P280: Wear standard laboratory gloves and eye protection."]
    },
    {
        "key": "MOPS",
        "name": "MOPS Buffer",
        "aliases": ["mops"],
        "category": "Buffers & Salts",
        "cas": "1132-61-2",
        "formula": "C₇H₁₅NO₄S",
        "mw": 209.26,
        "p_Codes": ["P280: Wear standard laboratory gloves and eye protection."]
    },
    {
        "key": "PBS",
        "name": "PBS (Phosphate Buffered Saline)",
        "aliases": ["pbs", "phosphate buffered saline"],
        "category": "Buffers & Salts",
        "cas": "7647-14-5 / 7558-79-4",
        "formula": "NaCl / Na₂HPO₄ / KH₂PO₄",
        "mw": 58.44,
        "p_Codes": ["P280: Wear standard laboratory gloves and eye protection."]
    },
    {
        "key": "NaCl",
        "name": "Sodium Chloride (NaCl)",
        "aliases": ["nacl", "sodium chloride", "saline"],
        "category": "Buffers & Salts",
        "cas": "7647-14-5",
        "formula": "NaCl",
        "mw": 58.44,
        "p_Codes": ["P280: Wear standard laboratory gloves and eye protection."]
    },
    {
        "key": "KCl",
        "name": "Potassium Chloride (KCl)",
        "aliases": ["kcl", "potassium chloride"],
        "category": "Buffers & Salts",
        "cas": "7447-40-7",
        "formula": "KCl",
        "mw": 74.55,
        "p_Codes": ["P280: Wear standard laboratory gloves and eye protection."]
    },
    {
        "key": "ABC",
        "name": "Ammonium Bicarbonate (ABC / NH₄HCO₃)",
        "aliases": ["abc", "nh4hco3", "ammonium bicarbonate", "ambic"],
        "category": "Buffers & Salts",
        "cas": "1066-33-7",
        "formula": "NH₄HCO₃",
        "mw": 79.06,
        "acute_4_min": 25.0, "acute_h_cat4": "H302: Harmful if swallowed.",
        "p_Codes": ["P280: Wear standard laboratory gloves and eye protection."]
    },
    {
        "key": "NH4OAc",
        "name": "Ammonium Acetate (NH₄OAc)",
        "aliases": ["nh4oac", "ammonium acetate"],
        "category": "Buffers & Salts",
        "cas": "631-61-8",
        "formula": "CH₃COONH₄",
        "mw": 77.08,
        "p_Codes": ["P280: Wear standard laboratory gloves and eye protection."]
    },
    {
        "key": "Imidazole",
        "name": "Imidazole",
        "aliases": ["imidazole"],
        "category": "Buffers & Salts",
        "cas": "288-32-4",
        "formula": "C₃H₄N₂",
        "mw": 68.08,
        "corr_1_min": 5.0, "eye_1_min": 3.0, "skin_2_min": 1.0, "eye_2_min": 1.0,
        "acute_4_min": 25.0, "acute_h_cat4": "H302: Harmful if swallowed.",
        "stot_1_min": 0.3,  # Repr. 1B H360D >= 0.3% (approx 44 mM)
        "stot_h": "H360D: May damage the unborn child (Repr. 1B ≥ 0.3% / ~44 mM).",
        "ehs_irrit_min": 0.1,
        "p_Codes": ["P201: Obtain special instructions before use.", "P280: Wear protective gloves, protective clothing, and eye/face protection.", "P308+P313: IF exposed or concerned: Get medical advice/attention."]
    },
    {
        "key": "EDTA",
        "name": "EDTA (Ethylenediaminetetraacetic Acid / Na₂EDTA)",
        "aliases": ["edta", "na2edta"],
        "category": "Buffers & Salts",
        "cas": "60-00-4",
        "formula": "C₁₀H₁₆N₂O₈",
        "mw": 292.24,
        "eye_2_min": 10.0,
        "stot_2_min": 10.0, "stot_2_h": "H373: May cause damage to organs (respiratory tract) through prolonged exposure if inhaled.",
        "p_Codes": ["P280: Wear protective gloves and eye protection."]
    },

    # --- REDUCING AGENTS, ALKYLATING AGENTS, FIXATIVES & OTHERS ---
    {
        "key": "DTT",
        "name": "Dithiothreitol (DTT)",
        "aliases": ["dtt", "dithiothreitol", "cleland's reagent"],
        "category": "Reducers, Alkylators & Fixatives",
        "cas": "3483-12-3",
        "formula": "C₄H₁₀O₂S₂",
        "mw": 154.25,
        "acute_4_min": 20.0, "acute_h_cat4": "H302: Harmful if swallowed.",
        "eye_1_min": 3.0, "skin_2_min": 10.0, "eye_2_min": 1.0,
        "ehs_irrit_min": 0.1,
        "p_Codes": ["P280: Wear protective gloves and eye/face protection.", "P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes."]
    },
    {
        "key": "BME",
        "name": "2-Mercaptoethanol (β-ME / BME)",
        "aliases": ["bme", "2-mercaptoethanol", "beta-mercaptoethanol", "2-me"],
        "category": "Reducers, Alkylators & Fixatives",
        "cas": "60-24-2",
        "formula": "C₂H₆OS",
        "mw": 78.13,
        "acute_3_min": 5.0, "acute_4_min": 1.0,
        "acute_h_cat3": "H301+H331: Toxic if swallowed or inhaled. H310: Fatal in contact with skin.",
        "acute_h_cat4": "H302+H312+H332: Harmful if swallowed, in contact with skin, or if inhaled.",
        "eye_1_min": 3.0, "skin_2_min": 10.0, "eye_2_min": 1.0,
        "sens_skin_min": 1.0,
        "stot_2_min": 10.0, "stot_2_h": "H373: May cause damage to organs (liver, heart) through prolonged exposure.",
        "aquat_min": 2.5,
        "ehs_irrit_min": 0.05,
        "p_Codes": ["P260: Do not breathe vapours.", "P273: Avoid release to the environment.", "P280: Wear protective gloves, clothing, and eye/face protection."]
    },
    {
        "key": "TCEP",
        "name": "TCEP Hydrochloride (TCEP-HCl)",
        "aliases": ["tcep", "tcep-hcl"],
        "category": "Reducers, Alkylators & Fixatives",
        "cas": "51805-45-9",
        "formula": "C₉H₁₅O₆P·HCl",
        "mw": 286.65,
        "corr_1_min": 5.0, "eye_1_min": 3.0, "skin_2_min": 1.0, "eye_2_min": 1.0,
        "ehs_irrit_min": 0.1,
        "p_Codes": ["P280: Wear protective gloves and eye/face protection.", "P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes."]
    },
    {
        "key": "IAA",
        "name": "Iodoacetamide (IAA / IAM)",
        "aliases": ["iaa", "iam", "iodoacetamide"],
        "category": "Reducers, Alkylators & Fixatives",
        "cas": "144-48-9",
        "formula": "C₂H₄INO",
        "mw": 184.96,
        "acute_3_min": 5.0, "acute_4_min": 0.5,
        "acute_h_cat3": "H301: Toxic if swallowed.",
        "acute_h_cat4": "H302: Harmful if swallowed.",
        "sens_skin_min": 0.1,
        "stot_1_min": 0.1,
        "stot_h": "H334: May cause allergy or asthma symptoms or breathing difficulties if inhaled.",
        "ehs_irrit_min": 0.05,
        "p_Codes": ["P261: Avoid breathing dust or mist.", "P280: Wear protective gloves and eye protection.", "P301+P310: IF SWALLOWED: Immediately call a POISON CENTER or doctor."]
    },
    {
        "key": "CAA",
        "name": "2-Chloroacetamide (CAA)",
        "aliases": ["caa", "chloroacetamide", "2-chloroacetamide"],
        "category": "Reducers, Alkylators & Fixatives",
        "cas": "79-07-2",
        "formula": "C₂H₄ClNO",
        "mw": 93.51,
        "acute_3_min": 10.0, "acute_4_min": 2.0,
        "acute_h_cat3": "H301: Toxic if swallowed.",
        "acute_h_cat4": "H302: Harmful if swallowed.",
        "sens_skin_min": 0.1,  # CLP Annex VI SCL for CAA Skin Sens. 1 >= 0.1%
        "stot_2_min": 3.0, "stot_2_h": "H361f: Suspected of damaging fertility.",
        "ehs_irrit_min": 0.05,
        "p_Codes": ["P261: Avoid breathing dust/mist.", "P280: Wear protective gloves and eye protection."]
    },
    {
        "key": "NaN3",
        "name": "Sodium Azide (NaN₃)",
        "aliases": ["nan3", "sodium azide", "azide"],
        "category": "Reducers, Alkylators & Fixatives",
        "cas": "26628-22-8",
        "formula": "NaN₃",
        "mw": 65.01,
        "acute_3_min": 0.5, "acute_4_min": 0.1,
        "acute_h_cat3": "H300+H310+H330: Fatal if swallowed, in contact with skin, or if inhaled.",
        "acute_h_cat4": "H302+H312: Harmful if swallowed or in contact with skin.",
        "aquat_min": 2.5,
        "ehs_irrit_min": 0.01,
        "advisory": "EUH032: Contact with acids liberates very toxic gas (HN₃); may form explosive heavy-metal azides in plumbing.",
        "p_Codes": ["P273: Avoid release to the environment.", "P280: Wear protective gloves, clothing, and eye protection."]
    },
    {
        "key": "Formaldehyde",
        "name": "Formaldehyde / Paraformaldehyde (PFA)",
        "aliases": ["formaldehyde", "pfa", "paraformaldehyde", "formalin"],
        "category": "Reducers, Alkylators & Fixatives",
        "cas": "50-00-0",
        "formula": "CH₂O",
        "mw": 30.03,
        "corr_1_min": 25.0, "eye_1_min": 25.0, "skin_2_min": 5.0, "eye_2_min": 5.0,  # CLP Annex VI SCL
        "acute_3_min": 5.0, "acute_4_min": 1.0,
        "acute_h_cat3": "H301+H311+H331: Toxic if swallowed, in contact with skin, or if inhaled.",
        "acute_h_cat4": "H302+H312+H332: Harmful if swallowed, in contact with skin, or if inhaled.",
        "sens_skin_min": 0.2,  # CLP Annex VI SCL Skin Sens. 1 >= 0.2%
        "stot_1_min": 0.1,  # Carc. 1B H350 >= 0.1%
        "stot_h": "H350: May cause cancer (Carc. 1B ≥ 0.1%). H341: Suspected of causing genetic defects.",
        "stot_3_min": 5.0, "stot_3_h": "H335: May cause respiratory irritation.",
        "p_Codes": ["P201: Obtain special instructions before use.", "P260: Do not breathe vapours.", "P280: Wear protective gloves, clothing, and eye/face protection.", "P308+P313: IF exposed or concerned: Get medical advice/attention."]
    },
    {
        "key": "Acrylamide",
        "name": "Acrylamide",
        "aliases": ["acrylamide", "bis-acrylamide"],
        "category": "Reducers, Alkylators & Fixatives",
        "cas": "79-06-1",
        "formula": "C₃H₅NO",
        "mw": 71.08,
        "acute_3_min": 10.0, "acute_4_min": 2.0,
        "acute_h_cat3": "H301: Toxic if swallowed. H312+H332: Harmful in contact with skin or inhaled.",
        "acute_h_cat4": "H302+H312+H332: Harmful if swallowed, in contact with skin, or if inhaled.",
        "skin_2_min": 10.0, "eye_2_min": 10.0,
        "sens_skin_min": 1.0,
        "stot_1_min": 0.1,  # Carc. 1B, Muta. 1B >= 0.1%
        "stot_h": "H350: May cause cancer. H340: May cause genetic defects. H361f: Suspected of damaging fertility. H372: Causes damage to peripheral nervous system.",
        "p_Codes": ["P201: Obtain special instructions before use.", "P260: Do not breathe dust or mist.", "P280: Wear protective gloves, protective clothing, and eye protection.", "P308+P313: IF exposed or concerned: Get medical advice/attention."]
    },
    {
        "key": "H2O2",
        "name": "Hydrogen Peroxide (H₂O₂)",
        "aliases": ["h2o2", "hydrogen peroxide"],
        "category": "Reducers, Alkylators & Fixatives",
        "cas": "7722-84-1",
        "formula": "H₂O₂",
        "mw": 34.01,
        "ox_min": 50.0,
        "corr_1_min": 35.0, "eye_1_min": 8.0, "skin_2_min": 35.0, "eye_2_min": 5.0,  # CLP Annex VI SCL
        "acute_4_min": 25.0, "acute_h_cat4": "H302+H332: Harmful if swallowed or inhaled.",
        "stot_3_min": 35.0, "stot_3_h": "H335: May cause respiratory irritation.",
        "ehs_irrit_min": 1.0,
        "p_Codes": ["P280: Wear protective gloves and eye/face protection.", "P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes."]
    },
    {
        "key": "Glycerol",
        "name": "Glycerol (Glycerin)",
        "aliases": ["glycerol", "glycerin", "glycerine"],
        "category": "Reducers, Alkylators & Fixatives",
        "cas": "56-81-5",
        "formula": "C₃H₈O₃",
        "mw": 92.09,
        "p_Codes": ["P280: Wear standard laboratory gloves and eye protection."]
    },
    {
        "key": "Cellulose",
        "name": "Cellulose",
        "aliases": ["cellulose", "microcrystalline cellulose"],
        "category": "Reducers, Alkylators & Fixatives",
        "cas": "9004-34-6",
        "formula": "(C₆H₁₀O₅)ₙ",
        "mw": 162.14,
        "advisory": "Avoid creating airborne dust concentrations.",
        "p_Codes": ["Avoid breathing dust. Store tightly closed in a dry, well-ventilated area."]
    },
    {
        "key": "DiethylEther",
        "name": "Diethyl Ether",
        "aliases": ["diethyl ether", "ether", "et2o", "ethoxyethane"],
        "category": "Organic Solvents",
        "cas": "60-29-7",
        "formula": "(C₂H₅)₂O",
        "mw": 74.12,
        "flam_min_cat2": 5.0, "flam_min_cat3": 1.0,
        "acute_4_min": 25.0, "acute_h_cat4": "H302: Harmful if swallowed.",
        "stot_3_min": 20.0, "stot_3_h": "H336: May cause drowsiness or dizziness.",
        "advisory": "EUH019: May form explosive peroxides. EUH066: Repeated exposure may cause skin dryness.",
        "p_Codes": ["P210: Keep away from heat, hot surfaces, sparks, open flames. No smoking.", "P261: Avoid breathing vapours.", "P280: Wear protective gloves and eye protection."]
    },
    {
        "key": "EthylAcetate",
        "name": "Ethyl Acetate (EtOAc)",
        "aliases": ["ethyl acetate", "etoac", "ea"],
        "category": "Organic Solvents",
        "cas": "141-78-6",
        "formula": "C₄H₈O₂",
        "mw": 88.11,
        "flam_min_cat2": 15.0, "flam_min_cat3": 5.0,
        "eye_2_min": 10.0,
        "stot_3_min": 20.0, "stot_3_h": "H336: May cause drowsiness or dizziness.",
        "p_Codes": ["P210: Keep away from heat, sparks, open flames. No smoking.", "P261: Avoid breathing vapours.", "P280: Wear protective gloves and eye protection."]
    },
    {
        "key": "Hexane",
        "name": "n-Hexane",
        "aliases": ["hexane", "n-hexane"],
        "category": "Organic Solvents",
        "cas": "110-54-3",
        "formula": "C₆H₁₄",
        "mw": 86.18,
        "flam_min_cat2": 5.0,
        "skin_2_min": 10.0,
        "stot_1_min": 10.0, "stot_2_min": 3.0,
        "stot_h": "H304: May be fatal if swallowed and enters airways. H361f: Suspected of damaging fertility. H373: May cause damage to nervous system.",
        "stot_3_min": 20.0, "stot_3_h": "H336: May cause drowsiness or dizziness.",
        "aquat_min": 2.5,
        "p_Codes": ["P210: Keep away from heat, sparks, open flames.", "P273: Avoid release to the environment.", "P280: Wear protective gloves, clothing, and eye protection."]
    },
    {
        "key": "Toluene",
        "name": "Toluene",
        "aliases": ["toluene", "methylbenzene"],
        "category": "Organic Solvents",
        "cas": "108-88-3",
        "formula": "C₇H₈",
        "mw": 92.14,
        "flam_min_cat2": 10.0,
        "skin_2_min": 10.0,
        "stot_1_min": 10.0, "stot_2_min": 3.0,
        "stot_h": "H304: May be fatal if swallowed and enters airways. H361d: Suspected of damaging the unborn child. H373: May cause organ damage.",
        "stot_3_min": 20.0, "stot_3_h": "H336: May cause drowsiness or dizziness.",
        "p_Codes": ["P210: Keep away from heat, sparks, open flames.", "P260: Do not breathe vapours.", "P280: Wear protective gloves, clothing, and eye protection."]
    },
    {
        "key": "Pyridine",
        "name": "Pyridine",
        "aliases": ["pyridine"],
        "category": "Organic Solvents",
        "cas": "110-86-1",
        "formula": "C₅H₅N",
        "mw": 79.10,
        "flam_min_cat2": 15.0,
        "acute_4_min": 20.0, "acute_h_cat4": "H302+H312+H332: Harmful if swallowed, in contact with skin, or if inhaled.",
        "skin_2_min": 10.0, "eye_2_min": 10.0,
        "p_Codes": ["P210: Keep away from heat, sparks, open flames.", "P280: Wear protective gloves, clothing, and eye protection."]
    },
    {
        "key": "Dioxane",
        "name": "1,4-Dioxane",
        "aliases": ["1,4-dioxane", "dioxane"],
        "category": "Organic Solvents",
        "cas": "123-91-1",
        "formula": "C₄H₈O₂",
        "mw": 88.11,
        "flam_min_cat2": 15.0,
        "eye_2_min": 10.0,
        "stot_1_min": 0.1,
        "stot_h": "H350: May cause cancer (Carc. 1B ≥ 0.1%).",
        "stot_3_min": 20.0, "stot_3_h": "H335: May cause respiratory irritation.",
        "advisory": "EUH019: May form explosive peroxides.",
        "p_Codes": ["P201: Obtain special instructions before use.", "P210: Keep away from heat, sparks, open flames.", "P280: Wear protective gloves, clothing, and eye protection."]
    },
    {
        "key": "HF",
        "name": "Hydrofluoric Acid (HF)",
        "aliases": ["hf", "hydrofluoric acid"],
        "category": "Acids",
        "cas": "7664-39-3",
        "formula": "HF",
        "mw": 20.01,
        "corr_1_min": 1.0, "eye_1_min": 1.0, "skin_2_min": 0.1, "eye_2_min": 0.1,  # CLP Annex VI SCL
        "acute_3_min": 0.1,
        "acute_h_cat3": "H300+H310+H330: Fatal if swallowed, in contact with skin, or if inhaled.",
        "extreme_ph_min": 0.05, "ehs_irrit_min": 0.01,
        "advisory": "CRITICAL: Causes deep tissue necrosis and systemic hypocalcemia. Keep Calcium Gluconate gel at bench!",
        "p_Codes": ["P260: Do not breathe vapours.", "P280: Wear HF-resistant gloves, full face shield, and acid apron.", "P301+P310: Immediately call a POISON CENTER or doctor."]
    },
    {
        "key": "PerchloricAcid",
        "name": "Perchloric Acid (HClO₄)",
        "aliases": ["hclo4", "perchloric acid"],
        "category": "Acids",
        "cas": "7601-90-3",
        "formula": "HClO₄",
        "mw": 100.46,
        "ox_min": 50.0,
        "corr_1_min": 10.0, "eye_1_min": 10.0, "skin_2_min": 1.0, "eye_2_min": 1.0,
        "extreme_ph_min": 0.5, "ehs_irrit_min": 0.05,
        "p_Codes": ["P210: Keep away from heat/sparks/open flames.", "P220: Keep away from clothing and combustible materials.", "P280: Wear protective gloves, clothing, and eye/face protection."]
    },
    {
        "key": "EtBr",
        "name": "Ethidium Bromide (EtBr)",
        "aliases": ["etbr", "ethidium bromide"],
        "category": "Reducers, Alkylators & Fixatives",
        "cas": "1239-45-8",
        "formula": "C₂₁H₂₀BrN₃",
        "mw": 394.31,
        "acute_3_min": 0.1, "acute_4_min": 0.02,
        "acute_h_cat3": "H330: Fatal if inhaled. H302: Harmful if swallowed.",
        "acute_h_cat4": "H332: Harmful if inhaled.",
        "stot_2_min": 1.0, "stot_2_h": "H341: Suspected of causing genetic defects (Muta. 2 ≥ 1%).",
        "ehs_irrit_min": 0.001,
        "p_Codes": ["P201: Obtain special instructions before use.", "P260: Do not breathe dust or mist.", "P280: Wear nitrile gloves, lab coat, and eye protection."]
    },
    {
        "key": "Glutaraldehyde",
        "name": "Glutaraldehyde",
        "aliases": ["glutaraldehyde"],
        "category": "Reducers, Alkylators & Fixatives",
        "cas": "111-30-8",
        "formula": "C₅H₈O₂",
        "mw": 100.12,
        "corr_1_min": 5.0, "eye_1_min": 3.0, "skin_2_min": 0.5, "eye_2_min": 0.5,
        "acute_3_min": 2.0, "acute_4_min": 0.5,
        "acute_h_cat3": "H301+H330: Toxic if swallowed; fatal if inhaled.",
        "sens_skin_min": 0.5,
        "stot_1_min": 0.2,
        "stot_h": "H334: May cause allergy or asthma symptoms or breathing difficulties if inhaled.",
        "stot_3_min": 0.5, "stot_3_h": "H335: May cause respiratory irritation.",
        "aquat_min": 2.5,
        "p_Codes": ["P260: Do not breathe vapours.", "P273: Avoid release to the environment.", "P280: Wear protective gloves, clothing, and eye/face protection."]
    },
    {
        "key": "Bleach",
        "name": "Sodium Hypochlorite (Bleach / NaOCl)",
        "aliases": ["bleach", "naocl", "sodium hypochlorite"],
        "category": "Reducers, Alkylators & Fixatives",
        "cas": "7681-52-9",
        "formula": "NaOCl",
        "mw": 74.44,
        "corr_1_min": 5.0, "eye_1_min": 3.0, "skin_2_min": 1.0, "eye_2_min": 1.0,
        "aquat_min": 2.5,
        "extreme_ph_min": 1.0, "ehs_irrit_min": 0.1,
        "advisory": "EUH031: Contact with acids liberates toxic gas (Cl₂).",
        "p_Codes": ["P273: Avoid release to the environment.", "P280: Wear protective gloves, clothing, and eye/face protection."]
    },
    {
        "key": "H2O",
        "name": "Water (Ultrapure / Milli-Q / H₂O)",
        "aliases": ["h2o", "water", "milli-q", "ddh2o", "dh2o"],
        "category": "Organic Solvents",
        "cas": "7732-18-5",
        "formula": "H₂O",
        "mw": 18.015,
        "p_Codes": []
    }
]


def find_chemical(query: str):
    q = query.strip().lower()
    for ch in CHEM_DB:
        if q == ch["cas"].lower() or q == ch["key"].lower() or q == ch["name"].lower() or q in ch["aliases"]:
            return ch
    for ch in CHEM_DB:
        for al in ch["aliases"]:
            if al in q or q in al:
                return ch
    return None


def to_pct_conc(amount: float, unit: str, mw: float) -> float:
    """Converts amount in (%, % v/v, % w/v, % w/w, M, mM) to effective % w/v (approx % w/w in water)."""
    u = unit.strip()
    if u.lower() in ["%", "% v/v", "% w/v", "% w/w", "pct"]:
        return float(amount)
    elif u == "M" or u.lower() == "mol/l":
        # 1 M = (MW g / 1000 mL) = (MW / 10) % w/v
        return float(amount) * (mw / 10.0)
    elif u == "mM" or u.lower() == "mmol/l":
        return float(amount) * (mw / 10000.0)
    return float(amount)


def parse_composition_string(comp_str: str) -> list:
    """
    Parses a free-text composition string like:
      '80% ACN, 0.1% FA'
      '10% DMSO + 1% TFA'
      '6 M GdnHCl, 50 mM Tris, 10 mM DTT'
      'TFA, 1%'
    into a list of component dicts: [{'chem': chem_dict, 'amount': float, 'unit': str, 'pct': float, 'raw_name': str}]
    """
    parts = [p.strip() for p in re.split(r"[,;+]+", comp_str) if p.strip()]
    # Special case: "TFA, 1%" where a 2-part split has name in part 0 and concentration in part 1
    if len(parts) == 2 and not re.search(r"\d", parts[0]) and re.match(r"^[\d.]+\s*(%|M|mM)$", parts[1], re.I):
        parts = [f"{parts[1]} {parts[0]}"]

    parsed = []
    for part in parts:
        # Pattern 1: "80% ACN" or "50 mM Tris" or "6 M Guanidine HCl"
        m1 = re.match(r"^([\d.]+)\s*(%\s*[vw]/[vw]|%|mM|M)\s+(.+)$", part)
        # Pattern 2: "ACN 80%" or "TFA 0.1%"
        m2 = re.match(r"^(.+?)\s+([\d.]+)\s*(%\s*[vw]/[vw]|%|mM|M)$", part)
        if m1:
            amt = float(m1.group(1))
            unit = m1.group(2).strip()
            name = m1.group(3).strip()
        elif m2:
            name = m2.group(1).strip()
            amt = float(m2.group(2))
            unit = m2.group(3).strip()
        else:
            # Pure chemical name with no number -> 100%
            name = part.strip()
            amt = 100.0
            unit = "%"

        ch = find_chemical(name)
        mw = ch["mw"] if ch else 100.0
        pct = to_pct_conc(amt, unit, mw)
        parsed.append({
            "chem": ch,
            "raw_name": ch["name"] if ch else name,
            "short_name": ch["key"] if ch else name,
            "cas": ch["cas"] if ch else "Custom",
            "amount": amt,
            "unit": unit,
            "pct": pct
        })
    return parsed


def calculate_mixture_ghs(components: list, mode: str = "reg") -> dict:
    """
    Applies CLP / UN GHS mixture calculation rules across all components in a solution.
    mode: 'reg' (Strict CLP/GHS Regulatory Cutoffs) or 'ehs' (Conservative Lab EHS Policy).
    Returns dict with pictograms, signal, h_statements, p_statements, cas_line, comp_line, audit_log.
    """
    pictos = set()
    signal_rank = 0  # 0: Non-hazardous / No signal word, 1: WARNING, 2: DANGER
    h_list = []
    p_list = []
    advisories = []
    audit = []

    def add_h(stmt: str):
        if stmt and stmt not in h_list:
            h_list.append(stmt)

    def add_p(stmt: str):
        if stmt and stmt not in p_list:
            p_list.append(stmt)

    # Track additive fractions for Skin/Eye corrosion & irritation
    corr_1_frac = 0.0
    eye_1_frac = 0.0
    skin_2_frac = 0.0
    eye_2_frac = 0.0

    for comp in components:
        ch = comp.get("chem")
        pct = float(comp.get("pct", 0.0))
        if not ch or pct <= 0 or ch["key"] == "H2O":
            continue

        cname = ch["key"]

        # P-statements
        for pc in ch.get("p_Codes", []):
            add_p(pc)
        if ch.get("advisory"):
            advisories.append(f"Advisory ({cname}): {ch['advisory']}")

        # 1. Oxidizing (GHS03)
        if ch.get("ox_min") and pct >= ch["ox_min"]:
            pictos.add("GHS03")
            signal_rank = max(signal_rank, 2)
            add_h("H272: May intensify fire; oxidizer.")
            audit.append(f"{cname} ({pct:.2g}% ≥ {ch['ox_min']}%): Oxidizer → GHS03 (Danger, H272)")

        # 2. Flammability (GHS02)
        if ch.get("flam_min_cat2") and pct >= ch["flam_min_cat2"]:
            pictos.add("GHS02")
            signal_rank = max(signal_rank, 2)
            add_h("H225: Highly flammable liquid and vapour.")
            audit.append(f"{cname} ({pct:.2g}% ≥ {ch['flam_min_cat2']}%): Flam. Liq. 2 → GHS02 (Danger, H225)")
        elif ch.get("flam_min_cat3") and pct >= ch["flam_min_cat3"]:
            pictos.add("GHS02")
            signal_rank = max(signal_rank, 1)
            add_h("H226: Flammable liquid and vapour.")
            audit.append(f"{cname} ({pct:.2g}% ≥ {ch['flam_min_cat3']}%): Flam. Liq. 3 → GHS02 (Warning, H226)")

        # 3. Acute Toxicity (GHS06 Cat 1-3 vs GHS07 Cat 4)
        if ch.get("acute_3_min") and pct >= ch["acute_3_min"]:
            pictos.add("GHS06")
            signal_rank = max(signal_rank, 2)
            add_h(ch.get("acute_h_cat3", "H301+H311+H331: Toxic if swallowed, in contact with skin, or if inhaled."))
            audit.append(f"{cname} ({pct:.2g}% ≥ {ch['acute_3_min']}%): Acute Tox. 1–3 → GHS06 (Danger)")
        elif ch.get("acute_4_min") and pct >= ch["acute_4_min"]:
            pictos.add("GHS07")
            signal_rank = max(signal_rank, 1)
            add_h(ch.get("acute_h_cat4", "H302+H312+H332: Harmful if swallowed, in contact with skin, or if inhaled."))
            audit.append(f"{cname} ({pct:.2g}% ≥ {ch['acute_4_min']}%): Acute Tox. 4 → GHS07 (Warning)")

        # 4. Skin Corrosion / Eye Damage / Irritation additive fractions (or SCLs)
        if ch.get("corr_1_min"):
            corr_1_frac += pct / ch["corr_1_min"]
        if ch.get("eye_1_min"):
            eye_1_frac += pct / ch["eye_1_min"]
        if ch.get("skin_2_min"):
            skin_2_frac += pct / ch["skin_2_min"]
        if ch.get("eye_2_min"):
            eye_2_frac += pct / ch["eye_2_min"]

        # Conservative EHS extreme-pH / dilute acid-base handling
        if mode == "ehs":
            if ch.get("extreme_ph_min") and pct >= ch["extreme_ph_min"]:
                corr_1_frac = max(corr_1_frac, 1.0)
                audit.append(f"{cname} ({pct:.2g}% ≥ {ch['extreme_ph_min']}% in EHS mode): Extreme pH → GHS05 (Danger, H314)")
            elif ch.get("ehs_irrit_min") and pct >= ch["ehs_irrit_min"]:
                skin_2_frac = max(skin_2_frac, 1.0)
                eye_2_frac = max(eye_2_frac, 1.0)
                audit.append(f"{cname} ({pct:.2g}% ≥ {ch['ehs_irrit_min']}% in EHS mode): Precautionary Irritant → GHS07 (Warning)")

        # 5. STOT SE/RE 1-2 & CMR 1A/1B/2 (GHS08)
        if ch.get("stot_1_min") and pct >= ch["stot_1_min"]:
            pictos.add("GHS08")
            signal_rank = max(signal_rank, 2)
            add_h(ch.get("stot_h", "H370/H350/H360: Causes organ damage or CMR hazard."))
            audit.append(f"{cname} ({pct:.2g}% ≥ {ch['stot_1_min']}%): STOT/CMR Cat 1 → GHS08 (Danger)")
        elif ch.get("stot_2_min") and pct >= ch["stot_2_min"]:
            pictos.add("GHS08")
            signal_rank = max(signal_rank, 1)
            add_h(ch.get("stot_2_h", ch.get("stot_h", "H371/H373: May cause organ damage.")))
            audit.append(f"{cname} ({pct:.2g}% ≥ {ch['stot_2_min']}%): STOT/CMR Cat 2 → GHS08 (Warning)")

        # 6. STOT SE 3 (GHS07, H335 / H336)
        if ch.get("stot_3_min") and pct >= ch["stot_3_min"]:
            pictos.add("GHS07")
            signal_rank = max(signal_rank, 1)
            add_h(ch.get("stot_3_h", "H335/H336: May cause respiratory irritation or drowsiness."))
            audit.append(f"{cname} ({pct:.2g}% ≥ {ch['stot_3_min']}%): STOT SE 3 → GHS07 (Warning)")

        # 7. Skin Sensitization (GHS07, H317)
        if ch.get("sens_skin_min") and pct >= ch["sens_skin_min"]:
            pictos.add("GHS07")
            signal_rank = max(signal_rank, 1)
            add_h("H317: May cause an allergic skin reaction.")
            audit.append(f"{cname} ({pct:.2g}% ≥ {ch['sens_skin_min']}%): Skin Sens. 1 → GHS07 (Warning, H317)")

        # 8. Aquatic Toxicity (GHS09)
        if ch.get("aquat_min") and pct >= ch["aquat_min"]:
            pictos.add("GHS09")
            add_h("H411: Toxic to aquatic life with long lasting effects.")
            audit.append(f"{cname} ({pct:.2g}% ≥ {ch['aquat_min']}%): Aquatic Chronic → GHS09 (H411)")

    # Evaluate additive Skin/Eye Corrosion & Irritation
    has_skin_eye_corr = False
    if corr_1_frac >= 1.0:
        pictos.add("GHS05")
        signal_rank = max(signal_rank, 2)
        add_h("H314: Causes severe skin burns and eye damage.")
        has_skin_eye_corr = True
        audit.append(f"Mixture Skin Corrosion sum = {corr_1_frac:.2f} (≥ 1.0) → GHS05 (Danger, H314)")
    elif eye_1_frac >= 1.0:
        pictos.add("GHS05")
        signal_rank = max(signal_rank, 2)
        add_h("H318: Causes serious eye damage.")
        has_skin_eye_corr = True
        if skin_2_frac >= 1.0:
            add_h("H315: Causes skin irritation.")
        audit.append(f"Mixture Eye Damage sum = {eye_1_frac:.2f} (≥ 1.0) → GHS05 (Danger, H318)")
    else:
        if skin_2_frac >= 1.0:
            pictos.add("GHS07")
            signal_rank = max(signal_rank, 1)
            add_h("H315: Causes skin irritation.")
            audit.append(f"Mixture Skin Irritation sum = {skin_2_frac:.2f} (≥ 1.0) → GHS07 (Warning, H315)")
        if eye_2_frac >= 1.0:
            pictos.add("GHS07")
            signal_rank = max(signal_rank, 1)
            add_h("H319: Causes serious eye irritation.")
            audit.append(f"Mixture Eye Irritation sum = {eye_2_frac:.2f} (≥ 1.0) → GHS07 (Warning, H319)")

    # CLP Article 26 Pictogram Precedence Rules:
    # 1. If GHS06 (Skull & Crossbones) applies, GHS07 (Exclamation Mark) shall not appear
    if "GHS06" in pictos and "GHS07" in pictos:
        pictos.remove("GHS07")
        audit.append("CLP Precedence (Art. 26): GHS06 present → GHS07 suppressed.")
    # 2. If GHS05 (Corrosion) applies, GHS07 shall not appear for skin/eye irritation
    #    (keep GHS07 only if there is an independent Acute Tox. 4 or STOT SE 3 or Skin Sens. 1 hazard)
    if "GHS05" in pictos and "GHS07" in pictos and mode == "reg":
        has_non_irrit_ghs07 = any(
            code in " ".join(h_list) for code in ["H302", "H312", "H332", "H335", "H336", "H317"]
        )
        if not has_non_irrit_ghs07:
            pictos.remove("GHS07")
            audit.append("CLP Precedence (Art. 26): GHS05 present → GHS07 (skin/eye irritation) suppressed.")

    for adv in advisories:
        add_h(adv)

    if not h_list:
        h_list.append("Not a hazardous substance or mixture according to GHS / CLP concentration thresholds.")
        audit.append("All components below CLP/GHS hazard concentration thresholds → No GHS pictogram required.")
    if not p_list:
        p_list.append("P280: Wear standard laboratory eye protection and protective gloves.")

    if signal_rank == 2:
        signal = "DANGER"
    elif signal_rank == 1:
        signal = "WARNING"
    else:
        signal = "NO SIGNAL WORD"

    ordered_pictos = [code for code in ["GHS01", "GHS02", "GHS03", "GHS04", "GHS05", "GHS06", "GHS07", "GHS08", "GHS09"] if code in pictos]

    cas_items = []
    comp_items = []
    for c in components:
        if c["unit"].startswith("%"):
            comp_items.append(f"{c['amount']:g}% {c['short_name']}")
        else:
            comp_items.append(f"{c['amount']:g} {c['unit']} {c['short_name']} (~{c['pct']:.2g}%)")
        if c.get("cas") and c["cas"] not in cas_items:
            cas_items.append(f"{c['cas']} ({c['short_name']})")

    return {
        "pictograms": ordered_pictos,
        "signal": signal,
        "h_statements": h_list[:4],
        "p_statements": p_list[:4],
        "cas": "CAS: " + " | ".join(cas_items[:3]) if cas_items else "Custom Mixture",
        "composition": ", ".join(comp_items) + " (in H₂O)" if len(comp_items) > 1 or (components and components[0]["pct"] < 99.9) else ", ".join(comp_items),
        "audit_log": audit
    }


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


def render_diamond_svg(code: str, x: float, y: float, size: float) -> str:
    sym = GHS_SYMBOLS_ALL[code]
    vb, inner = sym["viewBox"], sym["svg"]
    return f'<svg x="{x:.1f}" y="{y:.1f}" width="{size:.1f}" height="{size:.1f}" viewBox="{vb}">{inner}</svg>'


def render_minimal_solution_svg(title: str, subtitle: str, ghs_result: dict,
                                prep_date: str = "", prep_by: str = "", notes: str = "",
                                width_mm: float = 80.0, height_mm: float = 45.0) -> str:
    pictos = ghs_result["pictograms"]
    signal = ghs_result["signal"]

    if signal == "DANGER":
        sig_bg = "#d90000"
    elif "WARNING" in signal:
        sig_bg = "#d97706"
    else:
        sig_bg = "#16a34a"

    picto_parts = []
    if len(pictos) == 1:
        picto_parts.append(render_diamond_svg(pictos[0], 56, 86, 118))
        picto_parts.append(f'<text x="115" y="224" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#334155">{xml_escape(GHS_SYMBOLS_ALL[pictos[0]]["name"])}</text>')
    elif len(pictos) == 2:
        picto_parts.append(render_diamond_svg(pictos[0], 18, 96, 94))
        picto_parts.append(render_diamond_svg(pictos[1], 116, 96, 94))
        picto_parts.append(f'<text x="115" y="216" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#334155">{" + ".join(pictos)}</text>')
    elif len(pictos) == 3:
        picto_parts.append(render_diamond_svg(pictos[0], 74, 80, 82))
        picto_parts.append(render_diamond_svg(pictos[1], 24, 142, 82))
        picto_parts.append(render_diamond_svg(pictos[2], 124, 142, 82))
        picto_parts.append(f'<text x="115" y="242" text-anchor="middle" font-family="Arial, sans-serif" font-size="10.5" font-weight="bold" fill="#334155">{" + ".join(pictos)}</text>')
    elif len(pictos) >= 4:
        picto_parts.append(render_diamond_svg(pictos[0], 34, 82, 74))
        picto_parts.append(render_diamond_svg(pictos[1], 122, 82, 74))
        picto_parts.append(render_diamond_svg(pictos[2], 34, 156, 74))
        picto_parts.append(render_diamond_svg(pictos[3], 122, 156, 74))
        picto_parts.append(f'<text x="115" y="245" text-anchor="middle" font-family="Arial, sans-serif" font-size="9.5" font-weight="bold" fill="#334155">{" + ".join(pictos[:4])}</text>')
    else:
        picto_parts.append("""
        <rect x="34" y="112" width="162" height="92" rx="10" fill="#f0fdf4" stroke="#16a34a" stroke-width="2" stroke-dasharray="5,3"/>
        <circle cx="115" cy="142" r="16" fill="#16a34a"/>
        <path d="M108 142 L113.5 147.5 L123 137" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
        <text x="115" y="176" text-anchor="middle" font-family="Arial, sans-serif" font-size="11.5" font-weight="bold" fill="#15803d">NO GHS PICTOGRAM</text>
        <text x="115" y="191" text-anchor="middle" font-family="Arial, sans-serif" font-size="9.5" fill="#166534">Below CLP Cutoff / Non-Haz</text>
        """)

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 270" width="{width_mm}mm" height="{height_mm}mm">
  <rect x="2" y="2" width="476" height="266" rx="10" fill="#ffffff" stroke="#0f172a" stroke-width="2.5"/>
  <path d="M 12 3.5 L 468 3.5 C 473 3.5 476.5 7 476.5 12 L 476.5 13 L 3.5 13 L 3.5 12 C 3.5 7 7 3.5 12 3.5 Z" fill="{sig_bg}"/>
  <text x="16" y="40" font-family="Arial, sans-serif" font-size="22" font-weight="900" fill="#0f172a">{xml_escape(title)}</text>
  <text x="16" y="58" font-family="Arial, sans-serif" font-size="10.8" font-weight="bold" fill="#334155">{xml_escape(subtitle)}</text>

  <rect x="332" y="20" width="134" height="32" rx="6" fill="{sig_bg}"/>
  <text x="399" y="41" text-anchor="middle" font-family="Arial, sans-serif" font-size="13.5" font-weight="900" letter-spacing="0.8" fill="#ffffff">{xml_escape(signal)}</text>

  <line x1="12" y1="70" x2="468" y2="70" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="12" y="78" width="206" height="178" rx="8" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1.2"/>
  {''.join(picto_parts)}

  <rect x="228" y="78" width="238" height="53" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.2"/>
  <text x="238" y="94" font-family="Arial, sans-serif" font-size="9.5" font-weight="800" fill="#475569">DATE PREPARED:</text>
  <text x="238" y="116" font-family="Arial, sans-serif" font-size="13" font-weight="bold" fill="#0f172a">{xml_escape(prep_date)}</text>
  <line x1="238" y1="121" x2="454" y2="121" stroke="#cbd5e1" stroke-width="1.2"/>

  <rect x="228" y="140" width="238" height="53" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.2"/>
  <text x="238" y="156" font-family="Arial, sans-serif" font-size="9.5" font-weight="800" fill="#475569">PREPARED BY:</text>
  <text x="238" y="178" font-family="Arial, sans-serif" font-size="13" font-weight="bold" fill="#0f172a">{xml_escape(prep_by)}</text>
  <line x1="238" y1="183" x2="454" y2="183" stroke="#cbd5e1" stroke-width="1.2"/>

  <rect x="228" y="203" width="238" height="53" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.2"/>
  <text x="238" y="219" font-family="Arial, sans-serif" font-size="9.5" font-weight="800" fill="#475569">NOTES:</text>
  <text x="238" y="241" font-family="Arial, sans-serif" font-size="13" font-weight="bold" fill="#0f172a">{xml_escape(notes)}</text>
  <line x1="238" y1="246" x2="454" y2="246" stroke="#cbd5e1" stroke-width="1.2"/>
</svg>""".strip()


def render_solution_svg(title: str, subtitle: str, ghs_result: dict, mode: str = "reg",
                        prep_date: str = "", exp_date: str = "", prep_by: str = "", storage: str = "",
                        style: str = "minimal", width_mm: float = 80.0, height_mm: float = 45.0) -> str:
    if style == "minimal":
        return render_minimal_solution_svg(
            title, subtitle, ghs_result,
            prep_date=prep_date, prep_by=prep_by, notes=storage,
            width_mm=width_mm, height_mm=height_mm
        )
    pictos = ghs_result["pictograms"]
    signal = ghs_result["signal"]
    h_stmts = ghs_result["h_statements"]
    p_stmts = ghs_result["p_statements"]

    if signal == "DANGER":
        sig_bg = "#d90000"
    elif "WARNING" in signal:
        sig_bg = "#d97706"
    else:
        sig_bg = "#16a34a"

    picto_parts = []
    if len(pictos) == 1:
        picto_parts.append(render_diamond_svg(pictos[0], 30, 108, 96))
        picto_parts.append(f'<text x="78" y="218" text-anchor="middle" font-family="Arial, sans-serif" font-size="9.5" font-weight="bold" fill="#374151">{xml_escape(GHS_SYMBOLS_ALL[pictos[0]]["name"])}</text>')
    elif len(pictos) == 2:
        picto_parts.append(render_diamond_svg(pictos[0], 8, 114, 72))
        picto_parts.append(render_diamond_svg(pictos[1], 76, 114, 72))
        picto_parts.append(f'<text x="78" y="206" text-anchor="middle" font-family="Arial, sans-serif" font-size="9.5" font-weight="bold" fill="#374151">{" + ".join(pictos)}</text>')
    elif len(pictos) == 3:
        picto_parts.append(render_diamond_svg(pictos[0], 45, 88, 66))
        picto_parts.append(render_diamond_svg(pictos[1], 11, 142, 66))
        picto_parts.append(render_diamond_svg(pictos[2], 79, 142, 66))
        picto_parts.append(f'<text x="78" y="220" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" font-weight="bold" fill="#374151">{" + ".join(pictos)}</text>')
    elif len(pictos) >= 4:
        picto_parts.append(render_diamond_svg(pictos[0], 14, 86, 62))
        picto_parts.append(render_diamond_svg(pictos[1], 80, 86, 62))
        picto_parts.append(render_diamond_svg(pictos[2], 14, 150, 62))
        picto_parts.append(render_diamond_svg(pictos[3], 80, 150, 62))
        picto_parts.append(f'<text x="78" y="224" text-anchor="middle" font-family="Arial, sans-serif" font-size="8.5" font-weight="bold" fill="#374151">{" + ".join(pictos[:4])}</text>')
    else:
        picto_parts.append("""
        <rect x="20" y="115" width="116" height="72" rx="8" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.8" stroke-dasharray="4,3"/>
        <circle cx="78" cy="140" r="13" fill="#16a34a"/>
        <path d="M72 140 L76.5 144.5 L85 135.5" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>
        <text x="78" y="166" text-anchor="middle" font-family="Arial, sans-serif" font-size="9.5" font-weight="bold" fill="#15803d">NO GHS PICTOGRAM</text>
        <text x="78" y="178" text-anchor="middle" font-family="Arial, sans-serif" font-size="8.2" fill="#166534">Below CLP Cutoff / Non-Haz</text>
        """)

    text_els = []
    y = 96
    text_els.append(f'<text x="166" y="{y}" font-family="Arial, sans-serif" font-size="9.5" font-weight="bold" fill="#991b1b">HAZARD STATEMENTS:</text>')
    y += 12
    for st in h_stmts:
        for ln in wrap_text(st, 58):
            if y < 178:
                text_els.append(f'<text x="166" y="{y}" font-family="Arial, sans-serif" font-size="8.8" fill="#111827">{xml_escape(ln)}</text>')
                y += 11.2
    y = max(y + 4, 174)
    text_els.append(f'<text x="166" y="{y}" font-family="Arial, sans-serif" font-size="9.5" font-weight="bold" fill="#1e40af">PRECAUTIONARY STATEMENTS:</text>')
    y += 12
    for st in p_stmts:
        for ln in wrap_text(st, 58):
            if y < 252:
                text_els.append(f'<text x="166" y="{y}" font-family="Arial, sans-serif" font-size="8.6" fill="#1f2937">{xml_escape(ln)}</text>')
                y += 11.0

    mode_badge = "CLP/GHS Regulatory" if mode == "reg" else "Conservative Lab EHS"

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 330" width="{width_mm}mm" height="{height_mm}mm">
  <rect x="2" y="2" width="516" height="326" rx="10" fill="#ffffff" stroke="#111827" stroke-width="2.5"/>
  <path d="M 12 3.5 L 508 3.5 C 513 3.5 516.5 7 516.5 12 L 516.5 13 L 3.5 13 L 3.5 12 C 3.5 7 7 3.5 12 3.5 Z" fill="{sig_bg}"/>
  <text x="16" y="37" font-family="Arial, sans-serif" font-size="20" font-weight="900" fill="#0f172a">{xml_escape(title)}</text>
  <text x="16" y="53" font-family="Arial, sans-serif" font-size="10.2" font-weight="bold" fill="#334155">{xml_escape(subtitle)}</text>
  <text x="16" y="66" font-family="Arial, sans-serif" font-size="8.5" fill="#64748b">{xml_escape(ghs_result["cas"])}  •  {xml_escape(ghs_result["composition"])}</text>

  <rect x="374" y="19" width="132" height="28" rx="5" fill="{sig_bg}"/>
  <text x="440" y="37" text-anchor="middle" font-family="Arial, sans-serif" font-size="13" font-weight="900" letter-spacing="0.8" fill="#ffffff">{xml_escape(signal)}</text>
  <text x="440" y="59" text-anchor="middle" font-family="Arial, sans-serif" font-size="7.8" font-weight="bold" fill="#64748b">[{xml_escape(mode_badge)}]</text>

  <line x1="12" y1="74" x2="508" y2="74" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="10" y="80" width="144" height="170" rx="6" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1"/>
  {''.join(picto_parts)}
  {''.join(text_els)}

  <line x1="12" y1="256" x2="508" y2="256" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="12" y="263" width="158" height="53" rx="4" fill="#f8fafc" stroke="#94a3b8" stroke-width="1"/>
  <text x="18" y="276" font-family="Arial, sans-serif" font-size="8" font-weight="bold" fill="#475569">DATE PREPARED:</text>
  <text x="18" y="298" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#0f172a">{xml_escape(prep_date)}</text>
  <line x1="18" y1="304" x2="160" y2="304" stroke="#cbd5e1" stroke-width="1"/>

  <rect x="178" y="263" width="158" height="53" rx="4" fill="#f8fafc" stroke="#94a3b8" stroke-width="1"/>
  <text x="184" y="276" font-family="Arial, sans-serif" font-size="8" font-weight="bold" fill="#475569">PREPARED BY:</text>
  <text x="184" y="298" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#0f172a">{xml_escape(prep_by)}</text>
  <line x1="184" y1="304" x2="326" y2="304" stroke="#cbd5e1" stroke-width="1"/>

  <rect x="344" y="263" width="164" height="53" rx="4" fill="#f8fafc" stroke="#94a3b8" stroke-width="1"/>
  <text x="350" y="276" font-family="Arial, sans-serif" font-size="8" font-weight="bold" fill="#475569">NOTES:</text>
  <text x="350" y="298" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#0f172a">{xml_escape(storage)}</text>
  <line x1="350" y1="304" x2="498" y2="304" stroke="#cbd5e1" stroke-width="1"/>
</svg>""".strip()


def main():
    parser = argparse.ArgumentParser(description="Generate a GHS SVG label from any solution composition string.")
    parser.add_argument("--comp", type=str, help="Composition string, e.g. '80% ACN, 0.1% FA' or '6 M GdnHCl, 50 mM Tris'")
    parser.add_argument("--title", type=str, default="", help="Custom title on label (defaults to composition string)")
    parser.add_argument("--subtitle", type=str, default="", help="Custom subtitle on label")
    parser.add_argument("--style", choices=["minimal", "full"], default="minimal", help="'minimal' (default: no H/P statements) or 'full'")
    parser.add_argument("--width-mm", type=float, default=80.0, help="Physical print width in mm (default 80)")
    parser.add_argument("--height-mm", type=float, default=45.0, help="Physical print height in mm (default 45)")
    parser.add_argument("--mode", choices=["reg", "ehs"], default="reg", help="'reg' (CLP Regulatory) or 'ehs' (Conservative Lab EHS)")
    parser.add_argument("--out", type=str, default="custom_label.svg", help="Output SVG file path")
    args = parser.parse_args()

    if args.comp:
        comps = parse_composition_string(args.comp)
        res = calculate_mixture_ghs(comps, mode=args.mode)
        title = args.title or args.comp
        subtitle = args.subtitle or res["composition"]
        svg = render_solution_svg(title, subtitle, res, mode=args.mode, style=args.style, width_mm=args.width_mm, height_mm=args.height_mm)
        out_path = Path(args.out)
        out_path.write_text(svg, encoding="utf-8")
        print(f"Saved GHS SVG label ({args.style}, {args.width_mm}x{args.height_mm} mm) to: {out_path}")
        print(f"  Signal Word : {res['signal']}")
        print(f"  Pictograms  : {', '.join(res['pictograms']) if res['pictograms'] else 'None (Below CLP Cutoff)'}")
        for line in res["audit_log"]:
            print(f"  - {line}")


if __name__ == "__main__":
    main()


def generate_universal_html_app():
    symbols_json = json.dumps(GHS_SYMBOLS_ALL, ensure_ascii=False)
    chemdb_json = json.dumps(CHEM_DB, ensure_ascii=False)

    html = rf"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Laboratory GHS Pictogram &amp; Mixture Label Studio — Dr. Kathirvel Alagesan</title>
  <style id="dynamicPrintCss"></style>
  <style>
    :root {{
      --paper: #f6f4ee;
      --paper-deep: #ece8de;
      --surface: #ffffff;
      --ink: #141413;
      --ink-secondary: #52504a;
      --ink-muted: #78756d;
      --rule: #d5d0c3;
      --rule-dark: #141413;
      --accent: #9b1b1b;
      --accent-soft: #fdf2f2;
      --blue-editorial: #1e3a5f;
      --blue-soft: #f0f4f8;
      --green-editorial: #14532d;
      --serif: "Iowan Old Style", "Palatino Linotype", "Book Antiqua", Palatino, Georgia, "Times New Roman", serif;
      --sans: "Inter", -apple-system, BlinkMacSystemFont, "Helvetica Neue", Helvetica, Arial, sans-serif;
      --mono: "JetBrains Mono", "SF Mono", "Menlo", "Consolas", monospace;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      padding: 0;
      font-family: var(--sans);
      background-color: var(--paper);
      color: var(--ink);
      -webkit-font-smoothing: antialiased;
    }}

    /* Editorial Masthead */
    .masthead {{
      background: var(--paper);
      border-bottom: 2px solid var(--rule-dark);
      padding: 20px 28px 18px;
    }}
    .masthead-inner {{
      max-width: 1360px;
      margin: 0 auto;
    }}
    .masthead-meta {{
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      font-family: var(--mono);
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--ink-secondary);
      padding-bottom: 10px;
      border-bottom: 1px solid var(--rule);
      margin-bottom: 14px;
    }}
    .credit-pill {{
      background: var(--ink);
      color: var(--paper);
      padding: 3px 10px;
      border-radius: 2px;
      font-weight: 600;
      letter-spacing: 0.06em;
    }}
    .masthead-main {{
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: flex-end;
      gap: 16px;
    }}
    .masthead h1 {{
      font-family: var(--serif);
      font-size: 34px;
      font-weight: 700;
      letter-spacing: -0.02em;
      line-height: 1.1;
      margin: 0;
      color: var(--ink);
    }}
    .masthead-sub {{
      margin: 6px 0 0;
      font-family: var(--serif);
      font-style: italic;
      font-size: 15.5px;
      color: var(--ink-secondary);
    }}
    .masthead-actions {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }}

    /* Layout Grid */
    .workspace-grid {{
      max-width: 1360px;
      margin: 24px auto 40px;
      padding: 0 28px;
      display: grid;
      grid-template-columns: 1.12fr 0.88fr;
      gap: 28px;
      align-items: start;
    }}
    @media (max-width: 1024px) {{
      .workspace-grid {{ grid-template-columns: 1fr; }}
    }}

    /* Editorial Section Cards */
    .ed-card {{
      background: var(--surface);
      border: 1px solid var(--rule);
      box-shadow: 0 1px 2px rgba(20, 20, 19, 0.04);
      padding: 22px 24px;
    }}
    .ed-section-header {{
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: baseline;
      border-bottom: 1.5px solid var(--ink);
      padding-bottom: 8px;
      margin-bottom: 16px;
      gap: 8px;
    }}
    .ed-section-num {{
      font-family: var(--mono);
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: var(--accent);
      margin-right: 8px;
    }}
    .ed-section-title {{
      font-family: var(--serif);
      font-size: 21px;
      font-weight: 700;
      margin: 0;
      color: var(--ink);
    }}

    /* Typography & Inputs */
    .field-label {{
      display: block;
      font-family: var(--mono);
      font-size: 10.5px;
      font-weight: 700;
      color: var(--ink-secondary);
      margin-bottom: 5px;
      text-transform: uppercase;
      letter-spacing: 0.06em;
    }}
    input[type="text"], input[type="number"], select {{
      width: 100%;
      padding: 8px 10px;
      border: 1px solid var(--rule);
      border-radius: 2px;
      font-family: var(--sans);
      font-size: 13px;
      color: var(--ink);
      background: #faf9f6;
      transition: border-color 0.15s, background 0.15s;
    }}
    input[type="text"]:focus, input[type="number"]:focus, select:focus {{
      outline: none;
      border-color: var(--ink);
      background: #ffffff;
    }}

    /* Buttons */
    .btn {{
      cursor: pointer;
      border: 1px solid var(--ink);
      border-radius: 2px;
      padding: 8px 14px;
      font-family: var(--sans);
      font-size: 12.5px;
      font-weight: 600;
      letter-spacing: 0.01em;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s;
      white-space: nowrap;
    }}
    .btn-ink {{
      background: var(--ink);
      color: var(--paper);
      border-color: var(--ink);
    }}
    .btn-ink:hover {{ background: #2c2b29; }}
    .btn-accent {{
      background: var(--accent);
      color: #ffffff;
      border-color: var(--accent);
    }}
    .btn-accent:hover {{ background: #7f1616; }}
    .btn-paper {{
      background: var(--paper);
      color: var(--ink);
      border-color: var(--rule);
    }}
    .btn-paper:hover {{
      background: var(--paper-deep);
      border-color: var(--ink-secondary);
    }}
    .btn-blue {{
      background: var(--blue-editorial);
      color: #ffffff;
      border-color: var(--blue-editorial);
    }}
    .btn-blue:hover {{ background: #152943; }}

    /* Callout / CAS Box */
    .cas-box {{
      background: var(--blue-soft);
      border: 1px solid #c5d4e6;
      border-left: 3.5px solid var(--blue-editorial);
      padding: 14px;
      margin-bottom: 18px;
    }}
    .cas-help-note {{
      font-size: 11.5px;
      color: var(--ink-secondary);
      margin-top: 6px;
      line-height: 1.4;
    }}
    .chip-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 5px;
      margin-top: 8px;
      align-items: center;
    }}
    .chip {{
      cursor: pointer;
      background: #ffffff;
      border: 1px solid var(--rule);
      padding: 3px 9px;
      font-family: var(--mono);
      font-size: 11px;
      color: var(--ink);
      transition: all 0.12s;
    }}
    .chip:hover {{
      background: var(--ink);
      color: var(--paper);
      border-color: var(--ink);
    }}

    /* Component Rows */
    .comp-row {{
      display: grid;
      grid-template-columns: 1.85fr 0.65fr 0.7fr auto;
      gap: 8px;
      align-items: center;
      margin-bottom: 8px;
    }}
    .custom-chem-box {{
      grid-column: 1 / -1;
      background: var(--paper);
      border: 1px dashed var(--ink-muted);
      padding: 12px;
      margin-bottom: 8px;
      font-size: 12px;
    }}

    /* Desk Specimen Stage */
    .specimen-stage {{
      background: var(--paper-deep);
      border: 1px solid var(--rule);
      padding: 18px;
      position: relative;
    }}
    .specimen-meta-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-family: var(--mono);
      font-size: 11px;
      color: var(--ink-secondary);
      margin-bottom: 10px;
      padding-bottom: 6px;
      border-bottom: 1px dashed var(--rule);
    }}
    .svg-paper-mount {{
      background: #ffffff;
      padding: 8px;
      box-shadow: 0 4px 16px rgba(20, 20, 19, 0.08);
      border: 1px solid #dcd7ca;
    }}

    .audit-panel {{
      background: var(--paper);
      border-top: 1.5px solid var(--ink);
      padding: 12px 14px;
      font-size: 12px;
      color: var(--ink-secondary);
      margin-top: 16px;
    }}
    .audit-panel ul {{
      margin: 6px 0 0;
      padding-left: 18px;
      font-family: var(--mono);
      font-size: 11.2px;
      line-height: 1.5;
    }}

    .picto-toggles {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-top: 8px;
    }}
    .picto-btn {{
      cursor: pointer;
      border: 1px solid var(--rule);
      background: var(--paper);
      padding: 4px 9px;
      font-family: var(--mono);
      font-size: 11px;
      font-weight: 600;
      color: var(--ink-secondary);
    }}
    .picto-btn.active {{
      background: var(--accent-soft);
      border-color: var(--accent);
      color: var(--accent);
    }}

    /* Print Queue Section */
    .queue-section {{
      max-width: 1360px;
      margin: 0 auto 48px;
      padding: 0 28px;
    }}
    .queue-grid {{
      display: flex;
      flex-wrap: wrap;
      gap: 16px;
      margin-top: 16px;
    }}
    .queue-card {{
      background: #ffffff;
      border: 1px solid var(--rule);
      padding: 12px;
      width: calc(50% - 8px);
    }}
    .queue-card-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-family: var(--mono);
      font-size: 11px;
      color: var(--ink-secondary);
      margin-bottom: 8px;
      padding-bottom: 6px;
      border-bottom: 1px solid var(--paper-deep);
    }}

    /* Editorial Colophon Footer */
    .colophon {{
      max-width: 1360px;
      margin: 40px auto 32px;
      padding: 20px 28px 0;
      border-top: 2px solid var(--ink);
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      font-size: 12.5px;
      color: var(--ink-secondary);
    }}
    .colophon strong {{
      color: var(--ink);
      font-family: var(--serif);
      font-size: 14.5px;
    }}

    .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }}
    .grid-3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }}

    @media print {{
      body {{ background: #fff; }}
      .masthead, .no-print, .colophon {{ display: none !important; }}
      .queue-section {{ margin: 0; padding: 0; max-width: 100%; }}
      .queue-grid {{
        display: flex;
        flex-wrap: wrap;
        gap: 4mm;
        margin: 0;
      }}
      .queue-card {{
        border: none;
        box-shadow: none;
        padding: 0;
        page-break-inside: avoid;
        break-inside: avoid;
      }}
      .queue-card-bar {{ display: none !important; }}
    }}
  </style>
</head>
<body>
  <!-- Editorial Masthead -->
  <header class="masthead">
    <div class="masthead-inner">
      <div class="masthead-meta">
        <span>LABORATORY SAFETY &amp; CHEMICAL HYGIENE MONOGRAPH • UNECE GHS / EU CLP (EC) NO 1272/2008</span>
        <span class="credit-pill">CREDIT: DR. KATHIRVEL ALAGESAN</span>
      </div>
      <div class="masthead-main">
        <div>
          <h1>Laboratory GHS Pictogram &amp; Mixture Label Studio</h1>
          <p class="masthead-sub">Composition-driven hazard classification, live NCBI PubChem CAS lookup, and calibrated physical label press. Conceived &amp; developed by <strong>Dr. Kathirvel Alagesan</strong>.</p>
        </div>
        <div class="masthead-actions">
          <button class="btn btn-paper" onclick="loadAll18PresetsToQueue()">📚 Load All 18 Standard Buffers to Sheet</button>
          <button class="btn btn-paper" onclick="addCurrentToQueue()">➕ Queue Current Label (<span id="queueCount">0</span>)</button>
          <button class="btn btn-ink" onclick="printCurrentOrQueue()">🖨️ Print Label / Sheet</button>
        </div>
      </div>
    </div>
  </header>

  <div class="workspace-grid no-print">
    <!-- Left Column: Formulation & CAS Registry -->
    <div class="ed-card">
      <div class="ed-section-header">
        <div>
          <span class="ed-section-num">Section I</span>
          <h2 class="ed-section-title" style="display:inline;">Formulation &amp; Reagent Registry</h2>
        </div>
        <select id="modeSelect" onchange="recalculate()" style="width:auto; font-family:var(--mono); font-size:11px; font-weight:700;">
          <option value="reg">Classification: Strict CLP Cutoffs</option>
          <option value="ehs">Classification: Conservative Lab EHS</option>
        </select>
      </div>

      <!-- Layout & Physical Print Size -->
      <div class="grid-2" style="margin-bottom:16px; background:var(--paper); padding:12px; border:1px solid var(--rule);">
        <div>
          <label class="field-label">Label Format Style</label>
          <select id="layoutSelect" onchange="renderPreview()" style="font-weight:600;">
            <option value="minimal" selected>Minimal Bench Label (Pictograms + Date / Prepared By / Notes)</option>
            <option value="full">Full Regulatory Label (Includes H &amp; P Statements)</option>
          </select>
        </div>
        <div>
          <label class="field-label">Calibrated Physical Print Size</label>
          <select id="sizePreset" onchange="onSizeChange()" style="font-weight:600;">
            <option value="100x60">Large Bottle (500–1000 mL): 100 × 60 mm (3.94" × 2.36")</option>
            <option value="80x45" selected>Medium Bottle (250–500 mL): 80 × 45 mm (3.15" × 1.77")</option>
            <option value="60x35">Small Bottle / 50 mL Falcon: 60 × 35 mm (2.36" × 1.38")</option>
            <option value="45x25">Mini 15 mL Tube / Vial: 45 × 25 mm (1.77" × 0.98")</option>
            <option value="custom">Custom Dimensions (mm)...</option>
          </select>
          <div id="customSizeBox" style="display:none; gap:6px; align-items:center; margin-top:6px;">
            <input type="number" id="customW" value="80" min="20" max="200" oninput="renderPreview()" placeholder="W (mm)" />
            <span>×</span>
            <input type="number" id="customH" value="45" min="15" max="150" oninput="renderPreview()" placeholder="H (mm)" />
            <span style="font-family:var(--mono); font-size:11px;">mm</span>
          </div>
        </div>
      </div>

      <!-- Search by CAS Number or Chemical Name -->
      <div class="cas-box">
        <label class="field-label" style="color:var(--blue-editorial);">🔎 Search &amp; Lookup by CAS Number (Built-in Registry + Live NCBI PubChem 115M+ Database)</label>
        <div style="display:grid; grid-template-columns: 1.5fr 0.55fr 0.65fr; gap:6px; align-items:center; margin-bottom:8px;">
          <input type="text" id="casSearchInput" placeholder="Enter CAS (e.g. 67-56-1, 123-91-1, 109-89-7) or Chemical Name"
                 oninput="onCasTyping()"
                 onkeydown="if(event.key==='Enter') lookupCasAndAdd(true)"
                 style="background:#fff;" />
          <input type="number" id="casSearchAmt" value="100" min="0" step="any" title="Concentration" style="background:#fff;" />
          <select id="casSearchUnit" style="background:#fff;">
            <option value="% v/v">% (v/v)</option>
            <option value="% w/v">% (w/v)</option>
            <option value="% w/w">% (w/w)</option>
            <option value="M">M (mol/L)</option>
            <option value="mM">mM (mmol/L)</option>
          </select>
        </div>
        <div style="display:flex; flex-wrap:wrap; gap:8px; align-items:center;">
          <button class="btn btn-blue" style="padding:6px 12px; font-size:12px;" onclick="lookupCasAndAdd(true)">
            New Single-Chemical Label
          </button>
          <button class="btn btn-paper" style="padding:6px 12px; font-size:12px; background:#fff;" onclick="lookupCasAndAdd(false)">
            + Add Ingredient to Current Mixture
          </button>
          <span class="cas-help-note" style="margin:0;">
            <strong>Single-Chemical</strong> replaces the recipe below; <strong>+ Add Ingredient</strong> appends it to your buffer mixture.
          </span>
        </div>
        <div class="chip-row">
          <span style="font-family:var(--mono); font-size:10.5px; font-weight:700; color:var(--blue-editorial);">SAMPLE CAS:</span>
          <button class="chip" onclick="quickCasTest('75-05-8', 100, '% v/v')">75-05-8 (ACN)</button>
          <button class="chip" onclick="quickCasTest('67-56-1', 100, '% v/v')">67-56-1 (Methanol)</button>
          <button class="chip" onclick="quickCasTest('76-05-1', 1, '% v/v')">76-05-1 (1% TFA)</button>
          <button class="chip" onclick="quickCasTest('123-91-1', 100, '% v/v')">123-91-1 (1,4-Dioxane)</button>
          <button class="chip" onclick="quickCasTest('1239-45-8', 1, '% w/v')">1239-45-8 (EtBr)</button>
          <button class="chip" onclick="quickCasTest('7664-39-3', 5, '% v/v')">7664-39-3 (5% HF)</button>
          <button class="chip" onclick="quickCasTest('109-89-7', 100, '% v/v')">109-89-7 (Live PubChem)</button>
        </div>
        <div id="casLookupCard" style="display:none; margin-top:10px; background:#ffffff; border:1px solid var(--rule); padding:10px 12px; font-size:12px;"></div>
      </div>

      <!-- Standard 18 Presets + Formula Bar -->
      <div class="grid-2" style="margin-bottom:12px;">
        <div>
          <label class="field-label">Standard LC-MS &amp; Solvent Presets (18)</label>
          <select id="preset18Select" onchange="onPickStandard18(this.value)">
            <option value="">— Select from 18 Standard Buffers &amp; Solvents —</option>
            <optgroup label="Group 1: Aqueous TFA &amp; FA Buffers">
              <option value="1% TFA|TFA, 1%">1. TFA, 1%</option>
              <option value="0.1% TFA|TFA, 0.1%">2. TFA, 0.1%</option>
              <option value="1% FA|FA, 1%">3. FA, 1%</option>
              <option value="0.1% FA|FA, 0.1%">4. FA, 0.1%</option>
            </optgroup>
            <optgroup label="Group 2: 80% ACN Mobile Phases">
              <option value="1% TFA, 80% ACN|1% TFA, 80% ACN">5. 1% TFA, 80% ACN</option>
              <option value="0.1% TFA, 80% ACN|0.1% TFA, 80% ACN">6. 0.1% TFA, 80% ACN</option>
              <option value="1% FA, 80% ACN|1% FA, 80% ACN">7. 1% FA, 80% ACN</option>
              <option value="0.1% FA, 80% ACN|0.1% FA, 80% ACN">8. 0.1% FA, 80% ACN</option>
            </optgroup>
            <optgroup label="Group 3: 10% DMSO + Acid Buffers">
              <option value="10% DMSO, 1% TFA|10% DMSO + 1% TFA">9. 10% DMSO + 1% TFA</option>
              <option value="10% DMSO, 0.1% TFA|10% DMSO + 0.1% TFA">10. 10% DMSO + 0.1% TFA</option>
              <option value="10% DMSO, 1% FA|10% DMSO + 1% FA">11. 10% DMSO + 1% FA</option>
              <option value="10% DMSO, 0.1% FA|10% DMSO + 0.1% FA">12. 10% DMSO + 0.1% FA</option>
            </optgroup>
            <optgroup label="Group 4: Pure Solvents &amp; Cellulose">
              <option value="100% ACN|100% ACN">13. 100% ACN</option>
              <option value="100% ACN|Acetonitrile">14. Acetonitrile</option>
              <option value="100% Ethanol|Ethanol">15. Ethanol</option>
              <option value="100% Methanol|Methanol">16. Methanol</option>
              <option value="100% Isopropanol|Isopropanol">17. Isopropanol</option>
              <option value="100% Cellulose|Cellulose">18. Cellulose</option>
            </optgroup>
          </select>
        </div>
        <div>
          <label class="field-label">Free-Text Formula Parser (Names or CAS)</label>
          <div style="display:flex; gap:6px;">
            <input type="text" id="formulaInput" value="1% TFA, 80% ACN" placeholder="e.g. 6 M GdnHCl, 50 mM Tris  or  80% 75-05-8" onkeydown="if(event.key==='Enter') parseFormulaInput()" />
            <button class="btn btn-ink" style="padding:7px 12px;" onclick="parseFormulaInput()">Parse</button>
          </div>
        </div>
      </div>

      <!-- Active Mixture Ingredients Table -->
      <div style="display:flex; justify-content:space-between; align-items:center; margin: 14px 0 8px;">
        <span class="field-label" style="margin:0;">Active Solution Ingredients (Aqueous balance = H₂O)</span>
        <button class="btn btn-paper" style="padding:4px 10px; font-size:11.5px;" onclick="addRow()">+ Add Ingredient Row</button>
      </div>
      <div id="rowsContainer"></div>

      <hr style="border:none; border-top:1px solid var(--rule); margin:16px 0;" />

      <!-- Label Text & Write-In Metadata -->
      <div class="grid-2" style="margin-bottom:10px;">
        <div>
          <label class="field-label">Bottle / Container Title</label>
          <input type="text" id="titleInput" value="1% TFA, 80% ACN" oninput="renderPreview()" />
        </div>
        <div>
          <label class="field-label">Composition Subtitle</label>
          <input type="text" id="subtitleInput" value="" placeholder="Auto-generated from ingredients if blank" oninput="renderPreview()" />
        </div>
      </div>

      <div class="grid-3">
        <div>
          <label class="field-label">Date Prepared</label>
          <input type="text" id="prepDate" placeholder="e.g. 2026-11-26" oninput="renderPreview()" />
        </div>
        <div>
          <label class="field-label">Prepared By</label>
          <input type="text" id="prepBy" placeholder="Initials / Name" oninput="renderPreview()" />
        </div>
        <div>
          <label class="field-label">Notes</label>
          <input type="text" id="storageNote" placeholder="e.g. RT / Exp 6 mo" oninput="renderPreview()" />
        </div>
      </div>

      <details style="margin-top:14px; font-size:12px;">
        <summary style="cursor:pointer; font-family:var(--mono); font-size:11px; font-weight:700; color:var(--ink-secondary); text-transform:uppercase;">⚙️ Manual Pictogram &amp; Signal Word Override</summary>
        <div style="padding-top:10px;">
          <div style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">
            <label style="font-weight:700; font-size:12px;">Signal Word:</label>
            <select id="overrideSignal" onchange="renderPreview()" style="width:auto;">
              <option value="AUTO">Auto-Calculated from Composition</option>
              <option value="DANGER">DANGER (Red)</option>
              <option value="WARNING">WARNING (Amber)</option>
              <option value="NO SIGNAL WORD">NO SIGNAL WORD (Green / Non-Haz)</option>
            </select>
            <button class="btn btn-paper" style="padding:4px 8px; font-size:11px;" onclick="resetOverrides()">Reset to Auto</button>
          </div>
          <div id="pictoToggles" class="picto-toggles"></div>
        </div>
      </details>
    </div>

    <!-- Right Column: Specimen Preview & CLP Calculation Dossier -->
    <div class="ed-card">
      <div class="ed-section-header">
        <div>
          <span class="ed-section-num">Section II</span>
          <h2 class="ed-section-title" style="display:inline;">Label Specimen Proof</h2>
        </div>
        <div style="display:flex; gap:6px;">
          <button class="btn btn-paper" style="padding:6px 11px; font-size:12px;" onclick="addCurrentToQueue()">➕ Add to Print Sheet</button>
          <button class="btn btn-accent" style="padding:6px 12px; font-size:12px;" onclick="downloadCurrentSVG()">⬇️ Export Vector SVG</button>
        </div>
      </div>

      <div class="specimen-stage">
        <div class="specimen-meta-bar">
          <span>OFFICIAL UNECE VECTOR PICTOGRAMS</span>
          <span id="dimReadout" style="font-weight:700; color:var(--ink);">80 × 45 mm (3.15" × 1.77")</span>
        </div>
        <div id="svgPreviewBox" class="svg-paper-mount"></div>
      </div>

      <div class="audit-panel">
        <div style="font-family:var(--mono); font-size:10.5px; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:var(--ink);">
          CLP Regulation (EC) No 1272/2008 Calculation Dossier
        </div>
        <ul id="auditList"></ul>
      </div>
    </div>
  </div>

  <!-- Section III: Multi-Label Print Sheet Queue -->
  <div class="queue-section">
    <div class="ed-card no-print" style="margin-bottom:14px;">
      <div style="display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:12px;">
        <div>
          <span class="ed-section-num">Section III</span>
          <h2 class="ed-section-title" style="display:inline;">Press Sheet Queue (<span id="queueHeaderCount">0</span> Labels)</h2>
          <p style="margin:4px 0 0; font-size:12.5px; color:var(--ink-secondary);">
            Queue custom mixtures or load all 18 standard buffers, then print at <strong>100% (Actual Size)</strong> for exact millimeter output.
          </p>
        </div>
        <div style="display:flex; flex-wrap:wrap; gap:8px;">
          <button class="btn btn-paper" onclick="loadAll18PresetsToQueue()">📚 Add All 18 Standard Buffers</button>
          <button class="btn btn-paper" onclick="clearQueue()">🗑️ Clear Sheet</button>
          <button class="btn btn-ink" onclick="window.print()">🖨️ Print Sheet / Save as PDF</button>
        </div>
      </div>
    </div>
    <div id="queueGrid" class="queue-grid"></div>
  </div>

  <!-- Editorial Colophon Footer -->
  <footer class="colophon no-print">
    <div>
      <strong>Dr. Kathirvel Alagesan</strong> — Creator &amp; Scientific Author<br/>
      <span>Laboratory GHS Pictogram &amp; Mixture Label Studio • Open-Source Client-Side Web Application</span>
    </div>
    <div style="font-family:var(--mono); font-size:11px; text-align:right;">
      UNECE GHS Rev. 10 &amp; EU CLP Annex I/VI Threshold Engine<br/>
      Vector Pictograms: Official UNECE / ISO 7010 • Live CAS API: NCBI PubChem PUG-REST
    </div>
  </footer>

  <script>
    const SYMBOLS = {symbols_json};
    const CHEM_DB = {chemdb_json};

    const PRESET_18_LIST = [
      ["1% TFA", "TFA, 1%"],
      ["0.1% TFA", "TFA, 0.1%"],
      ["1% FA", "FA, 1%"],
      ["0.1% FA", "FA, 0.1%"],
      ["1% TFA, 80% ACN", "1% TFA, 80% ACN"],
      ["0.1% TFA, 80% ACN", "0.1% TFA, 80% ACN"],
      ["1% FA, 80% ACN", "1% FA, 80% ACN"],
      ["0.1% FA, 80% ACN", "0.1% FA, 80% ACN"],
      ["10% DMSO, 1% TFA", "10% DMSO + 1% TFA"],
      ["10% DMSO, 0.1% TFA", "10% DMSO + 0.1% TFA"],
      ["10% DMSO, 1% FA", "10% DMSO + 1% FA"],
      ["10% DMSO, 0.1% FA", "10% DMSO + 0.1% FA"],
      ["100% ACN", "100% ACN"],
      ["100% ACN", "Acetonitrile"],
      ["100% Ethanol", "Ethanol"],
      ["100% Methanol", "Methanol"],
      ["100% Isopropanol", "Isopropanol"],
      ["100% Cellulose", "Cellulose"]
    ];

    let rows = [];
    let manualPictos = null;
    let printQueue = [];
    let currentCalculated = null;

    // Load cached PubChem CAS entries from localStorage
    try {{
      const cached = JSON.parse(localStorage.getItem('ghs_pubchem_cas_cache_v1') || '[]');
      for (const c of cached) {{
        if (!CHEM_DB.some(x => x.key === c.key || x.cas === c.cas)) {{
          CHEM_DB.push(c);
        }}
      }}
    }} catch (e) {{}}

    function saveToCasCache(chemObj) {{
      try {{
        const cached = JSON.parse(localStorage.getItem('ghs_pubchem_cas_cache_v1') || '[]');
        const filtered = cached.filter(x => x.key !== chemObj.key && x.cas !== chemObj.cas);
        filtered.push(chemObj);
        localStorage.setItem('ghs_pubchem_cas_cache_v1', JSON.stringify(filtered));
      }} catch (e) {{}}
    }}

    function esc(s) {{
      return String(s || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
    }}

    function getDims() {{
      const preset = document.getElementById('sizePreset').value;
      if (preset === 'custom') {{
        const w = parseFloat(document.getElementById('customW').value) || 80;
        const h = parseFloat(document.getElementById('customH').value) || 45;
        return {{ w, h }};
      }}
      const [w, h] = preset.split('x').map(Number);
      return {{ w, h }};
    }}

    function onSizeChange() {{
      const preset = document.getElementById('sizePreset').value;
      document.getElementById('customSizeBox').style.display = preset === 'custom' ? 'flex' : 'none';
      if (preset !== 'custom') {{
        const [w, h] = preset.split('x').map(Number);
        document.getElementById('customW').value = w;
        document.getElementById('customH').value = h;
      }}
      renderPreview();
    }}

    function onPickStandard18(val) {{
      if (!val) return;
      const [formula, title] = val.split('|');
      loadExample(formula, title);
    }}

    function findChemical(q) {{
      const s = String(q || '').trim().toLowerCase();
      if (!s) return null;
      for (const ch of CHEM_DB) {{
        if (s === ch.cas.toLowerCase() || s === ch.key.toLowerCase() || s === ch.name.toLowerCase() || (ch.aliases && ch.aliases.includes(s))) return ch;
      }}
      for (const ch of CHEM_DB) {{
        if (ch.cas.toLowerCase().includes(s)) return ch;
        for (const al of (ch.aliases || [])) {{
          if (s.includes(al) || al.includes(s)) return ch;
        }}
      }}
      return null;
    }}

    function showCasCard(ch, sourceLabel = 'Built-in CLP Registry') {{
      const box = document.getElementById('casLookupCard');
      if (!ch) {{
        box.style.display = 'none';
        return;
      }}
      const pureBadges = [];
      if (ch.ox_min) pureBadges.push('GHS03');
      if (ch.flam_min_cat2 || ch.flam_min_cat3) pureBadges.push('GHS02');
      if (ch.corr_1_min || ch.eye_1_min) pureBadges.push('GHS05');
      if (ch.acute_3_min) pureBadges.push('GHS06');
      else if (ch.acute_4_min || ch.skin_2_min || ch.eye_2_min || ch.stot_3_min || ch.sens_skin_min) pureBadges.push('GHS07');
      if (ch.stot_1_min || ch.stot_2_min) pureBadges.push('GHS08');
      if (ch.aquat_min) pureBadges.push('GHS09');

      const miniDiamonds = pureBadges.length
        ? pureBadges.map(code => `<svg width="28" height="28" viewBox="${{SYMBOLS[code].viewBox}}" style="vertical-align:middle; margin-right:3px;">${{SYMBOLS[code].svg}}</svg>`).join('')
        : '<span style="color:#14532d; font-family:var(--mono); font-size:11px; font-weight:700;">NON-HAZARDOUS</span>';

      box.style.display = 'block';
      box.innerHTML = `
        <div style="display:flex; flex-wrap:wrap; justify-content:space-between; align-items:center; gap:8px;">
          <div>
            <strong style="font-family:var(--serif); font-size:15px; color:var(--ink);">${{esc(ch.name)}}</strong>
            <span style="background:var(--ink); color:var(--paper); font-family:var(--mono); font-weight:700; padding:2px 6px; font-size:10.5px; margin-left:6px;">CAS ${{esc(ch.cas)}}</span>
            <div style="color:var(--ink-secondary); font-family:var(--mono); font-size:11px; margin-top:3px;">Formula: ${{esc(ch.formula || 'N/A')}} • MW: ${{ch.mw || 100}} g/mol • Source: ${{esc(sourceLabel)}}</div>
          </div>
          <div>${{miniDiamonds}}</div>
        </div>
      `;
    }}

    function onCasTyping() {{
      const q = document.getElementById('casSearchInput').value.trim();
      if (!q) {{
        document.getElementById('casLookupCard').style.display = 'none';
        return;
      }}
      const localMatch = findChemical(q);
      if (localMatch) {{
        showCasCard(localMatch, localMatch.fromPubChem ? 'Cached PubChem GHS' : 'Built-in CLP Registry');
      }} else {{
        const box = document.getElementById('casLookupCard');
        box.style.display = 'block';
        box.innerHTML = `<span style="color:var(--ink-secondary);">CAS/Name <strong>"${{esc(q)}}"</strong> is not in the offline table — click <strong>New Single-Chemical Label</strong> or <strong>+ Add Ingredient</strong> to fetch live GHS classification from <strong>NCBI PubChem</strong>.</span>`;
      }}
    }}

    function mapPubChemGhsToEntry(queryStr, cid, title, formula, mw, ghsJsonText) {{
      const pictos = [...new Set(ghsJsonText.match(/GHS0[1-9]/g) || [])];
      const hCodes = [...new Set(ghsJsonText.match(/H[234]\d{{2}}[A-Za-z+]*/g) || [])];
      const hasH = (prefixList) => hCodes.some(h => prefixList.some(p => h.startsWith(p)));

      const isCas = /^\d{{2,7}}-\d{{2}}-\d$/.test(queryStr.trim());
      const casNum = isCas ? queryStr.trim() : (ghsJsonText.match(/\b\d{{2,7}}-\d{{2}}-\d\b/) || [queryStr])[0];
      const cleanKey = title.replace(/[^a-zA-Z0-9_-]/g, '');

      const entry = {{
        key: cleanKey || `CID_${{cid}}`,
        name: `${{title}}`,
        aliases: [title.toLowerCase(), casNum.toLowerCase(), queryStr.toLowerCase()],
        category: "PubChem CAS Lookup",
        cas: casNum,
        formula: formula || "",
        mw: parseFloat(mw) || 100.0,
        fromPubChem: true,
        p_Codes: ["P280: Wear protective gloves, protective clothing, and eye/face protection."]
      }};

      if (pictos.includes('GHS03') || hasH(['H271','H272'])) entry.ox_min = 50.0;
      if (hasH(['H224','H225'])) {{ entry.flam_min_cat2 = 15.0; entry.flam_min_cat3 = 5.0; entry.p_Codes.unshift("P210: Keep away from heat, hot surfaces, sparks, open flames. No smoking."); }}
      else if (pictos.includes('GHS02') || hasH(['H226','H228'])) {{ entry.flam_min_cat3 = 15.0; entry.p_Codes.unshift("P210: Keep away from heat, sparks, open flames."); }}

      if (pictos.includes('GHS05') || hasH(['H314','H290'])) {{
        entry.corr_1_min = 5.0; entry.eye_1_min = 3.0; entry.skin_2_min = 1.0; entry.eye_2_min = 1.0; entry.ehs_irrit_min = 0.05;
        entry.p_Codes.push("P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes.");
      }} else if (hasH(['H318'])) {{
        entry.eye_1_min = 3.0; entry.eye_2_min = 1.0; entry.ehs_irrit_min = 0.1;
      }}

      if (hasH(['H300','H310','H330'])) {{
        entry.acute_3_min = 1.0; entry.acute_4_min = 0.1;
        entry.acute_h_cat3 = "H300/H310/H330: Fatal if swallowed, in contact with skin, or if inhaled.";
      }} else if (pictos.includes('GHS06') || hasH(['H301','H311','H331'])) {{
        entry.acute_3_min = 10.0; entry.acute_4_min = 2.0;
        entry.acute_h_cat3 = "H301/H311/H331: Toxic if swallowed, in contact with skin, or if inhaled.";
      }} else if (hasH(['H302','H312','H332'])) {{
        entry.acute_4_min = 20.0;
        entry.acute_h_cat4 = "H302/H312/H332: Harmful if swallowed, in contact with skin, or if inhaled.";
      }}

      if (hasH(['H315']) && !entry.skin_2_min) {{ entry.skin_2_min = 10.0; entry.ehs_irrit_min = 0.5; }}
      if (hasH(['H319']) && !entry.eye_2_min) {{ entry.eye_2_min = 10.0; entry.ehs_irrit_min = 0.5; }}
      if (hasH(['H317'])) {{ entry.sens_skin_min = 1.0; }}
      if (hasH(['H335','H336'])) {{
        entry.stot_3_min = 20.0;
        entry.stot_3_h = hasH(['H335']) ? "H335: May cause respiratory irritation." : "H336: May cause drowsiness or dizziness.";
      }}

      if (hasH(['H334','H340','H350','H360'])) {{
        entry.stot_1_min = 0.1;
        entry.stot_h = `H340/H350/H360/H334: CMR or Respiratory Sensitizer (${{hCodes.filter(h=>/^H3[34567]/.test(h)).slice(0,3).join(', ')}}).`;
      }} else if (hasH(['H370','H372'])) {{
        entry.stot_1_min = 10.0; entry.stot_2_min = 1.0;
        entry.stot_h = "H370/H372: Causes damage to organs.";
      }} else if (pictos.includes('GHS08') || hasH(['H341','H351','H361','H371','H373','H304'])) {{
        entry.stot_2_min = 1.0;
        entry.stot_2_h = `H341/H351/H361/H373: Suspected CMR or organ toxicity (${{hCodes.filter(h=>/^H3[04567]/.test(h)).slice(0,3).join(', ')}}).`;
      }}

      if (pictos.includes('GHS09') || hasH(['H400','H410','H411'])) {{
        entry.aquat_min = 2.5;
      }}

      return entry;
    }}

    async function fetchPubChemCas(queryStr) {{
      const q = encodeURIComponent(queryStr.trim());
      let propResp = await fetch(`https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/${{q}}/property/Title,MolecularFormula,MolecularWeight/JSON`);
      if (!propResp.ok) {{
        propResp = await fetch(`https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/xref/RN/${{q}}/property/Title,MolecularFormula,MolecularWeight/JSON`);
      }}
      if (!propResp.ok) throw new Error(`Could not resolve CAS/Name "${{queryStr}}" on PubChem.`);
      const propData = await propResp.json();
      const props = propData.PropertyTable.Properties[0];
      const cid = props.CID;
      const title = props.Title || queryStr;
      const formula = props.MolecularFormula || "";
      const mw = parseFloat(props.MolecularWeight) || 100.0;

      let ghsText = "";
      try {{
        const ghsResp = await fetch(`https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/${{cid}}/JSON?heading=GHS+Classification`);
        if (ghsResp.ok) {{
          ghsText = await ghsResp.text();
        }}
      }} catch (e) {{}}

      const entry = mapPubChemGhsToEntry(queryStr, cid, title, formula, mw, ghsText);
      CHEM_DB.push(entry);
      saveToCasCache(entry);
      return entry;
    }}

    async function lookupCasAndAdd(replaceAll = false) {{
      const q = document.getElementById('casSearchInput').value.trim();
      if (!q) return;
      const amt = parseFloat(document.getElementById('casSearchAmt').value) || 100;
      const unit = document.getElementById('casSearchUnit').value;

      let ch = findChemical(q);
      if (!ch) {{
        const box = document.getElementById('casLookupCard');
        box.style.display = 'block';
        box.innerHTML = `<span style="color:var(--blue-editorial); font-weight:700;">⏳ Querying NCBI PubChem for "${{esc(q)}}" (CID, MW &amp; GHS Classification)...</span>`;
        try {{
          ch = await fetchPubChemCas(q);
        }} catch (err) {{
          box.innerHTML = `<span style="color:var(--accent); font-weight:700;">⚠️ ${{esc(err.message)}} — Added as a custom row so you can toggle hazards manually.</span>`;
          if (replaceAll) rows = [];
          rows.push({{
            chemKey: '__CUSTOM__',
            amount: amt,
            unit: unit,
            customName: q,
            customCas: q,
            customMw: 100,
            customHazards: {{ flam2: false, corr1: false, acute3: false, irrit2: true, stot1: false, aquat: false }}
          }});
          renderRows();
          recalculate();
          return;
        }}
      }}

      showCasCard(ch, ch.fromPubChem ? 'Live PubChem GHS Classification' : 'Built-in CLP Registry');
      if (replaceAll) {{
        rows = [{{ chemKey: ch.key, amount: amt, unit: unit }}];
        document.getElementById('titleInput').value = amt >= 99.9 && unit.startsWith('%') ? ch.name : `${{amt}}${{unit.replace(' ','')}} ${{ch.name}}`;
      }} else {{
        rows.push({{ chemKey: ch.key, amount: amt, unit: unit }});
        document.getElementById('titleInput').value = rows.map(r => {{
          const c = CHEM_DB.find(x => x.key === r.chemKey);
          const nm = c ? c.key : (r.customName || 'Custom');
          return r.unit.startsWith('%') ? `${{r.amount}}% ${{nm}}` : `${{r.amount}} ${{r.unit}} ${{nm}}`;
        }}).join(', ');
      }}
      document.getElementById('subtitleInput').value = '';
      resetOverrides(false);
      renderRows();
      recalculate();
    }}

    function quickCasTest(cas, amt, unit) {{
      document.getElementById('casSearchInput').value = cas;
      document.getElementById('casSearchAmt').value = amt;
      document.getElementById('casSearchUnit').value = unit;
      lookupCasAndAdd(true);
    }}

    function toPct(amount, unit, mw) {{
      const a = parseFloat(amount) || 0;
      const m = parseFloat(mw) || 100;
      if (unit === 'M') return a * (m / 10.0);
      if (unit === 'mM') return a * (m / 10000.0);
      return a;
    }}

    function loadExample(formula, title) {{
      document.getElementById('formulaInput').value = formula;
      document.getElementById('titleInput').value = title || formula;
      document.getElementById('subtitleInput').value = '';
      parseFormulaInput(true);
    }}

    function parseFormulaInput(keepTitle = false) {{
      const raw = document.getElementById('formulaInput').value.trim();
      if (!raw) return;
      if (!keepTitle) {{
        document.getElementById('titleInput').value = raw;
      }}
      let parts = raw.split(/[,;+]+/).map(x => x.trim()).filter(Boolean);
      if (parts.length === 2 && !/\d/.test(parts[0]) && /^[\d.]+\s*(%|M|mM)$/i.test(parts[1])) {{
        parts = [`${{parts[1]}} ${{parts[0]}}`];
      }}

      rows = [];
      for (const part of parts) {{
        const m1 = part.match(/^([\d.]+)\s*(%\s*[vw]\/[vw]|%|mM|M)\s+(.+)$/i);
        const m2 = part.match(/^(.+?)\s+([\d.]+)\s*(%\s*[vw]\/[vw]|%|mM|M)$/i);
        let amt = 100, unit = '% v/v', name = part;
        if (m1) {{
          amt = parseFloat(m1[1]);
          unit = m1[2].toUpperCase() === 'MM' ? 'mM' : (m1[2].toUpperCase() === 'M' ? 'M' : '% v/v');
          name = m1[3].trim();
        }} else if (m2) {{
          name = m2[1].trim();
          amt = parseFloat(m2[2]);
          unit = m2[3].toUpperCase() === 'MM' ? 'mM' : (m2[3].toUpperCase() === 'M' ? 'M' : '% v/v');
        }}
        const ch = findChemical(name);
        if (ch) {{
          rows.push({{ chemKey: ch.key, amount: amt, unit: unit }});
        }} else {{
          const rowIdx = rows.length;
          rows.push({{
            chemKey: '__CUSTOM__',
            amount: amt,
            unit: unit,
            customName: name,
            customCas: name,
            customMw: 100,
            customHazards: {{ flam2: false, corr1: false, acute3: false, irrit2: true, stot1: false, aquat: false }}
          }});
          fetchPubChemCas(name).then(entry => {{
            if (rows[rowIdx] && rows[rowIdx].customName === name) {{
              rows[rowIdx] = {{ chemKey: entry.key, amount: amt, unit: unit }};
              showCasCard(entry, 'Auto-Resolved via Live PubChem GHS');
              renderRows();
              recalculate();
            }}
          }}).catch(() => {{}});
        }}
      }}
      resetOverrides(false);
      renderRows();
      recalculate();
    }}

    function addRow() {{
      rows.push({{ chemKey: 'ACN', amount: 10, unit: '% v/v' }});
      renderRows();
      recalculate();
    }}

    function removeRow(idx) {{
      rows.splice(idx, 1);
      renderRows();
      recalculate();
    }}

    function onRowChange(idx, field, val) {{
      if (field === 'amount') rows[idx].amount = parseFloat(val) || 0;
      else if (field === 'chemKey') {{
        rows[idx].chemKey = val;
        if (val === '__CUSTOM__' && !rows[idx].customName) {{
          rows[idx].customName = 'Custom Reagent';
          rows[idx].customCas = 'N/A';
          rows[idx].customMw = 100;
          rows[idx].customHazards = {{ flam2: false, corr1: false, acute3: false, irrit2: true, stot1: false, aquat: false }};
        }}
      }} else {{
        rows[idx][field] = val;
      }}
      renderRows();
      recalculate();
    }}

    function onCustomHazChange(idx, hkey, checked) {{
      rows[idx].customHazards[hkey] = checked;
      recalculate();
    }}

    function renderRows() {{
      const container = document.getElementById('rowsContainer');
      const categories = [...new Set(CHEM_DB.map(c => c.category))];

      container.innerHTML = rows.map((r, idx) => {{
        const optGroups = categories.map(cat => {{
          const opts = CHEM_DB.filter(c => c.category === cat).map(c =>
            `<option value="${{c.key}}" ${{r.chemKey === c.key ? 'selected' : ''}}>${{esc(c.name)}} [CAS ${{c.cas}}]</option>`
          ).join('');
          return `<optgroup label="${{esc(cat)}}">${{opts}}</optgroup>`;
        }}).join('');

        let customBox = '';
        if (r.chemKey === '__CUSTOM__') {{
          const hz = r.customHazards || {{}};
          customBox = `<div class="custom-chem-box">
            <div style="display:grid; grid-template-columns: 1.5fr 1fr 0.8fr; gap:8px; margin-bottom:8px;">
              <div>
                <label class="field-label">Custom Chemical Name</label>
                <input type="text" value="${{esc(r.customName)}}" oninput="rows[${{idx}}].customName=this.value; recalculate();" />
              </div>
              <div>
                <label class="field-label">CAS Number</label>
                <input type="text" value="${{esc(r.customCas)}}" oninput="rows[${{idx}}].customCas=this.value; recalculate();" />
              </div>
              <div>
                <label class="field-label">MW (g/mol)</label>
                <input type="number" value="${{r.customMw || 100}}" oninput="rows[${{idx}}].customMw=parseFloat(this.value)||100; recalculate();" />
              </div>
            </div>
            <div style="display:flex; flex-wrap:wrap; gap:10px; align-items:center;">
              <strong>Pure Hazards:</strong>
              <label><input type="checkbox" ${{hz.flam2 ? 'checked' : ''}} onchange="onCustomHazChange(${{idx}},'flam2',this.checked)"/> Flammable (GHS02)</label>
              <label><input type="checkbox" ${{hz.corr1 ? 'checked' : ''}} onchange="onCustomHazChange(${{idx}},'corr1',this.checked)"/> Corrosive ≥5% (GHS05)</label>
              <label><input type="checkbox" ${{hz.acute3 ? 'checked' : ''}} onchange="onCustomHazChange(${{idx}},'acute3',this.checked)"/> Toxic ≥5% (GHS06)</label>
              <label><input type="checkbox" ${{hz.irrit2 ? 'checked' : ''}} onchange="onCustomHazChange(${{idx}},'irrit2',this.checked)"/> Irritant ≥1% (GHS07)</label>
              <label><input type="checkbox" ${{hz.stot1 ? 'checked' : ''}} onchange="onCustomHazChange(${{idx}},'stot1',this.checked)"/> Organ/CMR ≥1% (GHS08)</label>
              <label><input type="checkbox" ${{hz.aquat ? 'checked' : ''}} onchange="onCustomHazChange(${{idx}},'aquat',this.checked)"/> Aquatic ≥2.5% (GHS09)</label>
            </div>
          </div>`;
        }}

        return `<div class="comp-row">
          <select onchange="onRowChange(${{idx}}, 'chemKey', this.value)">
            ${{optGroups}}
            <optgroup label="Custom">
              <option value="__CUSTOM__" ${{r.chemKey === '__CUSTOM__' ? 'selected' : ''}}>➕ Custom Chemical (Specify Hazards)...</option>
            </optgroup>
          </select>
          <input type="number" step="any" min="0" value="${{r.amount}}" oninput="rows[${{idx}}].amount=parseFloat(this.value)||0; recalculate();" />
          <select onchange="onRowChange(${{idx}}, 'unit', this.value)">
            <option value="% v/v" ${{r.unit === '% v/v' ? 'selected' : ''}}>% (v/v)</option>
            <option value="% w/v" ${{r.unit === '% w/v' ? 'selected' : ''}}>% (w/v)</option>
            <option value="% w/w" ${{r.unit === '% w/w' ? 'selected' : ''}}>% (w/w)</option>
            <option value="M" ${{r.unit === 'M' ? 'selected' : ''}}>M (mol/L)</option>
            <option value="mM" ${{r.unit === 'mM' ? 'selected' : ''}}>mM (mmol/L)</option>
          </select>
          <button class="btn btn-paper" style="padding:7px 10px;" onclick="removeRow(${{idx}})" title="Remove ingredient">✕</button>
          ${{customBox}}
        </div>`;
      }}).join('');
    }}

    function resolveRowToChem(r) {{
      if (r.chemKey !== '__CUSTOM__') {{
        const ch = CHEM_DB.find(c => c.key === r.chemKey);
        const pct = toPct(r.amount, r.unit, ch ? ch.mw : 100);
        return {{ chem: ch, amount: r.amount, unit: r.unit, pct: pct, shortName: ch ? ch.key : r.chemKey }};
      }}
      const hz = r.customHazards || {{}};
      const synth = {{
        key: r.customName || 'Custom',
        name: r.customName || 'Custom',
        cas: r.customCas || 'Custom',
        mw: r.customMw || 100,
        flam_min_cat2: hz.flam2 ? 15.0 : null,
        corr_1_min: hz.corr1 ? 5.0 : null,
        eye_1_min: hz.corr1 ? 3.0 : null,
        skin_2_min: (hz.corr1 || hz.irrit2) ? 1.0 : null,
        eye_2_min: (hz.corr1 || hz.irrit2) ? 1.0 : null,
        ehs_irrit_min: (hz.corr1 || hz.irrit2) ? 0.05 : null,
        acute_3_min: hz.acute3 ? 5.0 : null,
        acute_4_min: hz.acute3 ? 1.0 : (hz.irrit2 ? 10.0 : null),
        stot_1_min: hz.stot1 ? 1.0 : null,
        aquat_min: hz.aquat ? 2.5 : null,
        p_Codes: ["P280: Wear protective gloves, protective clothing, and eye/face protection."]
      }};
      const pct = toPct(r.amount, r.unit, synth.mw);
      return {{ chem: synth, amount: r.amount, unit: r.unit, pct: pct, shortName: synth.key }};
    }}

    function recalculate() {{
      const mode = document.getElementById('modeSelect').value;
      const comps = rows.map(resolveRowToChem);

      let pictos = new Set();
      let signalRank = 0;
      let hList = [];
      let pList = [];
      let advisories = [];
      let audit = [];

      const addH = (s) => {{ if (s && !hList.includes(s)) hList.push(s); }};
      const addP = (s) => {{ if (s && !pList.includes(s)) pList.push(s); }};

      let corr1Frac = 0, eye1Frac = 0, skin2Frac = 0, eye2Frac = 0;

      for (const comp of comps) {{
        const ch = comp.chem;
        const pct = comp.pct;
        if (!ch || pct <= 0 || ch.key === 'H2O') continue;
        const cname = ch.key;

        (ch.p_Codes || []).forEach(addP);
        if (ch.advisory) advisories.push(`Advisory (${{cname}}): ${{ch.advisory}}`);

        if (ch.ox_min && pct >= ch.ox_min) {{
          pictos.add('GHS03'); signalRank = Math.max(signalRank, 2);
          addH('H272: May intensify fire; oxidizer.');
          audit.push(`${{cname}} (${{pct.toFixed(2)}}% ≥ ${{ch.ox_min}}%): Oxidizing → GHS03 (Danger, H272)`);
        }}
        if (ch.flam_min_cat2 && pct >= ch.flam_min_cat2) {{
          pictos.add('GHS02'); signalRank = Math.max(signalRank, 2);
          addH('H225: Highly flammable liquid and vapour.');
          audit.push(`${{cname}} (${{pct.toFixed(2)}}% ≥ ${{ch.flam_min_cat2}}%): Flam. Liq. 2 → GHS02 (Danger, H225)`);
        }} else if (ch.flam_min_cat3 && pct >= ch.flam_min_cat3) {{
          pictos.add('GHS02'); signalRank = Math.max(signalRank, 1);
          addH('H226: Flammable liquid and vapour.');
          audit.push(`${{cname}} (${{pct.toFixed(2)}}% ≥ ${{ch.flam_min_cat3}}%): Flam. Liq. 3 → GHS02 (Warning, H226)`);
        }}

        if (ch.acute_3_min && pct >= ch.acute_3_min) {{
          pictos.add('GHS06'); signalRank = Math.max(signalRank, 2);
          addH(ch.acute_h_cat3 || 'H301+H311+H331: Toxic if swallowed, in contact with skin, or if inhaled.');
          audit.push(`${{cname}} (${{pct.toFixed(2)}}% ≥ ${{ch.acute_3_min}}%): Acute Tox. 1–3 → GHS06 (Danger)`);
        }} else if (ch.acute_4_min && pct >= ch.acute_4_min) {{
          pictos.add('GHS07'); signalRank = Math.max(signalRank, 1);
          addH(ch.acute_h_cat4 || 'H302+H312+H332: Harmful if swallowed, in contact with skin, or if inhaled.');
          audit.push(`${{cname}} (${{pct.toFixed(2)}}% ≥ ${{ch.acute_4_min}}%): Acute Tox. 4 → GHS07 (Warning)`);
        }}

        if (ch.corr_1_min) corr1Frac += pct / ch.corr_1_min;
        if (ch.eye_1_min) eye1Frac += pct / ch.eye_1_min;
        if (ch.skin_2_min) skin2Frac += pct / ch.skin_2_min;
        if (ch.eye_2_min) eye2Frac += pct / ch.eye_2_min;

        if (mode === 'ehs') {{
          if (ch.extreme_ph_min && pct >= ch.extreme_ph_min) {{
            corr1Frac = Math.max(corr1Frac, 1.0);
            audit.push(`${{cname}} (${{pct.toFixed(2)}}% ≥ ${{ch.extreme_ph_min}}% in EHS mode): Extreme pH → GHS05 (Danger, H314)`);
          }} else if (ch.ehs_irrit_min && pct >= ch.ehs_irrit_min) {{
            skin2Frac = Math.max(skin2Frac, 1.0);
            eye2Frac = Math.max(eye2Frac, 1.0);
            audit.push(`${{cname}} (${{pct.toFixed(2)}}% ≥ ${{ch.ehs_irrit_min}}% in EHS mode): Precautionary Irritant → GHS07`);
          }}
        }}

        if (ch.stot_1_min && pct >= ch.stot_1_min) {{
          pictos.add('GHS08'); signalRank = Math.max(signalRank, 2);
          addH(ch.stot_h || 'H370/H350/H360: Causes organ damage or CMR hazard.');
          audit.push(`${{cname}} (${{pct.toFixed(2)}}% ≥ ${{ch.stot_1_min}}%): STOT/CMR Cat 1 → GHS08 (Danger)`);
        }} else if (ch.stot_2_min && pct >= ch.stot_2_min) {{
          pictos.add('GHS08'); signalRank = Math.max(signalRank, 1);
          addH(ch.stot_2_h || ch.stot_h || 'H371/H373: May cause organ damage.');
          audit.push(`${{cname}} (${{pct.toFixed(2)}}% ≥ ${{ch.stot_2_min}}%): STOT/CMR Cat 2 → GHS08 (Warning)`);
        }}

        if (ch.stot_3_min && pct >= ch.stot_3_min) {{
          pictos.add('GHS07'); signalRank = Math.max(signalRank, 1);
          addH(ch.stot_3_h || 'H335/H336: May cause respiratory irritation or drowsiness.');
          audit.push(`${{cname}} (${{pct.toFixed(2)}}% ≥ ${{ch.stot_3_min}}%): STOT SE 3 → GHS07 (Warning)`);
        }}

        if (ch.sens_skin_min && pct >= ch.sens_skin_min) {{
          pictos.add('GHS07'); signalRank = Math.max(signalRank, 1);
          addH('H317: May cause an allergic skin reaction.');
          audit.push(`${{cname}} (${{pct.toFixed(2)}}% ≥ ${{ch.sens_skin_min}}%): Skin Sens. 1 → GHS07 (Warning, H317)`);
        }}

        if (ch.aquat_min && pct >= ch.aquat_min) {{
          pictos.add('GHS09');
          addH('H411: Toxic to aquatic life with long lasting effects.');
          audit.push(`${{cname}} (${{pct.toFixed(2)}}% ≥ ${{ch.aquat_min}}%): Aquatic Chronic → GHS09 (H411)`);
        }}
      }}

      if (corr1Frac >= 1.0) {{
        pictos.add('GHS05'); signalRank = Math.max(signalRank, 2);
        addH('H314: Causes severe skin burns and eye damage.');
        audit.push(`Mixture Skin Corrosion additivity sum = ${{corr1Frac.toFixed(2)}} (≥ 1.0) → GHS05 (Danger, H314)`);
      }} else if (eye1Frac >= 1.0) {{
        pictos.add('GHS05'); signalRank = Math.max(signalRank, 2);
        addH('H318: Causes serious eye damage.');
        if (skin2Frac >= 1.0) addH('H315: Causes skin irritation.');
        audit.push(`Mixture Serious Eye Damage additivity sum = ${{eye1Frac.toFixed(2)}} (≥ 1.0) → GHS05 (Danger, H318)`);
      }} else {{
        if (skin2Frac >= 1.0) {{
          pictos.add('GHS07'); signalRank = Math.max(signalRank, 1);
          addH('H315: Causes skin irritation.');
          audit.push(`Mixture Skin Irritation additivity sum = ${{skin2Frac.toFixed(2)}} (≥ 1.0) → GHS07 (Warning, H315)`);
        }}
        if (eye2Frac >= 1.0) {{
          pictos.add('GHS07'); signalRank = Math.max(signalRank, 1);
          addH('H319: Causes serious eye irritation.');
          audit.push(`Mixture Eye Irritation additivity sum = ${{eye2Frac.toFixed(2)}} (≥ 1.0) → GHS07 (Warning, H319)`);
        }}
      }}

      if (pictos.has('GHS06') && pictos.has('GHS07')) {{
        pictos.delete('GHS07');
        audit.push('CLP Precedence (Art. 26): GHS06 present → GHS07 suppressed.');
      }}
      if (pictos.has('GHS05') && pictos.has('GHS07') && mode === 'reg') {{
        const hasOther07 = ['H302','H312','H332','H335','H336','H317'].some(c => hList.join(' ').includes(c));
        if (!hasOther07) {{
          pictos.delete('GHS07');
          audit.push('CLP Precedence (Art. 26): GHS05 present → GHS07 (skin/eye irritation) suppressed.');
        }}
      }}

      advisories.forEach(addH);
      if (!hList.length) {{
        hList.push('Not a hazardous substance or mixture according to GHS / CLP concentration thresholds.');
        audit.push('All components below CLP/GHS hazard concentration thresholds → No GHS pictogram required.');
      }}
      if (!pList.length) {{
        pList.push('P280: Wear standard laboratory eye protection and protective gloves.');
      }}

      let signal = signalRank === 2 ? 'DANGER' : (signalRank === 1 ? 'WARNING' : 'NO SIGNAL WORD');
      const ordered = ['GHS01','GHS02','GHS03','GHS04','GHS05','GHS06','GHS07','GHS08','GHS09'].filter(c => pictos.has(c));

      const casParts = [];
      const compParts = [];
      for (const c of comps) {{
        if (!c.chem || c.amount <= 0) continue;
        if (c.unit.startsWith('%')) compParts.push(`${{c.amount}}${{c.unit.replace(' ','')}} ${{c.shortName}}`);
        else compParts.push(`${{c.amount}} ${{c.unit}} ${{c.shortName}} (~${{c.pct.toFixed(2)}}%)`);
        if (c.chem.cas && !casParts.includes(`${{c.chem.cas}} (${{c.shortName}})`)) {{
          casParts.push(`${{c.chem.cas}} (${{c.shortName}})`);
        }}
      }}

      currentCalculated = {{
        pictograms: ordered,
        signal: signal,
        h_statements: hList.slice(0, 4),
        p_statements: pList.slice(0, 4),
        cas: casParts.length ? 'CAS: ' + casParts.slice(0, 3).join(' | ') : 'Custom Solution',
        composition: compParts.join(', ') + (comps.length === 1 && comps[0].pct >= 99.9 ? '' : ' (balance H₂O)'),
        audit_log: audit
      }};

      renderPictoToggles();
      renderPreview();
    }}

    function toggleManualPicto(code) {{
      if (!manualPictos) {{
        manualPictos = new Set(currentCalculated ? currentCalculated.pictograms : []);
      }}
      if (manualPictos.has(code)) manualPictos.delete(code);
      else manualPictos.add(code);
      renderPictoToggles();
      renderPreview();
    }}

    function resetOverrides(doRender = true) {{
      manualPictos = null;
      document.getElementById('overrideSignal').value = 'AUTO';
      if (doRender) {{
        renderPictoToggles();
        renderPreview();
      }}
    }}

    function renderPictoToggles() {{
      const activeSet = manualPictos || new Set(currentCalculated ? currentCalculated.pictograms : []);
      const holder = document.getElementById('pictoToggles');
      holder.innerHTML = Object.keys(SYMBOLS).map(code => {{
        const isAct = activeSet.has(code);
        return `<button type="button" class="picto-btn ${{isAct ? 'active' : ''}}" onclick="toggleManualPicto('${{code}}')" title="${{esc(SYMBOLS[code].desc)}}">${{esc(SYMBOLS[code].name)}}</button>`;
      }}).join('');
    }}

    function wrapText(text, maxChars = 58) {{
      const words = String(text).split(/\s+/);
      const lines = [];
      let cur = [], curLen = 0;
      for (const w of words) {{
        if (curLen + w.length + (cur.length ? 1 : 0) <= maxChars) {{
          cur.push(w);
          curLen += w.length + (cur.length > 1 ? 1 : 0);
        }} else {{
          lines.push(cur.join(' '));
          cur = [w];
          curLen = w.length;
        }}
      }}
      if (cur.length) lines.push(cur.join(' '));
      return lines;
    }}

    function renderDiamond(code, x, y, size) {{
      const sym = SYMBOLS[code];
      return `<svg x="${{x.toFixed(1)}}" y="${{y.toFixed(1)}}" width="${{size.toFixed(1)}}" height="${{size.toFixed(1)}}" viewBox="${{sym.viewBox}}">${{sym.svg}}</svg>`;
    }}

    function buildCurrentSVG() {{
      if (!currentCalculated) return '';
      const layout = document.getElementById('layoutSelect').value;
      const dims = getDims();
      const mode = document.getElementById('modeSelect').value;
      const overSig = document.getElementById('overrideSignal').value;
      const signal = overSig === 'AUTO' ? currentCalculated.signal : overSig;
      const pictos = manualPictos
        ? ['GHS01','GHS02','GHS03','GHS04','GHS05','GHS06','GHS07','GHS08','GHS09'].filter(c => manualPictos.has(c))
        : currentCalculated.pictograms;

      const title = document.getElementById('titleInput').value || 'Custom Solution';
      const subtitle = document.getElementById('subtitleInput').value || currentCalculated.composition;
      const prepDate = document.getElementById('prepDate').value;
      const prepBy = document.getElementById('prepBy').value;
      const storage = document.getElementById('storageNote').value;

      let sigBg = '#16a34a';
      if (signal === 'DANGER') sigBg = '#d90000';
      else if (signal.includes('WARNING')) sigBg = '#d97706';

      if (layout === 'minimal') {{
        let pictoParts = [];
        if (pictos.length === 1) {{
          pictoParts.push(renderDiamond(pictos[0], 56, 86, 118));
          pictoParts.push(`<text x="115" y="224" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#334155">${{esc(SYMBOLS[pictos[0]].name)}}</text>`);
        }} else if (pictos.length === 2) {{
          pictoParts.push(renderDiamond(pictos[0], 18, 96, 94));
          pictoParts.push(renderDiamond(pictos[1], 116, 96, 94));
          pictoParts.push(`<text x="115" y="216" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#334155">${{pictos.join(' + ')}}</text>`);
        }} else if (pictos.length === 3) {{
          pictoParts.push(renderDiamond(pictos[0], 74, 80, 82));
          pictoParts.push(renderDiamond(pictos[1], 24, 142, 82));
          pictoParts.push(renderDiamond(pictos[2], 124, 142, 82));
          pictoParts.push(`<text x="115" y="242" text-anchor="middle" font-family="Arial, sans-serif" font-size="10.5" font-weight="bold" fill="#334155">${{pictos.join(' + ')}}</text>`);
        }} else if (pictos.length >= 4) {{
          pictoParts.push(renderDiamond(pictos[0], 34, 82, 74));
          pictoParts.push(renderDiamond(pictos[1], 122, 82, 74));
          pictoParts.push(renderDiamond(pictos[2], 34, 156, 74));
          pictoParts.push(renderDiamond(pictos[3], 122, 156, 74));
          pictoParts.push(`<text x="115" y="245" text-anchor="middle" font-family="Arial, sans-serif" font-size="9.5" font-weight="bold" fill="#334155">${{pictos.slice(0,4).join(' + ')}}</text>`);
        }} else {{
          pictoParts.push(`
            <rect x="34" y="112" width="162" height="92" rx="10" fill="#f0fdf4" stroke="#16a34a" stroke-width="2" stroke-dasharray="5,3"/>
            <circle cx="115" cy="142" r="16" fill="#16a34a"/>
            <path d="M108 142 L113.5 147.5 L123 137" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
            <text x="115" y="176" text-anchor="middle" font-family="Arial, sans-serif" font-size="11.5" font-weight="bold" fill="#15803d">NO GHS PICTOGRAM</text>
            <text x="115" y="191" text-anchor="middle" font-family="Arial, sans-serif" font-size="9.5" fill="#166534">Below CLP Cutoff / Non-Haz</text>
          `);
        }}

        return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 270" width="${{dims.w}}mm" height="${{dims.h}}mm" style="width:100%; height:auto; display:block;">
          <rect x="2" y="2" width="476" height="266" rx="10" fill="#ffffff" stroke="#0f172a" stroke-width="2.5"/>
          <path d="M 12 3.5 L 468 3.5 C 473 3.5 476.5 7 476.5 12 L 476.5 13 L 3.5 13 L 3.5 12 C 3.5 7 7 3.5 12 3.5 Z" fill="${{sigBg}}"/>
          <text x="16" y="40" font-family="Arial, sans-serif" font-size="22" font-weight="900" fill="#0f172a">${{esc(title)}}</text>
          <text x="16" y="58" font-family="Arial, sans-serif" font-size="10.8" font-weight="bold" fill="#334155">${{esc(subtitle)}}</text>

          <rect x="332" y="20" width="134" height="32" rx="6" fill="${{sigBg}}"/>
          <text x="399" y="41" text-anchor="middle" font-family="Arial, sans-serif" font-size="13.5" font-weight="900" letter-spacing="0.8" fill="#ffffff">${{esc(signal)}}</text>

          <line x1="12" y1="70" x2="468" y2="70" stroke="#cbd5e1" stroke-width="1.5"/>
          <rect x="12" y="78" width="206" height="178" rx="8" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1.2"/>
          ${{pictoParts.join('')}}

          <rect x="228" y="78" width="238" height="53" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.2"/>
          <text x="238" y="94" font-family="Arial, sans-serif" font-size="9.5" font-weight="800" fill="#475569">DATE PREPARED:</text>
          <text x="238" y="116" font-family="Arial, sans-serif" font-size="13" font-weight="bold" fill="#0f172a">${{esc(prepDate)}}</text>
          <line x1="238" y1="121" x2="454" y2="121" stroke="#cbd5e1" stroke-width="1.2"/>

          <rect x="228" y="140" width="238" height="53" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.2"/>
          <text x="238" y="156" font-family="Arial, sans-serif" font-size="9.5" font-weight="800" fill="#475569">PREPARED BY:</text>
          <text x="238" y="178" font-family="Arial, sans-serif" font-size="13" font-weight="bold" fill="#0f172a">${{esc(prepBy)}}</text>
          <line x1="238" y1="183" x2="454" y2="183" stroke="#cbd5e1" stroke-width="1.2"/>

          <rect x="228" y="203" width="238" height="53" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.2"/>
          <text x="238" y="219" font-family="Arial, sans-serif" font-size="9.5" font-weight="800" fill="#475569">NOTES:</text>
          <text x="238" y="241" font-family="Arial, sans-serif" font-size="13" font-weight="bold" fill="#0f172a">${{esc(storage)}}</text>
          <line x1="238" y1="246" x2="454" y2="246" stroke="#cbd5e1" stroke-width="1.2"/>
        </svg>`;
      }}

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
      }} else if (pictos.length >= 4) {{
        pictoParts.push(renderDiamond(pictos[0], 14, 86, 62));
        pictoParts.push(renderDiamond(pictos[1], 80, 86, 62));
        pictoParts.push(renderDiamond(pictos[2], 14, 150, 62));
        pictoParts.push(renderDiamond(pictos[3], 80, 150, 62));
        pictoParts.push(`<text x="78" y="224" text-anchor="middle" font-family="Arial, sans-serif" font-size="8.5" font-weight="bold" fill="#374151">${{pictos.slice(0,4).join(' + ')}}</text>`);
      }} else {{
        pictoParts.push(`
          <rect x="20" y="115" width="116" height="72" rx="8" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.8" stroke-dasharray="4,3"/>
          <circle cx="78" cy="140" r="13" fill="#16a34a"/>
          <path d="M72 140 L76.5 144.5 L85 135.5" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>
          <text x="78" y="166" text-anchor="middle" font-family="Arial, sans-serif" font-size="9.5" font-weight="bold" fill="#15803d">NO GHS PICTOGRAM</text>
          <text x="78" y="178" text-anchor="middle" font-family="Arial, sans-serif" font-size="8.2" fill="#166534">Below CLP Cutoff / Non-Haz</text>
        `);
      }}

      let textEls = [];
      let y = 96;
      textEls.push(`<text x="166" y="${{y}}" font-family="Arial, sans-serif" font-size="9.5" font-weight="bold" fill="#991b1b">HAZARD STATEMENTS:</text>`);
      y += 12;
      for (const st of currentCalculated.h_statements) {{
        for (const ln of wrapText(st, 58)) {{
          if (y < 178) {{
            textEls.push(`<text x="166" y="${{y}}" font-family="Arial, sans-serif" font-size="8.8" fill="#111827">${{esc(ln)}}</text>`);
            y += 11.2;
          }}
        }}
      }}
      y = Math.max(y + 4, 174);
      textEls.push(`<text x="166" y="${{y}}" font-family="Arial, sans-serif" font-size="9.5" font-weight="bold" fill="#1e40af">PRECAUTIONARY STATEMENTS:</text>`);
      y += 12;
      for (const st of currentCalculated.p_statements) {{
        for (const ln of wrapText(st, 58)) {{
          if (y < 252) {{
            textEls.push(`<text x="166" y="${{y}}" font-family="Arial, sans-serif" font-size="8.6" fill="#1f2937">${{esc(ln)}}</text>`);
            y += 11.0;
          }}
        }}
      }}

      const modeBadge = mode === 'reg' ? 'CLP/GHS Regulatory' : 'Conservative Lab EHS';

      return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 330" width="${{dims.w}}mm" height="${{dims.h}}mm" style="width:100%; height:auto; display:block;">
        <rect x="2" y="2" width="516" height="326" rx="10" fill="#ffffff" stroke="#111827" stroke-width="2.5"/>
        <path d="M 12 3.5 L 508 3.5 C 513 3.5 516.5 7 516.5 12 L 516.5 13 L 3.5 13 L 3.5 12 C 3.5 7 7 3.5 12 3.5 Z" fill="${{sigBg}}"/>
        <text x="16" y="37" font-family="Arial, sans-serif" font-size="20" font-weight="900" fill="#0f172a">${{esc(title)}}</text>
        <text x="16" y="53" font-family="Arial, sans-serif" font-size="10.2" font-weight="bold" fill="#334155">${{esc(subtitle)}}</text>
        <text x="16" y="66" font-family="Arial, sans-serif" font-size="8.5" fill="#64748b">${{esc(currentCalculated.cas)}}  •  ${{esc(currentCalculated.composition)}}</text>

        <rect x="374" y="19" width="132" height="28" rx="5" fill="${{sigBg}}"/>
        <text x="440" y="37" text-anchor="middle" font-family="Arial, sans-serif" font-size="13" font-weight="900" letter-spacing="0.8" fill="#ffffff">${{esc(signal)}}</text>
        <text x="440" y="59" text-anchor="middle" font-family="Arial, sans-serif" font-size="7.8" font-weight="bold" fill="#64748b">[${{esc(modeBadge)}}]</text>

        <line x1="12" y1="74" x2="508" y2="74" stroke="#cbd5e1" stroke-width="1.5"/>
        <rect x="10" y="80" width="144" height="170" rx="6" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1"/>
        ${{pictoParts.join('')}}
        ${{textEls.join('')}}

        <line x1="12" y1="256" x2="508" y2="256" stroke="#cbd5e1" stroke-width="1.5"/>
        <rect x="12" y="263" width="158" height="53" rx="4" fill="#f8fafc" stroke="#94a3b8" stroke-width="1"/>
        <text x="18" y="276" font-family="Arial, sans-serif" font-size="8" font-weight="bold" fill="#475569">DATE PREPARED:</text>
        <text x="18" y="298" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#0f172a">${{esc(prepDate)}}</text>
        <line x1="18" y1="304" x2="160" y2="304" stroke="#cbd5e1" stroke-width="1"/>

        <rect x="178" y="263" width="158" height="53" rx="4" fill="#f8fafc" stroke="#94a3b8" stroke-width="1"/>
        <text x="184" y="276" font-family="Arial, sans-serif" font-size="8" font-weight="bold" fill="#475569">PREPARED BY:</text>
        <text x="184" y="298" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#0f172a">${{esc(prepBy)}}</text>
        <line x1="184" y1="304" x2="326" y2="304" stroke="#cbd5e1" stroke-width="1"/>

        <rect x="344" y="263" width="164" height="53" rx="4" fill="#f8fafc" stroke="#94a3b8" stroke-width="1"/>
        <text x="350" y="276" font-family="Arial, sans-serif" font-size="8" font-weight="bold" fill="#475569">NOTES:</text>
        <text x="350" y="298" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#0f172a">${{esc(storage)}}</text>
        <line x1="350" y1="304" x2="498" y2="304" stroke="#cbd5e1" stroke-width="1"/>
      </svg>`;
    }}

    function renderPreview() {{
      const dims = getDims();
      const inW = (dims.w / 25.4).toFixed(2);
      const inH = (dims.h / 25.4).toFixed(2);
      document.getElementById('dimReadout').textContent = `${{dims.w}} × ${{dims.h}} mm (${{inW}}" × ${{inH}}")`;
      document.getElementById('dynamicPrintCss').textContent = `
        @media print {{
          .queue-card {{
            width: ${{dims.w}}mm !important;
            height: ${{dims.h}}mm !important;
          }}
          .queue-card svg {{
            width: ${{dims.w}}mm !important;
            height: ${{dims.h}}mm !important;
          }}
        }}
      `;
      const svg = buildCurrentSVG();
      document.getElementById('svgPreviewBox').innerHTML = svg;
      const ul = document.getElementById('auditList');
      if (currentCalculated && currentCalculated.audit_log) {{
        ul.innerHTML = currentCalculated.audit_log.map(line => `<li>${{esc(line)}}</li>`).join('');
      }}
    }}

    function downloadCurrentSVG() {{
      const dims = getDims();
      const layout = document.getElementById('layoutSelect').value;
      const svg = '<?xml version="1.0" encoding="UTF-8"?>\n' + buildCurrentSVG();
      const title = (document.getElementById('titleInput').value || 'custom_label').replace(/[^a-zA-Z0-9_-]+/g, '_');
      const blob = new Blob([svg], {{type: 'image/svg+xml;charset=utf-8'}});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${{title}}_${{layout}}_${{dims.w}}x${{dims.h}}mm.svg`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }}

    function addCurrentToQueue() {{
      const dims = getDims();
      const svg = buildCurrentSVG();
      const title = document.getElementById('titleInput').value || 'Custom Solution';
      printQueue.push({{ title: `${{title}} (${{dims.w}}×${{dims.h}}mm)`, svg: svg }});
      renderQueue();
    }}

    function loadAll18PresetsToQueue() {{
      const savedFormula = document.getElementById('formulaInput').value;
      const savedTitle = document.getElementById('titleInput').value;
      for (const [formula, title] of PRESET_18_LIST) {{
        loadExample(formula, title);
        addCurrentToQueue();
      }}
      loadExample(savedFormula, savedTitle);
    }}

    function removeFromQueue(idx) {{
      printQueue.splice(idx, 1);
      renderQueue();
    }}

    function clearQueue() {{
      printQueue = [];
      renderQueue();
    }}

    function printCurrentOrQueue() {{
      if (printQueue.length === 0) {{
        addCurrentToQueue();
      }}
      window.print();
    }}

    function renderQueue() {{
      document.getElementById('queueCount').textContent = printQueue.length;
      document.getElementById('queueHeaderCount').textContent = printQueue.length;
      const grid = document.getElementById('queueGrid');
      grid.innerHTML = printQueue.map((item, idx) => `
        <div class="queue-card">
          <div class="queue-card-bar">
            <span><strong>SPECIMEN #${{idx + 1}}</strong> • ${{esc(item.title)}}</span>
            <button class="btn btn-paper" style="padding:2px 8px; font-size:11px;" onclick="removeFromQueue(${{idx}})">Remove</button>
          </div>
          <div>${{item.svg}}</div>
        </div>
      `).join('');
    }}

    parseFormulaInput(true);
  </script>
</body>
</html>""";

    for fname in ["index.html", "GHS_Custom_Solution_Generator.html"]:
        out_file = BASE_DIR / fname
        out_file.write_text(html, encoding="utf-8")
        print(f"Generated Editorial GHS Studio at: {out_file}")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        generate_universal_html_app()
