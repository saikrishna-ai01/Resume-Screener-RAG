from pathlib import Path
import fitz
from docx import Document


class JDParser:
    """
    Job Description Parser

    Supports:
    - PDF (.pdf)
    - Word (.docx)
    - Text (.txt)

    Returns:
        {
            "text": "<Extracted Job Description Text>"
        }
    """

    SUPPORTED_EXTENSIONS = {
        ".pdf",
        ".docx",
        ".txt"
    }

    def parse(self, file_path: str) -> dict:

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        extension = path.suffix.lower()

        if extension not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(f"Unsupported file type: {extension}")

        if extension == ".pdf":
            text = self._parse_pdf(path)

        elif extension == ".docx":
            text = self._parse_docx(path)

        else:
            text = self._parse_txt(path)

        return {
            "text": self._clean_text(text)
        }

    def _parse_pdf(self, file_path: Path) -> str:

        document = fitz.open(str(file_path))
        pages = []

        for page in document:
            pages.append(page.get_text())

        document.close()

        return "\n".join(pages)

    def _parse_docx(self, file_path: Path) -> str:

        document = Document(str(file_path))

        paragraphs = []

        for paragraph in document.paragraphs:
            text = paragraph.text.strip()

            if text:
                paragraphs.append(text)

        return "\n".join(paragraphs)

    def _parse_txt(self, file_path: Path) -> str:

        encodings = [
            "utf-8",
            "utf-8-sig",
            "cp1252",
            "latin-1"
        ]

        for encoding in encodings:

            try:
                with open(file_path, "r", encoding=encoding) as file:
                    return file.read()

            except UnicodeDecodeError:
                continue

        raise ValueError(f"Unable to decode text file: {file_path}")

    def _clean_text(self, text: str) -> str:

        lines = []

        for line in text.splitlines():

            line = line.strip()

            if line:
                lines.append(line)

        return "\n".join(lines)
    