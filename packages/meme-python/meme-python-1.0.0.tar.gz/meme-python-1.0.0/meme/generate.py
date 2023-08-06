from .utils import *
from math import floor, ceil

IMPACT_FONT_PATH = Path(__file__).parent / 'static' / 'impact.ttf'

def get_font_for_image(image: Image, font_path: PotentialPath) -> FreeTypeFont:
    # generally, larger images should use a larger font size
    width, height = image.size
    font_size = round(max(8, min(256, width / 10, height / 5)))
    
    return PIL.ImageFont.truetype(stringify_path(font_path), font_size)

def generate(
    image: Image | PotentialPath=None,
    text: str=None,
    font: FreeTypeFont | PotentialPath=IMPACT_FONT_PATH,
    output: Optional[PotentialPath]=None
):
    if not isinstance(image, Image):
        image = PIL.Image.open(stringify_path(image))
    width, height = image.size
    caption_padding = width * 0.05
    
    if not isinstance(font, FreeTypeFont):
        font = get_font_for_image(image, font)
    
    fitted_text = fit_text(
        text=text,
        font=font,
        bounds=Rectangle(caption_padding, caption_padding, width - caption_padding * 2, -1),
    )
    
    padded_image = expand_image(
        image=image,
        amount=ceil(fitted_text.bounds.height + caption_padding * 2)
    )
    
    draw_fitted_text(
        image=padded_image,
        text=fitted_text
    )
    
    if output:
        padded_image.save(stringify_path(output))
    
    return padded_image

__all__ = [
    'generate'
]
