import streamlit as st
import plotly.graph_objects as go
from rules import load_rules, load_profiles, interpret

st.set_page_config(page_title="PharmaGuideRx", page_icon="🧬", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
.block-container{max-width:1280px;padding-top:1.2rem}
.login{max-width:520px;margin:7vh auto 0;padding:2.4rem;border:1px solid #dbe4ee;border-radius:22px;background:#fff;box-shadow:0 12px 40px rgba(20,40,70,.08)}
.brand{letter-spacing:.2px}
.card{padding:1rem 1.1rem;border:1px solid #dbe4ee;border-radius:16px;background:#fbfdff}
.warning{padding:.8rem 1rem;border-radius:12px;background:#fff8e6;border:1px solid #f2d27a}
</style>
""", unsafe_allow_html=True)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("""<div class="login"><span style="font-size:2.3rem">🧬</span><h1>PharmaGuideRx</h1><p>Personalized pharmacogenomics, explained.</p></div>""", unsafe_allow_html=True)
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter username")
        password = st.text_input("Password", type="password", placeholder="Enter password")
        c1, c2 = st.columns(2)
        login = c1.form_submit_button("Login", type="primary", use_container_width=True)
        demo = c2.form_submit_button("Demo Login", use_container_width=True)
        if login:
            if username == "admin" and password == "pharmaguide":
                st.session_state.authenticated = True
                st.session_state.user = username
                st.rerun()
            else:
                st.error("Invalid credentials. Use Demo Login for the demonstration environment.")
        if demo:
            st.session_state.authenticated = True
            st.session_state.user = "Demo User"
            st.rerun()
    st.caption("Demo environment only; authentication is not production-grade.")
    st.info("Demo login: click Demo Login, or use username admin and password pharmaguide.")
    st.stop()

rules = load_rules()
profiles = load_profiles()
genes = sorted({r["gene"] for r in rules})
drugs_by_gene = {}
for r in rules:
    drugs_by_gene.setdefault(r["gene"], set()).add(r["drug"])

h1, h2 = st.columns([7,1])
h1.markdown("## 🧬 PharmaGuideRx")
h1.caption("Personalized pharmacogenomics • molecular visualization • virtual-screening workspace")
if h2.button("Logout"):
    st.session_state.authenticated = False
    st.rerun()

nav = st.radio("Workspace", ["Demo", "New Patient", "Molecular Viewer", "Virtual Screening", "Animation"], horizontal=True, label_visibility="collapsed")

if nav == "Demo":
    st.markdown('<div class="card"><b>Demo Workspace</b><br>Select a synthetic patient, gene, drug and phenotype, then run an explainable interpretation.</div>', unsafe_allow_html=True)
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Genes",len(genes)); c2.metric("Gene-drug examples",len(rules)); c3.metric("Sample profiles",len(profiles)); c4.metric("Mode","Demo")
    labels=["Select a sample profile"]+[p["label"] for p in profiles]
    selected=st.selectbox("Sample patient",labels)
    profile=None if selected==labels[0] else next(p for p in profiles if p["label"]==selected)
    patient=profile["patient_id"] if profile else "Demo Patient"
    default_gene=profile["gene"] if profile else genes[0]
    gene=st.selectbox("Pharmacogene",genes,index=genes.index(default_gene))
    drug_options=sorted(drugs_by_gene[gene])
    default_drug=profile["drug"] if profile and profile["drug"] in drug_options else drug_options[0]
    drug=st.selectbox("Medication",drug_options,index=drug_options.index(default_drug))
    phenotypes=sorted({p for r in rules if r["gene"]==gene and r["drug"]==drug for p in r["phenotypes"]})
    default_ph=profile["phenotype"] if profile and profile["phenotype"] in phenotypes else phenotypes[0]
    phenotype=st.selectbox("Phenotype",phenotypes+["Normal / not specified"],index=(phenotypes+["Normal / not specified"]).index(default_ph))
    if st.button("Run interpretation",type="primary",use_container_width=True):
        result=interpret(gene,drug,phenotype)
        st.markdown(f"""<div class="card"><h3>{result['gene']} → {result['drug']}</h3><b>Phenotype:</b> {phenotype}<br><b>Example genotype:</b> {result.get('example_diplotype','Not specified')}<br><b>Interpretation:</b> {result['interpretation']}<br><b>Potential action:</b> {result['action']}</div>""",unsafe_allow_html=True)
        st.info(result["evidence"])
    st.divider()
    st.subheader("Knowledge base")
    st.dataframe([{"Gene":r["gene"],"Drug":r["drug"],"Phenotype":", ".join(r["phenotypes"]),"Example genotype":r.get("example_diplotype","")} for r in rules],use_container_width=True,hide_index=True)

elif nav == "New Patient":
    st.subheader("➕ New Patient Profile")
    st.caption("Create a synthetic profile for demonstration. Do not enter real patient-identifying information.")
    with st.form("new_patient"):
        a,b=st.columns(2)
        pid=a.text_input("Patient ID / label","PGX-NEW-001")
        indication=b.text_input("Indication","Research demonstration")
        age=a.number_input("Age",0,120,40)
        sex=b.selectbox("Sex",["Female","Male","Other / not specified"])
        gene=a.selectbox("Gene",genes)
        drug=b.selectbox("Drug",sorted(drugs_by_gene[gene]))
        phenotype=a.text_input("Phenotype","Intermediate metabolizer")
        diplotype=b.text_input("Diplotype / marker","Example only")
        save=st.form_submit_button("Create demo profile",type="primary")
    if save:
        st.session_state.new_profile={"patient_id":pid,"label":pid,"age":age,"sex":sex,"indication":indication,"gene":gene,"drug":drug,"phenotype":phenotype,"diplotype":diplotype,"note":"Synthetic profile created in the current session."}
        st.success("Synthetic profile created for this session.")
        st.json(st.session_state.new_profile)

elif nav == "Molecular Viewer":
    st.subheader("🧪 Molecular Viewer")
    st.caption("PyMOL-inspired interactive 3D viewer using a generated molecular-style scene.")
    col1,col2=st.columns([3,1])
    with col2:
        representation=st.selectbox("Representation",["Ribbon-like backbone","Atoms","Ligand + backbone"])
        st.info("Use mouse/touch to rotate, zoom and inspect the scene.")
    import numpy as np
    t=np.linspace(0,4*np.pi,160); x=np.cos(t); y=np.sin(t); z=np.linspace(-2,2,160)
    fig=go.Figure()
    if representation in ["Ribbon-like backbone","Ligand + backbone"]:
        fig.add_trace(go.Scatter3d(x=x,y=y,z=z,mode="lines",line=dict(width=7),name="Protein backbone"))
    if representation in ["Atoms","Ligand + backbone"]:
        idx=np.arange(0,160,5)
        fig.add_trace(go.Scatter3d(x=x[idx],y=y[idx],z=z[idx],mode="markers",marker=dict(size=5),name="Atoms"))
        fig.add_trace(go.Scatter3d(x=[0.2,-0.2,0.1],y=[0.2,-0.3,0.0],z=[0.2,0.1,-0.2],mode="markers",marker=dict(size=10),name="Ligand"))
    fig.update_layout(height=620,margin=dict(l=0,r=0,t=10,b=0),paper_bgcolor="#0b1220",scene=dict(bgcolor="#0b1220",xaxis_visible=False,yaxis_visible=False,zaxis_visible=False))
    with col1: st.plotly_chart(fig,use_container_width=True)

elif nav == "Virtual Screening":
    st.subheader("⚗️ Virtual Screening Workspace")
    st.caption("PyRx-inspired interface for exploring synthetic docking-style results.")
    target=st.selectbox("Target",["CYP2C19 demonstration target","CYP2D6 demonstration target","TPMT demonstration target"])
    if st.button("Run demonstration screen",type="primary"):
        rows=[{"Ligand":f"Demo-Ligand-{chr(65+i)}","Target":target,"Demo binding score (kcal/mol)":round(-5.2-i*0.37,2),"Pose":i+1} for i in range(5)]
        st.session_state.screen=rows
    if "screen" in st.session_state:
        st.dataframe(st.session_state.screen,use_container_width=True,hide_index=True)
        st.bar_chart({r["Ligand"]:r["Demo binding score (kcal/mol)"] for r in st.session_state.screen})
    st.markdown('<div class="warning"><b>Important:</b> Scores are synthetic UI/demo values. No real AutoDock/PyRx docking is performed.</div>',unsafe_allow_html=True)

else:
    st.subheader("🎞️ Molecular Animation")
    st.caption("Interactive demonstration animation for teaching and presentation.")
    import numpy as np
    theta=np.linspace(0,2*np.pi,80); frames=[]
    for k in range(36):
        shift=k*np.pi/18
        frames.append(go.Frame(data=[go.Scatter3d(x=np.cos(theta+shift),y=np.sin(theta+shift),z=np.sin(2*theta+shift),mode="lines",line=dict(width=7))],name=str(k)))
    fig=go.Figure(data=[go.Scatter3d(x=np.cos(theta),y=np.sin(theta),z=np.sin(2*theta),mode="lines",line=dict(width=7))],frames=frames)
    fig.update_layout(height=620,margin=dict(l=0,r=0,t=10,b=0),scene=dict(xaxis_visible=False,yaxis_visible=False,zaxis_visible=False),updatemenus=[{"type":"buttons","showactive":False,"x":0.05,"y":0.05,"buttons":[{"label":"▶ Play","method":"animate","args":[None,{"frame":{"duration":70,"redraw":True},"fromcurrent":True}]}]}])
    st.plotly_chart(fig,use_container_width=True)

st.caption("PharmaGuideRx • Research / educational prototype • Synthetic demo data only")
