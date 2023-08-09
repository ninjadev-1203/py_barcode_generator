# import barcode
# from barcode.writer import ImageWriter

import os
import sys

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

import qrcode

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch


class QRcodeGenerator:
    def __init__(self):
        self.PN = None

        self.root = tk.Tk()
        self.root.title("QRcode_generator_beta")
        self.frame = tk.Frame(self.root)
        self.frame.grid(row=0, column=0, columnspan=2,
                        padx=5, pady=5, sticky="W")
        self.buttongOpen = tk.Button(
            self.frame, text="Open Project Folder", command=self.open_file_dialog)
        self.buttongOpen.pack(side="left")

        self.label_project_path = tk.Label(self.frame, text="Project Number:")
        self.label_project_path.pack(side="left", padx=5,)

        self.frame1 = tk.Frame(self.root)
        self.frame1.grid(row=1, column=0, columnspan=2, padx=5, pady=0)

        self.tree = ttk.Treeview(self.frame1, columns=(
            'No', 'DN'), show='headings')

        self.tree.heading('No', text='No')
        self.tree.heading('DN', text='DN')
        self.tree.column('No', width=60)
        self.tree.column('DN', width=600)

        scrollbar = ttk.Scrollbar(
            self.frame1, orient='horizontal', command=self.tree.xview)
        scrollbar.pack(side='bottom', fill='x')

        self.tree.configure(xscrollcommand=scrollbar.set)
        self.tree.pack()

        self.buttonGen = tk.Button(
            self.root, text="Generate QRcode", command=self.generate_qrcode)
        self.buttonGen.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

    def delete_all_tree_items(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def open_file_dialog(self):
        pn_path = filedialog.askdirectory()
        self.PN = pn_path.split('/')[-1]
        maxPathLen = 50
        self.label_project_path.configure(
            text=("PN: " + pn_path[:maxPathLen] + '/ ... /' + self.PN) if len(pn_path) > maxPathLen else pn_path)

        self.get_files_in_directory(pn_path)
        self.delete_all_tree_items()
        for i in range(len(self.DNs)):
            self.tree.insert('', 'end', values=(str(i+1), str(self.DNs[i])))
        self.buttonGen.configure(
            text="Generate QRcode (" + str(len(self.DNs)) + ")")

    def convert_to_pdf(self, file):
        pass

    def get_files_in_directory(self, directory):
        self.DNs = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                print('==========', dirs)
                if not file[file.rfind('.'):] == '.pdf':
                    self.convert_to_pdf(file)
                file = file[:file.rfind('.')]
                if not file in self.DNs:
                    self.DNs.append(file)

    def generate_qrcode(self):
        if self.PN == None:
            messagebox.showwarning("Warning!", "Please select Project Folder.")
            return

        self.abspath = os.path.join(os.path.dirname(
            sys.executable), (self.PN + "_qrcode"))
        if not os.path.isdir(self.abspath):
            os.mkdir(self.abspath)

        for DN in self.DNs:
            code = self.PN + DN
            fullname = os.path.join(self.abspath, DN)

            ############### BarCode Generation ######################
            # EAN = barcode.get_barcode_class('code128')            #
            # my_ean = EAN(code)                                    #
            # my_ean.save(fullname)                                 #
            #########################################################

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(code)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            img.save(fullname + ".png")

        self.create_pdf()

    def create_pdf(self):
        c = canvas.Canvas(os.path.join(
            self.abspath, (self.PN + "_QRcode.pdf")), pagesize=A4)

        x = 50
        y = A4[1] - 90

        for DN in self.DNs:
            # check if coordinates exceed page dimensions to start a new page
            image = os.path.join(self.abspath, (DN + ".png"))
            if y <= 10:
                c.showPage()
                y = A4[1] - 90

            c.drawImage(image, x, y, width=1*inch, height=1 *
                        inch, preserveAspectRatio=True)
            textobject = c.beginText()
            textobject.setTextOrigin(x + 120, y + 55)
            textobject.setFont('Times-Roman', 12)
            lines = ["Project Number: " + self.PN, "Drawing Number: " + DN]
            for line in lines:
                textobject.textLine(line)
            c.drawText(textobject)
            y -= 1*inch + 10  # adjust according to image size and required space

        try:
            c.save()
        except Exception as e:
            messagebox.showwarning("Warning!", str(e))

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    QRcodeGenerator().run()
