const handleError = (error, res) => {
    console.error(error);
    return res.status(500).json({
      message: 'Internal Server Error: ' + error.message,
    });
  };
  
  module.exports = handleError;
  