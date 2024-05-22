import React, { useState } from 'react';

export const Highlighter = () => {

    const pages = [
        { name: 'Subir archivos', route: '/upload'},
        { name: 'Descripción general', route: '/overview'},
        { name: 'Resultados', route: '/highlighter'}
    ]

    const data = {
        "fileA": {
            "indices": [[0, 5], [8,10], [20,55]],
            "condicionales": {
                "indices": [[0, 6], [22, 27]]
            },
            "loops": 5
        },
    };

    const resaltarPalabras = (contenido, indices) => {
        const palabras = contenido.split('');
        let palabraActual = '';
        let resaltado = [];
        let indiceActual = 0;

        for (let i = 0; i < palabras.length; i++) {
            if (indices.some(([inicio, fin]) => indiceActual >= inicio && indiceActual < fin)) {
                palabraActual += palabras[i];
            } else {
                if (palabraActual) {
                    resaltado.push(<span style={{ backgroundColor: "yellow" }}>{palabraActual}</span>);
                    palabraActual = '';
                }
                resaltado.push(palabras[i]);
            }
            indiceActual++;
        }

        if (palabraActual) {
            resaltado.push(<span style={{ backgroundColor: "yellow" }}>{palabraActual}</span>);
        }

        return resaltado;
    };

    const [fileContent, setFileContent] = useState('');

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        if (!file) return; // User didn't select a file
        const reader = new FileReader();
        reader.onload = (e) => {
            const content = e.target.result;
            setFileContent(content);
        };
        reader.readAsText(file);
    };

    return (
        <div>
            <input type="file" onChange={handleFileChange} />
            <div>
                <h2>File Content:</h2>
                {Object.entries(data).map(([archivo, info]) => (
                    <div key={archivo}>
                        <h3>{archivo}</h3>
                        <pre>
                            {resaltarPalabras(fileContent, info.indices)}
                        </pre>
                    </div>
                ))}
            </div>
        </div>
    );
};