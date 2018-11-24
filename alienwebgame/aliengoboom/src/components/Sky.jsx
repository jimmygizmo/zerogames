import React from 'react';
import constants, { skyAndGroundWidth } from '../utils/constants';

const Sky = () => {
    const skyStyle = {
        fill: '#30abef',
    };
    const skyWidth = skyAndGroundWidth;
    const gameHeight = 1200;
    return (
        <rect
            style={skyStyle}
            x={skyWidth / -2}
            y={100 - gameHeight}
            width={skyWidth}
            height={gameHeight}
        />
    );
};

export default Sky;
