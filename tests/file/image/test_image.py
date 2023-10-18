from base64 import b64decode
import os
import sys
import tempfile


BLACK_PIXEL_PNG = b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
)


class ImageMock:
    mode = "RGB"

    def open(self, *args, **kwargs):
        return ImageMock()


class DummyModel:
    received_kwargs = None

    def generate(self, *args, **kwargs):
        self.received_kwargs = kwargs

    def image_to_string(self, *args, **kwargs):
        self.received_kwargs = kwargs
        return ""


def test_model_kwargs_with_pytesseract():
    from llama_hub.file.image.base import ImageReader

    # Mock subdependencies to just test the kwargs passing
    pil_mock = type(sys)("PIL")
    pil_mock.Image = ImageMock
    sys.modules["PIL"] = pil_mock

    pytesseract_mock = type(sys)("pytesseract")
    sys.modules["pytesseract"] = pytesseract_mock

    dummy_model = DummyModel()

    parser_config = dict(model=dummy_model, processor=None)
    model_kwargs = dict(foo="2", bar=3)

    loader = ImageReader(parser_config=parser_config, model_kwargs=model_kwargs)

    with tempfile.TemporaryDirectory() as tmpdir:
        test_file_path = os.path.join(tmpdir, "test.png")
        with open(test_file_path, "wb") as f:
            f.write(BLACK_PIXEL_PNG)

        loader.load_data(test_file_path)

    assert dummy_model.received_kwargs is not None
    assert all(
        dummy_model.received_kwargs[model_key] == model_val
        for model_key, model_val in model_kwargs.items()
    )
