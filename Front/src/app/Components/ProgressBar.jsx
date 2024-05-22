import React, { useEffect, useState } from 'react';
import { LinearProgress, Typography, Box } from '@mui/material';
import { useTimer } from 'react-timer-hook';

export const ProgressBar = ({ duration, onComplete }) => {
  const [progress, setProgress] = useState(0);

  const time = new Date();
  time.setSeconds(time.getSeconds() + duration / 1000); // duration in milliseconds

  const {
    seconds,
    isRunning,
    start,
    pause,
    resume,
    restart,
  } = useTimer({ expiryTimestamp: time, onExpire: () => setProgress(100) });

  useEffect(() => {
    if (isRunning) {
      const interval = setInterval(() => {
        setProgress((prevProgress) => {
          const newProgress = prevProgress + (100 / (duration / 1000));
          return Math.min(newProgress, 100); // Ensure progress does not exceed 100%
        });
      }, 1000); // Update every second

      return () => clearInterval(interval);
    }
  }, [isRunning, duration]);

  useEffect(() => {
    if (progress === 100 && onComplete) {
      onComplete();
    }
  }, [progress, onComplete]);

  useEffect(() => {
    start();
  }, []);

  return (
    <Box sx={{ width: '50%' }}>
      <LinearProgress variant="determinate" value={progress} />
      <Typography variant='body2' color='textSecondary' align='center'>{`${Math.round(progress)}%`}</Typography>
    </Box>
  );
};