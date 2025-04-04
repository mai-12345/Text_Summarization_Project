
import streamlit as st  
from langchain.document_loaders import PyPDFLoader
import tempfile
from sumy.parsers.plaintext import PlaintextParser #pass text
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer #latent semantic analysis
from sumy.summarizers.luhn import LuhnSummarizer #select important sentences
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer


st.title("Text Summarization Application")


options=st.selectbox('Uploaded A File or Write A Text,Choose an Option...',('Write A Text','Upload File'))


if options=='Write A Text':
    text = st.text_area('Please, Enter a Text to Summarize...', height = 150)

elif options=='Upload File':
#upload pdf file
    upload_file = st.file_uploader('Choose File...', type = ['pdf'])

    # if upload_file is not None:
    #     with tempfile.NamedTemporaryFile(delete= False, suffix= '.pdf') as tempfile:
    #         tempfile.write(upload_file.read())
    #         tempfile_path = tempfile.name

    #     loader = PyPDFLoader(tempfile_path)
    #     text = loader.load()
    def extract_text_from_pdf(upload_file):
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf_file:
            temp_pdf_file.write(upload_file.read())
            tempfile_path = temp_pdf_file.name

        loader = PyPDFLoader(tempfile_path)
        documents = loader.load()  # بيستخرج محتوى الـ PDF

        text = ""
        for doc in documents:
            text += doc.page_content + "\n"  # جمع النص من كل صفحة

        return text.strip()

    text = extract_text_from_pdf(upload_file)

# عرض النص المستخرج في واجهة المستخدم
    st.write(text)

options = st.selectbox('Choose Summarizer Type:', ('LSA', 'Luhn', 'LexRank', 'TextRank'))

sentence_count = st.slider('Number of Sentences', 1, 10, 5)

lan=st.selectbox('Choose an Language About Text...',('arabic','english'))

#define a function for 4 summarizers algorithms
def Summarize_Text(text, summarizer_type = 'LSA', sentence_count = 5):
    #pass text with language
    parser = PlaintextParser.from_string(text, Tokenizer(lan)) #pass language

    if options == 'LSA':
        summarizer = LsaSummarizer()
    elif options == 'Luhn':
        summarizer = LuhnSummarizer()
    elif options == 'LexRank':
        summarizer = LexRankSummarizer()
    elif options == 'TextRank':
        summarizer = TextRankSummarizer()

    summary = summarizer(parser.document, sentence_count)

    return ' '.join(str(sentence) for sentence in summary) #join words to be a sentence

if st.button('Summarize Text'):
    if text:
         summary = Summarize_Text(text, options, sentence_count)
         st.subheader('Text Summary:')
         st.write(summary)
    else:
        st.write('Please, Write a Text to Summarize.')

