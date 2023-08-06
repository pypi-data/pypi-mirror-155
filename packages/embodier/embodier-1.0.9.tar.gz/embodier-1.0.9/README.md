
# Dynamic Avatar Generator  [[API](https://embodierapi.herokuapp.com)]
This library will help you to generate profile image for newly registered user on your application, like GitHub create profile picture for new users E.g. <br>
 <br>
![75605781 (2)](https://user-images.githubusercontent.com/40172813/125158648-02982e00-e190-11eb-912d-2c55b1051019.png)


## Generated images
![generatedimg](https://user-images.githubusercontent.com/40172813/125158557-9a494c80-e18f-11eb-956a-d49f42a6a6db.png)
![New Project (3)](https://user-images.githubusercontent.com/40172813/125189848-d5af4e00-e257-11eb-8b22-acc3b7b0c0f9.png)


## Usage
```python
import embodier 

# Initialize image generator
obj = embodier.AvatarGenerator()
# To Generate block image
img = obj.BlockAvatar() 
img.show()

# To Generate text image
img = obj.TextAvatar('PP') 
img.show()
```
### Advance 
BlockAvatar generate bit block image<br>
`obj.BlockAvatar(row_columns,pixel_size,background_color)`<br>
`@row_columns` `Integer`, block size of row and columns, default `5`<br>
`@pixel_size` `Integer`, pixel size, default `300`<br>
`@background_color` `String`, background color of blocks in image, default `lightgrey`<br>
`@border` `Boolean`, `True` to add border to image, `False` to without border image, default `True` <br><br>

TextAvatar generate text image<br>
`obj.TextAvatar(text,background_color)`<br>
`@text` `String`, Text to print on image<br>
`@background_color` `String`, background color of image, default `random color`<br><br>


Export options<br>
`img.show()` to open generated image <br>
`img.save('image.png')` to save image with image name <br>
`obj.toBase64(img)` to get Base64 value of generated image <br>


