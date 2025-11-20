import { useState } from 'react';
import FileUpload from './components/FileUpload';
import ResultsCard from './components/ResultsCard';

function App() {
  const [ocrData, setOcrData] = useState(null);

  const handleAnalysisComplete = (data) => {
    setOcrData(data);
  };

  const handleReset = () => {
    setOcrData(null);
  };

  return (
    <div style={styles.page}>
      <div style={styles.container}>
        {/* Header Section */}
        <div style={styles.headerContainer}>
          <h1 style={styles.title}>UnivAegis Admissions Verification</h1>
          {ocrData && (
            <button onClick={handleReset} style={styles.resetButton}>
              ↻ Reset
            </button>
          )}
        </div>

        {/* Component 1: File Upload */}
        <FileUpload onAnalysisComplete={handleAnalysisComplete} />

        {/* Component 2: Results Card (Conditional) */}
        {ocrData && <ResultsCard data={ocrData} />}
      </div>
    </div>
  );
}

const styles = {
  page: {
    minHeight: '100vh',
    backgroundColor: '#f5f5f5',
    padding: '40px 20px',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
  },
  container: {
    maxWidth: '800px',
    margin: '0 auto'
  },
  headerContainer: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '32px',
    flexWrap: 'wrap',
    gap: '16px'
  },
  title: {
    margin: '0',
    fontSize: '32px',
    fontWeight: '700',
    color: '#1a1a1a',
    letterSpacing: '-0.5px'
  },
  resetButton: {
    padding: '10px 20px',
    fontSize: '14px',
    fontWeight: '600',
    color: '#ffffff',
    backgroundColor: '#6c757d',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
    transition: 'background-color 0.3s ease',
    display: 'flex',
    alignItems: 'center',
    gap: '6px'
  }
};

export default App;