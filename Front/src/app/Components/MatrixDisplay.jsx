import React from 'react';
import { Grid, Button, Typography } from '@mui/material';

export const MatrixDisplay = ({ matrix }) => {
    const { size, data } = matrix;
    const adjustedSize = size + 1;

    const rows = [];
    for (let i = 0; i < data.length; i += adjustedSize) {
        rows.push(data.slice(i, i + adjustedSize));
    }

    const getButtonColor = (value) => {
        if (typeof value === 'number') {
            if (value >= 0 && value <= 33) {
                return 'App.green';
            } else if (value >= 34 && value <= 66) {
                return 'App.yellow';
            } else if (value >= 67 && value <= 100) {
                return 'App.red';
            }
        } else if (typeof value === 'string') {
            if (value == " ") {
                return 'App.lightgrey'
            }
        }
        return 'transparent';
    };

    return (
        <Grid container justifyContent="center" alignItems="center">
            {rows.map((row, rowIndex) => (
                <Grid container item key={rowIndex} padding={1} spacing={1} justifyContent="center">
                    {row.map((val, index) => (
                        <Grid item key={index}>
                            <Button
                                variant="contained"
                                sx={{
                                    boxShadow: 'none',
                                    minWidth: '100px',
                                    minHeight: '50px',
                                    backgroundColor: getButtonColor(val),
                                    textTransform: 'capitalize',
                                    '&:hover': {
                                        backgroundColor: getButtonColor(val),
                                        boxShadow: 'none'
                                    }
                                }}
                            >
                                <Typography variant="body1" sx={{ color: typeof val === 'number' ? 'App.white' : 'primary.main' }}>{val}</Typography>
                            </Button>
                        </Grid>
                    ))}
                </Grid>
            ))}
        </Grid>
    );
};