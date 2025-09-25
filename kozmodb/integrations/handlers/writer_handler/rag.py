from langchain_community.llms import Writer

from kozmodb.integrations.handlers.rag_handler.rag import RAGQuestionAnswerer
from kozmodb.integrations.handlers.writer_handler.settings import (
    WriterHandlerParameters,
)


class QuestionAnswerer(RAGQuestionAnswerer):
    def __init__(self, args: WriterHandlerParameters):

        super().__init__(args)

        self.llm = Writer(**args.llm_params.model_dump())
