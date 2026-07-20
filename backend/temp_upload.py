import os
import tempfile


class TempFileHandler:

    @staticmethod
    def save_temp_file(upload_file):

        suffix = os.path.splitext(upload_file.filename)[1]

        temp = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        )

        temp.write(upload_file.file.read())
        temp.close()

        return temp.name

    @staticmethod
    def delete_temp_file(file_path):

        if os.path.exists(file_path):
            os.remove(file_path)