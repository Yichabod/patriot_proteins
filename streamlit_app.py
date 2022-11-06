import streamlit as st
from stmol import showmol, render_pdb, obj_upload
import py3Dmol
import requests
import tempfile

#st.set_page_config(layout = 'wide')
st.title('🎈 ESMfold')

# stmol

def render_mol(pdb):
    pdbview = py3Dmol.view(width=400,height=400)
    pdbview.addModel(pdb,'pdb')
    pdbview.setStyle({'cartoon':{}})
    pdbview.setBackgroundColor('white')#('0xeeeeee')
    pdbview.zoomTo()
    showmol(pdbview, height = 500,width=800)

# ESMfold

DEFAULT_SEQ = "MGSSHHHHHHSSGLVPRGSHMRGPNPTAASLEASAGPFTVRSFTVSRPSGYGAGTVYYPTNAGGTVGAIAIVPGYTARQSSIKWWGPRLASHGFVVITIDTNSTLDQPSSRSSQQMAALRQVASLNGTSSSPIYGKVDTARMGVMGWSMGGGGSLISAANNPSLKAAAPQAPWDSSTNFSSVTVPTLIFACENDSIAPVNSSALPIYDSMSRNAKQFLEINGGSHSCANSGNSNQALIGKKGVAWMKRFMDNDTRYSTFACENPNSTRVSDFRTANCSLEDPAANKARKEAELAAATAEQ"

txt = st.text_area('Input sequence', DEFAULT_SEQ)

def update(sequence=txt):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    response = requests.post('https://api.esmatlas.com/foldSequence/v1/pdb/', headers=headers, data=sequence)
    name = sequence[:3] + sequence[-3:] 
    pdb_string = response.content.decode('utf-8')
    
    #tmp = tempfile.NamedTemporaryFile()
    #with open(tmp.name, "w") as f:
    #    f.write(pdb_string)
    #st.write("File name", tmp.name)
    #obj = makeobj(pdb_string, molformat='pdb', style='cartoon')
    return render_mol(pdb_string)

st.button('Predict', on_click=update)



#uploaded_file = st.sidebar.file_uploader('Upload PDB file')

##showmol(render_pdb(id = '3EQM'))

#if uploaded_file is not None:
#  showmol(obj_upload(uploaded_file).setStyle({'cartoon':{'color':'spectrum'}}) )
#else:
#  st.info('Awaiting input ...')
