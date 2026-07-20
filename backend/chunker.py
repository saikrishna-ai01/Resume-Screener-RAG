from langchain_text_splitters import RecursiveCharacterTextSplitter


class ResumeChunker:

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 100
    ):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def create_chunks(
        self,
        filename: str,
        document_type: str,
        text: str
    ) -> list:

        pieces = self.splitter.split_text(text)

        chunks = []

        for index, piece in enumerate(pieces, start=1):

            chunks.append({

                "chunk_id": index,

                "filename": filename,

                "document_type": document_type,

                "text": piece

            })

        return chunks