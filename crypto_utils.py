import os
import json
import base64
import hashlib


from Crypto.Cipher import DES

from Crypto.Random import get_random_bytes

from Crypto.PublicKey import RSA

from Crypto.Signature import pkcs1_15

from Crypto.Hash import SHA256





# ==================================================
# THƯ MỤC KEY
# ==================================================

KEY_FOLDER = "keys"


PRIVATE_KEY = os.path.join(
    KEY_FOLDER,
    "private.pem"
)


PUBLIC_KEY = os.path.join(
    KEY_FOLDER,
    "public.pem"
)





# ==================================================
# TẠO RSA KEY
# ==================================================

def generate_rsa_keys():


    os.makedirs(

        KEY_FOLDER,

        exist_ok=True

    )



    if os.path.exists(PRIVATE_KEY) and os.path.exists(PUBLIC_KEY):

        return




    key = RSA.generate(2048)



    private_key = key.export_key()

    public_key = key.publickey().export_key()



    with open(

        PRIVATE_KEY,

        "wb"

    ) as f:

        f.write(private_key)




    with open(

        PUBLIC_KEY,

        "wb"

    ) as f:

        f.write(public_key)





# ==================================================
# TẠO KHÓA DES
# ==================================================

def generate_des_key():


    return get_random_bytes(8)





# ==================================================
# DES ENCRYPT
# ==================================================

def des_encrypt(data, key):


    cipher = DES.new(

        key,

        DES.MODE_EAX

    )



    ciphertext, tag = cipher.encrypt_and_digest(

        data

    )



    package = {


        "nonce": cipher.nonce,

        "tag": tag,

        "data": ciphertext


    }


    return package





# ==================================================
# DES DECRYPT
# ==================================================

def des_decrypt(package, key):


    cipher = DES.new(

        key,

        DES.MODE_EAX,

        nonce=package["nonce"]

    )



    data = cipher.decrypt_and_verify(

        package["data"],

        package["tag"]

    )


    return data





# ==================================================
# SHA-256
# ==================================================

def sha256(data):


    if isinstance(data, dict):


        raw = (

            data["data"]

        )

    else:

        raw = data



    return hashlib.sha256(

        raw

    ).hexdigest()





# ==================================================
# RSA KÝ
# ==================================================

def rsa_sign(hash_value):


    with open(

        PRIVATE_KEY,

        "rb"

    ) as f:


        private_key = RSA.import_key(

            f.read()

        )



    h = SHA256.new(

        hash_value.encode()

    )



    signature = pkcs1_15.new(

        private_key

    ).sign(

        h

    )


    return signature





# ==================================================
# RSA VERIFY
# ==================================================

def rsa_verify(hash_value, signature):


    with open(

        PUBLIC_KEY,

        "rb"

    ) as f:


        public_key = RSA.import_key(

            f.read()

        )



    h = SHA256.new(

        hash_value.encode()

    )


    try:


        pkcs1_15.new(

            public_key

        ).verify(

            h,

            signature

        )


        return True



    except:


        return False





# ==================================================
# ĐÓNG GÓI JSON
# ==================================================

def create_package(

        encrypted_audio,

        des_key,

        signature,

        hash_value

):


    package = {


        "encrypted_audio": {


            "nonce":
            base64.b64encode(

                encrypted_audio["nonce"]

            ).decode(),



            "tag":
            base64.b64encode(

                encrypted_audio["tag"]

            ).decode(),



            "data":
            base64.b64encode(

                encrypted_audio["data"]

            ).decode()


        },



        "des_key":

        base64.b64encode(

            des_key

        ).decode(),



        "signature":

        base64.b64encode(

            signature

        ).decode(),



        "hash":

        hash_value

    }


    return package





# ==================================================
# LƯU JSON
# ==================================================

def save_json(package, filename):


    with open(

        filename,

        "w",

        encoding="utf-8"

    ) as f:


        json.dump(

            package,

            f,

            indent=4

        )





# ==================================================
# ĐỌC JSON
# ==================================================

def load_json(filename):


    with open(

        filename,

        "r",

        encoding="utf-8"

    ) as f:


        package = json.load(f)



    return decode_package(package)





# ==================================================
# GIẢI MÃ PACKAGE SAU KHI ĐỌC JSON
# ==================================================

def decode_package(package):


    package["encrypted_audio"] = {


        "nonce":

        base64.b64decode(

            package["encrypted_audio"]["nonce"]

        ),



        "tag":

        base64.b64decode(

            package["encrypted_audio"]["tag"]

        ),



        "data":

        base64.b64decode(

            package["encrypted_audio"]["data"]

        )

    }





    package["des_key"] = base64.b64decode(

        package["des_key"]

    )





    package["signature"] = base64.b64decode(

        package["signature"]

    )



    return package