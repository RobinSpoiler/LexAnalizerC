import React, { useState, useEffect } from 'react';
import { Grid, Box, Link, Button } from '@mui/material';
import { OverviewCard, MatrixDisplay, NavBar } from '../Components';
import { Link as RouterLink } from 'react-router-dom';
import { Co2Sharp } from '@mui/icons-material';
import axios from 'axios';


export const Overview = () => {
    const [view, setView] = useState('list'); // Estado para controlar la vista
    const [allfiles, setAllFiles] = useState(''); // Estado para controlar la vista
    const [data, setData] = useState(''); // Estado para controlar la data de compare

    useEffect(() => {
        setAllFiles(handleGetFiles())
    }, [])

    useEffect(() => {
        handleCompare()
    }, [allfiles])

    const pages = [
        { name: 'Subir archivos', route: '/upload' },
        { name: 'Descripción general', route: '/overview' },
    ];

    // const data = {
    //     "comp1": {
    //         "id": "Paola vs Marco",
    //         "file_names": ["prueba1.py", "prueba2.py"],
    //         "porcentaje": 78
    //     },
    //     "comp2": {
    //         "id": "Adrian vs Sofia",
    //         "file_names": ["prueba2.py", "prueba3.py"],
    //         "porcentaje": 46
    //     },
    //     "comp3": {
    //         "id": "Marco vs Paola",
    //         "file_names": ["prueba3.py", "prueba4.py"],
    //         "porcentaje": 24
    //     },
    //     "comp4": {
    //         "id": "Sofia vs Adrian",
    //         "file_names": ["prueba5.py", "prueba6.py"],
    //         "porcentaje": 0
    //     }
    // };

    const matrix = {
        "size": 4,
        "data": ["", "Paola", "Marco", "Adrian", "Sofia", "Paola", 100, 78, 0, 0, "Marco", 24, 100, 0, 0, "Adrian", 0, 0, 100, 46, "Sofia", 0, 0, 0, 100]
    };


    const handleGetFiles = async (event) => {
        try {
            const response = await fetch('http://127.0.0.1:5000/getFiles', {
                method: 'GET',
            });

            // console.log(response)
            if (!response.ok) {
                throw new Error('Error al subir archivos');
            }

            const res = await response.json();
            setAllFiles(res);

            console.log("handleGetFiles", allfiles)


            console.log('Archivos subidos exitosamente');
        } catch (error) {
            console.error('Error:', error.message);
        }
    };

    // Function to sort and set data
    function sortAndSetData(r) {
        if (typeof r === 'object' && !Array.isArray(r)) {
            // Convert dictionary to an array of objects
            let arrayOfObjects = Object.values(r);

            // Sort the array by 'porcentaje' in descending order
            arrayOfObjects.sort((a, b) => b.porcentaje - a.porcentaje);

            // Optional: Convert the sorted array back to a dictionary
            let sortedDict = {};
            arrayOfObjects.forEach((item, index) => {
                sortedDict[index + 1] = item; // Adjust keys as necessary
            });

            setData(sortedDict); // Use setData to update the data
        }
    }

    const handleCompare = async () => {
        try {

            // Realizar la llamada al servidor utilizando Axios
            const response = await axios.post('http://127.0.0.1:5000/compare', {
                headers: {
                    'Content-Type': 'multipart/form-data'

                },
                body: allfiles
            });

            sortAndSetData(response.data)
            // Manejar los datos de respuesta
        } catch (error) {
            console.error('Error al comparar archivos:', error);
        }
    };


    const ListView = () => (
        <>
            {Object.entries(data).map(([key, value]) => (
                <Grid key={key} item xs={12} align='center' sx={{
                    margin: '5px',

                }}>
                    <OverviewCard file_names={value.file_names} title={value.id} percentage={value.porcentaje} />
                </Grid>
            ))}
        </>
    );

    const MatrixView = () => (
        <Grid item xs={12} align='center' sx={{ margin: '5px' }}>
            <MatrixDisplay matrix={matrix} />
        </Grid>
    );

    return (
        <Box sx={{ width: '100%', position: 'relative' }}>
            <NavBar pages={pages} />
            <Box sx={{
                position: 'fixed',
                top: '20vh',
                left: '50%',
                transform: 'translateX(-50%)',
                display: 'flex',
                flexDirection: 'row', // Para alinear los botones horizontalmente
                gap: 10, // Espacio entre los botones
            }}
                onLoad={handleGetFiles}>
                <Link
                    component={RouterLink}
                    underline="none"
                    sx={{
                        color: view === 'list' ? 'secondary.main' : 'App.black',
                        borderBottom: view === 'list' ? '2px solid' : 'none',
                        textDecoration: 'none',
                        '&:hover': {
                            color: view === 'list' ? 'secondary.main' : 'App.black',
                        },
                    }}
                    onClick={() => setView('list')}
                >
                    Lista
                </Link>
                <Link
                    component={RouterLink}
                    underline="none"
                    sx={{
                        color: view === 'matrix' ? 'secondary.main' : 'App.black',
                        borderBottom: view === 'matrix' ? '2px solid' : 'none',
                        textDecoration: 'none',
                        '&:hover': {
                            color: view === 'matrix' ? 'secondary.main' : 'App.black',
                        },
                    }}
                    onClick={() => setView('matrix')}
                >
                    Matriz
                </Link>
            </Box>
            <Grid container justifyContent="center" alignItems="center" height='65vh' sx={{
                marginTop: 20,
                overflow: 'auto',
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
            }}>
                {view === 'list' ? <ListView /> : <MatrixView />}
            </Grid>
        </Box>
    );
};