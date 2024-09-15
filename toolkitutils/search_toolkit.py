import requests
import nltk
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
import arxiv
import trafilatura
import fitz 
import io
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

def extract_pdf_text(pdf_url: str) -> str:
    """
    Download and extract text from a PDF URL.
    
    :param pdf_url: The URL of the PDF to download and extract text from
    :return: Extracted text or a failure message
    """
    try:
        # Download the PDF
        response = requests.get(pdf_url)
        response.raise_for_status()
        
        # Save the PDF to a temporary file
        with open("temp.pdf", "wb") as pdf_file:
            pdf_file.write(response.content)
        
        # Open the PDF with PyMuPDF
        with fitz.open("temp.pdf") as pdf_document:
            text = ""
            for page in pdf_document:
                text += page.get_text()  # Extract text from each page
        
        # Return the extracted text
        return text if text.strip() else "No text found in PDF"
    
    except Exception as e:
        return f"Error extracting PDF content: {str(e)}"

BRAVE_API_KEY = "BSAp319zErkYaMrxMq8kB92rgq7lENy"
def summarize_text(text: str, sentence_count: int = 3) -> str:
    """
    Summarize the given text using LsaSummarizer.
    
    :param text: The text to summarize
    :param sentence_count: Number of sentences to include in the summary
    :return: The summarized text
    """
    if not text.strip():
        return "No content to summarize"
    
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentence_count)
    
    return ' '.join(str(sentence) for sentence in summary)

def arxiv_search_and_scrape(query: str, max_results: int = 5) -> list:
    """
    Search arXiv for papers matching the query and scrape full article information.
    
    :param query: The search query
    :param max_results: Maximum number of results to return (default 5)
    :return: A list of dictionaries containing the search results with full text
    """
    client = arxiv.Client()
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )
    
    results = []
    for paper in client.results(search):
        paper_info = {
            "title": paper.title,
            "authors": ", ".join(author.name for author in paper.authors),
            "summary": paper.summary,
            "link": paper.pdf_url,
            "full_text": extract_pdf_text(paper.pdf_url)  # Extract PDF content
        }
        results.append(paper_info)
    
    return results

def brave_search_and_scrape(query: str, num_results: int = 5) -> list:
    """
    Perform a web search using the Brave Search API and scrape full article content.
    
    :param query: The search query
    :param num_results: Number of results to return (default 5)
    :return: A list of dictionaries containing the search results with full text
    """
    url = "https://api.search.brave.com/res/v1/web/search"
    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": BRAVE_API_KEY
    }
    params = {
        "q": query,
        "count": num_results
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        return [{"error": f"Unable to fetch results (Status code: {response.status_code})"}]
    
    data = response.json()
    web_results = data.get('web', {}).get('results', [])
    
    results = []
    for result in web_results:
        title = result.get('title', 'No title')
        description = result.get('description', 'No description available')
        url = result.get('url', 'No URL available')
        
        # Scrape the full text content
        full_text = scrape_web_content(url)
        summarized_text = summarize_text(full_text)  # Add summarization here
        
        result_info = {
            "title": title,
            "description": description,
            "url": url,
            "full_text": full_text,
            "summary_excerpt": summarized_text
        }
        results.append(result_info)
    
    return results

def scrape_web_content(url: str) -> str:
    """
    Scrape the main content of a web page.
    
    :param url: The URL of the web page to scrape
    :return: The extracted main content as a string
    """
    try:
        downloaded = trafilatura.fetch_url(url)
        text = trafilatura.extract(downloaded, include_links=False, include_images=False, include_tables=False)
        return text if text else "Failed to extract content"
    except Exception as e:
        return f"Error scraping content: {str(e)}"


def test_search_and_scrape_functions():
    print("Testing arXiv Search and Scrape:")
    print("-" * 50)
    
    query = "quantum computing"
    results = arxiv_search_and_scrape(query, max_results=2)
    for i, result in enumerate(results, 1):
        print(f"{i}. Title: {result['title']}")
        print(f"   Authors: {result['authors']}")
        print(f"   Summary: {result['summary'][:200]}...")
        print(f"   Link: {result['link']}")
        print(f"   Full Text: {result['full_text']}")
        print(f"   Summary Excerpt: {result['summary_excerpt']}")
        print()
    
    print("Testing Brave Search and Scrape:")
    print("-" * 50)
    
    query = "latest advancements in artificial intelligence"
    results = brave_search_and_scrape(query, num_results=2)
    for i, result in enumerate(results, 1):
        print(f"{i}. Title: {result['title']}")
        print(f"   Description: {result['description']}")
        print(f"   URL: {result['url']}")
        print(f"   Full Text (first 200 chars): {result['full_text'][200]}...")
        print(f"   Summary Excerpt: {result['summary_excerpt']}")
        print()

if __name__ == "__main__":
    #test_search_and_scrape_functions()
    query = "quantum computing"
    results = arxiv_search_and_scrape(query, max_results=2)
    
    for i, result in enumerate(results, 1):
        print(f"{i}. Title: {result['title']}")
        print(f"   Authors: {result['authors']}")
        print(f"   Summary: {result['summary'][:200]}...")
        print(f"   Link: {result['link']}")
        print(f"   Full Text (first 500 chars): {result['full_text']}...")
        print()
