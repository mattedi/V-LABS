// src/pages/TextPage.tsx
import React, { useState } from 'react';
import UnifiedLayout from '../components/layout/UnifiedLayout';
import TextInput from '../components/multimodal/TextInput';
import { AiFeedbackPanel } from '../components/ai/AiFeedbackPanel';
import { useAiFeedback } from '../hooks/useAiFeedback';

export default function TextPage() {
  const [lastQuestion, setLastQuestion] = useState<string>('');
  const [lastContentId, setLastContentId] = useState<string>('');
  
  const {
    feedback,
    isLoading,
    requestAnalysis
  } = useAiFeedback();

  const handleSubmit = (question: string) => {
    const contentId = `text-${Date.now()}`;
    setLastQuestion(question);
    setLastContentId(contentId);
    requestAnalysis(contentId, question, 'text');
  };

  return (
    <UnifiedLayout pageTitle="Texto" showTutorButtons={true}>
      <TextInput onSubmit={handleSubmit} />

      {feedback && (
        <div className="mt-6">
          <AiFeedbackPanel
            analysisResult={feedback}
            isLoading={isLoading}
            onRetry={() => requestAnalysis(lastContentId, lastQuestion, 'text')}
          />
        </div>
      )}
    </UnifiedLayout>
  );
}
