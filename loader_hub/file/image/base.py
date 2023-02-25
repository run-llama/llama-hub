"""Image Reader.

A parser for image files.

"""

import re
from pathlib import Path
from typing import Dict, List, Optional

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document


class ImageReader(BaseReader):
    """Image parser.

    Extract text from images using DONUT.

    """

    def __init__(self, text_type: str = "plain_text") -> None:
        """Init parser."""

        if text_type == "plain_text":
            import pytesseract

            processor = None
            model = pytesseract
        else:
            from transformers import DonutProcessor, VisionEncoderDecoderModel

            processor = DonutProcessor.from_pretrained(
                "naver-clova-ix/donut-base-finetuned-cord-v2"
            )
            model = VisionEncoderDecoderModel.from_pretrained(
                "naver-clova-ix/donut-base-finetuned-cord-v2"
            )

        self.parser_config = {"processor": processor, "model": model}

    def load_data(
        self, file: Path, extra_info: Optional[Dict] = None
    ) -> List[Document]:
        """Parse file."""
        from PIL import Image

        model = self.parser_config["model"]
        processor = self.parser_config["processor"]

        if processor:
            import torch

            device = "cuda" if torch.cuda.is_available() else "cpu"
            model.to(device)
            # load document image
            image = Image.open(file)
            if image.mode != "RGB":
                image = image.convert("RGB")

            # prepare decoder inputs
            task_prompt = "<s_cord-v2>"
            decoder_input_ids = processor.tokenizer(
                task_prompt, add_special_tokens=False, return_tensors="pt"
            ).input_ids

            pixel_values = processor(image, return_tensors="pt").pixel_values

            outputs = model.generate(
                pixel_values.to(device),
                decoder_input_ids=decoder_input_ids.to(device),
                max_length=model.decoder.config.max_position_embeddings,
                early_stopping=True,
                pad_token_id=processor.tokenizer.pad_token_id,
                eos_token_id=processor.tokenizer.eos_token_id,
                use_cache=True,
                num_beams=1,
                bad_words_ids=[[processor.tokenizer.unk_token_id]],
                return_dict_in_generate=True,
            )

            sequence = processor.batch_decode(outputs.sequences)[0]
            sequence = sequence.replace(processor.tokenizer.eos_token, "").replace(
                processor.tokenizer.pad_token, ""
            )
            # remove first task start token
            text = re.sub(r"<.*?>", "", sequence, count=1).strip()
        else:
            # load document image
            image = Image.open(file)
            text = model.image_to_string(image)

        return [Document(text, extra_info=extra_info)]
