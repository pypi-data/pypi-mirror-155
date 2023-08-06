import PIL.Image, PIL.ImageDraw, PIL.ImageFont
from PIL.Image import Image
from PIL.ImageFont import FreeTypeFont

import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import Iterable, Optional
from functools import cache

PotentialPath = Path | str
Number = int | float

def get_path(path: PotentialPath) -> Path:
    '''
    converts a PotentialPath to a Path
    '''
    if isinstance(path, str):
        return Path(path)
    else:
        return path

def stringify_path(path: PotentialPath) -> str:
    '''
    returns the absolute path as a string
    '''
    return str(get_path(path).resolve().absolute())

@dataclass
class Point:
    x: Number
    y: Number
    
    def pixel(self):
        return round(self.x), round(self.y)

@dataclass
class Rectangle:
    x: Number
    y: Number
    width: Number
    height: Number
    
    x1: Number = field(repr=False)
    y1: Number = field(repr=False)
    x2: Number = field(repr=False)
    y2: Number = field(repr=False)
    
    left: Number = field(repr=False)
    right: Number = field(repr=False)
    top: Number = field(repr=False)
    bottom: Number = field(repr=False)
    
    top_left: Number = field(repr=False)
    tl: Number = field(repr=False)
    
    top_right: Number = field(repr=False)
    tr: Number = field(repr=False)
    
    bottom_right: Number = field(repr=False)
    br: Number = field(repr=False)
    
    bottom_left: Number = field(repr=False)
    bl: Number = field(repr=False)
    
    def __init__(self, x: Number=None, y: Number=None, width: Number=None, height: Number=None):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.x1, self.y1, self.x2, self.y2 = self.x, self.y, self.x + self.width, self.y + self.height
        
        self.top, self.right, self.bottom, self.left = self.y2, self.x2, self.y1, self.x1
        self.top_left = self.tl = Point(self.left, self.top)
        self.top_right = self.tr = Point(self.right, self.top)
        self.bottom_right = self.br = Point(self.right, self.bottom)
        self.bottom_left = self.bl = Point(self.left, self.bottom)
        
        self.area = self.width * self.height
    
    @classmethod
    def contain(cls, rectangles: Iterable['Rectangle']):
        '''
        Builds the smallest Rectangle that contains all of the provided rectangles.
        '''
        
        inf = float('inf')
        top, right, bottom, left = -inf, -inf, inf, inf
        
        found_one = False
        for rectangle in rectangles:
            found_one = True
            top = max(top, rectangle.top)
            right = max(right, rectangle.right)
            bottom = min(bottom, rectangle.bottom)
            left = min(left, rectangle.left)
        
        if not found_one:
            raise ValueError('You must provide at least one rectangle.')
        
        return cls(
            x=left,
            y=bottom,
            width=right - left,
            height=top - bottom
        )

@dataclass
class FittedLine:
    text: str
    bounds: Rectangle

@dataclass
class FittedText:
    font: FreeTypeFont
    lines: list[FittedLine]
    bounds: Rectangle

def tokenize(text: str):
    return re.findall(r'(?:[\w\']+|\A)(?:[^\w\']+|\Z)', text.strip())

def pull_line_from_tokens(tokens, line_is_valid, last_character_count=0):
    N = len(tokens)
    
    count = 0
    line = ''
    while count < N and len(line.strip()) < last_character_count:
        line += tokens[count]
        count += 1
    
    # increase count until line becomes invalid
    while count < N and line_is_valid(line.strip()):
        line += tokens[count]
        count += 1
    
    # decrease count until line becomes valid
    while not line_is_valid(line.strip()) and count > 1:
        count -= 1
        line = line[:-len(tokens[count])]
    
    return count, line.strip()

def fit_text(text: str=None, font: FreeTypeFont=None, bounds: Rectangle=None, line_spacing: float=0.3):
    if bounds.height <= 0:
        bounds = Rectangle(bounds.x, bounds.y, bounds.width, float('inf'))
    
    tokens = tokenize(text)
    last_character_count = 0
    
    @cache
    def line_size(line):
        left, top, right, bottom = font.getbbox(line, anchor='lt')
        return right - left, bottom - top
    
    def line_is_valid(line):
        width, height = line_size(line)
        return width <= bounds.width
    
    lines = []
    y = bounds.bottom
    while tokens and y + font.size <= bounds.top:
        count, line = pull_line_from_tokens(tokens, line_is_valid, last_character_count)
        last_character_count = len(line)
        del tokens[:count]
        
        width, height = line_size(line)
        lines.append(FittedLine(
            line,
            Rectangle(
                bounds.left + (bounds.width - width) / 2,
                y,
                width,
                height
            )
        ))
        
        y += font.size * (1 + line_spacing)
    
    return FittedText(
        font=font,
        lines=lines,
        bounds=Rectangle.contain(line.bounds for line in lines)
    )

def expand_image(image: Image=None, amount: int=None, color: tuple[int]=(255, 255, 255)) -> Image:
    width, height = image.size
    new_image = PIL.Image.new(image.mode, (width, height + amount), color)
    new_image.paste(image, (0, amount))
    return new_image

def draw_fitted_text(image: Image=None, text: FittedText=None) -> None:
    drawer = PIL.ImageDraw.Draw(image)
    for line in text.lines:
        drawer.text(line.bounds.bottom_left.pixel(), line.text, (0,0,0), font=text.font, anchor='lt')

__all__ = [
    'PIL',
    'Image',
    'FreeTypeFont',
    'Path',
    'Iterable',
    'Optional',
    'PotentialPath',
    'Number',
    'get_path',
    'stringify_path',
    'Point',
    'Rectangle',
    'FittedLine',
    'FittedText',
    'fit_text',
    'expand_image',
    'draw_fitted_text',
]
