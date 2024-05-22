import { useState } from 'react';

export const Highlighter = () => {
    const data = {
        "fileA": {
            "content": [
                { "lineNumber": 1, "indices": [[0, 15]] },
                { "lineNumber": 2, "indices": [[6, 7]] },
                { "lineNumber": 3, "indices": [[4, 5], [8, 9]] },
                { "lineNumber": 4, "indices": [[4, 21]] },
                { "lineNumber": 5, "indices": [[0,5]] }
            ]
        }
    };

    const resaltarPalabras = (linea, indices) => {
        const palabras = linea.split('');
        let resaltado = [];
        let palabraActual = '';
        let dentroDeResaltado = false;

        for (let i = 0; i < palabras.length; i++) {
            if (indices.some(([inicio, fin]) => i >= inicio && i < fin)) {
                if (!dentroDeResaltado) {
                    if (palabraActual) {
                        resaltado.push(palabraActual);
                        palabraActual = '';
                    }
                    dentroDeResaltado = true;
                }
                palabraActual += palabras[i];
            } else {
                if (dentroDeResaltado) {
                    resaltado.push(<span style={{ backgroundColor: "yellow" }}>{palabraActual}</span>);
                    palabraActual = '';
                    dentroDeResaltado = false;
                }
                palabraActual += palabras[i];
            }
        }

        if (palabraActual) {
            if (dentroDeResaltado) {
                resaltado.push(<span style={{ backgroundColor: "yellow" }}>{palabraActual}</span>);
            } else {
                resaltado.push(palabraActual);
            }
        }

        return resaltado;
    };

    const [fileContent, setFileContent] = useState('');

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        if (!file) return;
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
                            {fileContent.split('\n').map((line, index) => {
                                const lineNumber = index + 1;
                                const lineInfo = info.content.find(item => item.lineNumber === lineNumber);
                                if (lineInfo) {
                                    return (
                                        <div key={index}>
                                            {resaltarPalabras(line, lineInfo.indices)}
                                        </div>
                                    );
                                }
                                return <div key={index}>{line}</div>;
                            })}
                        </pre>
                    </div>
                ))}
            </div>
        </div>
    );
};
