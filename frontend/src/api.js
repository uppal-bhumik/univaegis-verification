import axios from 'axios';

// Create axios instance with base configuration
// Automatically switches between Localhost and Cloud Backend
const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api/v1';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

/**
 * Upload a document (PDF or Image) for OCR processing
 * @param {File} file - File object from HTML file input
 * @returns {Promise} - Axios response promise
 */
export const uploadDocument = async (file) => {
  // Create FormData object
  const formData = new FormData();
  formData.append('file', file);

  // Send POST request with multipart/form-data
  return await api.post('/upload-document', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
};

/**
 * Check student eligibility based on GPA and IELTS score
 * @param {string|number} gpa - GPA or percentage value
 * @param {number} ielts - IELTS score
 * @returns {Promise} - Axios response promise
 */
export const checkEligibility = async (gpa, ielts) => {
  // Construct JSON body
  const requestBody = {
    extracted_gpa: gpa,
    ielts_score: ielts
  };

  // Send POST request with JSON data
  return await api.post('/check-eligibility', requestBody);
};

export default api;