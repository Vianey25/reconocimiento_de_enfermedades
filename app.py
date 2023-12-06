from flask import Flask, render_template, request
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import base64

app = Flask(__name__)

# Load the model
model = load_model("keras_model.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()

def get_disease_info(class_name):
    print("get_disease_info - Class Name:", class_name)

    if class_name == "Cenicilla polvorienta":
        print("Selected: Cenicilla polvorienta")
        return {
            "name": "Cenicilla polvorienta",
            "info": "La cenicilla polvorienta es una enfermedad que ataca a los cultivos de jitomate, entre otras hortalizas, causada por varios agentes, como los hongos Leveillula taurica (o su anamorfo Oidiopsis taurica y Oidiopsis sícula) y Oidium neolycopersicum.",
            "sintomas": ["Manchas de polvo blanco desarrollan en ambos lados de la hoja y se expanden a medida que crece la infección", "Las hojas se tornan amarillentas o café y se caen, exponiendo a la planta o fruto a las quemaduras del sol", "En algunos casos, las hojas o los brotes se tuercen o distorsionan"],
            "recomendaciones": ["No aplique cantidades excesivas de fertilizante nitrogenado; el crecimiento frondoso abundante promueve las condiciones para el desarrollo de esta enfermedad.","Recoger toda la sobra de las plantas después de la cosecha y quemarla oenterrarla.", " Para disminuir la probabilidad de sufrir cenicilla en los invernaderos, se recomienda ventilar primero abriendo solo las ventanas de barlovento.", " No apliques un exceso de nitrógeno, ya que esto promueve la enfermedad"],
            "imagen": "uploads/1.jpg",
            "audio_path": "audios/1.mp3"
            }
    elif class_name == "Peste negra":
        print("Selected: Peste negra")
        return {
            "name": "Peste negra",
            "info": "La enfermedad conocida como peste negra, vira cabeza y virus del bronceado es causada por un virus transmitido por pequeños  insectos llamados trips o llaja.",
            "sintomas": ["Manchas irregulares en las hojas", "Marchitez rápida", "Tallo y frutas afectados","Esparcimiento rápido"],
            "recomendaciones": ["Realiza un monitoreo constante de tus plantas para detectar signos tempranos de la enfermedad", "Mantén un buen espaciado entre las plantas para favorecer la circulación de aire y reduce el riego por aspersión para minimizar la humedad en las hojas.", " Retira y destruye las plantas infectadas de inmediato."],
            "imagen": "uploads/2.jpg",
            "audio_path": "audios/1.mp3" }
    elif class_name == "tizon tardio":
        print("Selected: Tizon tardio")
        return {
            "name": "Tizon tardio",
            "info": "El tizón tardío es una enfermedad que afecta a la familia de las Solanáceas. Es ocasionada por Phytophthora infestans, un oomyceto que puede atacar en distintas etapas del cultivo y extenderse rápidamente cuando las condiciones ambientales son favorables.",
            "sintomas": ["En las hojas y tallos se presentan manchas cafés o negruzcas", " Se puede observar una esporulación blanca en las lesione", "En los frutos se observan lesiones firmes y aceitosas de color marrón"],
            "recomendaciones": ["Evitar el encharcamiento y el exceso de humedad en las charolas de siembra","Hacer una aplicación de fungicida protectante antes de llevar a cabo el trasplante.", "Inspeccionar las plántulas para detectar posibles síntomas antes de hacer el trasplante. "],
            "imagen": "uploads/3.jpg",
            "audio_path": "audios/3.mp3" }
    elif class_name == "Cancer bacteriano":
        print("Selected: Cancer bacteriano")
        return {
            "name": "Cancer bacteriano",
            "info": "El cancro bacteriano es una enfermedad vascular producida por la bacteria denominada Clavibacter michiganensis subesp michiganensis, cuyo único hospedero es el cultivo de tomate",
            "sintomas": ["Marchitamiento sistémico de la planta", " Las hojas de un lado de la planta pierden turgencia y se vuelven flácidas", "Cancros en tallos y peciolos"],
            "recomendaciones": ["Se aconseja el uso de material y plantines libres de la bacteria y el monitoreo constante de las plantas","Hay que reducir el contacto de las plantas sanas con aquellas sintomáticas y desinfectar las herramientas después de emplearlas","Embolsarla desde la parte superior y cortarla en la base del tallo, desinfectar la herramienta de corte y retirar la planta para proceder a enterrarla, quemarla o compostarla"],
            "imagen": "uploads/4.jpg",
            "audio_path": "audios/1.mp3"
            }
    elif class_name == "Cremallera de tomate":
        print("Selected: Cremallera de tomate")
        return {
            "name": "Cremallera de tomate",
            "info": "La formación de cremallera en tomate se ve literalmente como una cremallera que cruza desde la punta de la cicatriz hasta la parte apical del fruto y empieza a aparecer al iniciarse la maduración.",
            "sintomas": ["Finas cicatrices marrones y necróticas, suberizadas, más o menos rodeando los frutos a lo largo y / o ancho",  "Pueden conectar la cicatriz peduncular a la cicatriz estilar o, en ocasiones, formar una cicatriz longitudinal de forma perpendicular, dándoles la apariencia de una cremallera que es el origen del nombre de esta afección ( cremallera )."],
            "recomendaciones": ["Evite mantener los puntos de ajuste de la temperatura nocturna demasiado bajos.","Asegurar una humedad óptima en los refugios, especialmente ni demasiado baja ni demasiado alta."],
            "imagen": "uploads/5.jpg",
            "audio_path": "audios/5.mp3"
           }
    elif class_name == "Virus del rizado amarillo":
        print("Selected: Virus del rizado amarillo")
        return {
            "name": "Virus del rizado amarillo",
            "info": "El virus del rizado amarillo del tomate, trasmitido por la mosca blanca (Bemisia tabaci), constituye una seria amenaza para la producción de tomate .",
            "sintomas": ["Acucharado y reducción del limbo foliara", "Amarilleo internervial y marginal", "Fruncimiento de nervios y falta de desarrollo de la planta"],
            "recomendaciones": ["Utilizar variedades tolerantes cuando sea posible.","Comprar plantas sanas de semilleros autorizados.", " Eliminar las plantas afectadas"],
            "imagen": "uploads/6.jpg",
            "audio_path": "audios/1.mp3"
            }
    elif class_name == "Mosca blanca":
        print("Selected: Mosca blanca")
        return {
            "name": "Mosca blanca",
            "info": "La mosca blanca es una de las plagas más importantes del cultivo del tomate. Trasmite virus tan peligrosos como el virus de la cuchara (TYLCV) y el virus de la clorosis del tomate (ToCV) (Figura 1) y parece intervenir en la maduración irregular de la fruta (TIR).",
            "sintomas": ["Amarilleamiento de los nervios o internervial", "Amarilleamiento de la hoja", "Enrollamiento de las hojas y tallos","Retraso en el crecimiento de las plantas"],
            "recomendaciones": ["Utilización de trampas cromáticas amarillas (de monitoreo y control).","Uso de cerramientos adecuados (mallas, doble puertas, etc.) para evitar la entrada del exterior.","Eliminar las malas hierbas y restos de cultivos ya que pueden actuar como reservorio de la plaga."],
            "imagen": "uploads/7.jpg",
            "audio_path": "audios/1.mp3"
            }
    elif class_name == "Moscas minadoras o minadores":
        print("Selected:Moscas minadoras o minadores")
        return {
            "name": "Moscas minadoras o minadores",
            "info": "Las moscas minadoras, también conocidas como larvas de minadores, son insectos que pertenecen a la familia Agromyzidae. Sus larvas son conocidas por crear galerías o minas dentro de las hojas de las plantas al alimentarse de los tejidos internos. ",
            "sintomas": ["Las larvas de moscas minadoras crean túneles o galerías en el interior de las hojas al alimentarse de los tejidos. ", "A medida que las larvas se alimentan de los tejidos de las hojas, puede ocurrir la deformación de las hojas, causando rizos o enrollamientos.", "Las áreas afectadas por las larvas pueden volverse más claras o decoloradas."],
            "recomendaciones": ["Retira y destruye las hojas afectadas que contienen larvas y pupas para reducir la población de moscas minadoras.","Mantén tu jardín limpio de malezas y restos de plantas, ya que estos pueden servir como refugio para las moscas minadoras."],
            "imagen": "uploads/8.jpg",
            "audio_path": "audios/1.mp3"
            }
    elif class_name == "Áfidos o pulgones":
        print("Selected: Áfidos o pulgones")
        return {
            "name": "Áfidos o pulgones",
            "info": "Son insectos pequeños y suaves que se alimentan de la savia de las plantas. Pueden ser una plaga común en los cultivos de tomate y causar daños a las plantas",
            "sintomas": ["Deformación de Hojas", "Las hojas afectadas pueden enrollarse hacia arriba o hacia abajo debido a la succión de savia por parte de los áfidos.", "Los áfidos excretan una sustancia pegajosa llamada melaza. Esta melaza puede atraer el crecimiento de hongos, como el moho negro, en las hojas."],
            "recomendaciones": ["Utiliza una manguera de agua para enjuagar suavemente los áfidos de las plantas.","Aplica aceite de neem, un producto natural, sobre las plantas para controlar los áfidos.", "Puedes usar aceites hortícolas, como aceite de ajo o aceite de pimienta, para repeler y controlar los áfidos.","Coloca cinta adhesiva amarilla alrededor de las plantas para atrapar a los áfidos voladores."],
            "imagen": "uploads/9.jpg",
            "audio_path": "audios/1.mp3"
              }
    elif class_name == "Fusariosis":
        print("Selected: Fusariosis")
        return {
            "name": "Fusariosis",
            "info": "La fusariosis en tomates es una enfermedad causada por hongos del género Fusarium. Estos hongos suelen habitar en el suelo y pueden afectar diferentes partes de la planta de tomate, como las raíces, el tallo y los frutos. ",
            "sintomas": ["Las hojas de la planta pueden mostrar síntomas de marchitez, comenzando por las hojas más viejas.", "El tallo puede mostrar decoloración, típicamente en forma de manchas marrones o rojas.", "La enfermedad a menudo afecta solo una parte de la planta, provocando un marchitamiento parcial.","En casos severos, la planta puede morir, comenzando con la muerte de ramas y extendiéndose a toda la planta."],
            "recomendaciones": ["Evitar plantar tomates en el mismo lugar año tras año ayuda a reducir la acumulación de patógenos en el suelo.",". Mantener un buen drenaje ayuda a prevenir la propagación de la enfermedad.","Mantener un riego adecuado y evitar el estrés hídrico puede ayudar a fortalecer las plantas y reducir la susceptibilidad a enfermedades.","Desinfectar las herramientas de jardín entre usos puede prevenir la propagación de patógenos."],
            "imagen": "uploads/10.jpg",
            "audio_path": "audios/1.mp3"
           }
    else:
        print("Selected: Información no disponible.")
        return {
            "name": "Información no disponible.",
            "info": ""
        }

def preprocess_image(image_path):
    # Replace this with the path to your image
    image = Image.open(image_path).convert("RGB")
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data[0] = normalized_image_array
    return data
def process_captured_image(image_data):
    # Decodificar la imagen base64
    image_data_decoded = base64.b64decode(image_data.split(",")[1])

    # Guardar la imagen decodificada
    file_path = "uploads/captured_image.jpg"
    with open(file_path, "wb") as file:
        file.write(image_data_decoded)

    # Procesar la imagen
    data = preprocess_image(file_path)
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index][2:].strip().lower()
    print("Class Name:", class_name)
    confidence_score = prediction[0][index]

    disease_info = get_disease_info(class_name)

    print("Disease Info:", disease_info)

    return file_path, class_name, confidence_score, disease_info


