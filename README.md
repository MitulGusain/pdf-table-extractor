### ✅ **README.md for the PDF Table Extractor**

---

### 📚 **PDF Table Extractor**

**Description:**  
This script extracts **text-based tables without borders** from multiple PDFs (such as bank statements or transaction records) and exports them into structured Excel files.

---

### 🚀 **Features**
- **Batch Processing:** Processes multiple PDFs in one go.  
- **Text Extraction:** Extracts raw text using `PyMuPDF`.  
- **Regex Parsing:** Detects transaction rows with date, description, debit, credit, and balance.  
- **Excel Export:** Saves each PDF's table as a separate Excel file.  
- **Data Cleaning:** Removes irregular characters and normalizes whitespace.  

---

### ⚙️ **Folder Structure**
Ensure your project folder is structured as follows:
```
pdf-table-extractor/
 ├── pdfs/                      # Folder with multiple PDFs  
 │     ├── file1.pdf  
 │     ├── file2.pdf  
 │     ├── test3.pdf             # Your uploaded PDF  
 │     └── ...  
 ├── output/                    # Folder for the Excel outputs  
 ├── extract_bank_statement.py  # The Python script  
 ├── README.md                  # Documentation  
 ├── venv/                      # Virtual environment (optional)  
```

---

### ⚡ **Installation Instructions**

✅ **1. Clone or Create the Project**
```bash
git clone <your-repo-url>  
cd pdf-table-extractor
```
Or manually create the folder structure.

✅ **2. Create a Virtual Environment**
```bash
python -m venv venv
```

✅ **3. Activate the Virtual Environment**
- **Windows:**
```bash
.\venv\Scripts\activate
```
- **Linux/macOS:**
```bash
source venv/bin/activate
```

✅ **4. Install Dependencies**
```bash
pip install PyMuPDF pandas openpyxl
```

---

### ▶️ **How to Run the Script**

1. Place your PDFs in the `/pdfs` folder.  
2. Open the terminal in the project directory.  
3. Run the script:
```bash
python extract_bank_statement.py
```

✅ **Output:**  
- The script extracts tables from each PDF and saves them as Excel files in the `/output` folder.  
- Each Excel file corresponds to a PDF with the same name.

---

### 📊 **Excel Output Example**
| Date         | Type | Description                  | Debit      | Credit     | Balance          |
|--------------|------|------------------------------|------------|------------|------------------|
| 04-Apr-2022  | T    | BY 06971000010040            | 25,000.00  | 0.00       | 30,38,234.66 Dr  |
| 30-May-2022  | T    | Inspection Charges Yearly    | 3,540.00   | 0.00       | 29,90,942.66 Dr  |
| 22-Jun-2023  | T    | JAY PEE AND SONS             | 1,00,000.00| 0.00       | 29,79,398.36 Dr  |

---

### 🔥 **Customization**
You can modify the **regex pattern** in `extract_bank_statement.py` if you encounter PDFs with different transaction formats.

---

### 🔥 **Troubleshooting**

✅ **1. No transactions are detected?**
- Print the raw text by adding this line after extraction:
```python
print(raw_text[:2000])
```
- If the text appears garbled, try applying OCR for image-based PDFs.

✅ **2. Empty Excel files?**
- Ensure that the PDF is text-based and not an image.
- Use `pdf2image` and `pytesseract` for OCR on image-based PDFs.

✅ **3. Missing Tesseract?**
If using OCR, ensure you have Tesseract installed:
- **Windows:** [Download Tesseract](https://github.com/tesseract-ocr/tesseract)  
- **Linux:**  
```bash
sudo apt install tesseract-ocr
```
- **macOS:**  
```bash
brew install tesseract
```

---

### 🔥 **Dependencies**
- `PyMuPDF` → PDF text extraction.  
- `pandas` → DataFrame manipulation.  
- `openpyxl` → Excel export.  
- `pdf2image` & `pytesseract` → (Optional) for OCR if you add support for image-based PDFs.  

---

### ✅ **License**
This project is licensed under the **MIT License**.

---

### 🚀 **Contributing**
If you want to improve the script:
- Fork the repository.  
- Create a new branch.  
- Make your changes and submit a pull request.  

---

### 💡 **Future Enhancements**
- 🛠️ Add OCR support for image-based PDFs.  
- 🚀 Improve regex flexibility for varied table formats.  
- ⚡ Parallel PDF processing for faster performance.  
