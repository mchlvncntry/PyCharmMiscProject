from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageOps

# 1. Load Gutenberg text
import requests
url = "https://www.gutenberg.org/cache/epub/98/pg98.txt"
text = requests.get(url).text

# 2. Load the silhouette
img = Image.open("/Users/mvrayo-mini/Downloads/london_mask.png").convert("L")   # convert to grayscale

# 3. INVERT the mask so white = buildings, black = sky
#    This makes the words fill the buildings.
mask = ImageOps.invert(img)

# 4. Convert to numpy for WordCloud
mask = np.array(mask)

# 5. Generate the word cloud
wc = WordCloud(
    background_color="white",
    mask=mask,
    max_words=2000,
    contour_width=0
).generate(text)

# 6. Show + save
plt.figure(figsize=(12, 6))
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.savefig("tale_of_two_cities_london_wordcloud.png", dpi=150, bbox_inches="tight")
plt.show()
