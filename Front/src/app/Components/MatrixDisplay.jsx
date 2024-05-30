import React from 'react';
import { Grid, Button, Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';

export const MatrixDisplay = ({ matrix }) => {
    const navigate = useNavigate();
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
            if (value === " ") {
                return 'App.lightgrey';
            }
        }
        return 'transparent';
    };

    const handleClick = (val, rowIndex, colIndex) => {
        if (typeof val === 'number') {
            // Find the file names in the current row and column
            const rowFiles = rows[rowIndex].filter(item => typeof item === 'string' && item.includes('.py'));
            const colFiles = rows.map(row => row[colIndex]).filter(item => typeof item === 'string' && item.includes('.py'));
            console.log(`Row files: ${rowFiles}, Column files: ${colFiles}`);
            const file_names = [rowFiles, colFiles]
            navigate('/highlighter', { state: { file_names } });
        }
    };

    return (
        <Grid container justifyContent="center" alignItems="center">
            {rows.map((row, rowIndex) => (
                <Grid container item key={rowIndex} padding={1} spacing={1} justifyContent="center">
                    {row.map((val, colIndex) => (
                        <Grid item key={colIndex}>
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
                                onClick={() => handleClick(val, rowIndex, colIndex)}
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