import React from 'react';
import { Button, Typography } from '@mui/material';

export const OverviewCard = ({ title, percentage }) => {
    return (
        <Button 
            variant="contained" 
            sx={{ 
                bgcolor: 'grey', 
                borderRadius: '25px', 
                minWidth: '500px', 
                minHeight: '80px', 
                padding: '10px 20px', 
                display: 'flex', 
                justifyContent: 'space-between', 
                alignItems: 'center',
                textTransform: 'none' 
            }}
        >
            <Typography variant="h5">{percentage}%</Typography>
            <Typography variant="body1">{title}</Typography>
        </Button>
    );
};