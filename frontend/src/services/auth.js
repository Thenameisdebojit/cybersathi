import api from './api';

const AUTH_STORAGE_KEY = 'cybersathi_auth';

class AuthService {
  constructor() {
    this.user = this.getStoredUser();
    this.token = this.getStoredToken();
  }

  getStoredUser() {
    const stored = localStorage.getItem(AUTH_STORAGE_KEY);
    return stored ? JSON.parse(stored).user : null;
  }

  getStoredToken() {
    const stored = localStorage.getItem(AUTH_STORAGE_KEY);
    return stored ? JSON.parse(stored).access_token : null;
  }

  saveAuth(data) {
    localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(data));
    this.user = data.user;
    this.token = data.access_token;
    
    api.defaults.headers.common['Authorization'] = `Bearer ${data.access_token}`;
  }

  clearAuth() {
    localStorage.removeItem(AUTH_STORAGE_KEY);
    this.user = null;
    this.token = null;
    delete api.defaults.headers.common['Authorization'];
  }

  async register(userData) {
    const response = await api.post('/api/v1/auth/register', userData);
    return response.data;
  }

  async login(email, password) {
    const response = await api.post('/api/v1/auth/login', { email, password });
    this.saveAuth(response.data);
    return response.data;
  }

  async getGoogleAuthUrl() {
    return await api.get('/api/v1/auth/google/login');
  }

  async googleCallback(code) {
    const response = await api.post(`/api/v1/auth/google/callback?code=${code}`);
    this.saveAuth(response.data);
    return response.data;
  }

  logout() {
    this.clearAuth();
  }

  isAuthenticated() {
    return !!this.token;
  }

  getUser() {
    return this.user;
  }

  getToken() {
    return this.token;
  }

  async getCurrentUser() {
    try {
      const response = await api.get('/api/v1/auth/me');
      this.user = response.data;
      return response.data;
    } catch (error) {
      this.clearAuth();
      throw error;
    }
  }

  async updateProfile(updates) {
    const response = await api.put('/api/v1/auth/me', updates);
    this.user = response.data;
    
    const stored = JSON.parse(localStorage.getItem(AUTH_STORAGE_KEY));
    stored.user = response.data;
    localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(stored));
    
    return response.data;
  }

  async changePassword(currentPassword, newPassword) {
    const response = await api.post('/api/v1/auth/change-password', {
      current_password: currentPassword,
      new_password: newPassword,
    });
    return response.data;
  }
}

export const authService = new AuthService();

if (authService.token) {
  api.defaults.headers.common['Authorization'] = `Bearer ${authService.token}`;
}
