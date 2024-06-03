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
    const [isNivel1, setIsNivel1] = useState(false);
    const [isNivel2, setIsNivel2] = useState(false);
    const [isNivel3, setIsNivel3] = useState(false);

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
        variables: '#8851B6',  // Morado 
        ciclos: '#4056B6',     // Azul morado
        operadores: '#0880F2', // Azul medio 
        funciones: '#31C1EC',  // Azul claro 
        argumentos: '#4AB7A3', // Azul verdoso
        texto: '#2F9A7D',      // Rojo-naranja-rosa
        tokens: '#0FADCC'      // Morado
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
        if (category === 'nivel3') {
            setSelectedCategory('nivel3');
            setIsNivel3(true);
            setIsNivel2(false);
            setIsNivel1(false);

        }
        if (category === 'nivel2') {
            setSelectedCategory('tokens');
            setIsNivel3(false);
            setIsNivel2(true);
            setIsNivel1(false);
        }
        if (category === 'nivel1') {
            setSelectedCategory('texto');
            setIsNivel3(false);
            setIsNivel2(false);
            setIsNivel1(true);
        }
    };

    return (
        <Grid container spacing={0} margin={0} justifyContent='center' alignItems='center' minHeight='100vh' minWidth='100vw'>
            <NavBar pages={pages} />

            <Grid item xs={12} marginTop='15vh' align='center'>
                <Box display="flex" justifyContent="center" gap={2}>
                    <Button
                        variant="contained"
                        onClick={() => handleCategoryClick('nivel1')}
                        sx={{
                            boxShadow: 'none', 
                            backgroundColor: isNivel1 ? categoryColors[selectedCategory] : 'transparent', 
                            textTransform: 'capitalize', 
                            borderRadius: 4,
                            border: isNivel1 ? 0 : 1,
                            borderColor: 'secondary.main',
                            color: isNivel1 ? 'App.white' : 'App.black',
                            '&:hover': {
                                backgroundColor: isNivel1 ? categoryColors[selectedCategory] : 'transparent',
                            },
                            '&:focus': {
                                outline: 'none',
                            },
                            '&.Mui-focusVisible': {
                                outline: 'none',
                            },
                        }}
                    >
                        Nivel 1
                    </Button>
                    <Button
                        variant="contained"
                        onClick={() => handleCategoryClick('nivel2')}
                        sx={{
                            boxShadow: 'none', 
                            backgroundColor: isNivel2 ? categoryColors[selectedCategory] : 'transparent', 
                            textTransform: 'capitalize', 
                            borderRadius: 4,
                            border: isNivel2 ? 0 : 1,
                            borderColor: 'secondary.main',
                            color: isNivel2 ? 'App.white' : 'App.black',
                            '&:hover': {
                                backgroundColor: isNivel2 ? categoryColors[selectedCategory] : 'transparent',
                            },
                            '&:focus': {
                                outline: 'none',
                            },
                            '&.Mui-focusVisible': {
                                outline: 'none',
                            },
                        }}
                    >
                        Nivel 2
                    </Button>
                    <Button
                        variant="contained"
                        onClick={() => handleCategoryClick('nivel3')}
                        sx={{
                            boxShadow: 'none', 
                            backgroundColor: isNivel3 ? 'secondary.main' : 'transparent', 
                            textTransform: 'capitalize', 
                            borderRadius: 4,
                            border: isNivel3 ? 0 : 1,
                            borderColor: 'secondary.main',
                            color: isNivel3 ? 'App.white' : 'App.black',
                            '&:hover': {
                                backgroundColor: isNivel3 ? 'secondary.main' : 'transparent',
                            },
                            '&:focus': {
                                outline: 'none',
                            },
                            '&.Mui-focusVisible': {
                                outline: 'none',
                            },
                        }}
                    >
                        Nivel 3
                    </Button>
                </Box>

                {isNivel3 && (
                    <Box display="flex" justifyContent="center" gap={2} marginTop={2}>
                        {['variables', 'ciclos', 'operadores', 'funciones', 'argumentos'].map((category) => (
                            <Button
                                key={category}
                                variant="contained"
                                onClick={() => setSelectedCategory(category)}
                                sx={{ 
                                    backgroundColor: categoryColors[category], 
                                    textTransform: 'capitalize',
                                    '&:hover': {
                                        backgroundColor: categoryColors[category],
                                    },
                                    '&:focus': {
                                        outline: 'none',
                                    },
                                    '&.Mui-focusVisible': {
                                        outline: 'none',
                                    }, 
                                }}
                            >
                                {category.charAt(0).toUpperCase() + category.slice(1)}
                            </Button>
                        ))}
                    </Box>
                )}
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
