import React from 'react';
import Sky from './Sky';
import Ground from './Ground';

const Canvas = () => {
    const viewBox = [window.innerWidth / -2, 100 - window.innerhHeight, window.innerWidth, window.innerHeight];
    return (
    <svg
        id="aliens-go-boom-canvas"
        preserveAspectRatio="xMaxYMax none"
        viewBow={viewBox}
    >
        <Sky />
        <Ground />
        <circle cx={100} cy={50} r={50} />
    </svg>
    );
};

export default Canvas;
