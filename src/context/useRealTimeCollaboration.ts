import { useState } from 'react';

interface Collaborator {
  id: string;
  name: string;
  avatar: string;
  role: 'student' | 'tutor' | 'teacher';
  isOnline: boolean;
}

export function useRealTimeCollaboration() {
  const [collaborators, setCollaborators] = useState<Collaborator[]>([]);
  const [isCollaborating, setIsCollaborating] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const startCollaboration = async () => {
    setIsLoading(true);
    
    // Simular delay
    setTimeout(() => {
      setIsCollaborating(true);
      setCollaborators([
        {
          id: '1',
          name: 'Ana Silva',
          avatar: '/avatars/ana.png',
          role: 'student',
          isOnline: true,
        },
        {
          id: '2',
          name: 'Prof. Carlos',
          avatar: '/avatars/carlos.png',
          role: 'tutor',
          isOnline: true,
        },
      ]);
      setIsLoading(false);
    }, 1000);
  };

  const endCollaboration = async () => {
    setIsCollaborating(false);
    setCollaborators([]);
  };

  return {
    collaborators,
    isCollaborating,
    startCollaboration,
    endCollaboration,
    isLoading,
    error: null,
  };
}