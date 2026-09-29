import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from pdf_reader.pdfloading import load_pdf_pages
from langchain_reader.config import DATA_DIR

load_dotenv()

pdf_path = DATA_DIR / "Программа_ШАД.pdf"

# Model connection and initialisation
try:
    api_key = os.getenv("GEMINI_API_KEY")
except Exception as e:
    print(f"Error while parsing API key: {e}")
if not api_key: # type: ignore
    raise SystemExit("Google AI Studio API is not set. Check your .env file and try again.")

model = init_chat_model("google_genai:gemini-3.1-flash-lite", temperature=0)

# Embeddings are generated using Gemini Embedding - special model for this cases
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

vector_store = InMemoryVectorStore(embeddings)


# # Generating responce
# response = model.invoke([
#     ("system",""),
#     ("user", "What is RAG")
# ])
# usage = response.usage_metadata

# print("===== invoke ======")
# print(response.content)
# print()
# print("===== token usage  ======")
# print(f"- input={usage['input_tokens']}\n- output={usage['output_tokens']}\n- total={usage['total_tokens']}")

# Document is LangChain's built-in type for storing content
# documents = [
#     Document(
#         page_content = """
#             LangChain implements a Document abstraction for a unit of text and associated metadata. It has three attributes:
#             - page_content: a string representing the content.
#             - metadata: a dict containing arbitrary metadata.
#             - id: (optional) a string identifier for the document.
#             metadata can capture the source of the document, its relationship to other documents, and other information. An individual Document often represents a chunk of a larger document.",
#             """,
#         metadata = {"source": "langchain-doc"}
#     )
# ]

documents = load_pdf_pages(pdf_path)

# Generating vector with embedding model
vector_1 = embeddings.embed_query(documents[0].page_content)

print(f"Generated vector with {len(vector_1)} length\n")
print(vector_1[:15])