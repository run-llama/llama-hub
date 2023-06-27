"""Simple reader that reads flatten PDFs."""
import os
import pathlib
import warnings
from pathlib import Path

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document


class FlatPdfReader(BaseReader):
    image_loader: BaseReader

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

            pdf_dir: Path = file
            work_dir: str = str(
                pathlib.Path().resolve()
            ) + "/flat_pdf/{file_name}".format(
                file_name=file.name.replace(file.suffix, "")
            )
            pdf_content: str = ""

            shutil.rmtree(
                str(pathlib.Path().resolve()) + "/flat_pdf", ignore_errors=True
            )
            os.makedirs(work_dir)

            pdf_pages_count: int = self.convert_pdf_in_images(
                pdf_dir=pdf_dir, work_dir=work_dir
            )

            for page_number in range(0, pdf_pages_count):
                document = self.image_loader.load_data(
                    file=Path(work_dir + f"/page-{page_number}.png")
                )
                pdf_content += document[0].text
            return Document(text=pdf_content)

        except Exception as e:
            warnings.warn(f"{str(e)}")
        finally:
            shutil.rmtree(
                str(pathlib.Path().resolve()) + "/flat_pdf", ignore_errors=True
            )

    def convert_pdf_in_images(self, pdf_dir: Path, work_dir: str) -> int:
        """
        The convert_pdf_in_images function converts a PDF file into images.

        :param pdf_dir: Path: Specify the path of the pdf file to be converted
        :param work_dir: str: Specify the directory where the images will be saved
        :return: The number of pages in the pdf file
        """
        import fitz

        zoom_x = 2.0  # horizontal zoom
        zoom_y = 2.0  # vertical zoom
        mat = fitz.Matrix(zoom_x, zoom_y)
        pages = fitz.open(pdf_dir)
        for page in pages:  # iterate through the pages
            image = page.get_pixmap(matrix=mat)  # render page to an image
            image.save(f"{work_dir}/page-{page.number}.png")
        return pages.page_count
