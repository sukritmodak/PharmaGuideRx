# PharmaGuideRx

**Personalized Pharmacogenomics, Explained.**

PharmaGuideRx is an educational/research prototype combining pharmacogenomics interpretation with a visual bioinformatics workspace.

## Workspace

After the login page, the application provides five main workspaces:

- **Demo** — load synthetic patient profiles and explore gene-drug phenotype interpretation.
- **New Patient** — create a synthetic patient profile during the current session.
- **Molecular Viewer** — an interactive PyMOL-inspired 3D molecular-style viewer for rotation, zooming and representation changes.
- **Virtual Screening** — a PyRx-inspired workspace for viewing synthetic docking-style scores and plots.
- **Animation** — an interactive molecular-style animation with play controls.

PyMOL is a molecular visualization system, while PyRx is a virtual-screening tool for computational drug discovery. PharmaGuideRx does not embed or redistribute either product; these workspaces are inspired by those categories of functionality.

## Login

For the demonstration environment:
- Click **Demo Login**, or
- Username: admin
- Password: pharmaguide

This is intentionally simple and is **not production authentication**.

## Safety

All patient profiles are synthetic. The virtual-screening scores and molecular visualization are demonstration content. No clinical recommendation, real molecular docking result, or validated diagnostic output should be inferred from the prototype.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app/main.py
```

## Structure

```text
PharmaGuideRx/
├── app/
│   ├── main.py
│   └── rules.py
├── data/
│   ├── gene_drug_demo.json
│   └── sample_patient_profiles.json
├── .github/workflows/
├── README.md
├── LICENSE
└── requirements.txt
```
