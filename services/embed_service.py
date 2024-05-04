from ai_models.embed_model import EmbedModel

class EmbedService:
    embed_model = EmbedModel()

    def embed(self, file):
        return self.embed_model.embed("../test_resources/embed_test_file_1.pdf")

    def count(self):
        return self.embed_model.count()