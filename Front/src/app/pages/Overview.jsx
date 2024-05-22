import React, { useState } from 'react';
import { Grid, Box, Link } from '@mui/material';
import { OverviewCard, MatrixDisplay, NavBar } from '../Components';
import { Link as RouterLink } from 'react-router-dom';

export const Overview = () => {
    const [view, setView] = useState('list'); // Estado para controlar la vista

    const pages = [
        { name: 'Subir archivos', route: '/upload' },
        { name: 'Descripción general', route: '/overview' },
    ];

    const data = {
        "comp1": {
            "id": "Paola vs Marco",
            "porcentaje": 78
        },
        "comp2": {
            "id": "Adrian vs Sofia",
            "porcentaje": 46
        },
        "comp3": {
            "id": "Marco vs Paola",
            "porcentaje": 24
        },
        "comp4": {
            "id": "Sofia vs Adrian",
            "porcentaje": 0
        }
    };

    const matrix = {
        "size": 4,
        "data": ["", "Paola", "Marco", "Adrian", "Sofia", "Paola", 100, 78, 0, 0, "Marco", 24, 100, 0, 0, "Adrian", 0, 0, 100, 46, "Sofia", 0, 0, 0, 100]
    };

    const ListView = () => (
        <>
            {Object.entries(data).map(([key, value]) => (
                <Grid key={key} item xs={12} align='center' sx={{ margin: '5px' }}>
                    <OverviewCard title={value.id} percentage={value.porcentaje} />
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
            }}>
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
            <Grid container justifyContent="center" alignItems="center" sx={{ marginTop: 8 }}>
                {view === 'list' ? <ListView /> : <MatrixView />}
            </Grid>
        </Box>
    );
};