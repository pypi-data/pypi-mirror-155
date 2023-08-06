import base64
import hashlib
import hmac
import os
import struct
import sys
import time
from urllib.parse import parse_qs, urlparse

import cv2

import generated_python.google_auth_pb2


class GoogleAuthenticator:
    def __init__(self, data):
        """
        The data parameter accepts a filepath to an image of a google authenticator qr code, or a google
        authenticator url or a secret directly.

        Most of this clases induvidual functions also accept the respective data required to perform their actions.
        
        :param data: The data parameter accepts a filepath to an image of a google authenticator qr code,
        """
        self.data = data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._datatype = self.check_data_type(value)
        self._data = value

    def check_data_type(self, data):
        """
        It checks if the data is a url, filepath, or secret
        
        :param data: The data to be encrypted
        :return: the data type of the input.
        """
        data = data.strip()
        if "://" in data:
            return "url"
        elif "\\" in data or "/" in data:
            return "filepath"
        elif " " not in data:
            return "secret"
        raise ValueError("Not a valid datatype")

    @staticmethod
    def convert_secret_from_bytes_to_base32_str(bytes):
        return str(base64.b32encode(bytes), 'utf-8').replace('=', '')

    def grab_secret_from_url(self, url=None):
        """
        It takes a URL, parses it, decodes the base64 encoded data, parses the data into a protobuf object,
        and returns the secret
        
        :param url: The URL that you got from the QR code
        :return: The secret key in base32 format.
        """
        url = url or (self._data if self._datatype == "url" else None)

        parsed_url = urlparse(url)
        params = parse_qs(parsed_url.query)
        data_encoded = params['data'][0]

        b64 = base64.b64decode(data_encoded)
        payload = generated_python.google_auth_pb2.MigrationPayload()
        payload.ParseFromString(b64)

        otp = payload.otp_parameters

        return self.convert_secret_from_bytes_to_base32_str(otp[0].secret)

    def grab_secret_from_qr(self, filename=None):
        """
        It takes a filepath to an image, reads the image, detects the QR code, decodes the QR code, and then
        passes the decoded QR code to the `grab_secret_from_url` function
        
        :param filename: The path to the image file
        :return: The secret key is being returned.
        """
        filename = filename or self._data if self._datatype == "filepath" else None
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Unable to locate {filename}")
        image = cv2.imread(filename)
        detector = cv2.QRCodeDetector()
        data, vertices_array, binary_qrcode = detector.detectAndDecode(image)

        return self.grab_secret_from_url(data)

    def get_otp_qr_image(self, image_filename):
        return self._get_totp_token(self.grab_secret_from_qr(image_filename))

    def _get_hotp_token(self, secret, intervals_no):
        """
        It takes a secret key and an interval number, and returns a 6 digit number.
        
        :param secret: The secret key that is shared between the client and the server
        :param intervals_no: The number of intervals that have passed since the Unix epoch
        :return: A OTP
        """
        if secret is None:
            raise ValueError("Secret has not been set.")

        # Decoding the secret key from base32 to binary.
        key = base64.b32decode(secret, True)

        # Converting the intervals_no to a byte string.
        msg = struct.pack(">Q", intervals_no)

        # Creating a hash of the key and the message.
        h = hmac.new(key, msg, hashlib.sha1).digest()

        # Extracting the last 4 bits of the last byte of the hash.
        o = h[19] & 15
        h = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000

        return str(h).zfill(6)

    def _parse_data(self):
        """
        If the data type is a url, grab the secret from the url. If the data type is a filepath, grab the
        secret from the QR code. If the data type is a secret, return the data
        :return: The secret key
        """
        if self._datatype == "url":
            return self.grab_secret_from_url()
        elif self._datatype == "filepath":
            return self.grab_secret_from_qr()
        elif self._datatype == "secret":
            return self.data

    def display_code(self):
        """
        It prints the current TOTP code, and the time to expiration (TTE) of the code, in a loop
        """
        while 1:
            print(f"\rCode: {self._get_totp_token()} - TTE: {30-time.time()%30:.0f} ", end="")
            time.sleep(1)

    def _get_totp_token(self, secret=None):
        secret = secret or self._parse_data()
        return self._get_hotp_token(secret, intervals_no=int(time.time())//30)
    
    @property
    def otp(self):
        return self._get_totp_token()

if __name__ == "__main__":
    """Pass the the secret in as an argument and print the one time password."""
    auth = GoogleAuthenticator(" ".join(sys.argv[1:]))
    print(auth.otp)
