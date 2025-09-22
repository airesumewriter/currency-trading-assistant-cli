import axios from 'axios';

const API_BASE = 'http://localhost:8001';

export const api = {
  // Price endpoints
  getPrice: (instrument) => axios.get(`${API_BASE}/api/prices/${instrument}`),
  getMultiplePrices: (instruments) => axios.get(`${API_BASE}/api/prices?instruments=${instruments}`),
  getHistory: (instrument, days) => axios.get(`${API_BASE}/api/history/${instrument}/${days}`),
  
  // Trading endpoints
  placeOrder: (orderData) => axios.post(`${API_BASE}/api/orders`, orderData),
  closeOrder: (orderId) => axios.post(`${API_BASE}/api/orders/${orderId}/close`),
  
  // AI endpoints
  analyze: (message, instrument) => axios.post(`${API_BASE}/api/ai/analyze`, { message, instrument }),
  getSignals: () => axios.get(`${API_BASE}/api/signals`),
  
  // System endpoints
  health: () => axios.get(`${API_BASE}/api/health`)
};
