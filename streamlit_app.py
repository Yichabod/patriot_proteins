# This is app is based on the following repo https://github.com/dataprofessor/
# created by Chanin Nantasenamat (Data Professor) https://youtube.com/dataprofessor
# Credit: This app is inspired by https://huggingface.co/spaces/osanseviero/esmfold

from itertools import dropwhile
import streamlit as st
from stmol import showmol
import py3Dmol
import requests
import biotite.structure.io as bsio

# st.set_page_config(layout = 'wide')
# st.sidebar.title('🇺🇸 PATRIOT PROTEINS')
# st.sidebar.image('patriot_img.jpg', caption='Demonstrate your loyalty with Patriot Proteins.')

# st.title('🇺🇸 PATRIOT PROTEINS')
# st.title('Turn patriotic text into a protein')
# st.image('patriot_img.jpg', caption='Demonstrate your loyalty with Patriot Proteins.')
# st.write('Pick a text. Each letter maps to an amino acid. Folded with a machine learning model.')

st.markdown('# 🇺🇸 PATRIOT PROTEINS')
# st.image('patriot_img.jpg', caption='Demonstrate your loyalty with Patriot Proteins.')
# st.markdown('### Turn patriotic text into a protein')
# st.write('Pick a text. Each letter maps to an amino acid. Folded with a machine learning model.')

# Create two columns
col1, col2 = st.columns(2)

# Use the first column for text
with col1:
    st.markdown('*Hold the constitution in your hand as a 3D printed protein*')
    st.write('Pick your favorite patriotic text. We translate each letter to an amino acid. Using the latest machine learning model, we fold the amino acids into a protein. 3D printed copy available for pre-order now.')

# Use the second column for the image
with col2:
    st.image('patriot_img.jpg', caption='God Bless America.', use_column_width=True)


# st.sidebar.write("Are you seeking something extraordinary that symbolizes your profound love for America? Look no further than Patriot Proteins. These aren't just 3D printed plastic models of proteins, but cultural touchstones that encode messages from our American heritage, including the Federalist Papers and the Second Amendment. As decor, they ignite discussions about our national values, serving as a testament to our technological advancements and rich history. With Patriot Proteins, history and science combine to celebrate your American spirit in a truly distinctive way.")

# st.sidebar.write("Select from the following key documents from American history. An excerpt will be mapped to amino acids and folded into a 3D protein model. You can order the 3D model as a reminder of your patriotism for the United States of America.")
# [*ESMFold*](https://esmatlas.com/about) is an end-to-end single sequence protein structure predictor based on the ESM-2 language model. For more information, read the [research article](https://www.biorxiv.org/content/10.1101/2022.07.20.500902v2) and the [news article](https://www.nature.com/articles/d41586-022-03539-1) published in *Nature*.')

# Amino acid dictionary
amino_acid_dict = {
    'a': 'A', # Alanine
    'b': 'R', # Arginine
    'c': 'K', # Lysine
    'd': 'D', # Aspartic Acid
    'e': 'E', # Glutamic Acid
    'f': 'F', # Phenylalanine
    'g': 'G', # Glycine
    'h': 'H', # Histidine
    'i': 'I', # Isoleucine
    'j': 'L', # Leucine
    'k': 'K', # Lysine
    'l': 'L', # Leucine
    'm': 'M', # Methionine
    'n': 'N', # Asparagine
    'o': 'P', # Proline
    'p': 'P', # Proline
    'q': 'Q', # Glutamine
    'r': 'R', # Arginine
    's': 'S', # Serine
    't': 'T', # Threonine
    'u': 'C', # Cysteine
    'v': 'V', # Valine
    'w': 'V', # Valine
    'x': 'Y', # Tyrosine
    'y': 'Y', # Tyrosine
    'z': 'S'  # Serine
}
    # 'u' was mapped to Cysteine because the atomic symbol for the element sulfur, which is found in cysteine, is 'S', and 'u' and 's' are neighbors in the English alphabet.
    # 'v' and 'w' were both mapped to Valine. They are next to each other in the alphabet and have similar sounds, which might make this mapping easier to remember.
    # 'x' and 'y' were both mapped to Tyrosine. The reason for this is that 'x' is often used to represent unknowns or variables, and 'y' often represents a second variable. This could be a mnemonic to remember this mapping.
    # 'z' was mapped to Serine, since 'z' and 's' have similar sounds, making this mapping somewhat intuitive.

