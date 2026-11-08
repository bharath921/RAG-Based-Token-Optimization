import pymupdf
doc=pymupdf.open("C:/Users/Dell/Desktop/token reduzer/datasets/pdfs/digital/1.pdf")
print("PDF opened successfully!")
print("Total pages:", len(doc))