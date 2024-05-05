import os
from tempfile import NamedTemporaryFile
from typing import IO

from ai_models.embed_model import EmbedModel
from fastapi import UploadFile


class EmbedService:
    temp_directory_path = os.environ["PDF_TEMP_DIRECTORY"]
    embed_model = EmbedModel()

    def embed(self, file: UploadFile):
        f = self.embed_model.embed
        result = self.process_temp_file(file.file, f)
        return result

    def count(self):
        return self.embed_model.count()

    def process_temp_file(self, file: IO, f: type(str)):
        with NamedTemporaryFile("wb", delete=True) as temp_file:
            temp_file.write(file.read())
            filename = temp_file.name
            print(filename)
            return f(filename)
