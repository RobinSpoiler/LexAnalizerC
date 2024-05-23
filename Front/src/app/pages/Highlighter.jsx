import { Box, Grid, Paper, Typography } from '@mui/material';
import { useEffect, useState } from 'react';
import { NavBar } from '../Components';
import { useLocation } from 'react-router-dom';

export const Highlighter = () => {

    const location = useLocation();
    const { file_names } = location.state || {};

    const fileA = file_names[0];
    const fileB = file_names[1];

    console.log(file_names)

    const data = {
        "fileA": {
            "content": [
                { "lineNumber": 1, "indices": [[0, 15]] },
                { "lineNumber": 2, "indices": [[6, 7]] },
                { "lineNumber": 3, "indices": [[4, 5], [8, 9]] },
                { "lineNumber": 4, "indices": [[4, 21]] },
                { "lineNumber": 5, "indices": [[0, 5]] }
            ]
        }
    };

    const pages = [
        { name: 'Subir archivos', route: '/upload' },
        { name: 'Descripción general', route: '/overview' },
        { name: 'Comparador', route: '/highlighter' },
    ];


    const [fileData, setFileData] = useState({});

    const fetchFileData = async (fileKey) => {
        try {
            const response = await fetch(`http://127.0.0.1:5000/getFileByName?name=${fileKey}`);
            if (response.ok) {
                const fileData = await response.json();
                setFileData(prev => ({ ...prev, [fileKey]: fileData.content }));
            } else {
                console.error('Error fetching file content:', response.statusText);
            }
        } catch (error) {
            console.error('Error fetching file content:', error);
        }
    };

    useEffect(() => {
        fetchFileData(fileA);
        fetchFileData(fileB);
    }, []);

    // const d = {
    //     "prueba1.py": {
    //         "string": {
    //             "similitud": [
    //                 { "lineNumber": 1, "indices": [[0,15]] }
    //             ]
    //         },
    //         "token": {
    //             "similitud": [
    //                 { "lineNumber": 1, "indices": [[0,15]] }
    //             ]
    //         },
    //         "semántico": {
    //             "variables": [
    //                 { "lineNumber": 1, "indices": [[0,15]] }
    //             ],
    //             "ciclos": [
    //                 { "lineNumber": 1, "indices": [[0,15]] }
    //             ],
    //             "operators": [
    //                 { "lineNumber": 1, "indices": [[0,15]] }
    //             ],
    //             "argumentos": [
    //                 { "lineNumber": 1, "indices": [[0,15]] }
    //             ]
    //         }
    //     },
    //     "prueba2.py": {
    //         "string": {
    //             "similitud": [
    //                 { "lineNumber": 1, "indices": [[0,15]] }
    //             ]
    //         },
    //         "token": {
    //             "similitud": [
    //                 { "lineNumber": 1, "indices": [[0,15]] }
    //             ]
    //         },
    //         "semántico": {
    //             "variables": [
    //                 { "lineNumber": 1, "indices": [[0,15]] }
    //             ],
    //             "ciclos": [
    //                 { "lineNumber": 1, "indices": [[0,15]] }
    //             ],
    //             "operators": [
    //                 { "lineNumber": 1, "indices": [[0,15]] }
    //             ],
    //             "argumentos": [
    //                 { "lineNumber": 1, "indices": [[0,15]] }
    //             ]
    //         },
    //     }
    // }

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
        <Grid container spacing={0} margin={0} justifyContent='center' alignContent='center' minHeight='100vh' minWidth='100vw'>
            <NavBar pages={pages} />

            <Grid container spacing={2} justifyContent='center' padding={2} marginTop='10vh'>
                {Object.keys(fileData).map((fileKey, index) => (
                    <Grid item xs={12} md={6} key={fileKey}>
                        <Paper elevation={3} style={{ 
                            height: '70vh', 
                            padding: '15px', 
                            overflow: 'auto',
                            }}
                            
                            sx={{
                                '&::-webkit-scrollbar': {
                                    width: '8px',
                                },
                                '&::-webkit-scrollbar-track': {
                                    backgroundColor: 'App.grey',
                                },
                                '&::-webkit-scrollbar-thumb': {
                                    backgroundColor: "secondary.main",
                                    borderRadius: '10px',
                                },
                            }}
                            >

                            <Box display="flex" justifyContent="center">
                                <Typography
                                    variant="h6"
                                    sx={{
                                        color: 'App.white',
                                        bgcolor: 'secondary.main',
                                        borderRadius: "22px",
                                        px: 1, // Adds horizontal padding
                                        '&:hover': {
                                            backgroundColor: 'secondary.main'
                                        }
                                    }}
                                >
                                    {fileKey}
                                </Typography>
                            </Box>
                            <pre style={{ whiteSpace: 'pre-wrap', wordWrap: 'break-word' }}>
                                {fileData[fileKey]}
                            </pre>
                        </Paper>
                    </Grid>
                ))}
            </Grid>
        </Grid>
    );
};
