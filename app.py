from flask import Flask, render_template, request, jsonify

from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.vgg16 import preprocess_input, decode_predictions
# from keras.applications.vgg16 import decode_predictions
#from keras.applications.vgg16 import VGG16
from keras.applications.resnet50 import ResNet50

app = Flask(__name__)
model = ResNet50()

@app.route('/predict', methods=["GET",'POST'])
def predict():
    if request.method == "POST":
        imagefile= request.files['imagefile']
        if not imagefile:
            return jsonify({'msg':'Please upload image'})
        
        image_path = "./images/" + imagefile.filename
        imagefile.save(image_path)

        image = load_img(image_path, target_size=(224, 224))
        image = img_to_array(image)
        image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
        image = preprocess_input(image)
        yhat = model.predict(image)
        label = decode_predictions(yhat)
        label = label[0][0]

        classification = '%s (%.2f%%)' % (label[1], label[2]*100)
        print(classification)
        imagefile.close()

        return jsonify({'msg':classification})

@app.route('/', methods=['GET'])
def home():
    return jsonify({'msg':'Working...'})

if __name__ == '__main__':
    app.run(port=5000, debug=True)

# ngrok http --domain=great-quagga-bright.ngrok-free.app 5000