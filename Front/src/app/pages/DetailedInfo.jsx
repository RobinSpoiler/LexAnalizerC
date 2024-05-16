import React from 'react';
import { useLocation } from 'react-router-dom';

export const DetailedInfo = () => {
    const location = useLocation();
    const { title, percentage } = location.state || {};

    const data = {
        "id"         : title,
        "percentage" : percentage,
        "text1"      : 
`<pre>
    <span style='background-color: yellow;'>function</span> myFunction() {
        <span style='background-color: yellow;'>let</span> x = 10;
        <span style='background-color: yellow;'>if</span> (x < 20) {
            console.log("x is less than 20");
        }
    }
</pre>`
    }

    return (
        <div>
            <h1>Detailed Info</h1>
            <p>Comparison: {title}</p>
            <p>Percentage: {percentage}%</p>
            <div dangerouslySetInnerHTML={{ __html: data.text1 }}></div>
        </div>
    );
};