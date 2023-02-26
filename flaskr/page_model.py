
from PIL import Image

class Page:

    def __init__(self, title: str, content, image: Image):
        self.title: str = title 
        self.content = content #Each element is a paragraph
        self.image: Image = image
    
