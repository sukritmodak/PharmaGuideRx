import streamlit as st
from rules import load_rules, interpret

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
genes = sorted({r["gene"] for r in rules})
drugs_by_gene = {}
for r in rules:
    drugs_by_gene.setdefault(r["gene"], []).append(r["drug"])

st.markdown("""
<div class="hero">
<span class="badge">RESEARCH / EDUCATIONAL PROTOTYPE</span>
<h1>🧬 PharmaGuideRx</h1>
<p>Personalized pharmacogenomics, explained through transparent gene-drug rules.</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.header("Patient & medication")
patient = st.sidebar.text_input("Patient ID / label", value="Demo Patient")
gene = st.sidebar.selectbox("Pharmacogene", genes)
drug = st.sidebar.selectbox("Medication", sorted(drugs_by_gene[gene]))
phenotypes = sorted({r["phenotypes"][0] for r in rules if r["gene"] == gene and r["drug"] == drug})
phenotype = st.sidebar.selectbox("Phenotype", phenotypes + ["Normal / not specified"])

st.sidebar.divider()
st.sidebar.caption("Demo only. It does not diagnose, prescribe, or replace clinical guidelines.")

c1, c2, c3 = st.columns(3)
c1.metric("Genes in demo", len(genes))
c2.metric("Gene-drug pairs", len(rules))
c3.metric("Evidence mode", "Rule-based")

st.subheader("Patient-specific interpretation")

if st.button("Run pharmacogenomic interpretation", type="primary", use_container_width=True):
    result = interpret(gene, drug, phenotype)
    st.markdown(f"""
    <div class="result">
    <h3>{result['gene']} → {result['drug']}</h3>
    <p><b>Patient label:</b> {patient}</p>
    <p><b>Phenotype:</b> {phenotype}</p>
    <p><b>Interpretation:</b> {result['interpretation']}</p>
    <p><b>Potential action:</b> {result['action']}</p>
    </div>
    """, unsafe_allow_html=True)
    st.info(result["evidence"])

st.divider()
st.subheader("How the prototype works")
a, b, c, d = st.columns(4)
a.markdown("**1 · Genotype**

Variant/phenotype information is supplied.")
b.markdown("**2 · Gene**

A pharmacogene is selected.")
c.markdown("**3 · Evidence rule**

The local demonstration rule is matched.")
d.markdown("**4 · Interpretation**

A transparent explanation is displayed.")

st.divider()
st.subheader("Demonstration knowledge base")
st.dataframe(
    [{"Gene": r["gene"], "Drug": r["drug"], "Example phenotype": ", ".join(r["phenotypes"])} for r in rules],
    use_container_width=True,
    hide_index=True
)

with st.expander("Clinical safety and scope"):
    st.write(
        "A production clinical system would require validated laboratory inputs, authoritative "
        "guideline versions, clinical governance, security controls, auditability, testing, and regulatory review."
    )

st.caption("PharmaGuideRx • 2026 • Educational prototype")
