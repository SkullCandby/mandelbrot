import os
import argparse
import sys
import math
import time
import random
from tkinter import *
from PIL import Image, ImageTk
from mandelbrot import Mandelbrot


class Framework(Frame):
    def __init__(self, parent, h, x=-0.75, y=0, m=1.5, iterations=None, imgWidth=None, imgHeight=None, save=False, multi=True):
        Frame.__init__(self, parent)
        self.parent = parent
        self.parent.title("Mandelbrot")
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self)

        if None in {imgWidth, imgHeight}:
            imgWidth, imgHeight = h, h
        if imgWidth > imgHeight:
            ratio = imgHeight/imgWidth
            self.canvasW, self.canvasH = h, round(h*ratio)
        else:
            ratio = imgWidth/imgHeight
            self.canvasW, self.canvasH = round(h*ratio), h

        self.fractal = Mandelbrot(self.canvasW, self.canvasH, x=x, y=y, m=m, iterations=iterations, w=imgWidth, h=imgHeight, multi=multi)
        self.setPalette()
        self.pixelColors = []
        self.img = None
        self.save = save
        self.draw()

        parent.bind("<Button-1>", self.zoomIn)
        parent.bind("<Button-3>", self.zoomOut)
        parent.bind("<Control-1>", self.shiftView)
        parent.bind("<Control-3>", self.changePalette)
        parent.bind("<Button-2>", self.saveImage)

    def zoomIn(self, event):
        self.fractal.zoomIn(event)
        self.draw()

    def zoomOut(self, event):
        self.fractal.zoomOut(event)
        self.draw()

    def shiftView(self, event):
        self.fractal.shiftView(event)
        self.draw()

    def draw(self):
        print('-' * 20)
        start = time.time()
        self.fractal.getPixels()
        self.getColors()
        self.drawPixels()
        self.canvas.create_image(0, 0, image=self.background, anchor=NW)
        self.canvas.pack(fill=BOTH, expand=1)
        print("Process took {} seconds".format(round(time.time()-start, 2)))
        print("Current coordinates (x, y, m): {}, {}, {}".format(self.fractal.xCenter, self.fractal.yCenter, self.fractal.delta))

    def setPalette(self):
        palette = [(0, 0, 0)]
        redb = 2 * math.pi / (random.randint(0, 128) + 128)
        redc = 256 * random.random()
        greenb = 2 * math.pi / (random.randint(0, 128) + 128)
        greenc = 256 * random.random()
        blueb = 2 * math.pi / (random.randint(0, 128) + 128)
        bluec = 256 * random.random()
        for i in range(256):
            r = clamp(int(256 * (0.5 * math.sin(redb * i + redc) + 0.5)))
            g = clamp(int(256 * (0.5 * math.sin(greenb * i + greenc) + 0.5)))
            b = clamp(int(256 * (0.5 * math.sin(blueb * i + bluec) + 0.5)))
            palette.append((r, g, b))
        self.palette = palette

    def changePalette(self, event):
        self.setPalette()
        self.pixelColors = []
        self.getColors()
        self.drawPixels()
        self.canvas.create_image(0, 0, image=self.background, anchor=NW)
        self.canvas.pack(fill=BOTH, expand=1)

    def getColors(self):
        pixelColors = []
        for p in self.fractal.pixels:
            pixelColors.append(self.palette[p[2] % 256])
        self.pixelColors = pixelColors

    def drawPixels(self):
        img = Image.new('RGB', (self.fractal.w, self.fractal.h), "black")
        pixels = img.load()  # create the pixel map
        for index, p in enumerate(self.fractal.pixels):
            pixels[int(p[0]), int(p[1])] = self.pixelColors[index]
        self.img = img
        if self.save:
            self.saveImage(None)
        photoimg = ImageTk.PhotoImage(img.resize((self.canvasW, self.canvasH)))
        self.background = photoimg

    def saveImage(self, event):
        self.img.save("output/{}.png".format(time.strftime("%Y-%m-%d-%H:%M:%S")), "PNG", optimize=True)


def clamp(x):
    return max(0, min(x, 255))


def main():
    master = Tk()
    height = round(master.winfo_screenheight()*0.9)
    render = Framework(master, height, iterations=255,
                           imgWidth=800, imgHeight=800)
    master.geometry("{}x{}".format(render.canvasW, render.canvasH))
    master.mainloop()


if __name__ == "__main__":
    main()
