import React from 'react';
import { LoginForm } from '../components/auth/LoginForm';

export default function LoginPage() {
  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-50 dark:bg-gray-900">
      <LoginForm />
    </div>
  );
}
