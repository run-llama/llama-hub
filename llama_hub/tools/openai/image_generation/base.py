"""Azure Speech tool spec."""

from typing import Optional
from llama_index.tools.tool_spec.base import BaseToolSpec


class OpenAIImageGenerationToolSpec(BaseToolSpec):
    """OpenAI Image Generation tool spec."""

    spec_functions = ["image_generation"]

    def __init__(self, api_key: str) -> None:
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError(
                "Please install openai with `pip install openai` to use this tool"
            )

        """Initialize with parameters."""
        self.client = OpenAI(api_key=api_key)

    def image_generation(
        self,
        text: str,
        size: Optional[str] = "1024x1024",
        model: Optional[str] = "dall-e-3",
        quality: Optional[str] = "standard",
        num_images: Optional[int] = 1,
        response_format: Optional[str] = "url",
    ) -> str:
        """
        This tool accepts a natural language string and will use OpenAI's DALL-E model to generate an image.

        args:
            text (str): The text to generate an image from.
            size (str): The size of the image to generate (1024x1024, 256x256, 512x512).
            model (str): The model to use to generate the image (dall-e-3, dall-e-2).
            quality (str): The quality of the image to generate (standard, hd).
            num_images (int): The number of images to generate.
            response_format (str): The format of the response.
        """
        response = self.client.images.generate(
            model=model,
            prompt=text,
            size=size,
            quality=quality,
            n=num_images,
            response_format=response_format,
        )

        if response_format == "url":
            image = response.data[0].url
        elif response_format == "b64_json":
            image = response.data[0].b64_json

        return image
