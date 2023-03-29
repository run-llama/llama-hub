"""Simple reader that reads flatten PDFs."""
import os
import pathlib
import warnings
from pathlib import Path

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document


class FlatPdfReader(BaseReader):

    pdf_dir: Path
    pdf_name: str
    pdf_pages_count: int
    pdf_content: str = ""
    work_dir: str

    def __init__(self, image_loader: BaseReader):
        """
        :param self: Represent the instance of the class
        :param image_loader: BaseReader: Pass the image_loader object to the class
        :return: An object of the class
        """
        self.image_loader = image_loader

    def load_data(self, file: Path) -> Document:
        """
        The load_data function is the main function of the DataLoader class.
            It takes a PDF file path as input and returns a Document object with text extracted from that PDF.


        :param self: Represent the instance of the class
        :param file: Path: The file that we want to load
        :return: A document object
        """
        import shutil
        try:

            if not file.is_file() and file.suffix != ".pdf":
                raise Exception("Invalid file")

            self.pdf_dir = file
            self.pdf_name = file.name
            self.work_dir = str(pathlib.Path().resolve()) + "/flat_pdf/{file_name}".format(
                file_name=self.pdf_name.replace(file.suffix, ""))

            shutil.rmtree(str(pathlib.Path().resolve()) + f"/flat_pdf", ignore_errors=True)
            os.makedirs(self.work_dir)
            self.convert_pdf_in_images()
            for page_number in range(0, self.pdf_pages_count):
                document = self.image_loader.load_data(file=Path(self.work_dir + f"/page-{page_number}.png"))
                self.pdf_content += document.text
            return Document(text=self.pdf_content)

        except Exception as e:
            warnings.warn(
                f"{str(e)}"
            )
        finally:
            shutil.rmtree(str(pathlib.Path().resolve()) + f"/flat_pdf", ignore_errors=True)

    def convert_pdf_in_images(self) -> None:
        """
        The convert_pdf_in_images function takes a PDF file and converts it into images.
            The function uses the PyMuPDF library to open the PDF file, iterate through each page of the document,
            and render each page as an image. The rendered images are saved in a workdir.

        :param self: Represent the instance of the class
        :return: None
        """
        import fitz
        zoom_x = 2.0  # horizontal zoom
        zoom_y = 2.0  # vertical zoom
        mat = fitz.Matrix(zoom_x, zoom_y)
        pages = fitz.open(self.pdf_dir)
        self.pdf_pages_count = pages.page_count
        for page in pages:  # iterate through the pages
            image = page.get_pixmap(matrix=mat)  # render page to an image
            image.save(f"{self.work_dir}/page-{page.number}.png")
