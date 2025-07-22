// src/contexts/AuthContext.tsx - VERSÃO SIMPLIFICADA
// Implementa um sistema completo de autenticação em React
// utilizando Context API para gerenciamento de estado global, 
// com simulação de login/registro, controle de acesso
// a rotas protegidas e formulário de login.
// Este código é uma versão simplificada e otimizada,
// mantendo as funcionalidades essenciais de autenticação


// src/context/AuthContext.tsx
import React, {
  createContext,
  useContext,
  useEffect,
  useState,
  ReactNode,
} from 'react';

// Tipos locais
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
  register: (data: RegisterData) => Promise<void>;
  logout: () => Promise<void>;
  updateUser: (data: Partial<User>) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    try {
      const savedUser = localStorage.getItem('vlabs_user');
      const savedToken = localStorage.getItem('vlabs_token');

      if (savedUser && savedToken) {
        setUser(JSON.parse(savedUser));
      }
    } catch (error) {
      console.error('[Auth] Erro ao recuperar usuário do localStorage:', error);
      clearAuthData();
    } finally {
      setIsLoading(false);
    }
  }, []);

  const storeAuthData = (user: User, token: string) => {
    setUser(user);
    localStorage.setItem('vlabs_user', JSON.stringify(user));
    localStorage.setItem('vlabs_token', token);
  };

  const clearAuthData = () => {
    setUser(null);
    localStorage.removeItem('vlabs_user');
    localStorage.removeItem('vlabs_token');
    localStorage.removeItem('vlabs_refresh_token');
  };

  const simulateAuthResponse = async (userData: Partial<User>): Promise<User> => {
    await new Promise((res) => setTimeout(res, 1000)); // simular delay
    return {
      id: userData.id ?? 'user-' + Date.now(),
      username: userData.username ?? 'Demo User',
      email: userData.email ?? 'demo@vlabs.com',
      role: userData.role ?? 'student',
      createdAt: new Date().toISOString(),
    };
  };

  const login = async ({ email, password }: LoginCredentials): Promise<void> => {
    setIsLoading(true);
    try {
      if (email === 'demo@vlabs.com' && password === '123456') {
        const user = await simulateAuthResponse({ email });
        const token = 'mock-jwt-token-' + Date.now();
        storeAuthData(user, token);
      } else {
        throw new Error('Credenciais inválidas');
      }
    } catch (err) {
      console.error('[Auth] Erro no login:', err);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const register = async ({
    username,
    email,
    password,
    confirmPassword,
  }: RegisterData): Promise<void> => {
    setIsLoading(true);
    try {
      if (password !== confirmPassword) {
        throw new Error('Senhas não coincidem');
      }
      if (password.length < 6) {
        throw new Error('Senha deve ter pelo menos 6 caracteres');
      }

      const user = await simulateAuthResponse({ username, email });
      const token = 'mock-jwt-token-' + Date.now();
      storeAuthData(user, token);
    } catch (err) {
      console.error('[Auth] Erro no registro:', err);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = async (): Promise<void> => {
    setIsLoading(true);
    try {
      await new Promise((res) => setTimeout(res, 300));
      clearAuthData();
    } catch (err) {
      console.error('[Auth] Erro no logout:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const updateUser = (data: Partial<User>) => {
    if (user) {
      const updatedUser = { ...user, ...data };
      setUser(updatedUser);
      localStorage.setItem('vlabs_user', JSON.stringify(updatedUser));
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        isLoading,
        login,
        register,
        logout,
        updateUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth deve ser usado dentro de um <AuthProvider>');
  }
  return context;
};


// EXTENSÕES
// - Implementar suporte a autenticação via OAuth (Google, Facebook, etc.).
// - Adicionar recuperação de senha e verificação de email.
// - Implementar um sistema de roles e permissões mais complexo.
// - Adicionar suporte a autenticação de dois fatores (2FA).
// - Implementar um sistema de refresh token para manter a sessão ativa.
// - Adicionar suporte a logout automático após inatividade.
// - Implementar um sistema de notificações para eventos de autenticação (login, logout, etc.).
