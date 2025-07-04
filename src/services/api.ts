// src/services/api.ts - VERSÃO SIMPLIFICADA
import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';

// Tipos e configurações locais (elimina imports externos)
interface ApiError {
  message: string;
  code: string;
  statusCode: number;
}

interface User {
  id: string;
  username: string;
  email: string;
  role: 'student' | 'teacher' | 'admin';
  createdAt: string;
}

interface AuthResponse {
  token: string;
  user: User;
  expiresIn: number;
}

// Configuração da API local
const API_CONFIG = {
  BASE_URL: 'http://localhost:3001',
  TIMEOUT: 10000,
  RETRY_ATTEMPTS: 3,
};

// Endpoints da API
const API_ENDPOINTS = {
  AUTH: {
    LOGIN: '/api/auth/login',
    REGISTER: '/api/auth/register',
    REFRESH: '/api/auth/refresh',
    LOGOUT: '/api/auth/logout',
  },
  PROGRESS: {
    GET: (userId: string) => `/api/progress/${userId}`,
    UPDATE: (userId: string, mode: string) => `/api/progress/${userId}/${mode}`,
  },
  AI: {
    ANALYZE: '/api/ai/analyze',
  },
};

class ApiService {
  private api: AxiosInstance;
  private refreshTokenPromise: Promise<string> | null = null;

  constructor() {
    this.api = axios.create({
      baseURL: API_CONFIG.BASE_URL,
      timeout: API_CONFIG.TIMEOUT,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.setupInterceptors();
  }

  private setupInterceptors(): void {
    // Request interceptor para adicionar token
    this.api.interceptors.request.use(
      (config) => {
        const token = this.getStoredToken();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor para tratar erros e refresh token
    this.api.interceptors.response.use(
      (response: AxiosResponse) => response,
      async (error) => {
        const originalRequest = error.config;

        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;

          try {
            const newToken = await this.refreshToken();
            originalRequest.headers.Authorization = `Bearer ${newToken}`;
            return this.api(originalRequest);
          } catch (refreshError) {
            this.handleAuthError();
            return Promise.reject(refreshError);
          }
        }

        return Promise.reject(this.handleApiError(error));
      }
    );
  }

  private getStoredToken(): string | null {
    // CORREÇÃO: Usar chaves fixas em vez de import.meta.env
    return localStorage.getItem('vlabs_token');
  }

  private async refreshToken(): Promise<string> {
    if (this.refreshTokenPromise) {
      return this.refreshTokenPromise;
    }

    this.refreshTokenPromise = this.performRefreshToken();
    
    try {
      const token = await this.refreshTokenPromise;
      return token;
    } finally {
      this.refreshTokenPromise = null;
    }
  }

  private async performRefreshToken(): Promise<string> {
    // CORREÇÃO: Usar chave fixa
    const refreshToken = localStorage.getItem('vlabs_refresh_token');

    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    const response = await axios.post(`${API_CONFIG.BASE_URL}/api/auth/refresh`, {
      refreshToken,
    });

    const { token } = response.data;
    // CORREÇÃO: Usar chave fixa
    localStorage.setItem('vlabs_token', token);
    
    return token;
  }

  private handleAuthError(): void {
    // CORREÇÃO: Usar chaves fixas
    localStorage.removeItem('vlabs_token');
    localStorage.removeItem('vlabs_refresh_token');
    localStorage.removeItem('vlabs_user');
    window.location.href = '/login';
  }

  private handleApiError(error: any): ApiError {
    const apiError: ApiError = {
      message: error.response?.data?.message || error.message || 'Erro desconhecido',
      code: error.response?.data?.code || 'UNKNOWN_ERROR',
      statusCode: error.response?.status || 500,
    };

    console.error('API Error:', apiError);
    return apiError;
  }

  // Métodos HTTP públicos
  public async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.api.get<T>(url, config);
    return response.data;
  }

  public async post<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.api.post<T>(url, data, config);
    return response.data;
  }

  public async put<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.api.put<T>(url, data, config);
    return response.data;
  }

  public async patch<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.api.patch<T>(url, data, config);
    return response.data;
  }

  public async delete<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.api.delete<T>(url, config);
    return response.data;
  }

  // Método para fazer upload de arquivos
  public async uploadFile<T>(url: string, file: File, onProgress?: (progress: number) => void): Promise<T> {
    const formData = new FormData();
    formData.append('file', file);

    const config: AxiosRequestConfig = {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        if (onProgress && progressEvent.total) {
          const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          onProgress(progress);
        }
      },
    };

    const response = await this.api.post<T>(url, formData, config);
    return response.data;
  }

  // Método para simular delay (útil para desenvolvimento)
  public async delay(ms: number = 1000): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

export const apiService = new ApiService();

// src/services/auth.ts - VERSÃO SIMPLIFICADA
export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData extends LoginCredentials {
  username: string;
  confirmPassword: string;
}

