import React, { createContext, useContext, useState, ReactNode } from 'react';

interface AuthContextType {
  isSubscribed: boolean;
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  upgrade: (plan: string) => Promise<void>;
}

interface User {
  id: string;
  email: string;
  name: string;
  subscription: {
    plan: string;
    status: 'active' | 'trial' | 'expired';
    expiresAt: string;
  };
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isSubscribed, setIsSubscribed] = useState(false);

  const login = async (email: string, password: string) => {
    // Simulate login - in real app, this would call your backend
    const mockUser: User = {
      id: '1',
      email,
      name: 'Demo User',
      subscription: {
        plan: 'none',
        status: 'expired',
        expiresAt: new Date().toISOString()
      }
    };
    
    setUser(mockUser);
    setIsSubscribed(false);
  };

  const logout = () => {
    setUser(null);
    setIsSubscribed(false);
  };

  const upgrade = async (plan: string) => {
    // Simulate upgrade - in real app, this would call your payment processor
    if (user) {
      const updatedUser: User = {
        ...user,
        subscription: {
          plan,
          status: 'active',
          expiresAt: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString() // 30 days
        }
      };
      
      setUser(updatedUser);
      setIsSubscribed(true);
    }
  };

  const value: AuthContextType = {
    isSubscribed,
    user,
    login,
    logout,
    upgrade
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
