import React, { useState } from 'react';
import axios from 'axios';

export const Comparator = () => {
    const [file1Content, setFile1Content] = useState(null);
    const [file2Content, setFile2Content] = useState(null);

    const handleFile1Change = async (event) => {
        const file = event.target.files[0];
        const content = await readFileContent(file);
        setFile1Content(content);
    };

    const handleFile2Change = async (event) => {
        const file = event.target.files[0];
        const content = await readFileContent(file);
        setFile2Content(content);
    };

    const readFileContent = async (file) => {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result);
            reader.onerror = () => reject(reader.error);
            reader.readAsText(file);
        });
    };

    const compareFiles = async () => {
        // Aquí puedes utilizar file1Content y file2Content para enviar el contenido de los archivos al servidor
        console.log("Contenido del archivo 1:", file1Content);
        console.log("Contenido del archivo 2:", file2Content);

        try {
            // Crear un objeto FormData y agregar el contenido de los archivos
            const formData = new FormData();
            formData.append('file1', file1Content);
            formData.append('file2', file2Content);

            // Realizar la llamada al servidor utilizando Axios
            const response = await axios.post('http://127.0.0.1:5000/compare', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                },
            });

            console.log(response.data);
            // Manejar los datos de respuesta
        } catch (error) {
            console.error('Error al comparar archivos:', error);
        }
    };
    
    return (
        <div>
            <h2>Comparator</h2>
            <div>
                <input type="file" onChange={handleFile1Change} />
            </div>
            <div>
                <input type="file" onChange={handleFile2Change} />
            </div>
            <button onClick={compareFiles}>Compare Files</button>
        </div>
    );
};