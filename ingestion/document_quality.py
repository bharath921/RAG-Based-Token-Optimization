
def normalize_text(text):
    """
    Normalize whitespace in extracted PDF text.
    """
    normalized_text = " ".join(text.split())
    return normalized_text


def analyze_document(text):
    """
    Analyze the quality of extracted PDF text.
    """
    normalized_text = normalize_text(text)

    character_count = len(normalized_text)
    word_count = len(normalized_text.split())

    if not normalized_text:
        status = "empty"
    elif word_count < 5:
        status = "short"
    else:
        status = "usable"

    return {
        "normalized_text": normalized_text,
        "character_count": character_count,
        "word_count": word_count,
        "status": status
    }


def inspect_images(page):
    """
    Inspect images referenced by a PDF page.
    """
    images = page.get_images(full=True)

    image_details = []

    for image in images:
        xref = image[0]
        width = image[2]
        height = image[3]

        image_details.append({
            "xref": xref,
            "width": width,
            "height": height
        })

    return {
        "image_count": len(images),
        "image_details": image_details
    }


def calculate_image_coverage(page):
    """
    Estimate the fraction of the page covered by images.
    """
    page_area = page.rect.get_area()

    if page_area <= 0:
        return 0.0

    images = page.get_images(full=True)
    total_image_area = 0

    for image in images:
        xref = image[0]
        rects = page.get_image_rects(xref)

        for rect in rects:
            visible_rect = rect & page.rect

            if not visible_rect.is_empty:
                total_image_area += visible_rect.get_area()

    coverage_ratio = total_image_area / page_area

    return min(coverage_ratio, 1.0)


def detect_ocr_need(word_count, coverage_ratio):
    """
    Classify a page using preliminary OCR detection rules.
    """
    if word_count == 0 and coverage_ratio > 0.80:
        status = "ocr_candidate"

    elif word_count > 0 and coverage_ratio > 0.80:
        status = "needs_inspection"

    elif word_count == 0:
        status = "needs_inspection"

    else:
        status = "normal"

    return status


def analyze_page(page):
    text = page.get_text()

    text_result = analyze_document(text)
    image_result = inspect_images(page)
    coverage_ratio = calculate_image_coverage(page)

    ocr_status = detect_ocr_need(
        text_result["word_count"],
        coverage_ratio
    )

    return {
        "text_analysis": text_result,
        "image_analysis": image_result,
        "coverage_ratio": coverage_ratio,
        "ocr_status": ocr_status
    }


if __name__ == "__main__":
    import pymupdf

    pdf_path = "datasets/pdfs/scanned/your_file.pdf"

    with pymupdf.open(pdf_path) as doc:
        page = doc[0]

        result = analyze_page(page)

        print("TEXT ANALYSIS")
        print(result["text_analysis"])

        print("\nIMAGE ANALYSIS")
        print(result["image_analysis"])

        print("\nIMAGE COVERAGE")
        print(result["coverage_ratio"])

        print("\nOCR STATUS")
        print(result["ocr_status"])
