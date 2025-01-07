import base64

with open("E:/Piyush/Project/abc/express-quiz-app/public/images/Aanandi1.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    print(encoded_string)