@app.route("/capture", methods=["POST"])
def capture():
    image_data = request.form["image_data"]
    file_path, class_name, confidence_score, disease_info = process_captured_image(image_data)

    return render_template("result.html", image_path=file_path, class_name=class_name, confidence_score=confidence_score, disease_name=disease_info["name"], disease_info=disease_info["info"])


@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "POST":
        # Check if the post request has the file part
        if "file" not in request.files:
            return render_template("index.html", error="No file part")

        file = request.files["file"]

        # If the user does not select a file, browser also
        # submit an empty part without filename
        if file.filename == "":
            return render_template("index.html", error="No selected file")

        # Check file extension
        allowed_extensions = {"jpg", "jpeg", "png", "gif"}
        if "." not in file.filename or file.filename.rsplit(".", 1)[1].lower() not in allowed_extensions:
            return render_template("index.html", error="Invalid file extension")

        # Save the uploaded file
        file_path = "uploads/" + file.filename
        file.save(file_path)

        # Process the uploaded image
        data = preprocess_image(file_path)
        prediction = model.predict(data)
        index = np.argmax(prediction)
        class_name = class_names[index][2:].strip().lower()
        print("Class Name:", class_name)
        confidence_score = prediction[0][index]

        disease_info = get_disease_info(class_name)

        print("Disease Info:", disease_info)

        return render_template("result.html", image_path=file_path, class_name=class_name, confidence_score=confidence_score, disease_name=disease_info["name"], disease_info=disease_info["info"])


    return render_template("index.html", error=None)

if __name__ == "__main__":
    app.run(debug=True)
