// src/components/tutoring/TutorButtons.tsx
import React from 'react';
import { FiEdit, FiMic, FiDivide, FiPieChart } from "react-icons/fi";   
import { useNavigate } from 'react-router-dom';
import { useAppContext } from '../../context/AppContext';

const TutorButtons: React.FC = () => {
  const navigate = useNavigate();
  const { currentMode } = useAppContext();

  const handleNavigation = (path: string) => {
    navigate(path);
  };

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      <button 
        onClick={() => handleNavigation('/text')}
        className="flex flex-col items-center p-4 bg-blue-100 rounded-lg hover:bg-blue-200 transition-colors text-black dark:text-black"
      >
        <FiEdit className="text-2xl mb-2 text-blue-600 dark:text-blue-600" />
        <span className="text-sm font-medium">Texto</span>
      </button>
      
      <button 
        onClick={() => handleNavigation('/voice')}
        className="flex flex-col items-center p-4 bg-green-100 rounded-lg hover:bg-green-200 transition-colors text-black dark:text-black"
      >
        <FiMic className="text-2xl mb-2 text-green-600 dark:text-green-600" />
        <span className="text-sm font-medium">Voz</span>
      </button>
      
      <button 
        onClick={() => handleNavigation('/equation')}
        className="flex flex-col items-center p-4 bg-purple-100 rounded-lg hover:bg-purple-200 transition-colors text-black dark:text-black"
      >
        <FiDivide className="text-2xl mb-2 text-purple-600 dark:text-purple-600" />
        <span className="text-sm font-medium">Equação</span>
      </button>
      
      <button 
        onClick={() => handleNavigation('/image')}
        className="flex flex-col items-center p-4 bg-orange-100 rounded-lg hover:bg-orange-200 transition-colors text-black dark:text-black"
      >
        <FiPieChart className="text-2xl mb-2 text-orange-600 dark:text-orange-600" />
        <span className="text-sm font-medium">Imagem</span>
      </button>
    </div>
  );
};

export default TutorButtons;
