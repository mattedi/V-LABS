// src/contexts/AuthContext.tsx - VERSÃO SIMPLIFICADA
// Implementa um sistema completo de autenticação em React
// utilizando Context API para gerenciamento de estado global, 
// com simulação de login/registro, controle de acesso
// a rotas protegidas e formulário de login.
// Este código é uma versão simplificada e otimizada,
// mantendo as funcionalidades essenciais de autenticação


import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';

// Tipos locais (sem import externo)
interface User {
  id: string;
  username: string;
  email: string;
  role: 'student' | 'teacher' | 'admin';
  createdAt: string;
}

interface LoginCredentials {
  email: string;
  password: string;
}

interface RegisterData {
  username: string;
  email: string;
  password: string;
  confirmPassword: string;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (credentials: LoginCredentials) => Promise<void>;
  register: (userData: RegisterData) => Promise<void>;
  logout: () => Promise<void>;
  updateUser: (userData: Partial<User>) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Inicializar estado do usuário
  useEffect(() => {
    initializeAuth();
  }, []);

  const initializeAuth = (): void => {
    try {
      // Verificar se há usuário salvo no localStorage
      const savedUser = localStorage.getItem('vlabs_user');
      const savedToken = localStorage.getItem('vlabs_token');
      
      if (savedUser && savedToken) {
        setUser(JSON.parse(savedUser));
      }
    } catch (error) {
      console.error('Erro ao inicializar autenticação:', error);
      // Limpar dados corrompidos
      localStorage.removeItem('vlabs_user');
      localStorage.removeItem('vlabs_token');
    } finally {
      setIsLoading(false);
    }
  };

  const login = async (credentials: LoginCredentials): Promise<void> => {
    setIsLoading(true);
    try {
      // SIMULAÇÃO de login - substitua por chamada real à API
      await new Promise(resolve => setTimeout(resolve, 1000)); // Simular delay

      // Validação básica
      if (credentials.email === 'demo@vlabs.com' && credentials.password === '123456') {
        const mockUser: User = {
          id: 'user-123',
          username: 'Demo User',
          email: credentials.email,
          role: 'student',
          createdAt: new Date().toISOString(),
        };

        const mockToken = 'mock-jwt-token-' + Date.now();

        // Salvar no localStorage
        localStorage.setItem('vlabs_user', JSON.stringify(mockUser));
        localStorage.setItem('vlabs_token', mockToken);
        
        setUser(mockUser);
      } else {
        throw new Error('Credenciais inválidas');
      }
    } catch (error) {
      console.error('Erro no login:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (userData: RegisterData): Promise<void> => {
    setIsLoading(true);
    try {
      // SIMULAÇÃO de registro - substitua por chamada real à API
      await new Promise(resolve => setTimeout(resolve, 1000));

      // Validação básica
      if (userData.password !== userData.confirmPassword) {
        throw new Error('Senhas não coincidem');
      }

      if (userData.password.length < 6) {
        throw new Error('Senha deve ter pelo menos 6 caracteres');
      }

      const mockUser: User = {
        id: 'user-' + Date.now(),
        username: userData.username,
        email: userData.email,
        role: 'student',
        createdAt: new Date().toISOString(),
      };

      const mockToken = 'mock-jwt-token-' + Date.now();

      // Salvar no localStorage
      localStorage.setItem('vlabs_user', JSON.stringify(mockUser));
      localStorage.setItem('vlabs_token', mockToken);
      
      setUser(mockUser);
    } catch (error) {
      console.error('Erro no registro:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = async (): Promise<void> => {
    setIsLoading(true);
    try {
      // Limpar dados locais
      localStorage.removeItem('vlabs_user');
      localStorage.removeItem('vlabs_token');
      localStorage.removeItem('vlabs_refresh_token');
      
      setUser(null);
    } catch (error) {
      console.error('Erro no logout:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const updateUser = (userData: Partial<User>): void => {
    if (user) {
      const updatedUser = { ...user, ...userData };
      setUser(updatedUser);
      localStorage.setItem('vlabs_user', JSON.stringify(updatedUser));
    }
  };

  const value: AuthContextType = {
    user,
    isAuthenticated: !!user,
    isLoading,
    login,
    register,
    logout,
    updateUser,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth deve ser usado dentro de um AuthProvider');
  }
  return context;
};

// Componente ProtectedRoute simplificado
interface ProtectedRouteProps {
  children: React.ReactNode;
  requiredRole?: 'student' | 'teacher' | 'admin';
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ 
  children, 
  requiredRole 
}) => {
  const { isAuthenticated, user, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">Acesso Restrito</h2>
          <p className="text-gray-600 mb-4">
            Você precisa fazer login para acessar esta página.
          </p>
          <button 
            onClick={() => window.location.href = '/login'}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            Fazer Login
          </button>
        </div>
      </div>
    );
  }

  if (requiredRole && user?.role !== requiredRole) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-red-600 mb-4">Acesso Negado</h2>
          <p className="text-gray-600">
            Você não tem permissão para acessar esta página.
          </p>
        </div>
      </div>
    );
  }

  return <>{children}</>;
};

// Componente LoginForm simplificado
export const LoginForm: React.FC = () => {
  const [credentials, setCredentials] = useState<LoginCredentials>({
    email: '',
    password: '',
  });
  const [error, setError] = useState<string>('');
  const { login, isLoading } = useAuth();

  const handleSubmit = async (e: React.FormEvent): Promise<void> => {
    e.preventDefault();
    setError('');

    try {
      await login(credentials);
      // Redirecionar após login bem-sucedido
      window.location.href = '/dashboard';
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Erro ao fazer login');
    }
  };

  return (
    <div className="max-w-md mx-auto mt-8 p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold text-center mb-6">Login</h2>
      
      {error && (
        <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Email
          </label>
          <input
            type="email"
            value={credentials.email}
            onChange={(e) => setCredentials(prev => ({ ...prev, email: e.target.value }))}
            required
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="demo@vlabs.com"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Senha
          </label>
          <input
            type="password"
            value={credentials.password}
            onChange={(e) => setCredentials(prev => ({ ...prev, password: e.target.value }))}
            required
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="123456"
          />
        </div>

        <button
          type="submit"
          disabled={isLoading}
          className="w-full py-2 px-4 bg-blue-600 text-white font-semibold rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
        >
          {isLoading ? 'Entrando...' : 'Entrar'}
        </button>
      </form>

      <div className="mt-4 text-center text-sm text-gray-600">
        <p>Credenciais de teste:</p>
        <p>Email: demo@vlabs.com</p>
        <p>Senha: 123456</p>
      </div>
    </div>
  );
};

// EXTENSÕES
// - Implementar suporte a autenticação via OAuth (Google, Facebook, etc.).
// - Adicionar recuperação de senha e verificação de email.
// - Implementar um sistema de roles e permissões mais complexo.
// - Adicionar suporte a autenticação de dois fatores (2FA).
// - Implementar um sistema de refresh token para manter a sessão ativa.
// - Adicionar suporte a logout automático após inatividade.
// - Implementar um sistema de notificações para eventos de autenticação (login, logout, etc.).
