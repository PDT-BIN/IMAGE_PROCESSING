from panel import *


class Menu(ctk.CTkTabview):
    def __init__(
        self,
        parent,
        binding_source: dict[str, dict[str, ctk.Variable]],
        save_image: Callable[[str, str, str], None],
        make_predict: Callable[[ctk.Variable], str],
    ):
        super().__init__(master=parent)
        self.grid(column=0, row=0, sticky=ctk.NSEW, padx=10, pady=10)
        # TABS.
        self.add("AFFINE")
        self.add("COLOUR")
        self.add("EFFECT")
        self.add("CLASSIFY")
        # FRAMES.
        AffineFrame(self.tab("AFFINE"), binding_source["AFFINE"])
        ColourFrame(self.tab("COLOUR"), binding_source["COLOUR"])
        EffectFrame(self.tab("EFFECT"), binding_source["EFFECT"])
        ExportFrame(self.tab("CLASSIFY"), save_image, make_predict)


class AffineFrame(ctk.CTkFrame):
    def __init__(self, parent, data_source: dict[str, ctk.Variable]):
        super().__init__(master=parent, fg_color="transparent")
        self.pack(expand=True, fill=ctk.BOTH)
        # PANEL.
        SliderPanel(self, "Rotate", data_source["ROTATE"], 0, 360)
        SliderPanel(self, "Zoom", data_source["ZOOM"], 0, 200)
        SegmentPanel(self, "Flip", data_source["FLIP"], FLIP_OPTIONS)
        # RESET BUTTON.
        ResetButton(
            self,
            (data_source["ROTATE"], DEFAULT_ROTATE),
            (data_source["ZOOM"], DEFAULT_ZOOM),
            (data_source["FLIP"], FLIP_OPTIONS[0]),
        )


class ColourFrame(ctk.CTkFrame):
    def __init__(self, parent, data_source: dict[str, ctk.Variable]):
        super().__init__(master=parent, fg_color="transparent")
        self.pack(expand=True, fill=ctk.BOTH)
        # PANEL.
        SwitchPanel(
            self, ("B/W", data_source["GRAYSCALE"]), ("Invert", data_source["INVERT"])
        )
        SliderPanel(self, "Equalize", data_source["EQUALIZE"], 0, 255)
        SliderPanel(self, "Posterize", data_source["POSTERIZE"], 0, 8)
        SliderPanel(self, "Solarize", data_source["SOLARIZE"], 0, 255)
        SliderPanel(self, "Brightness", data_source["BRIGHTNESS"], 0, 10)
        SliderPanel(self, "Vibrance", data_source["VIBRANCE"], 0, 10)
        SliderPanel(self, "Contrast", data_source["CONTRAST"], 0, 10)
        SliderPanel(self, "Sharpness", data_source["SHARPNESS"], 0, 10)
        # RESET BUTTON.
        ResetButton(
            self,
            (data_source["INVERT"], DEFAULT_INVERT),
            (data_source["EQUALIZE"], DEFAULT_EQUALIZE),
            (data_source["POSTERIZE"], DEFAULT_POSTERIZE),
            (data_source["SOLARIZE"], DEFAULT_SOLARIZE),
            (data_source["BRIGHTNESS"], DEFAULT_BRIGHTNESS),
            (data_source["VIBRANCE"], DEFAULT_VIBRANCE),
            (data_source["CONTRAST"], DEFAULT_CONTRAST),
            (data_source["SHARPNESS"], DEFAULT_SHARPNESS),
            (data_source["GRAYSCALE"], DEFAULT_GRAYSCALE),
        )


class EffectFrame(ctk.CTkFrame):
    def __init__(self, parent, data_source: dict[str, ctk.Variable]):
        super().__init__(master=parent, fg_color="transparent")
        self.pack(expand=True, fill=ctk.BOTH)
        # PANEL.
        DropDownPanel(self, "Effect", data_source["EFFECT"], EFFECT_OPTIONS)
        DropDownPanel(self, "Filter", data_source["FILTER"], FILTER_OPTIONS)
        SliderPanel(self, "BoxBlur", data_source["BOXBLUR"], 0, 10)
        SliderPanel(self, "GaussianBlur", data_source["GAUSSIANBLUR"], 0, 10)
        SliderPanel(self, "UnsharpMask", data_source["UNSHARPMASK"], 0, 10)
        # RESET BUTTON.
        ResetButton(
            self,
            (data_source["EFFECT"], EFFECT_OPTIONS[0]),
            (data_source["FILTER"], FILTER_OPTIONS[0]),
            (data_source["BOXBLUR"], DEFAULT_BOXBLUR),
            (data_source["GAUSSIANBLUR"], DEFAULT_GAUSSIANBLUR),
            (data_source["UNSHARPMASK"], DEFAULT_UNSHARPMASK),
        )


class ExportFrame(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        save_image: Callable[[str, str, str], None],
        make_predict: Callable[[ctk.Variable], str],
    ):
        super().__init__(master=parent, fg_color="transparent")
        self.pack(expand=True, fill=ctk.BOTH)
        # BINDING DATA.
        self.bds_file_name = ctk.StringVar()
        self.bds_extension = ctk.StringVar(value="png")
        self.bds_file_path = ctk.StringVar()
        self.label_name = ctk.StringVar()
        # PANEL.
        ModelPanel(self, self.label_name, make_predict)
        SaveFilePanel(self, self.bds_file_name, self.bds_extension)
        SavePathPanel(self, self.bds_file_path)
        # SAVE BUTTON.
        SaveButton(
            self, self.bds_file_name, self.bds_extension, self.bds_file_path, save_image
        )
