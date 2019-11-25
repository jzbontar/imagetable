from PIL import Image
import collections

Cell = collections.namedtuple('Cell', ['row', 'col', 'el', 'width', 'height'], defaults=[None, None])

def cumsum(xs):
    ys = xs.copy()
    for i in range(1, len(ys)):
        ys[i] += ys[i - 1]
    return ys

class ImageTable:
    def __init__(self, bgcolor=None):
        self.tds = []
        self.row = 0
        self.col = 0
        self.bgcolor = bgcolor

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
            width.append(max(xs))

        height = []
        for i in range(nrow):
            xs = []
            for j in range(ncol):
                if (i, j) in table:
                    xs.append(table[i, j].height)
            height.append(max(xs))

        cum_width = [0] + cumsum(width)
        cum_height = [0] + cumsum(height)
        im = Image.new('RGB', (cum_width[-1], cum_height[-1]), color=self.bgcolor)
        for td in self.tds:
            pos = cum_width[td.col], cum_height[td.row]
            im.paste(td.el, pos)
        return im

if __name__ == '__main__':
    tbl = ImageTable()
    tbl.td(Image.open('img/baz.png'))
    tbl.td(Image.open('img/baz.png'))
    tbl.tr()
    tbl.td(Image.open('img/baz.png'))
    tbl.td(Image.open('img/baz.png'))
    im = tbl.image()

    tbl = ImageTable(bgcolor=(0, 255, 255, 255))
    tbl.td(Image.open('img/foo.png'))
    tbl.td(im)
    tbl.tr()
    tbl.td(Image.open('img/bar.png'))
    tbl.td(Image.open('img/foo.png'))
    tbl.td(Image.open('img/bar.png'))
    tbl.tr()
    tbl.td(Image.open('img/foo.png'), width=600)
    tbl.td(Image.open('img/foo.png'))
    tbl.image().save('output.png')
