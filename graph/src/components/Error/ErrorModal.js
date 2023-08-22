import React from 'react';
import { Button, Dialog, DialogTitle, DialogContent, DialogActions } from '@mui/material';

const ErrorModal = ({ message, onClose }) => {
  return (
    <Dialog open={true} onClose={onClose}>
      <DialogTitle>Error</DialogTitle>
      <DialogContent>
        <p>{message}</p>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Закрыть</Button>
      </DialogActions>
    </Dialog>
  );
};

export default ErrorModal;
