async function saveChanges() {
    const rows = Array.from(document.querySelectorAll("tbody tr"));
    const updatedData = rows.map(row => {
        const indexField = row.querySelector("input[name='index']");
        const originalTextField = row.querySelector("div[name='original_text']");
        const translatedTextField = row.querySelector("div[name='translated_text']");

        // Validar que todos los campos existan antes de acceder a ellos
        if (indexField && originalTextField && translatedTextField) {
            return {
                index: indexField.value,
                original_text: originalTextField.innerHTML.trim(),
                translated_text: translatedTextField.innerHTML.trim()
            };
        } else {
            console.error("Campos faltantes en la fila:", row);
            return null;
        }
    }).filter(row => row !== null); // Filtrar filas inválidas

    try {
        console.log("Datos actualizados:", updatedData);
        const response = await fetch('/update', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(updatedData)
        });

        const result = await response.json();
        alert(result.message);
        console.log("Cambios guardados:", result);
    } catch (error) {
        console.error("Error al guardar los cambios:", error);
        alert("Ocurrió un error al guardar los cambios.");
    }
}


function filterTable() {
    let input = document.getElementById('searchInput');
    let filter = input.value.toLowerCase();
    let table = document.querySelector('table tbody');
    let rows = table.getElementsByTagName('tr');

    for (let i = 0; i < rows.length; i++) {
        let originalText = rows[i].getElementsByTagName('td')[0].innerText.toLowerCase();
        let translatedText = rows[i].getElementsByTagName('td')[1].innerText.toLowerCase();
        if (originalText.includes(filter) || translatedText.includes(filter)) {
            rows[i].style.display = '';
        } else {
            rows[i].style.display = 'none';
        }
    }
}

function replaceWordFunction(searchWordId, replaceWordId, columnClass) {
    var searchWord = document.getElementById(searchWordId).value;
    var replaceWord = document.getElementById(replaceWordId).value;

    var cells = document.getElementsByClassName(columnClass);
    
    for (var i = 0; i < cells.length; i++) {
        cells[i].innerHTML = cells[i].innerHTML.replace(new RegExp(searchWord, 'g'), replaceWord);
    }
}