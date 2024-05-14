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
        }
        return 'default';
    };

    return (
        <Grid container justifyContent="center" alignItems="center">
            {rows.map((row, rowIndex) => (
                <Grid container item key={rowIndex} spacing={2} justifyContent="center">
                    {row.map((item, itemIndex) => (
                        <Grid item key={itemIndex}>
                            <Button
                                variant="contained"
                                sx={{
                                    minWidth: '100px',
                                    minHeight: '50px',
                                    backgroundColor: getButtonColor(item),
                                    '&:hover': {
                                        backgroundColor: getButtonColor(item)
                                    }
                                }}
                            >
                                <Typography variant="body1">{item}</Typography>
                            </Button>
                        </Grid>
                    ))}
                </Grid>
            ))}
        </Grid>
    );
};