import PyPDF2
import nltk


def tokenizePdf(file_name):
    def load_raw(file_name):
        with open(file_name, 'rb') as f:
            pdfReader = PyPDF2.PdfFileReader(f)
            cv = []
            for i in range(0, pdfReader.getNumPages()):
                text = pdfReader.getPage(i).extractText()
                zn = nltk.word_tokenize(text)
                cv.append(zn)
            return [val for sublist in cv for val in sublist]

    try:
        return(load_raw(file_name))
    except UnicodeDecodeError:
        print("File cannot be loaded")
