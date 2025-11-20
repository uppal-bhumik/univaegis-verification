import { useState } from 'react';
import { checkEligibility } from '../api';

const ResultsCard = ({ data }) => {
  const [ieltsScore, setIeltsScore] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleCheck = async () => {
    if (!ieltsScore) return;

    setLoading(true);

    try {
      const response = await checkEligibility(data.extracted_gpa, parseFloat(ieltsScore));
      setResult(response.data);
      setLoading(false);
    } catch (err) {
      console.error('Eligibility check failed:', err);
      setLoading(false);
    }
  };

  // Determine confidence color with better thresholds
  const getConfidenceColor = (score) => {
    if (score >= 0.7) return '#28a745'; // Green - High confidence
    if (score >= 0.5) return '#ffc107'; // Yellow - Medium confidence
    return '#fd7e14'; // Orange - Low confidence
  };

  const confidenceColor = getConfidenceColor(data.confidence_score);

  return (
    <div style={styles.container}>
      <h2 style={styles.header}>2. Results & Eligibility</h2>

      {/* Section A: Extracted Details */}
      <div style={styles.section}>
        <h3 style={styles.sectionTitle}>Extracted Details</h3>
        <div style={styles.detailsGrid}>
          <div style={styles.detailItem}>
            <span style={styles.label}>Student Name:</span>
            <span style={styles.value}>
              {data.extracted_name || <span style={styles.notFound}>Not Found</span>}
            </span>
          </div>
          
          <div style={styles.detailItem}>
            <span style={styles.label}>Extracted GPA:</span>
            <span style={styles.value}>
              {data.extracted_gpa || <span style={styles.notFound}>Not Found</span>}
            </span>
          </div>

          {/* Only show Financial Balance if it exists */}
          {data.extracted_balance && (
            <div style={styles.detailItem}>
              <span style={styles.label}>Financial Balance:</span>
              <span style={styles.value}>
                Rs. {data.extracted_balance}
              </span>
            </div>
          )}

          <div style={styles.detailItem}>
            <span style={styles.label}>AI Confidence:</span>
            <span style={{...styles.value, color: confidenceColor, fontWeight: '600'}}>
              {(data.confidence_score * 100).toFixed(0)}%
            </span>
          </div>
        </div>

        {/* Show warning if confidence is low */}
        {data.confidence_score < 0.5 && (
          <div style={styles.warningBox}>
            ⚠️ Low confidence detected. Please verify extracted information manually.
          </div>
        )}
      </div>

      {/* Section B: Manual Verification */}
      <div style={styles.section}>
        <h3 style={styles.sectionTitle}>Manual Verification</h3>
        <div style={styles.inputGroup}>
          <label style={styles.inputLabel}>IELTS Score:</label>
          <input
            type="number"
            min="0"
            max="9"
            step="0.5"
            value={ieltsScore}
            onChange={(e) => setIeltsScore(e.target.value)}
            placeholder="Enter IELTS score (0-9)"
            disabled={loading}
            style={styles.input}
          />
          <button
            onClick={handleCheck}
            disabled={!ieltsScore || loading}
            style={{
              ...styles.button,
              ...((!ieltsScore || loading) && styles.buttonDisabled)
            }}
          >
            {loading ? 'Checking...' : 'Check Eligibility'}
          </button>
        </div>
      </div>

      {/* Section C: Verdict */}
      {result && (
        <div style={styles.section}>
          <h3 style={styles.sectionTitle}>Verdict</h3>
          <div style={styles.verdictContainer}>
            <div
              style={{
                ...styles.badge,
                backgroundColor: result.eligible ? '#28a745' : '#dc3545'
              }}
            >
              {result.eligible ? '✓ ELIGIBLE' : '✗ NOT ELIGIBLE'}
            </div>
            
            <div style={styles.reasonsContainer}>
              <h4 style={styles.reasonsTitle}>Details:</h4>
              <ul style={styles.reasonsList}>
                {result.reasons.map((reason, index) => (
                  <li key={index} style={styles.reasonItem}>
                    {reason}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

const styles = {
  container: {
    border: '1px solid #e0e0e0',
    borderRadius: '8px',
    padding: '24px',
    backgroundColor: '#ffffff',
    boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)'
  },
  header: {
    margin: '0 0 24px 0',
    fontSize: '24px',
    fontWeight: '600',
    color: '#333333'
  },
  section: {
    marginBottom: '24px',
    paddingBottom: '24px',
    borderBottom: '1px solid #f0f0f0'
  },
  sectionTitle: {
    margin: '0 0 16px 0',
    fontSize: '18px',
    fontWeight: '600',
    color: '#555555'
  },
  detailsGrid: {
    display: 'flex',
    flexDirection: 'column',
    gap: '12px'
  },
  detailItem: {
    display: 'flex',
    justifyContent: 'space-between',
    padding: '12px',
    backgroundColor: '#f8f9fa',
    borderRadius: '4px'
  },
  label: {
    fontSize: '14px',
    fontWeight: '500',
    color: '#666666'
  },
  value: {
    fontSize: '14px',
    fontWeight: '500',
    color: '#333333'
  },
  notFound: {
    color: '#dc3545',
    fontStyle: 'italic'
  },
  warningBox: {
    marginTop: '16px',
    padding: '12px 16px',
    backgroundColor: '#fff3cd',
    border: '1px solid #ffc107',
    borderRadius: '6px',
    color: '#856404',
    fontSize: '14px',
    fontWeight: '500'
  },
  inputGroup: {
    display: 'flex',
    flexDirection: 'column',
    gap: '12px'
  },
  inputLabel: {
    fontSize: '14px',
    fontWeight: '500',
    color: '#555555'
  },
  input: {
    padding: '12px',
    fontSize: '14px',
    border: '1px solid #d0d0d0',
    borderRadius: '4px',
    outline: 'none'
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
  verdictContainer: {
    display: 'flex',
    flexDirection: 'column',
    gap: '20px'
  },
  badge: {
    padding: '20px',
    fontSize: '24px',
    fontWeight: '700',
    color: '#ffffff',
    textAlign: 'center',
    borderRadius: '8px',
    textTransform: 'uppercase',
    letterSpacing: '1px'
  },
  reasonsContainer: {
    backgroundColor: '#f8f9fa',
    padding: '16px',
    borderRadius: '6px'
  },
  reasonsTitle: {
    margin: '0 0 12px 0',
    fontSize: '16px',
    fontWeight: '600',
    color: '#555555'
  },
  reasonsList: {
    margin: '0',
    paddingLeft: '24px',
    listStyleType: 'disc'
  },
  reasonItem: {
    fontSize: '14px',
    color: '#666666',
    marginBottom: '8px',
    lineHeight: '1.6'
  }
};

export default ResultsCard;