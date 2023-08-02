from flask import Flask, request, jsonify, render_template
import matlab.engine
import base64

app = Flask(__name__)

def matlab_file_to_base64(matlab_file):
    eng = matlab.engine.start_matlab()
    eng.run(matlab_file, nargout=0)
    fig = eng.gcf()
    graph_file = 'graph.png'
    eng.saveas(fig, graph_file, 'png', nargout=0)
    with open(graph_file, 'rb') as f:
        image_data = f.read()
    base64_image = base64.b64encode(image_data).decode('utf-8')
    eng.quit()
    return base64_image

@app.route('/', methods=['GET'])
def index():
    return render_template('matlab-3.html')

@app.route('/upload', methods=['POST'])
def process_upload():
    file = request.files['file']
    
    file.save('uploaded_file.m')
    
   
    base64_image = matlab_file_to_base64('uploaded_file.m')

    
    print("base64 image: "+base64_image)
    return jsonify({'graph': base64_image})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
