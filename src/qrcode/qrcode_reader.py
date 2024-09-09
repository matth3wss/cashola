import os

import requests


class QRCodeReader:
    def __init__(self, api_url="http://api.qrserver.com/v1/read-qr-code/"):
        self.api_url = api_url

    def read_qr_code(self, image_path: str) -> str:
        """Lê um código QR de uma imagem e retorna os dados contidos nele.

        Parameters
        ----------
        image_path : str
            O caminho para a imagem contendo o código QR.

        Returns
        -------
        str
            Os dados contidos no código QR.

        Raises
        ------
        FileNotFoundError
            O arquivo não foi encontrado.
        ValueError
            O código QR não pôde ser lido.
        """
        try:
            # Check if the file exists
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"The file at {image_path} does not exist.")

            # Open the image file and send it to the API
            with open(image_path, "rb") as image_file:
                files = {"file": image_file}
                response = requests.post(self.api_url, files=files)

                # Check for HTTP errors
                response.raise_for_status()

                # Parse the JSON response
                qr_data = response.json()

                # Check if the QR code was successfully read
                if qr_data and qr_data[0]["symbol"][0]["error"] is None:
                    return qr_data[0]["symbol"][0]["data"]
                else:
                    error_message = qr_data[0]["symbol"][0]["error"] or "Unknown error"
                    raise ValueError(f"Error reading QR code: {error_message}")

        except FileNotFoundError as fnf_error:
            return f"File error: {fnf_error}"
        except requests.exceptions.RequestException as req_error:
            return f"Request error: {req_error}"
        except ValueError as val_error:
            return f"QR code error: {val_error}"
        except Exception as general_error:
            return f"An unexpected error occurred: {general_error}"
