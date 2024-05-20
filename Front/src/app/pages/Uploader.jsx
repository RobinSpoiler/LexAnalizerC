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
            // console.log(JSON.stringify(formData));
        } catch (error) {
            console.error('Error:', error.message);
        }
    };

    //Borrar depsues
    const handleFileRetrieve = async (event) => {

        try {
            const response = await fetch('http://127.0.0.1:5000/getFiles', {
                method: 'GET',
                // mode: 'no-cors'
            });

            if (!response.ok) {
                console.log("adfad", response) 
                 throw new Error('Error al recibir archivos');
            }

            // console.log(response);
            const respuesta = await response.json();
            console.log(respuesta);
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
                <Button
                    variant="contained"
                    component="label"
                    sx={{ fontSize: '10px', padding: '10px 10px', textTransform: 'none' }}
                    onClick={handleFileRetrieve}
                >
                    Retrieve archivo(s)

                </Button>
            </Grid>
        </Grid>
    );
}