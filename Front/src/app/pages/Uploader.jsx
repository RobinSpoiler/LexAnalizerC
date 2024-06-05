import React, { useState } from 'react';
import { Grid, Button, Typography, Box } from '@mui/material';
import { FileUploadOutlined } from '@mui/icons-material';
import { NavBar, ProgressBar } from '../Components';
import { useNavigate } from 'react-router-dom';

export const Uploader = () => {
    const navigate = useNavigate();
    const [uploading, setUploading] = useState(false);

    const pages = [
        { name: 'Subir archivos', route: '/upload' }
    ];

    const handleFileUpload = async (event) => {
        const files = event.target.files;
        const formData = new FormData();
        Array.from(files).forEach((file) => {
            formData.append('files', file);
        });

        try {
            const response = await fetch('http://127.0.0.1:5000/addFile', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Error al subir archivos');
            }

            console.log('Archivos subidos exitosamente');
            setUploading(true);
        } catch (error) {
            console.error('Error:', error.message);
        }
    };


    const handleProgressComplete = () => {
        navigate("/overview")
    }

    return (
        <Grid
            container
            spacing={0}
            margin={0}
            justifyContent='center'
            alignItems='center'
            alignContent='center'
            sx={{ minHeight: '100vh', minWidth: '100vw' }}
        >
            <NavBar pages={pages} />

            <Grid item xs={12} align='center'>
                <Typography variant='h2'>
                    Detector de plagio
                </Typography>
            </Grid>

            <Grid item xs={12} align='center'>
                <Typography variant='body'>
                    Code Sync detecta el plagio de su código con mayor precisión.
                </Typography>
            </Grid>

            <Grid item xs={12} align='center' sx={{mt:5}}>
                <Button
                    variant="contained"
                    component="label"
                    sx={{ fontSize: '20px', padding: '100px 100px', textTransform: 'none' }}
                    startIcon={<FileUploadOutlined sx={{ fontSize: '30px' }} />}
                >
                    Subir archivos
                    <input
                        type="file"
                        hidden
                        multiple
                        onChange={handleFileUpload}
                    />
                </Button>
            </Grid>

            {uploading && (
                <Grid item xs={12} align='center' sx={{ mt: 5 }}>
                    <ProgressBar duration={5000} onComplete={handleProgressComplete} /> 
                </Grid>
            )}
        </Grid>
    );
}