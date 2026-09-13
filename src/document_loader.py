from pypdf import PdfReader


"""
Loading the pdf > extract the texts > append it as a whole string > convert it to words(token)
Manual chunking
"""
# Load the pdf and seperate text page by page and combine it to one string
def load_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""

    # Loop through pages
    for page in reader.pages:
        # Extract the text from each page
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


# chunk the big strings after splitting the string to words
def chunk_text(text, chunk_size = 500, overlap = 100):
    chunks = []
    words = text.split()

    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunk = " ".join(chunk_words)
        chunks.append(chunk)
        
        # Stop if the current chunk has reached the end of the document
        if end >= len(words):
            break
        start = end - overlap

    return chunks
        