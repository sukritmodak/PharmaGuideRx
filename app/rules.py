from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "gene_drug_demo.json"
PATIENT_PATH = ROOT / "data" / "sample_patient_profiles.json"

def load_rules():
    with DATA_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)

def load_profiles():
    with PATIENT_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)

def interpret(gene, drug, phenotype):
    for r in load_rules():
        if r["gene"] == gene and r["drug"] == drug and phenotype in r["phenotypes"]:
            return r

    return {
        "gene": gene,
        "drug": drug,
        "interpretation": "No demonstration rule matched the supplied phenotype.",
        "action": "Do not infer a clinical recommendation from this prototype. Verify the variant, phenotype, and current guideline.",
        "evidence": "No rule match in the local demonstration dataset."
    }
