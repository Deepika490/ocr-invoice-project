
import os
import json
import traceback
from invoice_ocr import extract_text_from_pdf
from invoice_to_json import convert_document_to_json  # updated function name

PDF_FOLDER = "input_pdfs"
OUTPUT_FOLDER = "json_outputs"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

if __name__ == "__main__":

    print("Starting Batch Document Processing...\n")

    pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.lower().endswith(".pdf")]

    if not pdf_files:
        print("No PDF files found in input_pdfs folder.")
    else:
        total_files = len(pdf_files)
        success_count = 0
        failed_count = 0

        for index, pdf_file in enumerate(pdf_files, start=1):

            print(f"[{index}/{total_files}] Processing: {pdf_file}")

            pdf_path = os.path.join(PDF_FOLDER, pdf_file)

            try:
                # ==========================
                # Step 1: OCR
                # ==========================
                print(" Extracting text...")
                document_text = extract_text_from_pdf(pdf_path)

                if not document_text.strip():
                    raise ValueError("OCR returned empty text.")

                # ==========================
                # Step 2: Convert to JSON (AI)
                # ==========================
                print(" Converting to structured JSON...")
                result = convert_document_to_json(document_text)

                if not result:
                    raise ValueError("AI returned empty JSON.")

                # ==========================
                # Step 3: Save JSON
                # ==========================
                json_filename = os.path.splitext(pdf_file)[0] + ".json"
                json_path = os.path.join(OUTPUT_FOLDER, json_filename)

                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(result, f, indent=4)

                print(f" Saved: {json_filename}\n")
                success_count += 1

            except Exception as e:
                print(f" Error processing {pdf_file}")
                print(f"  {str(e)}")
                traceback.print_exc()
                print()
                failed_count += 1

        
        print("=====================================")
        print("Processing Summary")
        print(f"Total Files: {total_files}")
        print(f"Successful: {success_count}")
        print(f"Failed: {failed_count}")
        print("Batch Processing Completed!")