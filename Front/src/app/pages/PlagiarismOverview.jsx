import React from 'react';
import { Grid } from '@mui/material';
import { MatrixDisplay, OverviewCard } from '../Components';

export const PlagiarismOverview = () => {
    const data = {
        "comp1": {
            "id" : "Paola vs Marco",  
            "porcentaje": 78 
        },
        "comp2": { 
            "id" : "Adrian vs Sofia",  
            "porcentaje": 46 
        },
        "comp3": { 
            "id" : "Marco vs Paola",  
            "porcentaje": 24 
        },
        "comp4": { 
            "id" : "Sofia vs Adrian",  
            "porcentaje": 0 
        }
    };

    const matrix = {
        "size" : 4,
        "data" : ["","Paola", "Marco", "Adrian", "Sofia", "Paola", 100, 78, 0, 0, "Marco", 24, 100, 0, 0, "Adrian", 0, 0, 100, 46, "Sofia", 0, 0, 0, 100]
    }

    return (
        <Grid
            container
            spacing={0}
            margin={0}
            justifyContent='center'
            alignItems='center'
            alignContent='center'
            sx={{ minHeight: '100vh', minWidth: '100vw'}}
        >
            {Object.entries(data).map(([key, value]) => (
                <Grid key={key} item xs={12} align='center' sx={{margin: '5px'}}>
                    <OverviewCard title={value.id} percentage={value.porcentaje} />
                </Grid>
            ))}

            <Grid item>
                <MatrixDisplay matrix={matrix}/>

            </Grid>


        </Grid>
    );
};
