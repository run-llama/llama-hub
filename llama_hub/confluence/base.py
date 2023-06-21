"""Confluence reader."""
import os
from typing import List, Optional, Dict

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document

CONFLUENCE_API_TOKEN = "CONFLUENCE_API_TOKEN"
CONFLUENCE_PASSWORD = "CONFLUENCE_PASSWORD"
CONFLUENCE_USERNAME = "CONFLUENCE_USERNAME"


class ConfluenceReader(BaseReader):
    """Confluence reader.

    Reads a set of confluence pages given a space key and optionally a list of page ids

    For more on OAuth login, checkout:
        - https://atlassian-python-api.readthedocs.io/index.html
        - https://developer.atlassian.com/cloud/confluence/oauth-2-3lo-apps/

    Args:
        oauth2 (dict): Atlassian OAuth 2.0, minimum fields are `client_id` and `token`, where `token` is a dict and must at least contain "access_token" and "token_type".
        base_url (str): 'base_url' for confluence cloud instance, this is suffixed with '/wiki', eg 'https://yoursite.atlassian.com/wiki'
        cloud (bool): connecting to Confluence Cloud or self-hosted instance

    """

    def __init__(self, base_url: str = None, oauth2: Optional[Dict] = None, cloud: bool = True) -> None:
        if base_url is None:
            raise ValueError("Must provide `base_url`")

        self.base_url = base_url

        try:
            from atlassian import Confluence
        except ImportError:
            raise ImportError("`atlassian` package not found, please run `pip install atlassian-python-api`")
        self.confluence: Confluence = None
        if oauth2:
            self.confluence = Confluence(url=base_url, oauth2=oauth2, cloud=cloud)
        else:
            api_token = os.getenv(CONFLUENCE_API_TOKEN)
            if api_token is not None:
                self.confluence = Confluence(url=base_url, token=api_token, cloud=cloud)
            else:
                user_name = os.getenv(CONFLUENCE_USERNAME)
                if user_name is None:
                    raise ValueError(
                        "Must set environment variable `CONFLUENCE_USERNAME` if oauth, oauth2, or `CONFLUENCE_API_TOKEN` are not provided."
                    )
                password = os.getenv(CONFLUENCE_PASSWORD)
                if password is None:
                    raise ValueError(
                        "Must set environment variable `CONFLUENCE_PASSWORD` if oauth, oauth2, or `CONFLUENCE_API_TOKEN` are not provided."
                    )
                self.confluence = Confluence(url=base_url, username=user_name, password=password, cloud=cloud)

    def load_data(self, space_key: Optional[str] = None, page_ids: Optional[List[str]] = None,
                  label: Optional[str] = None, cql: Optional[str] = None, include_attachments=False,
                  include_children=False, limit = 50) -> List[Document]:
        if not space_key and not page_ids and not label and not cql:
            raise ValueError("Must specify at least one among `space_key`, `page_ids`, `label`, `cql` parameters.")

        try:
            import html2text  # type: ignore
        except ImportError:
            raise ImportError("`html2text` package not found, please run `pip install html2text`")

        docs = []

        text_maker = html2text.HTML2Text()
        text_maker.ignore_links = True
        text_maker.ignore_images = True

        if space_key:
            # Don't just query all the pages since the number of pages can be very large
            # instead we can page through them
            start = 0
            pages = []
            while True:
                pages_iter = self.confluence.get_all_pages_from_space(space_key, start=start, limit=limit, expand='body.storage.value')

                if len(pages_iter) == 0:
                    break

                start += len(pages_iter)
                pages.extend(pages_iter)

                # no more to fetch
                if len(pages_iter) < limit:
                    break

            for page in pages:
                doc = self.process_page(page, include_attachments, text_maker)
                docs.append(doc)

        if label:
            pages = self.confluence.get_all_pages_by_label(label=label, limit=limit, expand='body.storage.value')
            for page in pages:
                doc = self.process_page(page, include_attachments, text_maker)
                docs.append(doc)

        if cql:
            pages = self.confluence.cql(cql=cql, limit=limit, expand='body.storage.value')
            for page in pages:
                doc = self.process_page(page, include_attachments, text_maker)
                docs.append(doc)

        if label:
            pages = self.confluence.get_all_pages_by_label(label=label, expand='body.storage.value')
            for page in pages:
                doc = self.process_page(page, include_attachments, text_maker)
                docs.append(doc)

        if page_ids:
            # with the include children option we will dfs and get the children of all the pages 
            # requested
            if include_children:
                page_ids = self._dfs_page(self.confluence, page_ids[0])
            for page_id in page_ids:
                page = self.confluence.get_page_by_id(page_id=page_id, expand='body.storage.value')
                doc = self.process_page(page, include_attachments, text_maker)
                docs.append(doc)

        return docs

    def _dfs_page(self, raw_confluence, page_id):
        ret = []
        ret += [page_id]
        pages = self.confluence.get_page_child_by_type(page_id,  type='page', start=None, limit=None, expand=None)
        ids = [page['id'] for page in pages]
        for id in ids:
            ret += self._dfs_page(raw_confluence, id)
        return ret

    def process_page(self, page, include_attachments, text_maker):
        if include_attachments:
            attachment_texts = self.process_attachment(page['id'])
        else:
            attachment_texts = []
        text = text_maker.handle(page['body']['storage']['value']) + "".join(attachment_texts)
        return Document(text=text, doc_id=page['id'], extra_info={"title": page['title']})

    def process_attachment(self, page_id):
        try:
            import requests
            from PIL import Image
        except ImportError:
            raise ImportError("`pytesseract` or `pdf2image` or `Pillow` package not found, please run `pip install "
                              "pytesseract pdf2image Pillow`")

        # depending on setup you may also need to set the correct path for poppler and tesseract
        attachments = self.confluence.get_attachments_from_content(page_id)['results']
        texts = []
        for attachment in attachments:
            media_type = attachment['metadata']['mediaType']
            absolute_url = self.base_url + attachment['_links']['download']
            title = attachment['title']
            if media_type == 'application/pdf':
                text = title + self.process_pdf(absolute_url)
            elif media_type == 'image/png' or media_type == 'image/jpg' or media_type == 'image/jpeg':
                text = title + self.process_image(absolute_url)
            elif media_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                text = title + self.process_doc(absolute_url)
            elif media_type == 'application/vnd.ms-excel':
                text = title + self.process_xls(absolute_url)
            elif media_type == 'image/svg+xml':
                text = title + self.process_svg(absolute_url)
            else:
                continue
            texts.append(text)

        return texts

    def process_pdf(self, link):
        try:
            import pytesseract  # type: ignore
            from pdf2image import convert_from_bytes  # type: ignore
        except ImportError:
            raise ImportError(
                "`pytesseract` or `pdf2image` package not found, please run `pip install pytesseract pdf2image`")

        import pytesseract  # type: ignore
        from pdf2image import convert_from_bytes  # type: ignore

        response = self.confluence.request(path=link, absolute=True)
        text = ''

        if response.status_code != 200 or response.content == b'' or response.content is None:
            return text
        try:
            images = convert_from_bytes(response.content)
        except ValueError:
            return text

        for i, image in enumerate(images):
            image_text = pytesseract.image_to_string(image)
            text += f"Page {i + 1}:\n{image_text}\n\n"

        return text

    def process_image(self, link):
        try:
            import pytesseract  # type: ignore
            from PIL import Image  # type: ignore
            from io import BytesIO  # type: ignore
        except ImportError:
            raise ImportError(
                "`pytesseract` or `Pillow` package not found, please run `pip install pytesseract Pillow`")

        response = self.confluence.request(path=link, absolute=True)
        text = ''

        if response.status_code != 200 or response.content == b'' or response.content is None:
            return text
        try:
            image = Image.open(BytesIO(response.content))
        except OSError:
            return text

        return pytesseract.image_to_string(image)

    def process_doc(self, link):
        try:
            import docx2txt  # type: ignore
            from io import BytesIO  # type: ignore
        except ImportError:
            raise ImportError("`docx2txt` package not found, please run `pip install docx2txt`")

        response = self.confluence.request(path=link, absolute=True)
        text = ''

        if response.status_code != 200 or response.content == b'' or response.content is None:
            return text
        file_data = BytesIO(response.content)

        return docx2txt.process(file_data)

    def process_xls(self, link):
        try:
            import xlrd  # type: ignore
        except ImportError:
            raise ImportError("`xlrd` package not found, please run `pip install xlrd`")

        response = self.confluence.request(path=link, absolute=True)
        text = ''

        if response.status_code != 200 or response.content == b'' or response.content is None:
            return text

        workbook = xlrd.open_workbook(file_contents=response.content)
        for sheet in workbook.sheets():
            text += f"{sheet.name}:\n"
            for row in range(sheet.nrows):
                for col in range(sheet.ncols):
                    text += f"{sheet.cell_value(row, col)}\t"
                text += "\n"
            text += "\n"

        return text

    def process_svg(self, link):
        try:
            import pytesseract  # type: ignore
            from PIL import Image  # type: ignore
            from io import BytesIO  # type: ignore
            from svglib.svglib import svg2rlg  # type: ignore
            from reportlab.graphics.shapes import Drawing
            from reportlab.graphics import renderPM  # type: ignore
        except ImportError:
            raise ImportError(
                "`pytesseract`, `Pillow`, or `svglib` package not found, please run `pip install pytesseract Pillow svglib`")

        response = self.confluence.request(path=link, absolute=True)
        text = ''

        if response.status_code != 200 or response.content == b'' or response.content is None:
            return text

        drawing = svg2rlg(BytesIO(response.content))

        img_data = BytesIO()
        renderPM.drawToFile(drawing, img_data, fmt="PNG")
        img_data.seek(0)
        image = Image.open(img_data)

        return pytesseract.image_to_string(image)


if __name__ == "__main__":
    reader = ConfluenceReader()
