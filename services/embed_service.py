from tempfile import NamedTemporaryFile
from typing import IO

from ai_models.embed_model import EmbedModel
from fastapi import UploadFile

from models.embed_count import EmbedCount
from models.embed_result import EmbedResult


class EmbedService:
    embed_model = EmbedModel()

    def embed(self, file: UploadFile) -> EmbedResult:
        f = self.embed_model.embed
        filename = self.__process_with_file(file.file, f)
        return EmbedResult(filename)

    def count(self) -> EmbedCount:
        return EmbedCount(self.embed_model.count())

    @staticmethod
    def __process_with_file(file: IO, f: type(str)):
        with NamedTemporaryFile("wb", delete=True) as temp_file:
            temp_file.write(file.read())
            filename = temp_file.name
            return filename
