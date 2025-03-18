import os
import logging
import argparse
import pdfplumber
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def extract_tables_from_pdf(pdf_path):
    """
    Extract tables from a PDF file using pdfplumber.
    """
    tables = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                logging.info(f"Processing page {page_num + 1} of {pdf_path}")
                page_tables = page.extract_tables()
                if page_tables:
                    logging.info(f"Found {len(page_tables)} tables on page {page_num + 1}")
                    tables.extend(page_tables)
                else:
                    logging.warning(f"No tables found on page {page_num + 1}")
    except Exception as e:
        logging.error(f"Error extracting tables from {pdf_path}: {e}")
    return tables

def validate_and_clean_table(table):
    """
    Validate and clean extracted table data.
    """
    if not table:
        return None
    # Remove empty rows and columns
    cleaned_table = [row for row in table if any(cell and str(cell).strip() for cell in row)]
    if not cleaned_table:
        return None
    return cleaned_table

def save_tables_to_excel(tables, output_path, pdf_name):
    """
    Save extracted tables to an Excel file.
    """
    try:
        wb = Workbook()
        ws = wb.active
        ws.title = "Table_1"
        
        for i, table in enumerate(tables):
            if i > 0:
                ws = wb.create_sheet(title=f"Table_{i + 1}")
            df = pd.DataFrame(table)
            for row in dataframe_to_rows(df, index=False, header=False):
                ws.append(row)
        
        excel_file = os.path.join(output_path, f"{pdf_name}_tables.xlsx")
        wb.save(excel_file)
        logging.info(f"Saved tables to {excel_file}")
    except Exception as e:
        logging.error(f"Error saving tables to Excel: {e}")

def process_pdf(pdf_path, output_path):
    """
    Process a single PDF file.
    """
    try:
        logging.info(f"Processing PDF: {pdf_path}")
        tables = extract_tables_from_pdf(pdf_path)
        if not tables:
            logging.warning(f"No tables found in {pdf_path}")
            return
        
        cleaned_tables = [validate_and_clean_table(table) for table in tables]
        cleaned_tables = [table for table in cleaned_tables if table]
        
        if not cleaned_tables:
            logging.warning(f"No valid tables found in {pdf_path}")
            return
        
        pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
        save_tables_to_excel(cleaned_tables, output_path, pdf_name)
    except Exception as e:
        logging.error(f"Error processing {pdf_path}: {e}")

def process_folder(input_folder, output_folder):
    """
    Process all PDFs in a folder.
    """
    if not os.path.exists(input_folder):
        logging.error(f"Input folder does not exist: {input_folder}")
        return
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        logging.info(f"Created output folder: {output_folder}")
    
    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_folder, filename)
            logging.info(f"Found PDF: {filename}")
            process_pdf(pdf_path, output_folder)

def main():
    """
    Command-line interface for the tool.
    """
    parser = argparse.ArgumentParser(description="Extract tables from PDFs and save them to Excel files.")
    parser.add_argument("input", help="Path to the input PDF file or folder.")
    parser.add_argument("output", help="Path to the output folder for Excel files.")
    args = parser.parse_args()
    
    if os.path.isfile(args.input) and args.input.endswith(".pdf"):
        process_pdf(args.input, args.output)
    elif os.path.isdir(args.input):
        process_folder(args.input, args.output)
    else:
        logging.error("Invalid input path. Please provide a valid PDF file or folder.")

if __name__ == "__main__":
    main()
