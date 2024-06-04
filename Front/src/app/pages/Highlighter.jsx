import { Accordion, AccordionDetails, AccordionSummary, Box, Button, Grid, Paper, Typography } from '@mui/material';
import { useEffect, useState } from 'react';
import { CircularProgressBar, NavBar } from '../Components';
import { useLocation } from 'react-router-dom';
import axios from 'axios';
import { GridExpandMoreIcon } from '@mui/x-data-grid';

export const Highlighter = () => {
    const [comparisonRes, setComparisonRes] = useState({});
    const [fileData, setFileData] = useState({});
    const [indices, setIndices] = useState({});
    const [nCategory, setNCategory] = useState({});
    const [percentages, setPercentages] = useState({});
    const [selectedCategory, setSelectedCategory] = useState(null);
    const [isNivel1, setIsNivel1] = useState(false);
    const [isNivel2, setIsNivel2] = useState(false);
    const [isNivel3, setIsNivel3] = useState(false);
    const [selectedNivel, setSelectedNivel] = useState('');
    const [selectedPercentage, setSelectedPercentage] = useState('');

    const [expandedExpander, setExpandedExpander] = useState('main');

    const location = useLocation();
    const { file_names } = location.state || {};

    const fileA = file_names[0];
    const fileB = file_names[1];

    const pages = [
        { name: 'Subir archivos', route: '/upload' },
        { name: 'Descripción general', route: '/overview' },
        { name: 'Comparador', route: '/highlighter' },
    ];

    const descriptions = [
        { nivel1: 'La comparación de textos por caracteres es un método que analiza dos cadenas de texto comparando cada carácter en ambas posiciones correspondientes.' },
        { nivel2: 'La comparación por tokens es un método que analiza dos cadenas de texto dividiéndolas en unidades significativas llamadas tokens, que pueden ser palabras, frases, u otros elementos sintácticos. Este método permite detectar cambios más semánticos, como la adición, eliminación o modificación de palabras completas.' },
        { nivel3: 'La descomposición del código en sus estructuras más simples (main, funciones, ciclos y condicionales), permite al evaluador enfocarse en estructuras específicas, siendo que se puede analizar los argumentos, enteros, flotantes, identificadores, ciclos, operadores y cadenas que componen a dicha porción de código.' },
    ]

    const categoryColors = {
        arguments: '#4AB7A3',
        enteros: '#31C1EC',
        floats: '#0880F2',
        identifiers: '#8851B6',
        loops: '#4056B6',
        operators: '#2F9A7D',
        strings: '#E94A4A',
        texto: '#2F9A7D',
        tokens: '#0FADCC'
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
        if (comparisonRes && fileA && comparisonRes[fileA]) {
            setPercentages(comparisonRes[fileA][3].porcentajes)
        }
    }, [comparisonRes, fileA])

    useEffect(() => {
        const updateIndices = (fileKey) => {
            if (comparisonRes && comparisonRes[fileKey]) {
                const fileData = comparisonRes[fileKey];
                const newIndices = {};
                const categoryQuantity = {};
                const porcentajes = {}

                fileData.forEach(data => {
                    if (data.semantico) {
                        Object.keys(data.semantico).forEach(category => {
                            if (!newIndices[category]) {
                                newIndices[category] = [];
                            }
                            if (!categoryQuantity[category]) {
                                categoryQuantity[category] = [];
                            }
                            const categoryData = data.semantico[category].characteristics;
                            if (categoryData) {
                                // Itera sobre las características de la categoría
                                Object.keys(categoryData).forEach(characteristic => {
                                    const characteristicData = categoryData[characteristic];
                                    // Verifica si la característica tiene una ubicación definida
                                    if (characteristicData && characteristicData.location && characteristicData.location) {

                                        categoryQuantity[category].push({
                                            category: characteristic,
                                            cantidad: characteristicData.cantidad
                                        })
                                        // Accede a los índices dentro de la propiedad location
                                        characteristicData.location.forEach(location => {
                                            // Guarda los índices y el número de línea en newIndices
                                            newIndices[category].push({
                                                characteristic: characteristic,
                                                indices: location.indices,
                                                lineNumber: location.lineNumber,
                                            });
                                        });
                                    }
                                    else if (characteristicData && characteristicData.cantidad) {
                                        categoryQuantity[category].push({
                                            category: characteristic,
                                            cantidad: characteristicData.cantidad
                                        })
                                    }
                                });
                            }
                            newIndices[category].push(data.semantico[category].code)
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
                setNCategory(prev => ({ ...prev, [fileKey]: categoryQuantity }));
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
        if (isNivel3) {
            const size = indices[fileKey][category].length;
            const content = indices[fileKey][category][size - 1];
            const fileIndices = indices[fileKey] ? indices[fileKey][category] || [] : [];
            return (
                <pre style={{ whiteSpace: 'pre-wrap', wordWrap: 'break-word' }}>
                    {content && content.split('\n').map((line, lineIndex) => {
                        const lineIndices = fileIndices
                            .filter(item => item.lineNumber === lineIndex + 1 && item.characteristic === selectedCategory)
                            .flatMap(item => item.indices);
                        return (
                            <div key={lineIndex}>
                                {resaltarPalabras(line, lineIndices, categoryColors[selectedCategory])}
                            </div>
                        );
                    })}
                </pre>
            );

        } else {
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
        }
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
            setSelectedNivel('nivel3');
            setSelectedPercentage('semantico');
            setIsNivel3(true);
            setIsNivel2(false);
            setIsNivel1(false);

        }
        if (category === 'nivel2') {
            setSelectedCategory('tokens');
            setSelectedNivel('nivel2');
            setSelectedPercentage('tokens');
            setIsNivel3(false);
            setIsNivel2(true);
            setIsNivel1(false);
        }
        if (category === 'nivel1') {
            setSelectedCategory('texto');
            setSelectedNivel('nivel1');
            setSelectedPercentage('string');
            setIsNivel3(false);
            setIsNivel2(false);
            setIsNivel1(true);
        }
    };

    const handleExpanderClick = (category) => {
        if (expandedExpander === category) {
            setExpandedExpander(null);
        } else {
            setExpandedExpander(category);
        }
    };

    const handleFeaturesClick = (category) => {
        setSelectedCategory(category);
    }

    const getDescriptionByKey = (key) => {
        const descriptionObject = descriptions.find(desc => desc[key]);
        return descriptionObject ? descriptionObject[key] : '';
    };

    return (
        <Grid container spacing={0} margin={0} justifyContent='center' alignItems='center' minHeight='100vh' minWidth='100vw'>
            <NavBar pages={pages} />

            {selectedPercentage && (
                <Grid item xs={12} align='right' px={5} marginTop='12vh'>
                    <CircularProgressBar percentage={percentages[selectedPercentage].toFixed(2)} />
                </Grid>
            )}

            <Grid item xs={12} align='center' marginTop={selectedNivel ? '0vh' : '15vh'}>
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
                        {['arguments', 'enteros', 'floats', 'identifiers', 'loops', 'operators', 'strings'].map((category) => (
                            <Button
                                key={category}
                                variant="contained"
                                onClick={() => handleFeaturesClick(category)}
                                sx={{
                                    backgroundColor: 'transparent',
                                    boxShadow: 'none',
                                    color: 'App.black',
                                    border:  1,
                                    borderColor: categoryColors[category],
                                    textTransform: 'capitalize',
                                    '&:hover': {
                                        backgroundColor: categoryColors[category],
                                        color : 'App.white',
                                        borderColor: categoryColors[category],
                                    },
                                    '&:focus': {
                                        outline: 'none',
                                        backgroundColor: categoryColors[category],
                                        color : 'App.white'
                                    },
                                    '&.Mui-focusVisible': {
                                        outline: 'none',
                                    },
                                }}
                            >
                                {category}
                            </Button>
                        ))}
                    </Box>
                )}

                {selectedNivel && (
                    <Box display="flex" gap={2} marginTop={2} px={3}>
                        <Typography sx={{ fontWeight: 'bold', color: 'primary.main' }}>Descripción.</Typography>
                        <Typography sx={{ color: 'App.black', textAlign: 'justify' }}>{getDescriptionByKey(selectedNivel)}</Typography>
                    </Box>
                )}

            </Grid>

            <Grid container spacing={2} justifyContent='center' padding={3} >
                {!isNivel3 && ([fileA, fileB].map((fileKey) => (
                    <Grid item xs={12} md={6} key={fileKey}>
                        <Paper elevation={3} style={{
                            height: selectedNivel ? '60vh' : '70vh',
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
                )))}

                {isNivel3 && ([fileA, fileB].map((fileKey) => (
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
                            <Box display="flex" justifyContent="center" flexDirection='column' marginTop='5vh'>
                                {['main', 'functions', 'loops', 'conditionals'].map((category) => (

                                    <Accordion key={category} expanded={expandedExpander === category} onChange={() => handleExpanderClick(category)} disabled={indices && !indices[fileKey][category][indices[fileKey][category].length - 1]}>
                                        <AccordionSummary
                                            expandIcon={<GridExpandMoreIcon />}
                                            sx={{ textTransform: 'capitalize', fontWeight: 'bold', color: 'primary.main' }}
                                        >
                                            {category}
                                        </AccordionSummary>
                                        <AccordionDetails>
                                            <Box display="flex" justifyContent="space-between">
                                                {['arguments', 'enteros', 'floats', 'identifiers', 'loops', 'operators', 'strings'].map(subCategory => {
                                                    const cantidad = nCategory ? nCategory[fileKey][category].find(item => item.category == subCategory).cantidad : '';
                                                    return (
                                                        <Typography key={subCategory} sx={{ color: categoryColors[subCategory] }}>
                                                            {subCategory}: {cantidad}
                                                        </Typography>
                                                    );
                                                })}
                                            </Box>

                                            {renderFileContent(fileKey, category)}
                                        </AccordionDetails>
                                    </Accordion>
                                ))}
                            </Box>
                        </Paper>
                    </Grid>
                )))}
            </Grid>
        </Grid>
    );
};