# Key quotations:
quotations = {
    "gettysburg": "Four score and seven years ago our fathers brought forth on this continent, a new nation, conceived in Liberty, and dedicated to the proposition that all men are created equal.",
    
    "constitution": "We the People of the United States, in Order to form a more perfect Union, establish Justice, insure domestic Tranquility, provide for the common defence, promote the general Welfare, and secure the Blessings of Liberty to ourselves and our Posterity, do ordain and establish this Constitution for the United States of America", 

    "second_amendment":"A well regulated Militia, being necessary to the security of a free State, the right of the people to keep and bear Arms, shall not be infringed.",

    "fourth_amendment":"The right of the people to be secure in their persons, houses, papers, and effects, against unreasonable searches and seizures, shall not be violated, and no Warrants shall issue, but upon probable cause, supported by Oath or affirmation, and particularly describing the place to be searched, and the persons or things to be seized"
}



def word_to_amino(sentence):
    # Clean the sentence: remove non-alphabetic characters and convert to lower case
    cleaned_sentence = ''.join(c for c in sentence if c.isalpha()).lower()

    # Convert to amino acids
    amino_acids = ''.join(amino_acid_dict[c] for c in cleaned_sentence)

    return amino_acids

# stmol
def render_mol(pdb):
    pdbview = py3Dmol.view()
    pdbview.addModel(pdb,'pdb')
    # pdbview.setStyle({'cartoon':{'color':'spectrum'}})
    pdbview.setStyle({'cartoon':{'color':'blue'}})
    pdbview.setBackgroundColor('white')#('0xeeeeee')
    pdbview.zoomTo()
    pdbview.zoom(2, 800)
    pdbview.spin(False) #try to change spin rate
    showmol(pdbview, height = 500,width=800)

# ESMfold
def update(sequence):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.post('https://api.esmatlas.com/foldSequence/v1/pdb/', headers=headers, data=sequence)
    name = sequence[:3] + sequence[-3:]
    pdb_string = response.content.decode('utf-8')
    print(pdb_string.startswith('HEADER'))
    if not pdb_string.startswith('HEADER'):  # Adjust this based on what a valid PDB string should start with
        st.error('The API did not return a valid PDB structure. Please try again.')
        return

    with open('predicted.pdb', 'w') as f:
        f.write(pdb_string)

    struct = bsio.load_structure('predicted.pdb', extra_fields=["b_factor"])
    # b_value = round(struct.b_factor.mean(), 4)

    # Display protein structure
    st.markdown('_Your Patriot Protein_')
    render_mol(pdb_string)

    # # plDDT value is stored in the B-factor field
    # st.subheader('plDDT')
    # st.write('plDDT is a per-residue estimate of the confidence in prediction on a scale from 0-100.')
    # st.info(f'plDDT: {b_value}')


    # st.download_button(
    #     label="Download PDB",
    #     data=pdb_string,
    #     file_name='predicted.pdb',
    #     mime='text/plain',
    # )

# Protein sequence input

DEFAULT_SEQ = quotations['constitution']
# "Four score and seven years ago our fathers brought forth on this continent, a new nation, conceived in Liberty, and dedicated to the proposition that all men are created equal."


# txt = st.sidebar.text_area('Input sequence', DEFAULT_SEQ, height=200)
# amino_acids = word_to_amino(txt)

dropdown_options = {
    'CONSTITUTION':'constitution',
'SECOND AMENDMENT':'second_amendment',
'FOURTH AMENDMENT':'fourth_amendment',
'GETTYSBURG ADDRESS':'gettysburg',
}

option_selected = st.selectbox("CHOOSE YOUR TEXT", options=list(dropdown_options.keys()))

if option_selected:
    text_name = dropdown_options[option_selected]
    text = quotations[text_name]
    amino_acids = word_to_amino(text)
    col1, col2 = st.columns(2)
    
    # Display text in the first column and amino sequence in the second
    col1.markdown(f"**Text:** {text}")
    col2.markdown(f"**Amino Sequence:** {amino_acids}")
    update(amino_acids)
else:
    option_selected = st.selectbox("CHOOSE YOUR TEXT", options=list(dropdown_options.keys()))


col1, col2 = st.columns(2)

# Add a button to the first column and another button to the second column
if col1.button('FIND OUT MORE'):
    # Handle 'Find out more' click here
    st.write('You clicked Find out more')

if col2.button('PRE-ORDER NOW'):
    # Handle 'Pre-order now' click here
    st.write('You clicked Pre-order now')

# elif st.button('GETTYSBURG ADDRESS'):
#     txt = quotations['gettysburg']
#     st.write(txt)
#     update(word_to_amino(txt))

# add_selectbox = st.sidebar.selectbox(
#     "How would you like to be contacted?",
#     ("Email", "Home phone", "Mobile phone")
# )







# if st.sidebar.button('PATRIOTIZE'):
#     update()
# else:
#     st.warning('👈 Choose a Patriot Protein here 🇺🇸')
# predict = st.sidebar.button('PATRIOTIZE', on_click=update)


# if not predict:
#     st.warning('👈 Your Patriot Protein message goes here 🇺🇸')

