from pathlib import Path

from langchain_core.documents import Document
from pypdf import PdfReader

from src.langchain_reader.config import DATA_DIR


def load_pdf_pages(file_path: Path) -> list[Document]:
    reader = PdfReader(file_path)
    page = reader.pages[0]
    text = page.extract_text()
    output_file = DATA_DIR / (file_path.stem + "_parsed.md")

    # print(Path(path).name)   # file.txt
    # print(Path(path).stem)   # file

    # just testing
    with open(output_file, "w") as f:
        # f.write(text)
        for page in reader.pages:
            f.write(page.extract_text())

    parsed_pages = [
        # generating Document object from pypdf pages array using generator and enumerator
        Document(
            page_content=page.extract_text() or "",
            metadata={"source": {file_path}, "page": i}
        ) for i, page in enumerate(reader.pages, start=1)
    ]

    return parsed_pages