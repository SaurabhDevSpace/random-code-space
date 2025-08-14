import trafilatura
import os
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import logging
logger = logging.getLogger(__name__)

url = "https://www.google.com/"
try:
    downloaded = trafilatura.fetch_url(url)
    md_content = trafilatura.extract(downloaded, output_format="markdown")
except Exception as e:
    md_content = ""
    logger.error(f"Failed to fetch URL: {url}. Error: {e}")

if not md_content:
    md_content = ""
    logger.error(f"Failed to extract content from {url}")

# 2. Save to session folder
session_folder = '.session_folder'
os.makedirs(session_folder, exist_ok=True)
md_filename = url.replace("https://", "").replace("http://", "").replace("/", "_") + ".md"
md_path = os.path.join(session_folder, md_filename)
with open(md_path, "w", encoding="utf-8") as f:
    f.write(md_content)

# 3. Split into chunks for vector store
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_text(md_content)
documents = [Document(page_content=text, metadata={"source_url": url, "file_name_md": md_path}) for text in chunks]

print(f"Number of chunks created: {len(documents)}")
for doc in documents:
    print(f"Chunk metadata: {doc.metadata}")
    print(f"Chunk content preview: {doc.page_content[:1000]}...")  # Print first 100 characters of each chunk

