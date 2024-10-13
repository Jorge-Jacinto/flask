import re

escuelas_filosoficas = {
    "Platonismo": [
        "formas", "ideas", "alma", "verdad", "razón", "justicia", "bien", "mundo de las ideas",
        "reminiscencia", "dialéctica", "conocimiento innato", "dualismo", "idealismo",
        "belleza", "virtud", "inmortalidad", "esencia", "arquetipo", "caverna", "sombras",
        "realidad inteligible", "mundo sensible", "anamnesis", "nous", "demiurgo"
    ],
    "Aristotelismo": [
        "sustancia", "accidente", "materia", "potencia", "acto", "causa final",
        "causa eficiente", "causa material", "causa formal", "entelequia", "silogismo",
        "ética", "política", "lógica", "metafísica", "virtud media", "eudaimonia",
        "categorías", "alma", "physis", "teología", "biología", "retórica", "poética"
    ],
    "Idealismo": [
        "idea", "mente", "espíritu", "conciencia", "absoluto", "trascendental", "fenómeno",
        "noúmeno", "síntesis", "dialéctica", "razón pura", "razón práctica", "libertad",
        "yo", "no-yo", "intuición", "voluntad", "representación", "apercepción",
        "imperativo categórico", "cosa en sí", "aufheben", "espíritu absoluto", "tesis", "antítesis"
    ],
    "Estoicismo": [
        "virtud", "destino", "apatía", "fortaleza", "serenidad", "control", "aceptar",
        "logos", "ataraxia", "autosuficiencia", "cosmopolitismo", "deber", "ética",
        "providencia", "razón universal", "sabiduría", "física", "lógica", "determinismo",
        "imperturbabilidad", "disciplina", "autoperfeccionamiento", "naturaleza", "vivir conforme",
        "ecuanimidad"
    ],
    "Realismo": [
        "realidad objetiva", "mundo externo", "verdad", "correspondencia", "hechos",
        "independencia ontológica", "universales", "esencias", "naturaleza", "ciencia",
        "empirismo", "materialismo", "sustancia", "propiedad", "relación", "causalidad",
        "percepción", "representación", "objetividad", "realismo científico", "sentido común",
        "realismo modal", "realismo moral", "realismo epistemológico", "realismo semántico"
    ],
    "Racionalismo": [
        "razón", "mente", "lógica", "conocimiento", "verdad", "pensar", "deducción",
        "innato", "a priori", "ideas claras y distintas", "método", "duda metódica",
        "cogito ergo sum", "sustancia", "sistema", "evidencia", "axioma", "geometría",
        "matemáticas", "necesidad", "universalidad", "intuición intelectual", "demostración",
        "certeza", "principios fundamentales"
    ],
    "Empirismo": [
        "experiencia", "sentidos", "observación", "realidad", "conocimiento", "sensoriales",
        "tabula rasa", "inducción", "percepción", "datos", "evidencia", "fenómenos",
        "impresiones", "asociación de ideas", "hábito", "probabilidad", "escepticismo",
        "causa y efecto", "verificación", "experimento", "a posteriori", "sensación",
        "introspección", "pragmatismo", "falsacionismo"
    ],
    "Humanismo": [
        "dignidad humana", "razón", "libertad", "educación", "cultura", "individualidad",
        "ética secular", "virtud cívica", "autorrealización", "antropocentrismo", "studia humanitatis",
        "retórica", "gramática", "poesía", "historia", "filosofía moral", "renacimiento",
        "ilustración", "secularismo", "racionalismo", "empirismo", "libre pensamiento",
        "tolerancia", "progreso", "humanidad"
    ],
    "Existencialismo": [
        "existencia", "esencia", "libertad", "responsabilidad", "angustia", "autenticidad",
        "absurdo", "nada", "ser-para-sí", "ser-en-sí", "mala fe", "situación límite",
        "proyecto", "elección", "compromiso", "facticidad", "trascendencia", "contingencia",
        "temporalidad", "muerte", "finitud", "subjetividad", "intersubjetividad", "ser-para-otros",
        "náusea"
    ],
    "Hedonismo": [
        "placer", "felicidad", "bienestar", "satisfacción", "goce", "deleite", "disfrute",
        "sensualidad", "epicureísmo", "utilitarismo", "eudemonismo", "deseo", "apetito",
        "gratificación", "indulgencia", "voluptuosidad", "hedoné", "ataraxia", "ausencia de dolor",
        "calidad de vida", "bienestar subjetivo", "experiencia positiva", "placer sensorial",
        "placer intelectual", "felicidad hedónica"
    ],
    "Nihilismo": [
        "nada", "vacío", "sin sentido", "absurdo", "negación", "descreimiento", "nihil",
        "ausencia de valores", "relativismo", "escepticismo radical", "amoralismo",
        "antifundacionalismo", "deconstrucción", "muerte de Dios", "voluntad de poder",
        "eterno retorno", "perspectivismo", "antiesencialismo", "antirrealismo",
        "antimetafísica", "antiteología", "antiteleología", "antiverdad", "antirazón",
        "antihumanismo"
    ],
    "Cinismo": [
        "naturalidad", "autosuficiencia", "ascetismo", "parresía", "desvergüenza",
        "cosmopolitismo", "virtud", "libertad", "crítica social", "simplicidad",
        "desprecio por las convenciones", "independencia", "autarquía", "austeridad",
        "ironía", "provocación", "anticonvencionalismo", "mendicidad", "animalidad",
        "indiferencia", "vida conforme a la naturaleza", "rechazo de la riqueza",
        "rechazo del poder", "rechazo de la fama", "sabiduría práctica"
    ]
}

def clean_text(texto):
    texto = texto.lower() 
    texto = re.sub(r'[^\w\s]', '', texto) 
    return texto

def classifier(texto_usuario):
    texto_limpio = clean_text(texto_usuario)
    
    coincidencias = {escuela: 0 for escuela in escuelas_filosoficas}
    
    for escuela, palabras_clave in escuelas_filosoficas.items():
        for palabra in palabras_clave:
            if palabra in texto_limpio:
                coincidencias[escuela] += 1
    
    escuela_clasificada = max(coincidencias, key=coincidencias.get)
    
    if coincidencias[escuela_clasificada] == 0:
        return "No se pudo clasificar"
    
    return escuela_clasificada

'''@app.route('/', methods=['GET', 'POST'])
def index():                                                # MODIFICAR SEGUN EL NOMBRE DEL HTML
    resultado = None
    if request.method == 'POST':
        comentario = request.form['comentario']
        resultado = classifier(comentario)
    return render_template('index.html', resultado=resultado) # MODIFICAR NOMBRE DEL HTML

if __name__ == '__main__':
    app.run(debug=True)'''