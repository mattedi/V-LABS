import React, { useEffect, useState } from 'react';
import axios from 'axios';

const UsuariosPage: React.FC = () => {
  const [usuarios, setUsuarios] = useState<string[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchUsuarios = async () => {
      try {
        setLoading(true);
        const response = await axios.get("http://127.0.0.1:8000/usuarios/");
        setUsuarios(response.data);
        setError(null);
      } catch (err) {
        console.error("Erro ao buscar usuários:", err);
        setError("Falha ao carregar usuários");
      } finally {
        setLoading(false);
      }
    };

    fetchUsuarios();
  }, []);

  if (loading) {
    return (
      <div className="p-6 bg-white dark:bg-gray-800 rounded shadow">
        <div className="animate-pulse">
          <div className="h-6 bg-gray-300 dark:bg-gray-600 rounded mb-4 w-48"></div>
          <div className="space-y-2">
            {[...Array(3)].map((_, index) => (
              <div key={index} className="h-4 bg-gray-300 dark:bg-gray-600 rounded w-full"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 bg-white dark:bg-gray-800 rounded shadow">
        <div className="text-red-600 dark:text-red-400">
          <h2 className="text-xl font-bold mb-2">Erro</h2>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 bg-white dark:bg-gray-800 rounded shadow">
      <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
        Lista de Usuários
      </h2>
      
      {usuarios.length > 0 ? (
        <ul className="list-disc pl-6 text-gray-800 dark:text-gray-100 space-y-1">
          {usuarios.map((usuario, index) => (
            <li key={usuario || `usuario-${index}`} className="leading-relaxed">
              {usuario}
            </li>
          ))}
        </ul>
      ) : (
        <div className="text-gray-500 dark:text-gray-400 italic text-center py-8">
          Nenhum usuário encontrado
        </div>
      )}
    </div>
  );
};

export default UsuariosPage;
