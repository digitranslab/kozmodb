import { useState, useEffect } from 'react';
import { Provider } from '@/constants/messages';

interface UseAuthReturn {
  kozmodbApiKey: string;
  openaiApiKey: string;
  provider: Provider;
  user: string;
  setAuth: (kozmodb: string, openai: string, provider: Provider) => void;
  setUser: (user: string) => void;
  clearAuth: () => void;
  clearUser: () => void;
}

export const useAuth = (): UseAuthReturn => {
  const [kozmodbApiKey, setKozmodbApiKey] = useState<string>('');
  const [openaiApiKey, setOpenaiApiKey] = useState<string>('');
  const [provider, setProvider] = useState<Provider>('openai');
  const [user, setUser] = useState<string>('');

  useEffect(() => {
    const kozmodb = localStorage.getItem('kozmodbApiKey');
    const openai = localStorage.getItem('openaiApiKey');
    const savedProvider = localStorage.getItem('provider') as Provider;
    const savedUser = localStorage.getItem('user');

    if (kozmodb && openai && savedProvider) {
      setAuth(kozmodb, openai, savedProvider);
    }
    if (savedUser) {
      setUser(savedUser);
    }
  }, []);

  const setAuth = (kozmodb: string, openai: string, provider: Provider) => {
    setKozmodbApiKey(kozmodb);
    setOpenaiApiKey(openai);
    setProvider(provider);
    localStorage.setItem('kozmodbApiKey', kozmodb);
    localStorage.setItem('openaiApiKey', openai);
    localStorage.setItem('provider', provider);
  };

  const clearAuth = () => {
    localStorage.removeItem('kozmodbApiKey');
    localStorage.removeItem('openaiApiKey');
    localStorage.removeItem('provider');
    setKozmodbApiKey('');
    setOpenaiApiKey('');
    setProvider('openai');
  };

  const updateUser = (user: string) => {
    setUser(user);
    localStorage.setItem('user', user);
  };

  const clearUser = () => {
    localStorage.removeItem('user');
    setUser('');
  };

  return {
    kozmodbApiKey,
    openaiApiKey,
    provider,
    user,
    setAuth,
    setUser: updateUser,
    clearAuth,
    clearUser,
  };
}; 