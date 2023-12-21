import customtkinter as ctk
from PIL import Image, ImageEnhance, ImageFilter, ImageOps, ImageTk

from widgets import *
from menu import Menu
from settings import *
from model import Model


class Application(ctk.CTk):
    def __init__(self):
        # LOAD MODEL.
        self.model = Model()
        # SET-UP.
        super().__init__()
        ctk.set_appearance_mode("DARK")
        self.center_window(1000, 720)
        self.title("Photoshop")
        self.minsize(800, 500)
        self.binding_data()
        # CANVAS DATA.
        self.image_width = self.image_height = 0
        self.canvas_width = self.canvas_height = 0
        # LAYOUT.
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=3, uniform="A")
        self.columnconfigure(1, weight=7, uniform="A")
        # WIDGET.
        self.loader = ImageLoader(self, self.load_image)

    def center_window(self, width: int, height: int):
        self.geometry(
            f"{width}x{height}"
            + f"+{(self.winfo_screenwidth() - width) // 2}"
            + f"+{(self.winfo_screenheight() - height) // 2}"
        )

    def binding_data(self):
        # BINDING.
        self.load_default_effects()
        # TRACING.
        for data_source in self.binding_source.values():
            for binding_data in data_source.values():
                binding_data.trace_add("write", self.manipulate_image)

    def load_default_effects(self):
        self.binding_source: dict[str, dict[str, ctk.Variable]] = {
            "AFFINE": {
                "ROTATE": ctk.DoubleVar(value=DEFAULT_ROTATE),
                "ZOOM": ctk.DoubleVar(value=DEFAULT_ZOOM),
                "FLIP": ctk.StringVar(value=FLIP_OPTIONS[0]),
            },
            "COLOUR": {
                "GRAYSCALE": ctk.BooleanVar(value=DEFAULT_GRAYSCALE),
                "INVERT": ctk.BooleanVar(value=DEFAULT_INVERT),
                "EQUALIZE": ctk.IntVar(value=DEFAULT_EQUALIZE),
                "POSTERIZE": ctk.IntVar(value=DEFAULT_POSTERIZE),
                "SOLARIZE": ctk.IntVar(value=DEFAULT_SOLARIZE),
                "BRIGHTNESS": ctk.DoubleVar(value=DEFAULT_BRIGHTNESS),
                "VIBRANCE": ctk.DoubleVar(value=DEFAULT_VIBRANCE),
                "CONTRAST": ctk.DoubleVar(value=DEFAULT_CONTRAST),
                "SHARPNESS": ctk.DoubleVar(value=DEFAULT_SHARPNESS),
            },
            "EFFECT": {
                "EFFECT": ctk.StringVar(value=EFFECT_OPTIONS[0]),
                "FILTER": ctk.StringVar(value=FILTER_OPTIONS[0]),
                "BOXBLUR": ctk.IntVar(value=DEFAULT_BOXBLUR),
                "GAUSSIANBLUR": ctk.IntVar(value=DEFAULT_GAUSSIANBLUR),
                "UNSHARPMASK": ctk.IntVar(value=DEFAULT_UNSHARPMASK),
            },
        }

    def load_image(self, path: str):
        self.original = Image.open(path)
        self.image = self.original.copy()
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.image_ratio = self.image.width / self.image.height
        # HIDE THE IMAGE LOADER.
        self.loader.grid_forget()
        # OPEN THE IMAGE EDITOR.
        self.menu = Menu(self, self.binding_source, self.save_image, self.make_predict)
        self.editor = ImageEditor(self, self.resize_image)
        self.closer = CloseEditor(self, self.close_editor)

    # MENU METHOD.
    def save_image(self, file_path: str = None, file_name: str = None, extension: str = None):
        self.image.save(
            f"{file_path or 'image'}/{file_name or 'output'}.{extension or 'png'}"
        )

    def make_predict(self, bds_label_name: ctk.Variable):
        bds_label_name.set(self.model.predict(self.original))

    # EDITOR METHOD.
    def resize_image(self, event):
        # CURRENT RATIO.
        canvas_ratio = event.width / event.height
        # GET NEW WIDTH & HEIGHT OF IMAGE & CANVAS.
        self.canvas_width = event.width
        self.canvas_height = event.height
        if canvas_ratio > self.image_ratio:
            self.image_height = int(event.height)
            self.image_width = int(self.image_height * self.image_ratio)
        else:
            self.image_width = int(event.width)
            self.image_height = int(self.image_width / self.image_ratio)
        # SHOW IMAGE.
        self.show_image()

    # CLOSER METHOD.
    def close_editor(self):
        # CLEAR ALL EFFECTS.
        self.binding_data()
        # HIDE THE IMAGE EDITOR.
        self.menu.grid_forget()
        self.editor.grid_forget()
        self.closer.place_forget()
        # OPEN THE IMAGE LOADER.
        self.loader = ImageLoader(self, self.load_image)

    # MANIPULATE IMAGE.
    def manipulate_image(self, *args):
        # SEPERATE FROM ORIGINAL.
        self.image = self.original.copy()
        # MANIPULATE IMAGE.
        self.apply_affine()
        self.apply_colour()
        self.apply_effect()
        # SHOW MANIPULATED IMAGE.
        self.show_image()

    def apply_affine(self):
        # ROTATE.
        if (value := self.binding_source["AFFINE"]["ROTATE"].get()) != DEFAULT_ROTATE:
            self.image = self.image.rotate(value)
        # ZOOM.
        if (value := self.binding_source["AFFINE"]["ZOOM"].get()) != DEFAULT_ZOOM:
            self.image = ImageOps.crop(self.image, value)
        # FLIP.
        match self.binding_source["AFFINE"]["FLIP"].get():
            case "NONE":
                pass
            case "X":
                self.image = ImageOps.mirror(self.image)
            case "Y":
                self.image = ImageOps.flip(self.image)
            case "BOTH":
                self.image = ImageOps.flip(ImageOps.mirror(self.image))

    def apply_colour(self):
        # GRAYSCALE.
        if self.binding_source["COLOUR"]["GRAYSCALE"].get():
            self.image = ImageOps.grayscale(self.image)
        # INVERT.
        if self.binding_source["COLOUR"]["INVERT"].get():
            self.image = ImageOps.invert(self.image)
        # EQUALIZE.
        if (value := self.binding_source["COLOUR"]["EQUALIZE"].get()) != DEFAULT_EQUALIZE:
            grayscale = ImageOps.grayscale(self.image)
            mask = grayscale.point(lambda e: e < value)
            self.image = ImageOps.equalize(grayscale, mask=mask)
        # POSTERIZE.
        if (value := self.binding_source["COLOUR"]["POSTERIZE"].get()) != DEFAULT_POSTERIZE:
            grayscale = ImageOps.grayscale(self.image)
            self.image = ImageOps.posterize(grayscale, bits=value)
        # SOLARIZE.
        if (value := self.binding_source["COLOUR"]["SOLARIZE"].get()) != DEFAULT_SOLARIZE:
            self.image = ImageOps.solarize(self.image, threshold=value)
        # BRIGHTNESS.
        if (value := self.binding_source["COLOUR"]["BRIGHTNESS"].get()) != DEFAULT_BRIGHTNESS:
            ENHANCER = ImageEnhance.Brightness(self.image)
            self.image = ENHANCER.enhance(value)
        # VIBRANCE.
        if (value := self.binding_source["COLOUR"]["VIBRANCE"].get()) != DEFAULT_VIBRANCE:
            ENHANCER = ImageEnhance.Color(self.image)
            self.image = ENHANCER.enhance(value)
        # CONTRAST.
        if (value := self.binding_source["COLOUR"]["CONTRAST"].get()) != DEFAULT_CONTRAST:
            ENHANCER = ImageEnhance.Contrast(self.image)
            self.image = ENHANCER.enhance(value)
        # SHARPNESS.
        if (value := self.binding_source["COLOUR"]["SHARPNESS"].get()) != DEFAULT_SHARPNESS:
            ENHANCER = ImageEnhance.Sharpness(self.image)
            self.image = ENHANCER.enhance(value)

    def apply_effect(self):
        # EFFECT.
        match self.binding_source["EFFECT"]["EFFECT"].get():
            case "NONE":
                pass
            case "BLUR":
                self.image = self.image.filter(ImageFilter.BLUR)
            case "CONTOUR":
                self.image = self.image.filter(ImageFilter.CONTOUR)
            case "DETAIL":
                self.image = self.image.filter(ImageFilter.DETAIL)
            case "EMBOSS":
                self.image = self.image.filter(ImageFilter.EMBOSS)
            case "EDGE ENHANCE":
                self.image = self.image.filter(ImageFilter.EDGE_ENHANCE_MORE)
            case "FIND EDGES":
                self.image = self.image.filter(ImageFilter.FIND_EDGES)
            case "SHARPEN":
                self.image = self.image.filter(ImageFilter.SHARPEN)
            case "SMOOTH":
                self.image = self.image.filter(ImageFilter.SMOOTH_MORE)
        # FILTER.
        match self.binding_source["EFFECT"]["FILTER"].get():
            case "NONE":
                pass
            case "MEDIAN FILTER":
                self.image = self.image.filter(ImageFilter.MedianFilter(size=5))
            case "LOWPASS FILTER":
                self.image = self.image.filter(ImageFilter.MinFilter(size=5))
            case "HIGHPASS FILTER":
                self.image = self.image.filter(ImageFilter.MaxFilter(size=5))
            case "FREQUENCY FILTER":
                self.image = self.image.filter(ImageFilter.ModeFilter(size=5))
        # BLUR.
        if (value := self.binding_source["EFFECT"]["BOXBLUR"].get()) != DEFAULT_BOXBLUR:
            self.image = self.image.filter(ImageFilter.BoxBlur(value))
        if (value := self.binding_source["EFFECT"]["GAUSSIANBLUR"].get()) != DEFAULT_GAUSSIANBLUR:
            self.image = self.image.filter(ImageFilter.GaussianBlur(value))
        if (value := self.binding_source["EFFECT"]["UNSHARPMASK"].get()) != DEFAULT_UNSHARPMASK:
            self.image = self.image.filter(ImageFilter.UnsharpMask(value))

    def show_image(self):
        # CUSTOMIZED IMAGE.
        self.image_tk = ImageTk.PhotoImage(
            self.image.resize((self.image_width, self.image_height))
        )
        # DISCARD BEFORE DRAW.
        self.editor.delete(ctk.ALL)
        self.editor.create_image(
            self.canvas_width / 2, self.canvas_height / 2, image=self.image_tk
        )

if __name__ == "__main__":
    Application().mainloop()
