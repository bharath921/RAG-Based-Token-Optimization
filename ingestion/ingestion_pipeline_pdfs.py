
from pathlib import Path

from ingestion.pdf_loader import discover_pdfs, extract_pdf


def ingest_dataset(dataset_path):

    pdf_files = discover_pdfs(dataset_path)

    # Step 2: Prepare storage
    all_documents = []

    successful_files = 0
    failed_files = 0
    empty_pages = 0

    failed_documents = []

    for pdf_path in pdf_files:

        try:
            documents = extract_pdf(pdf_path)

            all_documents.extend(documents)

            successful_files += 1

            for document in documents:
                if document.metadata.get("extraction_status") == "no_extractable_text":
                    empty_pages += 1

        except Exception as error:
            failed_files += 1

            failed_documents.append({
                "file": str(pdf_path),
                "error": str(error)
            })

    # Step 4: Create ingestion report
    report = {
        "total_pdfs": len(pdf_files),
        "successful_files": successful_files,
        "failed_files": failed_files,
        "total_pages_extracted": len(all_documents),
        "pages_without_text": empty_pages,
        "failed_documents": failed_documents
    }

    return all_documents, report


if __name__ == "__main__":

    dataset_path = Path("datasets/pdfs")

    documents, report = ingest_dataset(dataset_path)

    print("\nINGESTION REPORT")
    print("-------------------------")

    for key, value in report.items():
        print(f"{key}: {value}")

    print("\nFIRST EXTRACTED PAGE")
    print("-------------------------")

    if documents:
        print(documents[0].page_content[:500])
        print(documents[0].metadata)
