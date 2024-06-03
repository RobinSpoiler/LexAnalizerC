import { Box, Button, Grid, Paper, Typography } from '@mui/material';
import { useEffect, useState } from 'react';
import { NavBar } from '../Components';
import { useLocation } from 'react-router-dom';
import axios from 'axios';

export const Highlighter = () => {
    const [comparisonRes, setComparisonRes] = useState({});
    const [fileData, setFileData] = useState({});
    const [indices, setIndices] = useState({});
    const [selectedCategory, setSelectedCategory] = useState(null);
    console.log(comparisonRes)
    const location = useLocation();
    const { file_names } = location.state || {};

    const fileA = file_names[0];
    const fileB = file_names[1];

    const pages = [
        { name: 'Subir archivos', route: '/upload' },
        { name: 'Descripción general', route: '/overview' },
        { name: 'Comparador', route: '/highlighter' },
    ];

    const categoryColors = {
        variables: '#B8860B',  // Dorado 
        ciclos: '#2E8B57',     // Verde
        operadores: '#4682B4', // Azul 
        funciones: '#CD5C5C',  // Rojo 
        argumentos: '#8B4513', // Cafe
        texto: '#FF6347',  // Rojo-naranja-rosa ish
        tokens: '#CA53CB' //Morado
    };

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
                const fileData = comparisonRes[fileKey];
                const newIndices = {};

                fileData.forEach(data => {
                    if (data.semantico) {
                        Object.keys(data.semantico).forEach(category => {
                            if (!newIndices[category]) {
                                newIndices[category] = [];
                            }
                            data.semantico[category].forEach(lineData => {
                                newIndices[category].push(lineData);
                            });
                        });
                    }
                    if (data.string) {
                        if (!newIndices.texto) {
                            newIndices.texto = [];
                        }
                        data.string.texto.forEach(lineData => {
                            newIndices.texto.push(lineData);
                        });
                    }
                    if (data.token) {
                        if (!newIndices.tokens) {
                            newIndices.tokens = [];
                        }
                        data.token.tokens.forEach(lineData => {
                            newIndices.tokens.push(lineData);
                        });
                    }
                });

                setIndices(prev => ({ ...prev, [fileKey]: newIndices }));
            }
        };

        updateIndices(fileA);
        updateIndices(fileB);
    }, [comparisonRes, fileA, fileB]);

    const resaltarPalabras = (linea, indices, color) => {
        const palabras = linea.split('');
        let resaltado = [];
        let palabraActual = '';
        let dentroDeResaltado = false;

        for (let i = 0; i < palabras.length; i++) {
            if (indices.some(indexRange => i + 1 >= indexRange[0] && i + 1 < indexRange[1])) {
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
                    resaltado.push(<span style={{ backgroundColor: color, color: '#fff' }}>{palabraActual}</span>);
                    palabraActual = '';
                    dentroDeResaltado = false;
                }
                palabraActual += palabras[i];
            }
        }

        if (palabraActual) {
            if (dentroDeResaltado) {
                resaltado.push(<span style={{ backgroundColor: color, color: '#fff' }}>{palabraActual}</span>);
            } else {
                resaltado.push(palabraActual);
            }
        }
        return resaltado;
    };

    const renderFileContent = (fileKey, category) => {
        const content = fileData[fileKey];
        const fileIndices = indices[fileKey] ? indices[fileKey][category] || [] : [];
        return (
            <pre style={{ whiteSpace: 'pre-wrap', wordWrap: 'break-word' }}>
                {content && content.split('\n').map((line, lineIndex) => {
                    const lineIndices = fileIndices
                        .filter(item => item.lineNumber === lineIndex + 1)
                        .flatMap(item => item.indices);

                    return (
                        <div key={lineIndex}>
                            {resaltarPalabras(line, lineIndices, categoryColors[category])}
                        </div>
                    );
                })}
            </pre>
        );
    };

    const renderPlainFileContent = (fileKey) => {
        const content = fileData[fileKey];
        return (
            <pre style={{ whiteSpace: 'pre-wrap', wordWrap: 'break-word' }}>
                {content && (
                    content
                )}
            </pre>
        );
    };

    const handleCategoryClick = (category) => {
        setSelectedCategory(category);
    };

    return (
        <Grid container spacing={0} margin={0} justifyContent='center' alignItems='center' minHeight='100vh' minWidth='100vw'>
            <NavBar pages={pages} />

            <Grid item xs={12} marginTop='15vh' align='center'>
                <Box display="flex" justifyContent="center" gap={2}>
                    {Object.keys(categoryColors).map((category) => (
                        <Button
                            key={category}
                            variant="contained"
                            onClick={() => handleCategoryClick(category)}
                            style={{ backgroundColor: categoryColors[category] }}
                        >
                            {category.charAt(0).toUpperCase() + category.slice(1)}
                        </Button>
                    ))}
                </Box>
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
                            {selectedCategory
                                ? renderFileContent(fileKey, selectedCategory)
                                : renderPlainFileContent(fileKey)}
                        </Paper>
                    </Grid>
                ))}
            </Grid>
        </Grid>
    );
};