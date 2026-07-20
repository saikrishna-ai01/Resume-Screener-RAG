from pathlib import Path
from typing import Union

import fitz
from docx import Document

from backend.utils import (
    extract_email,
    extract_phone,
    extract_name,
)


class ResumeParser:

    SUPPORTED_EXTENSIONS = {
        ".pdf",
        ".docx",
        ".txt",
    }
    
    def parse(self, file_path: Union[str, Path]) -> dict:
        file_path = Path(file_path)
        if not file_path.exists():
           raise FileNotFoundError(file_path)
        extension = file_path.suffix.lower()

        if extension not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file type: {extension}"
            )

        if extension == ".pdf":
            text = self._parse_pdf(file_path)

        elif extension == ".docx":
            text = self._parse_docx(file_path)

        else:
            text = self._parse_txt(file_path)

        cleaned_text = self._clean_text(text)

        return {
            "filename": file_path.name,
            "extension": extension,
            "name": extract_name(cleaned_text),
            "email": extract_email(cleaned_text),
            "phone": extract_phone(cleaned_text),
            "text": cleaned_text,
        }

    def _parse_pdf(self, file_path):

        document = fitz.open(file_path)

        pages = []

        for page in document:
            pages.append(page.get_text())

        document.close()

        return "\n".join(pages)

    def _parse_docx(self, file_path):

        document = Document(file_path)

        paragraphs = []

        for paragraph in document.paragraphs:
            paragraphs.append(paragraph.text)

        return "\n".join(paragraphs)

    def _parse_txt(self, file_path):

        with open(
            file_path,
            "r",
            encoding="utf-8",
        ) as file:
            return file.read()

    def _clean_text(self, text):

        lines = []

        for line in text.splitlines():

            line = line.strip()

            if line:
                lines.append(line)

        return "\n".join(lines)