class AuthService {
  public async login(credentials: LoginCredentials): Promise<AuthResponse> {
    try {
      // Simulação de login (substitua por chamada real)
      await apiService.delay(1000);

      // Validação de credenciais mock
      if (credentials.email === 'demo@vlabs.com' && credentials.password === '123456') {
        const mockResponse: AuthResponse = {
          token: 'mock-jwt-token-' + Date.now(),
          user: {
            id: 'user-123',
            username: 'Demo User',
            email: credentials.email,
            role: 'student',
            createdAt: new Date().toISOString(),
          },
          expiresIn: 3600
        };

        this.storeAuthData(mockResponse);
        return mockResponse;
      } else {
        throw new Error('Credenciais inválidas');
      }
    } catch (error) {
      console.error('Erro no login:', error);
      throw error;
    }
  }

  public async register(userData: RegisterData): Promise<AuthResponse> {
    try {
      // Simulação de registro
      await apiService.delay(1000);

      if (userData.password !== userData.confirmPassword) {
        throw new Error('Senhas não coincidem');
      }

      if (userData.password.length < 6) {
        throw new Error('Senha deve ter pelo menos 6 caracteres');
      }

      const mockResponse: AuthResponse = {
        token: 'mock-jwt-token-' + Date.now(),
        user: {
          id: 'user-' + Date.now(),
          username: userData.username,
          email: userData.email,
          role: 'student',
          createdAt: new Date().toISOString(),
        },
        expiresIn: 3600
      };

      this.storeAuthData(mockResponse);
      return mockResponse;
    } catch (error) {
      console.error('Erro no registro:', error);
      throw error;
    }
  }

  public async logout(): Promise<void> {
    try {
      // Em uma implementação real, chamaria a API
      // await apiService.post(API_ENDPOINTS.AUTH.LOGOUT);
      await apiService.delay(500);
    } catch (error) {
      console.error('Erro ao fazer logout:', error);
    } finally {
      this.clearAuthData();
    }
  }

  public getCurrentUser(): User | null {
    try {
      const userData = localStorage.getItem('vlabs_user');
      return userData ? JSON.parse(userData) : null;
    } catch (error) {
      console.error('Erro ao obter usuário atual:', error);
      return null;
    }
  }

  public isAuthenticated(): boolean {
    const token = localStorage.getItem('vlabs_token');
    return !!token;
  }

  private storeAuthData(authResponse: AuthResponse): void {
    // CORREÇÃO: Usar chaves fixas
    localStorage.setItem('vlabs_token', authResponse.token);
    localStorage.setItem('vlabs_user', JSON.stringify(authResponse.user));
  }

  private clearAuthData(): void {
    // CORREÇÃO: Usar chaves fixas
    localStorage.removeItem('vlabs_token');
    localStorage.removeItem('vlabs_refresh_token');
    localStorage.removeItem('vlabs_user');
  }
}

export const authService = new AuthService();

// src/services/progress.ts - SERVIÇO DE PROGRESSO
interface ProgressItem {
  completed: number;
  totalAttempts: number;
  masteryLevel: 'iniciante' | 'intermediário' | 'avançado';
}

interface UserProgress {
  equation: ProgressItem;
  voice: ProgressItem;
  image: ProgressItem;
  text: ProgressItem;
}

class ProgressService {
  public async getProgress(userId: string): Promise<UserProgress> {
    try {
      // Simulação de busca de progresso
      await apiService.delay(500);
      
      // Buscar dados do localStorage ou retornar padrão
      const savedProgress = localStorage.getItem(`progress_${userId}`);
      if (savedProgress) {
        return JSON.parse(savedProgress);
      }

      const defaultProgress: UserProgress = {
        equation: { completed: 0, totalAttempts: 0, masteryLevel: 'iniciante' },
        voice: { completed: 0, totalAttempts: 0, masteryLevel: 'iniciante' },
        image: { completed: 0, totalAttempts: 0, masteryLevel: 'iniciante' },
        text: { completed: 0, totalAttempts: 0, masteryLevel: 'iniciante' }
      };

      return defaultProgress;
    } catch (error) {
      console.error('Erro ao buscar progresso:', error);
      throw error;
    }
  }

  public async updateProgress(
    userId: string,
    mode: keyof UserProgress,
    result: { success: boolean; score?: number }
  ): Promise<{ success: boolean; message: string }> {
    try {
      await apiService.delay(300);

      const currentProgress = await this.getProgress(userId);
      const modeProgress = currentProgress[mode];

      // Atualizar progresso
      const updatedProgress: UserProgress = {
        ...currentProgress,
        [mode]: {
          completed: result.success ? modeProgress.completed + 1 : modeProgress.completed,
          totalAttempts: modeProgress.totalAttempts + 1,
          masteryLevel: this.calculateMasteryLevel(
            result.success ? modeProgress.completed + 1 : modeProgress.completed,
            modeProgress.totalAttempts + 1
          )
        }
      };

      // Salvar no localStorage
      localStorage.setItem(`progress_${userId}`, JSON.stringify(updatedProgress));

      return { success: true, message: 'Progresso atualizado com sucesso' };
    } catch (error) {
      console.error('Erro ao atualizar progresso:', error);
      throw error;
    }
  }

  private calculateMasteryLevel(completed: number, attempts: number): 'iniciante' | 'intermediário' | 'avançado' {
    if (attempts === 0) return 'iniciante';
    
    const ratio = completed / attempts;
    if (ratio >= 0.8) return 'avançado';
    if (ratio >= 0.6) return 'intermediário';
    return 'iniciante';
  }
}

export const progressService = new ProgressService();