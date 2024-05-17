import React from 'react';
import { Grid, Button } from '@mui/material';
import { FileUploadOutlined } from '@mui/icons-material';

export const Uploader = () => {

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
        } catch (error) {
            console.error('Error:', error.message);
        }
    };

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
            <Grid item>
                <Button
                    variant="contained"
                    component="label"
                    sx={{ fontSize: '24px', padding: '100px 100px', textTransform: 'none' }}
                    startIcon={<FileUploadOutlined sx={{ fontSize: '30px' }} />}
                >
                    Subir archivo(s)
                    <input
                        type="file"
                        hidden
                        multiple
                        onChange={handleFileUpload}
                    />
                </Button>
            </Grid>
        </Grid>
    );
}