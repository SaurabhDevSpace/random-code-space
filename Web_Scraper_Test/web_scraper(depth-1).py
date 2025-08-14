import trafilatura
import os
import logging
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)

def scrape_url_with_links(start_url, session_folder, depth=1, chunk_size=1000, chunk_overlap=200):
    start_time = time.time()  # Start timer

    os.makedirs(session_folder, exist_ok=True)
    visited = set()
    all_md_content = []

    def is_same_domain(base_url, link_url):
        return urlparse(base_url).netloc == urlparse(link_url).netloc

    def scrape_page(url, current_depth):
        if url in visited or current_depth > depth:
            return
        visited.add(url)
        logger.info(f"Scraping: {url}")

        try:
            downloaded = trafilatura.fetch_url(url)
            if not downloaded:
                logger.warning(f"No HTML fetched from {url}")
                return

            md_content = trafilatura.extract(downloaded, output_format="markdown")
            if md_content:
                all_md_content.append(f"# {url}\n\n{md_content}\n\n")
            else:
                logger.warning(f"Failed to extract content from {url}")
                return

            if current_depth < depth:
                soup = BeautifulSoup(downloaded, "html.parser")
                for link_tag in soup.find_all("a", href=True):
                    full_link = urljoin(url, link_tag["href"])
                    if is_same_domain(start_url, full_link):
                        scrape_page(full_link, current_depth + 1)

        except Exception as e:
            logger.error(f"Failed to process {url}: {e}")

    scrape_page(start_url, 0)

    # Save all collected Markdown into one file
    md_filename = urlparse(start_url).netloc.replace(".", "_") + ".md"
    md_path = os.path.join(session_folder, md_filename)
    with open(md_path, "w", encoding="utf-8") as f:
        f.writelines(all_md_content)

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_text("".join(all_md_content))
    documents = [Document(page_content=text, metadata={"source_url": start_url, "file_name_md": md_path}) for text in chunks]

    logger.info(f"Number of chunks created: {len(documents)}")

    elapsed_minutes = (time.time() - start_time) / 60
    logger.info(f"Time taken for scraping {start_url}: {elapsed_minutes:.2f} minutes")

    return documents

# Example usage
if __name__ == "__main__":
    session_folder = ".session_folder"
    url = "https://www.blueplanet.com/" # "https://www.ciena.com/" # "https://www.google.com/"  # "https://www.blueplanet.com/"
    docs = scrape_url_with_links(url, session_folder, depth=1)
    for doc in docs:
        print(f"Chunk metadata: {doc.metadata}")
        print(f"Chunk content preview: {doc.page_content[:200]}...")
