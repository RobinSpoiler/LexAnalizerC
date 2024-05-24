import { Box, Button, Grid, Paper, Typography } from '@mui/material';
import { useEffect, useState } from 'react';
import { NavBar } from '../Components';
import { useLocation } from 'react-router-dom';
import axios from 'axios';


export const Highlighter = () => {
    const [comparisonRes, setcomparisonRes] = useState({}); // Estado para controlar la data de compare

    const location = useLocation();
    const { file_names } = location.state || {};

    const fileA = file_names[0];
    const fileB = file_names[1];

    const pages = [
        { name: 'Subir archivos', route: '/upload' },
        { name: 'Descripción general', route: '/overview' },
        { name: 'Comparador', route: '/highlighter' },
    ];


    const [fileData, setFileData] = useState({});
    const [content, setContent] = useState({});


    const fetchFileData = async (fileKey) => {
        try {
            const response = await fetch(`http://127.0.0.1:5000/getFileByName?name=${fileKey}`);
            if (response.ok) {
                const fileData = await response.json();
                setFileData(prev => ({ ...prev, [fileKey]: fileData.content }));
                setContent(prev => ({ ...prev, [fileKey]: fileData.content }));

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

    const handleHighlights = async () => {
        try {

            // Realizar la llamada al servidor utilizando Axios
            const response = await axios.post('http://127.0.0.1:5000/highlight', {
                headers: {
                    'Content-Type': 'multipart/form-data'

                },
                body: fileData
            });

            const data = response.data

            setcomparisonRes(data)

            // Manejar los datos de respuesta
        } catch (error) {
            console.error('Error al comparar archivos:', error);
        }
    };

    // console.log(comparisonRes)

    useEffect(() => {
        if (Object.keys(fileData).length == 2) {
            handleHighlights();
        }
    }, [fileData])




    const resaltarPalabras = (linea, indices) => {

        console.log("Linea", linea)
        console.log("indices", indices)


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

    const handleSemanticClick = (fileKey) => {
        const semanticData = comparisonRes[fileKey].semantico;
        const indices = []
        Object.entries(semanticData).forEach(([key, value]) => {
            if(value.length > 0){
                indices.push(value)
            }
        });
        
        const highlightedContent = resaltarPalabras(content[fileKey], indices);

        console.log(indices)
        setContent(prevData => ({
            ...prevData,
            [fileKey]: highlightedContent,
          }));
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
                                {content[fileKey]}
                            </pre>
                            <Button variant="contained" onClick={() => handleSemanticClick(fileKey)}>Semantic Info</Button>

                        </Paper>
                    </Grid>
                ))}
            </Grid>
        </Grid>
    );
};
