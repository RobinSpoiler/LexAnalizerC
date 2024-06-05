import { Grid, Modal, Button } from '@mui/material';
import React from 'react';

export const ImageModal = ({ open, close, selectedImage }) => {
    return (
        <Modal
            open={open}
            onClose={close}
            sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}
        >
            <Grid container
                justifyContent='center'
                alignItems='center'
                sx={{
                    boxShadow: 10,
                    width: '95vw',
                    maxHeight: '60vh',
                    backgroundColor: 'App.white'
                }}
            >
                <Grid item xs={12} sx={{ maxHeight: '60vh'}}>
                    <img 
                        src={selectedImage} 
                        alt="Large Image" 
                        style={{ width: '100%', height: '100%', objectFit: 'contain' }} 
                    />
                </Grid>
            </Grid>
        </Modal>
    );
};
