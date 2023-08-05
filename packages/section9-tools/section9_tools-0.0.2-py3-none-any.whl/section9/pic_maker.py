import fire
import arrow
from PIL import Image, ImageFont, ImageDraw


def generate_text_layer(
    size=(300, 100),
    font_name="Arial",
    font_size=16,
    bg=(0, 0, 0, 0),
    fg="magenta",
    text_list=None,
):
    """Generate a piece of canvas and draw text on it"""
    canvas = Image.new("RGBA", size, bg)
    # Get a drawing context
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.truetype(font_name, font_size)
    for i, text in enumerate(text_list):
        draw.text((10, (font_size + 2) * i), text, font=font, fill=fg)
    return canvas


def gen_pic(width=600, height=300):
    # Create empty yellow image
    im = Image.new("RGB", (width, height), "yellow")
    text_list = [f"{width}x{height}", f"{arrow.now()}"]
    file_name = ".".join(text_list)
    text_overlay = generate_text_layer(
        text_list=text_list,
    )
    im.paste(text_overlay, mask=text_overlay)
    im.save(f"{file_name}.png")


def main():
    fire.Fire(gen_pic)
