import streamlit as st
from rules import load_rules, load_profiles, interpret

st.set_page_config(page_title="PharmaGuideRx", page_icon="🧬", layout="wide")

st.markdown("""
<style>
.block-container {max-width: 1200px; padding-top: 2rem;}
.hero {padding: 1.4rem 1.6rem; border: 1px solid #d9e2ec; border-radius: 18px; background: #f7fafc;}
.badge {display:inline-block; padding:0.25rem 0.65rem; border-radius:999px; background:#e6fffa; color:#234e52; font-size:0.8rem; font-weight:600;}
.result {padding:1rem 1.2rem; border-left:5px solid #3182ce; background:#f8fbff; border-radius:10px;}
</style>
""", unsafe_allow_html=True)

rules = load_rules()
profiles = load_profiles()
genes = sorted({r["gene"] for r in rules})
drugs_by_gene = {}
for r in rules:
    drugs_by_gene.setdefault(r["gene"], set()).add(r["drug"])

st.markdown("""
<div class="hero">
<span class="badge">RESEARCH / EDUCATIONAL PROTOTYPE</span>
<h1>🧬 PharmaGuideRx</h1>
<p>Personalized pharmacogenomics, explained through transparent gene-drug rules.</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.header("Patient & medication")
profile_labels = ["Custom patient"] + [p["label"] for p in profiles]
selected_profile = st.sidebar.selectbox("Load sample patient profile", profile_labels)

if selected_profile != "Custom patient":
    profile = next(p for p in profiles if p["label"] == selected_profile)
    patient = profile["patient_id"]
    default_gene = profile["gene"]
else:
    profile = None
    patient = st.sidebar.text_input("Patient ID / label", value="Demo Patient")
    default_gene = genes[0]

gene = st.sidebar.selectbox("Pharmacogene", genes, index=genes.index(default_gene))
drug_options = sorted(drugs_by_gene[gene])
default_drug = profile["drug"] if profile and profile["gene"] == gene and profile["drug"] in drug_options else drug_options[0]
drug = st.sidebar.selectbox("Medication", drug_options, index=drug_options.index(default_drug))
phenotypes = sorted({p for r in rules if r["gene"] == gene and r["drug"] == drug for p in r["phenotypes"]})
default_phenotype = profile["phenotype"] if profile and profile["gene"] == gene and profile["drug"] == drug and profile["phenotype"] in phenotypes else phenotypes[0]
phenotype = st.sidebar.selectbox("Phenotype", phenotypes + ["Normal / not specified"], index=(phenotypes + ["Normal / not specified"]).index(default_phenotype))

st.sidebar.divider()
st.sidebar.caption("All profiles are synthetic. The dataset is for software demonstration, not clinical decision-making.")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Genes", len(genes))
c2.metric("Gene-drug examples", len(rules))
c3.metric("Sample profiles", len(profiles))
c4.metric("Evidence mode", "Rule-based")

if profile:
    st.subheader("Loaded synthetic patient profile")
    st.dataframe([{
        "Patient": profile["patient_id"],
        "Age": profile["age"],
        "Sex": profile["sex"],
        "Indication": profile["indication"],
        "Gene": profile["gene"],
        "Drug": profile["drug"],
        "Diplotype / marker": profile["diplotype"],
        "Phenotype": profile["phenotype"]
    }], use_container_width=True, hide_index=True)

st.subheader("Patient-specific interpretation")
if st.button("Run pharmacogenomic interpretation", type="primary", use_container_width=True):
    result = interpret(gene, drug, phenotype)
    st.markdown(f"""
    <div class="result">
    <h3>{result['gene']} → {result['drug']}</h3>
    <p><b>Patient label:</b> {patient}</p>
    <p><b>Example genotype/diplotype:</b> {result.get('example_diplotype', 'Not specified')}</p>
    <p><b>Phenotype:</b> {phenotype}</p>
    <p><b>Interpretation:</b> {result['interpretation']}</p>
    <p><b>Potential action:</b> {result['action']}</p>
    </div>
    """, unsafe_allow_html=True)
    st.info(result["evidence"])

st.divider()
st.subheader("How the prototype works")
a, b, c, d = st.columns(4)
a.markdown("**1 · Genotype**\n\nA synthetic or laboratory-derived phenotype is supplied.")
b.markdown("**2 · Gene**\n\nA pharmacogene is selected.")
c.markdown("**3 · Evidence rule**\n\nA local demonstration rule is matched.")
d.markdown("**4 · Interpretation**\n\nA transparent explanation is displayed.")

st.divider()
st.subheader("Expanded demonstration knowledge base")
st.dataframe(
    [{"Gene": r["gene"], "Drug": r["drug"], "Example phenotype": ", ".join(r["phenotypes"]), "Example genotype": r.get("example_diplotype", "")} for r in rules],
    use_container_width=True,
    hide_index=True
)

st.subheader("Synthetic patient profiles")
st.dataframe(profiles, use_container_width=True, hide_index=True)

with st.expander("Clinical safety and scope"):
    st.write(
        "This expanded dataset is synthetic and intended for software demonstration. A production clinical "
        "system would require validated laboratory inputs, current authoritative guideline versions, clinical "
        "governance, security controls, auditability, testing, clinical validation, and regulatory review."
    )

st.caption("PharmaGuideRx • 2026 • Educational prototype")
