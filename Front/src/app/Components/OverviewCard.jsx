import React from 'react';
import { Button, Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';

export const OverviewCard = ({ title, percentage }) => {
    const navigate = useNavigate();

    const handleClick = () => {
        navigate('/detailedinfo', { state: { title, percentage } });
    };

    return (
        <Button 
            onClick={handleClick}
            variant="contained" 
            sx={{ 
                bgcolor: 'App.grey', 
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