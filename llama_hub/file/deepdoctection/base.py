"""Deepdoctection Data Reader."""

from pathlib import Path
from typing import List, Optional, Set

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document


class DeepDoctectionReader(BaseReader):
    """Deepdoctection reader for pdf's and image scans

    Uses deepdoctection as a library to parse PDF files.

    """

    def __init__(
        self,
        split_by_layout: bool = False,
        config_overwrite: Optional[List] = None,
        extra_info: Optional[Set] = None,
    ) -> None:
        """Init params.

        Args:
            split_by_layout (bool): If `True` will use layout section detected by deepdoctection's layout models to
                                    create documents.
                                    For the default settings this will be `text`, `title`, `list` and `table`.
                                    Otherwise, it will generate one document per page.
            config_overwrite (List): Overwrite the deepdoctection default configuration, e.g.
                                     ['USE_TABLE_SEGMENTATION=False', 'USE_OCR=False'].
            extra_info (Set): Adding metadata to a document. Available attributes depend on `split_by_layout`.
                              When creating Documents on page level, then available will be:
                              - `file_name`: Original name of PDF-document/ image file
                              - `location`: Full path to the original document
                              - `document_id`: uuid derived from the location
                              - `page_number`: page number in multipage document. Defaults to 1 for a single image file
                              - `image_id`: uuid for a single page. Coincides with `document_id` for single page files
                              When using layout sections as documents, then all attributes on page level are available
                              as well as:
                              - `annotation_id`: uuid for layout section
                              - `reading_order`: reading order position of layout section within page scope
                              - `category_name`: type of layout section described above
        """
        import deepdoctection as dd

        self.analyzer = dd.get_dd_analyzer(config_overwrite=config_overwrite)
        self.split_by_layout = split_by_layout
        self.extra_info_attrs = extra_info or set()
        self._key_to_chunk_position = {
            "document_id": 0,
            "image_id": 1,
            "page_number": 2,
            "annotation_id": 3,
            "reading_order": 4,
            "category_name": 5,
        }

    def load_data(self, file: Path) -> List[Document]:
        """Parse file or directory with scans."""
        df = self.analyzer.analyze(path=str(file))
        df.reset_state()
        result_docs = []
        for page in df:
            if self.split_by_layout:
                result_docs.extend(
                    Document(
                        text=chunk[6],
                        extra_info={
                            k: chunk[self._key_to_chunk_position[k]]
                            for k in self.extra_info_attrs
                        },
                    )
                    for chunk in page.chunks
                )
            else:
                extra_info = {
                    k: getattr(page, k)
                    for k in self.extra_info_attrs
                    if hasattr(page, k)
                }
                result_docs.append(Document(text=page.text, extra_info=extra_info))
        return result_docs
