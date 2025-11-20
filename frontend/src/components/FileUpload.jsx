import { useState } from 'react';
import { uploadDocument } from '../api';

const FileUpload = ({ onAnalysisComplete }) => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    setFile(selectedFile);
    setError(''); // Clear any previous errors
  };

  const handleUpload = async () => {
    if (!file) return;

    setLoading(true);
    setError('');

    try {
      const response = await uploadDocument(file);
      
      // Pass extracted data back to parent component
      onAnalysisComplete(response.data.data);
      
      setLoading(false);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to process document. Please try again.');
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.header}>1. Document Scan</h2>
      
      <div style={styles.content}>
        <input
          type="file"
          accept=".pdf,.jpg,.jpeg,.png"
          onChange={handleFileChange}
          disabled={loading}
          style={styles.fileInput}
        />
        
        {file && (
          <p style={styles.fileName}>
            Selected: <strong>{file.name}</strong>
          </p>
        )}
        
        <button
          onClick={handleUpload}
          disabled={!file || loading}
          style={{
            ...styles.button,
            ...((!file || loading) && styles.buttonDisabled)
          }}
        >
          {loading ? 'Scanning...' : 'Scan Document'}
        </button>
        
        {loading && (
          <p style={styles.loadingText}>
            🔍 AI is extracting data from your document...
          </p>
        )}
        
        {error && (
          <p style={styles.errorText}>
            ⚠️ {error}
          </p>
        )}
      </div>
    </div>
  );
};

const styles = {
  container: {
    border: '1px solid #e0e0e0',
    borderRadius: '8px',
    padding: '24px',
    backgroundColor: '#ffffff',
    boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
    marginBottom: '24px'
  },
  header: {
    margin: '0 0 20px 0',
    fontSize: '24px',
    fontWeight: '600',
    color: '#333333'
  },
  content: {
    display: 'flex',
    flexDirection: 'column',
    gap: '16px'
  },
  fileInput: {
    padding: '10px',
    fontSize: '14px',
    border: '1px solid #d0d0d0',
    borderRadius: '4px',
    cursor: 'pointer'
  },
  fileName: {
    margin: '0',
    fontSize: '14px',
    color: '#555555'
  },
  button: {
    padding: '12px 24px',
    fontSize: '16px',
    fontWeight: '600',
    color: '#ffffff',
    backgroundColor: '#007bff',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
    transition: 'background-color 0.3s ease'
  },
  buttonDisabled: {
    backgroundColor: '#cccccc',
    cursor: 'not-allowed'
  },
  loadingText: {
    margin: '0',
    fontSize: '14px',
    color: '#007bff',
    fontWeight: '500',
    textAlign: 'center'
  },
  errorText: {
    margin: '0',
    fontSize: '14px',
    color: '#dc3545',
    fontWeight: '500',
    textAlign: 'center',
    backgroundColor: '#fff5f5',
    padding: '12px',
    borderRadius: '4px',
    border: '1px solid #ffcccc'
  }
};

export default FileUpload;