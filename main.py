import PIL
import matplotlib.font_manager as mpl
from tkinter import *
from tkinter import filedialog as fd
from tkinter import Tk, colorchooser, filedialog
from PIL import Image, ImageDraw, ImageFont, ImageTk

system_fonts = mpl.findSystemFonts(fontpaths=None, fontext='ttf')


def hex_to_rgba(hexa, alpha):
    rgb = []
    for i in (1, 3, 5):
        decimal = int(hexa[i:i + 2], 16)
        rgb.append(decimal)
    rgb.append(int(alpha / .39))
    return tuple(rgb)


class Watermark:
    def __init__(self, rt):
        self.bg = '#8c9ab5'
        self.photoImg = None
        self.families = system_fonts
        self.filename = StringVar()
        self.font_color = "#ffffff"
        self.wm_text = StringVar()
        self.opacity = IntVar()
        self.opacity.set(50)
        self.x = IntVar()
        self.x.set(1)
        self.y = IntVar()
        self.y.set(1)
        self.font_text = StringVar()
        self.family = self.families[0]

        self.logoImg = Image.open('wm_logo.png')
        self.logoImg = self.logoImg.resize((150, 100))
        self.logoImg = ImageTk.PhotoImage(self.logoImg)

        self.bgImg = Image.open('bgimg.png')
        self.bgImg = self.bgImg.resize((1200, 800))
        self.bgImg = ImageTk.PhotoImage(self.bgImg)

        self.clicked = StringVar()
        self.clicked.set('Select Font')
        self.font_size = IntVar()
        self.font_size.set(16)
        self.bucket = None
        self.rotate = IntVar()
        self.rotate.set(0)
        self.xpositions = ['left', 'center', 'right']
        self.ypositions = ['top', 'center', 'bottom']
        self.color = None
        self.text = None
        self.multi = False
        self.num_spaces = IntVar()
        self.num_spaces.set(0)
        rt.title('Watermark 2.0')
        rt.resizable(False, False)
        # main panel
        self.panel = Label(rt, width=800, height=800, padx=10, pady=10, background=self.bg, image=self.bgImg)
        self.panel.grid(column=0, row=0, sticky=NSEW)

        # options panel
        self.panel2 = Frame(self.panel, background=self.bg)
        self.panel2.grid(column=0, row=1)

        # logo
        self.logo = Label(self.panel2, image=self.logoImg, background=self.bg)
        self.logo.grid(column=2, row=0, sticky=NSEW)

        # intial load button
        self.action = Button(self.panel2, text='Load Photo', command=self.load_photo)
        self.action.grid(column=0, row=0)

        # settings group
        self.font_text = Entry(self.panel2)
        self.watermark_label = Label(self.panel2, text='Watermark Text:', background=self.bg)
        self.opacity_label = Label(self.panel2, text='Opacity', background=self.bg)
        self.opacity_scale = Scale(self.panel2, from_=0, to=100, command=self.scale_opacity, variable=self.opacity,
                                   orient='horizontal', bg=self.bg)
        self.color = Button(self.panel2, text='Font Color', command=self.choose_color, background=self.font_color)
        self.size_label = Label(self.panel2, text='Font Size', background=self.bg)
        self.size_scale = Scale(self.panel2, variable=self.font_size, orient='horizontal', command=self.set_family,
                                bg=self.bg)
        self.family_label = Label(self.panel2, text='Font Family', background=self.bg)
        self.family_option = OptionMenu(self.panel2, self.clicked, *self.families, command=self.set_family)
        self.reset_button = Button(self.panel2, text='Reset', command=self.reset)
        # self.photo = Frame(self.panel)
        self.save_button = Button(self.panel2, text='Save Photo', command=lambda: self.save_pic())
        self.rotate_check = Checkbutton(self.panel2, text='Rotate', command=self.rotate_enable, background=self.bg)
        self.rotate_scale = Scale(self.panel2, from_=0, to=359, command=self.submit_text, variable=self.rotate,
                                  orient='horizontal',
                                  bg=self.bg)
        self.multiline_check = Checkbutton(self.panel2, text='multiline', command=self.multiline_enable, bg=self.bg)
        self.spaces_label = Label(self.panel2, text='Number of Spaces', bg=self.bg)
        self.spaces_scale = Scale(self.panel2, from_=0, to=10, command=self.submit_text, variable=self.num_spaces,
                                  orient='horizontal', bg=self.bg)

        self.x_pos_label = Label(self.panel2, text='x position', background=self.bg)
        self.y_pos_label = Label(self.panel2, text='y position', background=self.bg)

        # copyright
        Label(self.panel, text='Copyright John Oden, 2022', background=self.bg).grid(column=1, row=12)

        # binding to submit
        self.font_text.bind('<Return>', self.submit_text)
        self.x_scale = Scale(self.panel2, from_=-500, to=500, command=self.set_x, orient='horizontal',
                             bg=self.bg)
        self.y_scale = Scale(self.panel2, from_=-500, to=500, command=self.set_y, orient='vertical',
                             bg=self.bg)

    def multiline_enable(self):
        if self.multi:
            self.multi = False
        else:
            self.multi = True
        self.submit_text()

    def rotate_enable(self):
        self.rotate_scale.grid(column=7, row=4)

    def get_x(self):
        try:
            return self.photoImg.width()
        except:
            return 0

    def get_y(self):
        try:
            return self.photoImg.height()
        except:
            return 0

    def set_x(self, new_pos):
        self.x.set(new_pos)
        self.submit_text()

    def set_y(self, new_pos):
        self.y.set(new_pos)
        self.submit_text()

    def save_pic(self):
        result = filedialog.asksaveasfilename(initialdir="/", title="Select file", filetypes=(
            ('JPEG', ('*.jpg', '*.jpeg', '*.jpe')), ('PNG', '*.png'), ('BMP', ('*.bmp', '*.jdib')), ('GIF', '*.gif')))
        if result:
            self.photoImg.save(f'{result}.png', dpi=(300, 300))

    def reset(self):
        self.multi = False
        self.photoImg = None
        self.font_size.set(16)
        self.clicked.set('Select Font')
        self.opacity.set(50)
        self.font_color = '#ffffff'
        self.font_text.delete(0, END)
        self.font_text.grid_forget()
        self.watermark_label.grid_forget()
        self.opacity_label.grid_forget()
        self.opacity_scale.grid_forget()
        self.color.grid_forget()
        self.size_label.grid_forget()
        self.size_scale.grid_forget()
        self.family_label.grid_forget()
        self.family_option.grid_forget()
        self.x_pos_label.grid_forget()
        self.x_scale.grid_forget()
        self.y_pos_label.grid_forget()
        self.y_scale.grid_forget()
        self.reset_button.grid_forget()
        self.save_button.grid_forget()
        self.rotate_check.grid_forget()
        self.rotate_scale.grid_forget()
        self.multiline_check.grid_forget()
        self.spaces_scale.grid_forget()
        self.spaces_label.grid_forget()
        try:
            self.bucket.destroy()
        except AttributeError:
            pass

    def set_family(self, *args):
        self.family = self.clicked.get()
        self.submit_text()

    def submit_text(self, *args):
        font2 = ImageFont.truetype(self.family, self.font_size.get())
        self.photoImg = PIL.Image.open(self.filename.get())
        self.photoImg.thumbnail((500, 500))
        text_mask = Image.new('RGBA', (self.photoImg.width + 400, self.photoImg.height + 400))
        mdr = ImageDraw.Draw(text_mask)
        fill = hex_to_rgba(self.font_color, self.opacity.get())
        W = self.photoImg.width * 2
        H = self.photoImg.height * 2
        word = self.font_text.get().strip()
        filler = (' ' * self.num_spaces.get())
        word = word + filler
        ht, wt = font2.getsize(text=word)
        h = -100
        if self.multi:
            while h <= H:
                w = -100
                i = 0
                fore = " "
                while w <= W:
                    mdr.text(text=(str(fore * i) + word), xy=(h, w), fill=fill, font=font2)
                    i += 20
                    if i >= int(len(word)):
                        i = 0
                    w += wt + (self.num_spaces.get() * 1.5)
                h += ht
        else:
            mdr.text((self.x.get(), self.y.get()), self.font_text.get(), font=font2, fill=fill)
        text_mask = text_mask.rotate(self.rotate.get())
        self.photoImg.paste(text_mask, (self.x.get(), self.y.get()), text_mask)
        self.show_photo()

    def scale_opacity(self, *args):
        self.opacity.set(args[0])
        self.set_family()

    def choose_color(self):
        self.font_color = colorchooser.askcolor()[1]

        try:
            self.color.config(background=self.font_color)
        except:
            self.color.config(background='')
        self.submit_text()

    def load_photo(self):
        self.filename.set(fd.askopenfilename())
        if self.filename.get() == '':
            return
        try:
            self.photoImg = Image.open(self.filename.get())
        except PIL.UnidentifiedImageError:
            pass
        self.photoImg.thumbnail((500, 500))

        self.watermark_label.grid(column=0, row=1)
        self.font_text.grid(column=0, row=2)
        self.opacity_label.grid(column=0, row=3)
        self.color.grid(column=0, row=4)
        self.opacity_scale.grid(column=0, row=5)
        self.size_label.grid(column=0, row=6)
        self.size_scale.grid(column=0, row=7)
        self.family_label.grid(column=0, row=8)
        self.family_option.grid(column=0, row=9)
        self.x_pos_label.grid(column=0, row=11)
        self.x_scale.grid(column=0, row=12)
        self.y_pos_label.grid(column=0, row=13)
        self.y_scale.grid(column=0, row=14)
        self.reset_button.grid(column=0, row=15, pady=(10, 0))
        self.save_button.grid(column=7, row=0)
        self.rotate_check.grid(column=7, row=3)
        self.multiline_check.grid(column=7, row=5)
        self.spaces_label.grid(column=7, row=6)
        self.spaces_scale.grid(column=7, row=7)
        self.show_photo()

    def show_photo(self):
        try:
            self.bucket.grid_forget()
        except:
            pass
        photo = ImageTk.PhotoImage(self.photoImg)
        self.bucket = Label(self.panel2, background=self.bg, image=photo, relief='raised', width=self.photoImg.width,
                            height=self.photoImg.height)
        self.bucket.image = photo
        self.bucket.grid(rowspan=10, column=2, row=2, sticky=NSEW)


root = Tk()
Button(root)
Watermark(root)
root.mainloop()
