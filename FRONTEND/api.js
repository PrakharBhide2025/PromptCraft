import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';  // Get base URL from .env

const api = axios.create({
  baseURL: API_URL,
});

export const get = async (url) => {
  try {
    const response = await api.get(url);
    return response.data;
  } catch (error) {
    console.error('Error fetching data', error);
    throw error;
  }
};

export const post = async (url, data) => {
  try {
    const response = await api.post(url, data);
    return response.data;
  } catch (error) {
    console.error('Error posting data', error);
    throw error;
  }
};
