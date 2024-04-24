import React, { useState } from 'react';
import axios from 'axios';

export const Comparator = () => {
    const [file1, setFile1] = useState(null);
    const [file2, setFile2] = useState(null);

    const handleFile1Change = (event) => {
        const file = event.target.files[0];
        setFile1(file);
    };

    const handleFile2Change = (event) => {
        const file = event.target.files[0];
        setFile2(file);
    };

    const compareFiles = async () => {
        if (!file1 || !file2) {
            console.error("Debes seleccionar dos archivos para comparar.");
            return;
        }

        try {
            // Crear un objeto FormData y agregar los archivos
            const formData = new FormData();
            formData.append('file1', file1);
            formData.append('file2', file2);

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