import barcode
from barcode.writer import ImageWriter
import os
import sys
import tkinter as tk
from tkinter import messagebox
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
import cairosvg

class BarcodeGenerator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("barcode_generator_beta")
        # Create input fields and a button
        label1 = tk.Label(self.root, text="Project Number:")
        label1.pack()
        self.entry1 = tk.Entry(self.root, width=100)
        self.entry1.pack()
        label2 = tk.Label(self.root, text="Drawing Number:")
        label2.pack()
        self.entry2 = tk.Entry(self.root, width=100)
        self.entry2.pack()

        button = tk.Button(self.root, text="Generate Barcode", command=self.generate_barcode)
        button.pack()

    def generate_barcode(self):
        value1 = self.entry1.get()
        value2 = self.entry2.get()
        code = value1 + value2
        abspath = os.path.join(os.path.dirname(sys.executable), str(value1))
        if not os.path.isdir(abspath): 
            os.mkdir(abspath)
        fullname = os.path.join(abspath, value2)

        EAN = barcode.get_barcode_class('ean13')
        my_ean = EAN(code)
        my_ean.save(fullname)

        self.create_pdf(fullname, value2)

    def create_pdf(self, fullname, dnumber):
        pngfilename = fullname + '.png'
        cairosvg.svg2png(url=fullname +'.svg', write_to=pngfilename)

        # Create a new PDF
        c = canvas.Canvas(os.path.join(os.path.dirname(pngfilename), str(dnumber) + '.pdf'), pagesize=landscape(letter))
        # Draw the barcode image on the PDF
        c.drawImage(pngfilename, 20, 20, width=450, height=200)
        # Finalize the PDF
        c.save()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    BarcodeGenerator().run()
