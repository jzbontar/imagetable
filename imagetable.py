from PIL import Image, ImageDraw, ImageFont
import collections

Cell = collections.namedtuple('Cell', ['row', 'col', 'el', 'width', 'height'], defaults=[None, None])

def cumsum(xs):
    ys = xs.copy()
    for i in range(1, len(ys)):
        ys[i] += ys[i - 1]
    return ys

def txt2im(txt):
    font = ImageFont.truetype('/System/Library/Fonts/Courier.dfont', 16)
    im = Image.new('RGB', (0, 0))
    draw = ImageDraw.Draw(im)
    size = draw.textsize(txt, font)
    im = Image.new('RGB', size)
    draw = ImageDraw.Draw(im)
    draw.text((0, 0), txt, font=font)
    return im

class ImageTable:
    def __init__(self, bgcolor=None, cellpadding=2):
        self.tds = []
        self.row = 0
        self.col = 0
        self.bgcolor = bgcolor
        self.cellpadding = cellpadding

    def tr(self):
        self.col = 0
        self.row += 1

    def td(self, el, width=None, height=None):
        if width is None:
            width = el.size[0]
        if height is None:
            height = el.size[1]
        self.tds.append(Cell(self.row, self.col, el, width, height))
        self.col += 1

    def image(self):
        nrow = 0
        ncol = 0
        table = dict()
        for td in self.tds:
            nrow = max(nrow, td.row + 1)
            ncol = max(ncol, td.col + 1)
            table[td.row, td.col] = td

        width = []
        for j in range(ncol):
            xs = []
            for i in range(nrow):
                if (i, j) in table:
                    xs.append(table[i, j].width)
            width.append(max(xs) + self.cellpadding)

        height = []
        for i in range(nrow):
            xs = []
            for j in range(ncol):
                if (i, j) in table:
                    xs.append(table[i, j].height)
            height.append(max(xs) + self.cellpadding)

        cum_width = [0] + cumsum(width)
        cum_height = [0] + cumsum(height)
        im = Image.new('RGB', (cum_width[-1] + self.cellpadding, cum_height[-1] + self.cellpadding), color=self.bgcolor)
        for td in self.tds:
            pos = cum_width[td.col] + self.cellpadding, cum_height[td.row] + self.cellpadding
            im.paste(td.el, pos)
        return im

if __name__ == '__main__':
    tbl = ImageTable(cellpadding=4)
    tbl.td(Image.open('img/baz.png'))
    tbl.td(Image.open('img/baz.png'))
    tbl.tr()
    tbl.td(Image.open('img/baz.png'))
    tbl.td(Image.open('img/baz.png'))
    im = tbl.image()

    tbl = ImageTable(bgcolor=(0, 255, 255, 255), cellpadding=2)
    tbl.td(txt2im('Epoch: 5'))
    tbl.tr()
    tbl.td(Image.open('img/foo.png'))
    tbl.td(im)
    tbl.tr()
    tbl.td(Image.open('img/bar.png'))
    tbl.td(Image.open('img/foo.png'))
    tbl.td(Image.open('img/bar.png'))
    tbl.tr()
    tbl.td(Image.open('img/foo.png'))
    tbl.td(Image.open('img/foo.png'))
    tbl.image().save('output.png')
