
from pathlib import Path
import pymupdf

from ingestion.document_quality import analyze_page


def test_pdf(pdf_path):
    with pymupdf.open(pdf_path) as doc:
        print(f"\nPDF: {pdf_path.name}")
        print(f"Total pages: {len(doc)}")

        for page_number, page in enumerate(doc, start=1):
            result = analyze_page(page)

            word_count = result["text_analysis"]["word_count"]
            coverage = result["coverage_ratio"]
            status = result["ocr_status"]

            print(
                f"Page {page_number}: "
                f"Words={word_count}, "
                f"Coverage={coverage:.2f}, "
                f"Status={status}"
            )


if __name__ == "__main__":
    pdf_path = Path("datasets/pdfs/scanned/Adobe Scan 02-Apr-2024.pdf")

    test_pdf(pdf_path)
