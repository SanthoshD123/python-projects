
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Ask the user for input text
text = input("Enter some text for the word cloud: ")

# Generate a word cloud
wordcloud = WordCloud(width=800, height=400, background_color="white", colormap="viridis").generate(text)

# Display the word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Your Word Cloud", fontsize=16)
plt.show()

