# PharmaGuideRx

**Personalized Pharmacogenomics, Explained.**

PharmaGuideRx is an educational and research-oriented pharmacogenomics decision-support prototype. It demonstrates how pharmacogene, medication, phenotype, and synthetic patient-profile information can be connected to transparent, rule-based interpretations.

> **Important:** This is a research/educational prototype. It is not a medical device and must not be used as a substitute for a qualified clinician, validated laboratory, or current CPIC/DPWG/FDA guidance.

## Expanded demonstration dataset

The demo knowledge base now contains **29 gene-drug examples** spanning multiple pharmacogenes and phenotype styles, including metabolizer categories and HLA/G6PD response markers.

Examples include:
- CYP2C19 → clopidogrel, omeprazole, voriconazole
- CYP2D6 → codeine, tramadol, tamoxifen, atomoxetine
- CYP2C9 / VKORC1 / CYP4F2 → warfarin
- TPMT / NUDT15 → thiopurines
- DPYD → fluorouracil, capecitabine
- SLCO1B1 / ABCG2 → statins
- CYP3A5 → tacrolimus
- CYP2B6 → efavirenz, sertraline
- UGT1A1 → atazanavir
- HLA-B / HLA-A → selected drug hypersensitivity examples
- G6PD → rasburicase
- CFTR → ivacaftor
- NAT2 → hydralazine

The expanded set is aligned to gene-drug areas represented in CPIC materials, but individual demo records are simplified for software testing and are **not prescribing rules**. CPIC maintains current guideline versions and standardized genotype-to-phenotype interpretation; always verify against the current source before any clinical use. citeturn0search1turn0search13

## Synthetic patient profiles

Eight fictional patient profiles are included for demonstrations. They contain no real patient information and are designed to exercise the UI with realistic-looking phenotype/diplotype combinations.

## Features
- Interactive Streamlit web application
- Sample patient profile loader
- Custom patient label
- Pharmacogene and medication selection
- Multiple phenotype examples
- Explainable local gene-drug rules
- Example diplotype/marker display
- Expanded demonstration knowledge base
- Synthetic patient profile table
- Evidence/source notes in the interface
- GitHub Actions Python syntax check

## Run locally

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app/main.py
```

## Project structure

```text
PharmaGuideRx/
├── app/
│   ├── main.py
│   └── rules.py
├── data/
│   ├── gene_drug_demo.json
│   └── sample_patient_profiles.json
├── .github/
│   └── workflows/
│       └── syntax-check.yml
├── .gitignore
├── .env.example
├── LICENSE
├── PROJECT_STATUS.md
├── README.md
└── requirements.txt
```

## Data provenance and safety

The dataset is synthetic and intended for application development, demonstrations, teaching, and testing. It should not be interpreted as a clinical knowledge base.

CPIC states that its guidelines are intended to help clinicians understand how available genetic test results can be used to optimize drug therapy, and its current guideline collection is periodically updated. citeturn0search1

## Future development
Potential next stages include validated CPIC/DPWG guideline ingestion, VCF and star-allele support, evidence/version provenance, FHIR/EHR interoperability, authentication, audit logging, clinical validation, and regulatory review.

## License
MIT License.
