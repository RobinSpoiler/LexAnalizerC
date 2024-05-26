import { Box, Button, Grid, Paper, Typography } from '@mui/material';
import { useEffect, useState } from 'react';
import { NavBar } from '../Components';
import { useLocation } from 'react-router-dom';
import axios from 'axios';

export const Highlighter = () => {
    const [comparisonRes, setComparisonRes] = useState({});
    const [fileData, setFileData] = useState({});
    const [indices, setIndices] = useState({});
    const [showContent, setShowContent] = useState(false); // Controlar la visibilidad de ambos archivos

    const location = useLocation();
    const { file_names } = location.state || {};

    const fileA = file_names[0];
    const fileB = file_names[1];

    const pages = [
        { name: 'Subir archivos', route: '/upload' },
        { name: 'Descripción general', route: '/overview' },
        { name: 'Comparador', route: '/highlighter' },
    ];

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

    const handleHighlights = async () => {
        try {
            const response = await axios.post('http://127.0.0.1:5000/highlight', {
                headers: {
                    'Content-Type': 'multipart/form-data'
                },
                body: fileData
            });

            const data = response.data;
            setComparisonRes(data);
        } catch (error) {
            console.error('Error al comparar archivos:', error);
        }
    };

    useEffect(() => {
        if (Object.keys(fileData).length === 2) {
            handleHighlights();
        }
    }, [fileData]);

    useEffect(() => {
        const updateIndices = (fileKey) => {
            if (comparisonRes && comparisonRes[fileKey]) {
                const semanticData = comparisonRes[fileKey]["semantico"];
                const newIndices = [];

                if (semanticData) {
                    Object.values(semanticData).forEach(lineDataArray => {
                        lineDataArray.forEach(lineData => {
                            newIndices.push(lineData);
                        });
                    });
                }
                setIndices(prev => ({ ...prev, [fileKey]: newIndices }));
            }
        };

        updateIndices(fileA);
        updateIndices(fileB);
    }, [comparisonRes, fileA, fileB]);

    const resaltarPalabras = (linea, indices) => {
        const palabras = linea.split('');
        let resaltado = [];
        let palabraActual = '';
        let dentroDeResaltado = false;

        for (let i = 0; i < palabras.length; i++) {
            if (indices.some(indexRange => i >= indexRange[0] && i < indexRange[1])) {
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

    const renderFileContent = (fileKey) => {
        const content = fileData[fileKey];
        const fileIndices = indices[fileKey] || [];

        return (
            <pre style={{ whiteSpace: 'pre-wrap', wordWrap: 'break-word' }}>
                {content && Array.isArray(fileIndices) && fileIndices.length > 0 && (
                    content.split('\n').map((line, lineIndex) => {
                        const lineIndices = fileIndices
                            .filter(item => item.lineNumber === lineIndex + 1)
                            .flatMap(item => item.indices);

                        return (
                            <div key={lineIndex}>
                                {resaltarPalabras(line, lineIndices)}
                            </div>
                        );
                    })
                )}
            </pre>
        );
    };

    const handleSemanticClick = () => {
        setShowContent(prev => !prev);
    };

    return (
        <Grid container spacing={0} margin={0} justifyContent='center' alignItems='center' minHeight='100vh' minWidth='100vw'>
            <NavBar pages={pages} />

            <Grid item xs={12} marginTop='15vh' align='center'>
                <Button variant="contained" onClick={handleSemanticClick}>Semantic Info</Button>
            </Grid>

            <Grid container spacing={2} justifyContent='center' padding={2} >

                {[fileA, fileB].map((fileKey) => (
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
                                        px: 1,
                                        '&:hover': {
                                            backgroundColor: 'secondary.main'
                                        }
                                    }}
                                >
                                    {fileKey}
                                </Typography>
                            </Box>
                            {showContent && renderFileContent(fileKey)}
                        </Paper>
                    </Grid>
                ))}
            </Grid>
        </Grid>
    );
};