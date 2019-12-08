from PIL import Image, ImageDraw, ImageFont
import collections

Cell = collections.namedtuple('Cell', ['row', 'col', 'el', 'width', 'height'], defaults=[None, None])

def cumsum(xs):
    ys = [xs[0]]
    for i in range(1, len(xs)):
        ys.append(ys[-1] + xs[i])
    return ys

def txt2im(txt, color, background_color):
    font = ImageFont.truetype('/System/Library/Fonts/Courier.dfont', 16)
    im = Image.new('RGB', (0, 0))
    draw = ImageDraw.Draw(im)
    size = draw.textsize(txt, font)
    im = Image.new('RGB', size, color=background_color)
    draw = ImageDraw.Draw(im)
    draw.text((0, 0), txt, fill=color, font=font)
    return im

class ImageTable:
    def __init__(self, color='black', background_color='white', cellpadding=2):
        self.tds = []
        self.row = 0
        self.col = 0
        self.color = color
        self.background_color = background_color
        self.cellpadding = cellpadding

    def tr(self):
        self.col = 0
        self.row += 1

    def td(self, el, width=None, height=None):
        if isinstance(el, str):
            el = txt2im(el, color=self.color, background_color=self.background_color)
        if width is None:
            width = el.size[0]
        if height is None:
            height = el.size[1]
        self.tds.append(Cell(self.row, self.col, el, width, height))
        self.col += 1

    def image(self):
        width = collections.Counter()
        height = collections.Counter()
        for td in self.tds:
            width[td.col] = max(width[td.col], td.width + self.cellpadding)
            height[td.row] = max(height[td.row], td.height + self.cellpadding)
        cum_width = [0] + cumsum(width)
        cum_height = [0] + cumsum(height)
        im = Image.new('RGB', (cum_width[-1] + self.cellpadding, cum_height[-1] + self.cellpadding), color=self.background_color)
        for td in self.tds:
            pos = cum_width[td.col] + self.cellpadding, cum_height[td.row] + self.cellpadding
            im.paste(td.el, pos)
        return im

if __name__ == '__main__':
    from PIL import Image

    red_fat = Image.new('RGB', (128, 64), color=(255, 0, 0, 255))
    green_thin = Image.new('RGB', (32, 128), color=(0, 255, 0, 255))

    tbl = ImageTable()
    tbl.td('Some text')
    tbl.tr()
    tbl.td(red_fat)
    tbl.td('More text')
    tbl.tr()
    tbl.td(green_thin)
    tbl.td(red_fat)
    tbl.td(green_thin)
    tbl.td(green_thin)
    tbl.image().save('table.png')
