async function saveChanges() {
    const rows = Array.from(document.querySelectorAll("tbody tr"));
    const updatedData = rows.map(row => {
        const indexField = row.querySelector("input[name='index']");
        const originalTextField = row.querySelector("div[name='original_text']");
        const translatedTextField = row.querySelector("div[name='translated_text']");
        const check = row.querySelector("input[name^='check_translate_']");

        // Validar que todos los campos existan antes de acceder a ellos
        if (indexField && originalTextField && translatedTextField && check) {
            return {
                index: indexField.value,
                original_text: originalTextField.innerHTML.trim(),
                translated_text: translatedTextField.innerHTML.trim(),
                check: check.checked,
            };
        } else {
            return null;
        }
    }).filter(row => row !== null); // Filtrar filas inválidas

    try {
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


async function saveOriginalColumns() {
    try {
        const response = await fetch('/save_data_original', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const result = await response.json();
        alert(result.message);
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

let value = false;

function filterRows() {
    console.log("checkFilterValids");
    const filterEnabled = document.getElementById("filterValids").checked;
    value = filterEnabled;
    console.log("Filtro de validos activado:", filterEnabled);
    checkFilterValids();
}

    function checkFilterValids(){
        const rows = document.querySelectorAll("tbody tr");

        rows.forEach(row => {
            // Obtener los checkboxes de la fila actual
            const check = row.querySelector("input[name^='check_translate_']");

            if (value) {
                // Ocultar la fila si ambos checkboxes están marcados
                if (check?.checked) {
                    row.style.display = "none";
                } else {
                    row.style.display = ""; // Mostrar la fila
                }
            } else {
                row.style.display = ""; // Mostrar todas las filas si el filtro está deshabilitado
            }
        });
    }

document.addEventListener("DOMContentLoaded", () => {
    const filterCheckbox = document.getElementById("filterValids");
    // const checks = document.getElementsByClassName("validCheck");
    if (filterCheckbox) {
        filterCheckbox.addEventListener("click", checkFilterValids);
        // checks.addEventListener("click", checkFilterValids);
    } else {
        console.error("El elemento con ID 'filterValids' no se encontró.");
    }
});

async function translateText(rowIndex, sourceLanguage) {
    const row = document.querySelector(`tr[data-index='${rowIndex}']`);
    const translatedTextField = row.querySelector("div[name='translated_text']");

    if (translatedTextField) {

        try {
            const response = await fetch('/translate_text', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    index: rowIndex,
                    translate_to: sourceLanguage
                })
            });

            const result = await response.json();
            translatedTextField.innerHTML = result.translated_text;
            alert(result.message);
        } catch (error) {
            console.error("Error al traducir el texto:", error);
            alert("Ocurrió un error al traducir el texto.");
        }
    } else {
        console.error("Campos faltantes en la fila:", row);
    }
}