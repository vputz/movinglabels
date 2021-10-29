#!/usr/bin/env python
import labels
from toolz.itertoolz import concat, partition
from reportlab.graphics import shapes
import click
import os

specs = labels.Specification(101, 150, 2, 3, 48, 48, corner_radius=2)

def draw_label(label, width, height, obj):
    label.add(shapes.String(25, 40, str(obj), fontName="Helvetica", fontSize = 72 ))

def numbers(start, end, num_each, num_per_sheet):
    return partition(num_per_sheet, concat([ [x]*num_each for x in range(start,end+1)]), pad="")

def create_sheet(numbers):
    sheet = labels.Sheet(specs, draw_label, border=True)
    sheet.add_labels(numbers)
    return sheet

@click.command()
@click.option("--start", help="starting number for labels", type=int)
@click.option("--end", help="ending number for labels", type=int)
@click.option("--num_each", help="number of minilabels for each number", type=int)
@click.option("--do-print/--no-print", default=False)
def print_labels(start, end, num_each, do_print):
    sheets = ([x, create_sheet(x)] for x in numbers(start,end,num_each, 6))
    for index, sheet in enumerate(sheets):
        filename = f"labels_{index}.pdf"
        sheet[1].save(filename)
        if do_print:
            os.system(f'lp {filename}')

if __name__=="__main__":
    print_labels()
