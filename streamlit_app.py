# This is app is based on the following repo https://github.com/dataprofessor/
# created by Chanin Nantasenamat (Data Professor) https://youtube.com/dataprofessor
# Credit: This app is inspired by https://huggingface.co/spaces/osanseviero/esmfold

from itertools import dropwhile
import streamlit as st
from stmol import showmol
import py3Dmol
import requests
import biotite.structure.io as bsio

st.set_page_config(page_title="Patriot Protein", page_icon="🇺🇸")
# st.set_page_config(layout = 'wide')

AUDIO_FILE = "give_it_to_me.mp3"

st.markdown('# 🇺🇸 PATRIOT PROTEINS')
# st.image('patriot_img.jpg', caption='Demonstrate your loyalty with Patriot Proteins.')
# st.markdown('### Turn patriotic text into a protein')
# st.write('Pick a text. Each letter maps to an amino acid. Folded with a machine learning model.')


# Create two columns
col1, col2 = st.columns(2)

# Use the first column for text
with col1:
    st.markdown('*Hold the constitution in your hand as a 3D printed protein.*')
    st.write('Pick your favorite patriotic text. We translate each letter to an amino acid. Using the latest structural protein prediction model, we fold the amino acids into a protein. 3D printed copies available for pre-order now.')

# Use the second column for the image
with col2:
    st.image('patriot_img.jpg', caption='Freedom.', use_column_width=True)


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

    "first_amendment": "Congress shall make no law respecting an establishment of religion, or prohibiting the free exercise thereof; or abridging the freedom of speech, or of the press; or the right of the people peaceably to assemble, and to petition the Government for a redress of grievances.",

    "second_amendment":"A well regulated Militia, being necessary to the security of a free State, the right of the people to keep and bear Arms, shall not be infringed.",

    "fourth_amendment":"The right of the people to be secure in their persons, houses, papers, and effects, against unreasonable searches and seizures, shall not be violated, and no Warrants shall issue, but upon probable cause, supported by Oath or affirmation, and particularly describing the place to be searched, and the persons or things to be seized",
    
    "declaration": "We hold these truths to be self-evident, that all men are created equal, that they are endowed by their Creator with certain unalienable Rights, that among these are Life, Liberty and the pursuit of Happiness.",
    
    "emancipation": "That on the first day of January, in the year of our Lord one thousand eight hundred and sixty-three, all persons held as slaves within any State or designated part of a State, the people whereof shall then be in rebellion against the United States, shall be then, thenceforward, and forever free...",
    
    "MLK_dream": "I have a dream that one day this nation will rise up and live out the true meaning of its creed: 'We hold these truths to be self-evident, that all men are created equal.'",
    
    "pledge_allegiance": "I pledge allegiance to the Flag of the United States of America, and to the Republic for which it stands, one Nation under God, indivisible, with liberty and justice for all.",
    
    "second_treatise": "The end of law is not to abolish or restrain, but to preserve and enlarge freedom.",
}

about_text = """
It is a dark and windy night. Your hand are stuffed into your trenchcoat pockets as leaves whip around your fedora. After stepping out of the cemetery, you look up into the sullen sky. *Things used to be different.* You think back to the days of long automobiles with hard tops, the rollerskating drive throughs with smiling blond curls, children laughing white teeth gasoline stations. 

O the laughs and good joys of Ye Olde days! Now look where we are now… not a pittance in our pockets. Where are our flying cars? Where is the children? We need to go back, lang lang agone, and take them back — our values!! 

If only we had a way to re-member old Freedom, Lady Liberty, Sir Locke. Do we need God, or surgery? Science it is! Yes, science indeed. We will hold the old Amendments in our hands like babes just-born. Computers, yes, the genie goblins in the computers will spit them out, out! 

*Are you tired of the ordinary, craving something extraordinary that embodies your deep love for this great nation? Stand out with Patriot Proteins, 3D printed plastic models of proteins that aren't just scientifically fascinating, but culturally resonant. Each one is a tribute to our cherished heritage, encoding messages from the bedrock of American thought - the Federalist Papers, the Second Amendment, and more.*

YES

*In the realm of home or office decor, these aren't just unique items, they're talking points. Stimulate thought-provoking conversations about the foundations of our nation's values, all emanating from an encoded protein model that's as much a testament to our advancements in technology as it is to our rich history.
Patriot Proteins, where past and present, science and patriotism come together to create something truly special. Show your American pride and spirit with this remarkable addition to your space!*

YES PLEASE

*We’ve collected all your favorite patriotic texts and done the hard work of translating it to amino acids and protein sequences so that you can admire the structure from the comfort of your living room.*

ILL TAKE IT. ILL TAKE ALL OF IT NOW"""



instructions = """## The Way
1. Take input text, and translate English letters into amino acids using the following mapping:

|   Key   | Value |     Name      |
|:-------:|:-----:|:-------------:|
|    a    |   A   |    Alanine    |
|    b    |   R   |   Arginine    |
|    c    |   K   |    Lysine     |
|    d    |   D   | Aspartic Acid |
|    e    |   E   | Glutamic Acid |
|    f    |   F   | Phenylalanine |
| ...     |  ...  |    ...        |
|    y    |   Y   |   Tyrosine    |
|    z    |   S   |    Serine     |


2. Using [ESMFold](https://github.com/facebookresearch/esm), a sequence-to-structure transformer, predict the folding of the amino acids into a protein. 
3. Visualize the resulting protein in PyMol. It is now in a PDB file.
4. Convert the PDB to an STL file using Connolly molecular surface estimation, point reduction, format conversion. A library will handle this for you
5. Load the STL file into an Ultimaker S5 (or similar) and print.
6. Behold the great freedom of the Patriot Protein in the palm of your hand

*Note: the beginning batch of the Patriot Proteins are still in production. You may pre-order one now, and will be refunded in the event of a nuclear war, plague, rogue autonomous system, or any other event that prevents the manufacture of the 3D models within two months.*"""


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
    # st.markdown('_Your Patriot Protein_')
    # render_mol(pdb_string)

    if not st.checkbox("Show / Hide Protein"):
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
    'GETTYSBURG ADDRESS': 'gettysburg',
    'CONSTITUTION': 'constitution',
    'FIRST AMENDMENT': 'first_amendment',
    'SECOND AMENDMENT': 'second_amendment',
    'FOURTH AMENDMENT': 'fourth_amendment',
    'DECLARATION OF INDEPENDENCE': 'declaration',
    'EMANCIPATION PROCLAMATION': 'emancipation',
    'MARTIN LUTHER KING DREAM': 'MLK_dream',
    'PLEDGE OF ALLEGIANCE': 'pledge_allegiance',
    'JOHN LOCKE SECOND TREATISE': 'second_treatise',
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

st.markdown("")

col1, col2 = st.columns(2)

# Add a button to the first column and another button to the second column
if col1.button('FIND OUT MORE'):
    # Handle 'Find out more' click here
    st.markdown(about_text)
    st.audio(AUDIO_FILE, format='audio/mp3')
    st.markdown(instructions)
    
        

col2.markdown('[PRE-ORDER NOW](https://buy.stripe.com/00geXwaxId2jdxeeUU)', unsafe_allow_html=True)
# Handle 'Pre-order now' click here

