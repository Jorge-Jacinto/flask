function nextSection(currentSection, nextSection) {
    // Validar si se ha seleccionado una respuesta en la sección actual
    const selectedAnswer = document.querySelector(`input[name="answer${currentSection}"]:checked`);
    if (!selectedAnswer) {
        alert("Por favor selecciona una respuesta antes de continuar.");
        return;
    }

    // Ocultar la sección actual
    document.querySelector(".section.active").classList.remove("active");

    // Mostrar la siguiente sección
    document.getElementById("section-" + nextSection).classList.add("active");
}

function prevSection(sectionNumber) {
    // Ocultar la sección actual
    document.querySelector(".section.active").classList.remove("active");

    // Mostrar la sección anterior
    document.getElementById("section-" + sectionNumber).classList.add("active");
}

function showResults() {
    // Validar si se ha seleccionado una respuesta en la tercera sección
    const selectedAnswer3 = document.querySelector('input[name="answer3"]:checked');
    if (!selectedAnswer3) {
        alert("Por favor selecciona una respuesta en la última sección.");
        return;
    }

    // Obtener las respuestas seleccionadas de cada sección
    const selectedAnswer1 = document.querySelector('input[name="answer1"]:checked');
    const selectedAnswer2 = document.querySelector('input[name="answer2"]:checked');
    const selectedAnswer3Value = selectedAnswer3 ? selectedAnswer3.value : null;

    const result1Text = selectedAnswer1.getAttribute('data-text');
    const result1Value = selectedAnswer1.value;
    const result2Text = selectedAnswer2.getAttribute('data-text');
    const result2Value = selectedAnswer2.value;
    const result3Text = selectedAnswer3.getAttribute('data-text');
    const result3Value = selectedAnswer3.value;

    // Mostrar las respuestas en la sección de resultados
    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = `
        <p>Respuesta 1: ${result1Text}</p>
        <p>Respuesta 2: ${result2Text}</p>
        <p>Respuesta 3: ${result3Text}</p>
    `;

    // Generar las opciones para la selección final
    const finalSelectionDiv = document.getElementById("final-selection");
    finalSelectionDiv.innerHTML = `
        <label class="option">
            <input type="radio" name="finalAnswer" value="${result1Value}" data-text="${result1Text}"> ${result1Text}<br>
        </label>    
        <label class="option">
            <input type="radio" name="finalAnswer" value="${result2Value}" data-text="${result2Text}"> ${result2Text}<br>
        </label>
        <label class="option">
            <input type="radio" name="finalAnswer" value="${result3Value}" data-text="${result3Text}"> ${result3Text}<br>
        </label>
    `;

    // Ocultar la sección actual y mostrar los resultados
    document.querySelector(".section.active").classList.remove("active");
    document.getElementById("section-results").classList.add("active");
}

function selectFinalAnswer() {
    // Validar si el usuario seleccionó una respuesta final
    const finalAnswer = document.querySelector('input[name="finalAnswer"]:checked');
    if (!finalAnswer) {
        alert("Por favor selecciona una respuesta final.");
        return;
    }

    // Mostrar la respuesta final seleccionada
    const finalAnswerText = finalAnswer.getAttribute('data-text');
    const finalAnswerValue = finalAnswer.value;
    document.getElementById("final-answer").textContent = `Has seleccionado: ${finalAnswerText} (Valor: ${finalAnswerValue})`;

    // Mostrar el resultado final
    var actualPage = window.location.href;
    var nextNumberPage = parseInt(actualPage.split("/register")[1]) + 1;
    const formData = new FormData();
    formData.append('data', finalAnswerValue);
    fetch('/register7', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log('Respuesta de Flask:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
    
    setTimeout(function(){
        window.location.href = '/register' + nextNumberPage;
    }, 1000);
    
}

function restartForm() {
    // Volver a mostrar la primera sección
    document.getElementById("section-results").classList.remove("active");
    document.getElementById("section-1").classList.add("active");

    // Desmarcar cualquier opción seleccionada
    document.querySelectorAll('input[type="radio"]').forEach(radio => radio.checked = false);

    // Ocultar el resultado final
    document.getElementById("final-result").style.display = "none";
}