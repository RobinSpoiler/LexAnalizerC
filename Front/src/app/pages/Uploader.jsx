import React from 'react';
import { Grid, Button } from '@mui/material';
import { FileUploadOutlined } from '@mui/icons-material';

export const Uploader = () => {

    const handleFileUpload = (event) => {
        const files = event.target.files;
        Array.from(files).forEach((file) => {
            const reader = new FileReader();
            reader.onload = (e) => {
                console.log(`Content of ${file.name}:\n`, e.target.result);
            };
            reader.readAsText(file);
        });
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
                    sx={{ fontSize: '24px',padding: '100px 100px', textTransform: 'none' }}
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