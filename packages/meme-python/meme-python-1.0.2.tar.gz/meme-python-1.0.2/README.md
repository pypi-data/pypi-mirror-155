# meme-python
 
Lets you easily generate text-based memes on images or gifs.
```py
import meme

output = meme.generate(
    image='static/nerd.jpg',
    text='POV: You don\'t use meme-python'
)

output.show()
```
![example](examples/output/meme.jpg)


## Setup
1. Clone this repository (or download it as a .zip package)
2. `pip install -r requirements.txt`
    - *Attention Windows users:* Most python installations use the `py` version manager, so pip is accessed like `py -m pip install -r requirements.txt`
    - *Attention Linux/MacOS users:* Most computers default to using Python version 2.x, you will need to speficially use Python 3.x like `pip3 -m pip install -r requirements.txt`

## Docs
TODO
