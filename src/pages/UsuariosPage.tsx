// src/pages/UsuariosPage.tsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const UsuariosPage: React.FC = () => {
  const [usuarios, setUsuarios] = useState<string[]>([]);

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/usuarios/")
      .then(response => setUsuarios(response.data))
      .catch(error => console.error("Erro ao buscar usuários:", error));
  }, []);

  return (
    <div className="p-6 bg-white dark:bg-gray-800 rounded shadow">
      <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Lista de Usuários</h2>
      <ul className="list-disc pl-6 text-gray-800 dark:text-gray-100">
        {usuarios.map((usuario, index) => (
          <li key={index}>{usuario}</li>
        ))}
      </ul>
    </div>
  );
};

export default UsuariosPage;
