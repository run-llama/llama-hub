from llama_hub.smart_pdf_loader import SmartPDFLoader
import unittest

class TestLayoutReader(unittest.TestCase):
    def test_loader(self):
        llmsherpa_api_url = "https://readers.llmsherpa.com/api/document/developer/parseDocument?renderFormat=all"
        pdf_url = "https://arxiv.org/pdf/1910.13461.pdf" # also allowed is a file path e.g. /home/downloads/xyz.pdf
        pdf_loader = SmartPDFLoader(llmsherpa_api_url=llmsherpa_api_url)
        documents = pdf_loader.load_data(pdf_url)
        self.assertEqual(len(documents), 126)
        
if __name__ == '__main__':
    unittest.main()