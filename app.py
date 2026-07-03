import customtkinter as ctk

from tkinter import filedialog, messagebox

from datetime import datetime

import os


# ===============================
# Module tự xây dựng
# ===============================

import audio_utils

import crypto_utils



# ===============================
# Cấu hình giao diện
# ===============================

ctk.set_appearance_mode("System")

ctk.set_default_color_theme("blue")





class SecureVoiceApp(ctk.CTk):


    def __init__(self):

        super().__init__()



        # ===============================
        # CẤU HÌNH CỬA SỔ
        # ===============================


        self.title(
            "ỨNG DỤNG BẢO MẬT TIN NHẮN THOẠI"
        )


        self.geometry(
            "1200x760"
        )


        self.resizable(
            False,
            False
        )




        # ===============================
        # TẠO THƯ MỤC
        # ===============================


        os.makedirs(
            "recordings",
            exist_ok=True
        )


        os.makedirs(
            "messages",
            exist_ok=True
        )


        os.makedirs(
            "keys",
            exist_ok=True
        )


        os.makedirs(
            "logs",
            exist_ok=True
        )




        # ===============================
        # TẠO RSA KEY
        # ===============================


        crypto_utils.generate_rsa_keys()




        # ===============================
        # BIẾN CHƯƠNG TRÌNH
        # ===============================


        self.current_audio = None

        self.current_json = None

        self.current_package = None

        self.current_des_key = None

        self.received_audio = None





        # ===============================
        # TIÊU ĐỀ
        # ===============================


        self.title_label = ctk.CTkLabel(


            self,


            text=
            "ỨNG DỤNG BẢO MẬT TIN NHẮN THOẠI\n"
            "Mã hóa DES và Xác thực RSA",


            font=
            ctk.CTkFont(
                size=24,
                weight="bold"
            )

        )


        self.title_label.pack(

            pady=18

        )





        # ===============================
        # FRAME CHÍNH
        # ===============================


        self.main_frame = ctk.CTkFrame(

            self,

            fg_color="transparent"

        )


        self.main_frame.pack(

            fill="both",

            expand=True,

            padx=20

        )





        ##################################################
        # KHUNG HÙNG - BÊN GỬI
        ##################################################


        self.sender_frame = ctk.CTkFrame(

            self.main_frame,

            width=420

        )


        self.sender_frame.pack(

            side="left",

            fill="both",

            expand=True,

            padx=10

        )





        self.sender_title = ctk.CTkLabel(

            self.sender_frame,


            text="BÊN GỬI (HÙNG)",


            font=
            ctk.CTkFont(

                size=18,

                weight="bold"

            )

        )


        self.sender_title.pack(

            pady=15

        )





        # ===============================
        # GHI ÂM
        # ===============================


        self.btn_record = ctk.CTkButton(


            self.sender_frame,


            text="🎙 Ghi âm tin nhắn",


            height=42,


            command=self.record_audio


        )


        self.btn_record.pack(

            padx=20,

            pady=8,

            fill="x"

        )





        # ===============================
        # NGHE LẠI
        # ===============================


        self.btn_preview = ctk.CTkButton(


            self.sender_frame,


            text="▶ Nghe lại bản ghi",


            height=42,


            command=self.preview_voice


        )


        self.btn_preview.pack(

            padx=20,

            pady=8,

            fill="x"

        )





        # ===============================
        # GỬI TIN
        # ===============================


        self.btn_encrypt = ctk.CTkButton(


            self.sender_frame,


            text="📤 Gửi tin nhắn",


            height=42,


            fg_color="green",


            hover_color="darkgreen",


            command=self.encrypt_voice


        )


        self.btn_encrypt.pack(

            padx=20,

            pady=8,

            fill="x"

        )
                ##################################################
        # KHUNG TUẤN - BÊN NHẬN
        ##################################################


        self.receiver_frame = ctk.CTkFrame(

            self.main_frame,

            width=420

        )


        self.receiver_frame.pack(

            side="right",

            fill="both",

            expand=True,

            padx=10

        )





        self.receiver_title = ctk.CTkLabel(

            self.receiver_frame,


            text="BÊN NHẬN (TUẤN)",


            font=
            ctk.CTkFont(

                size=18,

                weight="bold"

            )

        )


        self.receiver_title.pack(

            pady=15

        )





        # ===============================
        # NHẬN JSON
        # ===============================


        self.btn_open = ctk.CTkButton(


            self.receiver_frame,


            text="📂 Nhận gói tin JSON",


            height=42,


            command=self.open_json


        )


        self.btn_open.pack(

            padx=20,

            pady=8,

            fill="x"

        )





        # ===============================
        # XÁC THỰC RSA
        # ===============================


        self.btn_verify = ctk.CTkButton(


            self.receiver_frame,


            text="✔ Xác thực chữ ký số",


            height=42,


            command=self.verify_signature


        )


        self.btn_verify.pack(

            padx=20,

            pady=8,

            fill="x"

        )





        # ===============================
        # GIẢI MÃ
        # ===============================


        self.btn_decrypt = ctk.CTkButton(


            self.receiver_frame,


            text="🔓 Giải mã tin nhắn",


            height=42,


            fg_color="#d48806",


            hover_color="#ad6800",


            command=self.decrypt_voice


        )


        self.btn_decrypt.pack(

            padx=20,

            pady=8,

            fill="x"

        )





        # ===============================
        # PHÁT ÂM THANH
        # ===============================


        self.btn_play = ctk.CTkButton(


            self.receiver_frame,


            text="▶ Phát tin nhắn",


            height=42,


            command=self.play_voice


        )


        self.btn_play.pack(

            padx=20,

            pady=8,

            fill="x"

        )






        # ==================================================
        # KHUNG THÔNG TIN HỆ THỐNG
        # ==================================================


        self.info_frame = ctk.CTkFrame(

            self

        )


        self.info_frame.pack(

            fill="x",

            padx=20,

            pady=10

        )





        # ===============================
        # DES KEY
        # ===============================


        self.des_label = ctk.CTkLabel(

            self.info_frame,


            text="Khóa DES : --------",


            font=
            ctk.CTkFont(

                size=13

            )

        )


        self.des_label.grid(

            row=0,

            column=0,

            padx=15,

            pady=8,

            sticky="w"

        )





        # ===============================
        # RSA
        # ===============================


        self.rsa_label = ctk.CTkLabel(

            self.info_frame,


            text="RSA : Đã sẵn sàng",


            font=
            ctk.CTkFont(

                size=13

            )

        )


        self.rsa_label.grid(

            row=0,

            column=1,

            padx=15,

            pady=8

        )





        # ===============================
        # CHỮ KÝ
        # ===============================


        self.signature_label = ctk.CTkLabel(

            self.info_frame,


            text="Chữ ký số : Chưa xác thực",


            font=
            ctk.CTkFont(

                size=13

            )

        )


        self.signature_label.grid(

            row=0,

            column=2,

            padx=15,

            pady=8

        )





        # ===============================
        # HASH
        # ===============================


        self.hash_label = ctk.CTkLabel(

            self.info_frame,


            text="SHA-256 : --------",


            font=
            ctk.CTkFont(

                size=13

            )

        )


        self.hash_label.grid(

            row=1,

            column=0,

            columnspan=3,

            padx=15,

            pady=8,

            sticky="w"

        )






        # ==================================================
        # TRẠNG THÁI
        # ==================================================


        self.status_label = ctk.CTkLabel(

            self.info_frame,


            text="Trạng thái : Sẵn sàng",


            font=
            ctk.CTkFont(

                size=14,

                weight="bold"

            )

        )


        self.status_label.grid(

            row=2,

            column=0,

            columnspan=3,

            padx=15,

            pady=8,

            sticky="w"

        )





        # ==================================================
        # THỜI GIAN
        # ==================================================


        self.time_label = ctk.CTkLabel(

            self.info_frame,


            text="Thời gian : --",


            font=
            ctk.CTkFont(

                size=13

            )

        )


        self.time_label.grid(

            row=3,

            column=0,

            columnspan=3,

            padx=15,

            pady=5,

            sticky="w"

        )



        # chạy đồng hồ

        self.update_time()
            # ==================================================
    # CẬP NHẬT TRẠNG THÁI
    # ==================================================

    def update_status(self, text):

        self.status_label.configure(

            text=f"Trạng thái : {text}"

        )

        self.update()



    # ==================================================
    # HIỂN THỊ THỜI GIAN
    # ==================================================

    def update_time(self):

        now = datetime.now().strftime(

            "%H:%M:%S   %d/%m/%Y"

        )


        self.time_label.configure(

            text=f"Thời gian : {now}"

        )


        self.after(

            1000,

            self.update_time

        )
            # ==================================================
    # PHẦN HÙNG - BÊN GỬI
    # ==================================================


    # ==================================================
    # GHI ÂM TIN NHẮN
    # ==================================================

    def record_audio(self):

        try:

            self.update_status(
                "🎙 Hùng đang ghi âm..."
            )


            filename = audio_utils.record_voice()


            self.current_audio = filename


            self.update_status(
                "✔ Ghi âm hoàn tất"
            )


            messagebox.showinfo(
                "Ghi âm",
                f"Đã ghi âm thành công:\n{filename}"
            )


        except Exception as e:


            self.update_status(
                "❌ Lỗi ghi âm"
            )


            messagebox.showerror(
                "Lỗi ghi âm",
                str(e)
            )



    # ==================================================
    # NGHE LẠI BẢN GHI
    # ==================================================

    def preview_voice(self):

        try:


            if self.current_audio is None:


                messagebox.showwarning(
                    "Thông báo",
                    "Chưa có bản ghi âm"
                )

                return



            self.update_status(
                "▶ Đang phát bản ghi..."
            )


            audio_utils.play_audio(
                self.current_audio
            )


            self.update_status(
                "✔ Đã bắt đầu phát"
            )



        except Exception as e:


            self.update_status(
                "❌ Lỗi phát âm thanh"
            )


            messagebox.showerror(
                "Lỗi phát",
                str(e)
            )





    # ==================================================
    # MÃ HÓA VÀ GỬI TIN NHẮN
    # ==================================================

    def encrypt_voice(self):

        try:


            if self.current_audio is None:


                messagebox.showwarning(
                    "Thông báo",
                    "Hãy ghi âm trước khi gửi"
                )

                return



            # ===============================
            # Tạo khóa DES
            # ===============================

            self.update_status(
                "🔑 Đang tạo khóa DES..."
            )


            des_key = crypto_utils.generate_des_key()


            self.current_des_key = des_key



            self.des_label.configure(

                text=f"Khóa DES : {des_key.hex()}"

            )




            # ===============================
            # Đọc file âm thanh
            # ===============================

            self.update_status(
                "📖 Đang đọc file âm thanh..."
            )


            with open(

                self.current_audio,

                "rb"

            ) as file:


                audio_data = file.read()






            # ===============================
            # DES ENCRYPT
            # ===============================

            self.update_status(
                "🔐 Đang mã hóa DES..."
            )


            encrypted_audio = crypto_utils.des_encrypt(

                audio_data,

                des_key

            )






            # ===============================
            # HASH SHA-256
            # ===============================

            self.update_status(
                "🔎 Đang tạo SHA-256..."
            )



            # Ghép dữ liệu để hash

            hash_data = (

                encrypted_audio["nonce"]

                +

                encrypted_audio["tag"]

                +

                encrypted_audio["data"]

            )



            hash_value = crypto_utils.sha256(

                hash_data

            )



            self.hash_label.configure(

                text=f"SHA-256 : {hash_value[:32]}..."

            )







            # ===============================
            # RSA SIGN
            # ===============================

            self.update_status(
                "✍ Đang ký RSA..."
            )


            signature = crypto_utils.rsa_sign(

                hash_value

            )







            # ===============================
            # ĐÓNG GÓI JSON
            # ===============================

            self.update_status(
                "📦 Đang tạo gói tin JSON..."
            )


            package = crypto_utils.create_package(

                encrypted_audio,

                des_key,

                signature,

                hash_value

            )







            # ===============================
            # LƯU FILE JSON
            # ===============================

            filename = (

                "messages/message_"

                +

                datetime.now().strftime(

                    "%Y%m%d_%H%M%S"

                )

                +

                ".json"

            )



            crypto_utils.save_json(

                package,

                filename

            )



            self.current_json = filename





            self.update_status(
                "📤 Hùng đã gửi gói tin thành công"
            )



            messagebox.showinfo(

                "Gửi thành công",

                f"Gói tin đã tạo:\n{filename}"

            )



        except Exception as e:


            self.update_status(

                "❌ Lỗi mã hóa"

            )


            messagebox.showerror(

                "Lỗi mã hóa",

                str(e)

            )
                # ==================================================
    # PHẦN TUẤN - BÊN NHẬN
    # ==================================================



    # ==================================================
    # NHẬN GÓI TIN JSON
    # ==================================================

    def open_json(self):

        try:


            filename = filedialog.askopenfilename(

                title="Chọn gói tin JSON",

                filetypes=[

                    (

                        "JSON Files",

                        "*.json"

                    )

                ]

            )



            if not filename:

                return





            self.update_status(

                "📂 Đang mở gói tin..."

            )



            self.current_json = filename



            self.current_package = crypto_utils.load_json(

                filename

            )





            self.update_status(

                "✔ Tuấn đã nhận gói tin"

            )



            messagebox.showinfo(

                "Nhận gói tin",

                f"Đã mở:\n{filename}"

            )




        except Exception as e:


            self.update_status(

                "❌ Lỗi mở JSON"

            )


            messagebox.showerror(

                "Lỗi",

                str(e)

            )





    # ==================================================
    # XÁC THỰC CHỮ KÝ RSA
    # ==================================================

    def verify_signature(self):

        try:



            if self.current_package is None:


                messagebox.showwarning(

                    "Thông báo",

                    "Chưa nhận gói tin"

                )

                return





            self.update_status(

                "🔎 Đang kiểm tra SHA-256..."

            )




            package = self.current_package



            encrypted_audio = package["encrypted_audio"]



            old_hash = package["hash"]





            # ===============================
            # Tính lại hash
            # ===============================


            hash_data = (

                encrypted_audio["nonce"]

                +

                encrypted_audio["tag"]

                +

                encrypted_audio["data"]

            )



            new_hash = crypto_utils.sha256(

                hash_data

            )






            if new_hash != old_hash:


                self.signature_label.configure(

                    text="Chữ ký số : Dữ liệu bị thay đổi ❌"

                )


                self.update_status(

                    "❌ Sai Hash"

                )


                messagebox.showerror(

                    "Thất bại",

                    "Dữ liệu đã bị thay đổi"

                )


                return





            self.update_status(

                "✍ Đang kiểm tra RSA..."

            )



            result = crypto_utils.rsa_verify(

                old_hash,

                package["signature"]

            )






            if result:


                self.signature_label.configure(

                    text="Chữ ký số : Hợp lệ ✔"

                )


                self.update_status(

                    "✔ Xác thực thành công"

                )



                messagebox.showinfo(

                    "RSA",

                    "Chữ ký hợp lệ\nTin nhắn an toàn"

                )



            else:


                self.signature_label.configure(

                    text="Chữ ký số : Không hợp lệ ❌"

                )


                self.update_status(

                    "❌ RSA thất bại"

                )



                messagebox.showerror(

                    "RSA",

                    "Sai chữ ký"

                )





        except Exception as e:


            messagebox.showerror(

                "Lỗi xác thực",

                str(e)

            )





    # ==================================================
    # GIẢI MÃ ÂM THANH
    # ==================================================

    def decrypt_voice(self):

        try:



            if self.current_package is None:


                messagebox.showwarning(

                    "Thông báo",

                    "Chưa có gói tin"

                )

                return





            self.update_status(

                "🔓 Đang giải mã DES..."

            )





            package = self.current_package




            des_key = package["des_key"]



            self.current_des_key = des_key




            self.des_label.configure(

                text=f"Khóa DES : {des_key.hex()}"

            )






            decrypted_audio = crypto_utils.des_decrypt(

                package["encrypted_audio"],

                des_key

            )







            filename = audio_utils.save_audio(

                decrypted_audio

            )





            self.received_audio = filename





            self.update_status(

                "✔ Giải mã hoàn tất"

            )



            messagebox.showinfo(

                "Giải mã",

                f"Đã giải mã:\n{filename}"

            )





        except Exception as e:


            self.update_status(

                "❌ Lỗi giải mã"

            )


            messagebox.showerror(

                "Lỗi",

                str(e)

            )







    # ==================================================
    # PHÁT TIN NHẮN
    # ==================================================

    def play_voice(self):

        try:



            if self.received_audio is None:


                messagebox.showwarning(

                    "Thông báo",

                    "Chưa có file giải mã"

                )

                return





            self.update_status(

                "▶ Tuấn đang nghe..."

            )



            audio_utils.play_audio(

                self.received_audio

            )



            self.update_status(

                "✔ Đang phát âm thanh"

            )




        except Exception as e:



            messagebox.showerror(

                "Lỗi phát",

                str(e)

            )
            # ==================================================
# CHẠY CHƯƠNG TRÌNH
# ==================================================

if __name__ == "__main__":

    app = SecureVoiceApp()

    app.mainloop()