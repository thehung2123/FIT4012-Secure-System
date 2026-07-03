import sounddevice as sd
import soundfile as sf

import os
import datetime
import threading

import playsound



# ==================================================
# CẤU HÌNH AUDIO
# ==================================================

SAMPLE_RATE = 44100

CHANNELS = 1

RECORD_SECONDS = 5





# ==================================================
# GHI ÂM
# ==================================================

def record_voice():

    try:


        os.makedirs(

            "recordings",

            exist_ok=True

        )



        filename = (

            "recordings/voice_"

            +

            datetime.datetime.now().strftime(

                "%Y%m%d_%H%M%S"

            )

            +

            ".wav"

        )




        print(

            "🎙 Bắt đầu ghi âm..."

        )




        audio = sd.rec(

            int(

                RECORD_SECONDS *

                SAMPLE_RATE

            ),


            samplerate=SAMPLE_RATE,


            channels=CHANNELS,


            dtype="int16"

        )





        sd.wait()





        sf.write(

            filename,

            audio,

            SAMPLE_RATE

        )





        print(

            "✔ Ghi âm xong:",

            filename

        )




        return filename





    except Exception as e:


        raise Exception(

            "Không thể ghi âm: "

            +

            str(e)

        )







# ==================================================
# PHÁT AUDIO
# ==================================================

def play_audio(filename):

    try:



        if not os.path.exists(filename):


            raise FileNotFoundError(

                "Không tìm thấy file âm thanh"

            )





        print(

            "▶ Đang phát:",

            filename

        )





        # chạy riêng để không khóa giao diện

        thread = threading.Thread(

            target=playsound.playsound,

            args=(filename,)

        )



        thread.start()





    except Exception as e:



        raise Exception(

            "Không thể phát âm thanh: "

            +

            str(e)

        )







# ==================================================
# ĐỌC FILE AUDIO
# Dùng trước khi mã hóa DES
# ==================================================

def read_audio(filename):

    try:


        with open(

            filename,

            "rb"

        ) as file:



            data = file.read()



        return data





    except Exception as e:



        raise Exception(

            "Không đọc được file audio: "

            +

            str(e)

        )







# ==================================================
# LƯU AUDIO SAU GIẢI MÃ
# ==================================================

def save_audio(data):

    try:



        os.makedirs(

            "recordings",

            exist_ok=True

        )





        filename = (

            "recordings/received_"

            +

            datetime.datetime.now().strftime(

                "%Y%m%d_%H%M%S"

            )

            +

            ".wav"

        )





        with open(

            filename,

            "wb"

        ) as file:



            file.write(data)





        return filename





    except Exception as e:



        raise Exception(

            "Không thể lưu audio: "

            +

            str(e)

        )