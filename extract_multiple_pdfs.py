import os
import fitz  # PyMuPDF
import pandas as pd
from openpyxl import Workbook
import re


def extract_text_from_pdf(pdf_path):
    """Extract raw text from PDF."""
    doc = fitz.open(pdf_path)
    all_text = ""

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()
        all_text += text + "\n"

    doc.close()
    return all_text


def clean_text(raw_text):
    """Normalize and clean extracted text."""
    cleaned = re.sub(r'[^\x00-\x7F]+', ' ', raw_text)  # Remove non-ASCII characters
    cleaned = re.sub(r'\s+', ' ', cleaned)  # Normalize whitespace
    return cleaned.strip()


def parse_transactions(raw_text):
    """Parse transaction data from the extracted PDF text."""
    # Regex pattern to match transaction rows
    pattern = re.compile(
        r'(\d{2}-[A-Z]{3}-\d{4})\s+([A-Z])\s+(.*?)\s+([\d,]+(?:\.\d{2})?)?\s+([\d,]+(?:\.\d{2})?)?\s+([\d,]+(?:\.\d{2})?Dr|Cr)?'
    )

    transactions = []

    for match in pattern.finditer(raw_text):
        date, txn_type, description, debit, credit, balance = match.groups()

        # Clean the extracted data
        debit = debit.replace(",", "") if debit else "0.00"
        credit = credit.replace(",", "") if credit else "0.00"
        balance = balance.replace(",", "") if balance else "0.00"

        transactions.append({
            "Date": date.strip(),
            "Type": txn_type.strip(),
            "Description": description.strip(),
            "Debit": float(debit),
            "Credit": float(credit),
            "Balance": balance.strip()
        })

    return transactions


def save_to_excel(transactions, output_path):
    """Save transaction data to Excel."""
    df = pd.DataFrame(transactions)

    if df.empty:
        print(f"⚠️ No transactions found. Skipping {output_path}")
        return

    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Transactions')

    print(f"✅ Transactions saved to {output_path}")


def process_pdf(input_folder, output_folder):
    """Process all PDFs in the folder."""
    os.makedirs(output_folder, exist_ok=True)

    pdf_files = [f for f in os.listdir(input_folder) if f.endswith('.pdf')]

    if not pdf_files:
        print("❌ No PDF files found in the folder.")
        return

    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_folder, pdf_file)
        output_path = os.path.join(output_folder, f"{os.path.splitext(pdf_file)[0]}.xlsx")

        print(f"🔍 Processing {pdf_file}...")

        # Extract raw text
        raw_text = extract_text_from_pdf(pdf_path)
        cleaned_text = clean_text(raw_text)

        # Parse transactions
        transactions = parse_transactions(cleaned_text)

        # Save to Excel
        if transactions:
            save_to_excel(transactions, output_path)
        else:
            print(f"⚠️ No transactions found in {pdf_file}")


def main():
    """Main execution function."""
    input_folder = "./pdfs"
    output_folder = "./output"

    process_pdf(input_folder, output_folder)
    print("\n✅ Batch processing completed!")


if __name__ == "__main__":
    main()
