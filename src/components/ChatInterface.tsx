import React, { useState, useEffect, useRef } from 'react';

interface Mensagem {
  tipo: 'usuario' | 'assistente';
  conteudo: string;
  timestamp: string;
  complexidade?: number;
  feedback?: string;
}

interface Conversa {
  id: string;
  titulo: string;
  mensagens: Mensagem[];
  data_criacao: string;
  data_ultima_interacao: string;
}

export const ChatInterface: React.FC = () => {
  const [conversaAtual, setConversaAtual] = useState<Conversa | null>(null);
  const [mensagens, setMensagens] = useState<Mensagem[]>([]);
  const [novaMensagem, setNovaMensagem] = useState('');
  const [carregando, setCarregando] = useState(false);
  const chatContainerRef = useRef<HTMLDivElement>(null);

  // Scroll automático para última mensagem
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [mensagens]);

  const criarNovaConversa = async () => {
    const novaConversa = {
      titulo: `Conversa ${new Date().toLocaleDateString()}`,
      mensagens: [],
      data_criacao: new Date().toISOString(),
      data_ultima_interacao: new Date().toISOString()
    };

    const response = await fetch('http://127.0.0.1:8002/api/conversas', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(novaConversa)
    });

    const conversa = await response.json();
    setConversaAtual(conversa);
    setMensagens([]);
  };

  const enviarMensagem = async () => {
    if (!novaMensagem.trim() || !conversaAtual) return;

    setCarregando(true);
    
    // Adicionar mensagem do usuário
    const mensagemUsuario: Mensagem = {
      tipo: 'usuario',
      conteudo: novaMensagem,
      timestamp: new Date().toISOString()
    };

    setMensagens(prev => [...prev, mensagemUsuario]);
    setNovaMensagem('');

    try {
      // Salvar mensagem no backend
      await fetch(`http://127.0.0.1:8002/api/conversas/${conversaAtual.id}/mensagens`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(mensagemUsuario)
      });

      // Processar pergunta (sua lógica existente de análise)
      const respostaProcessamento = await processarPergunta(novaMensagem);
      
      // Adicionar resposta do assistente
      const mensagemAssistente: Mensagem = {
        tipo: 'assistente',
        conteudo: respostaProcessamento.resposta,
        timestamp: new Date().toISOString(),
        complexidade: respostaProcessamento.complexidade,
        feedback: respostaProcessamento.feedback
      };

      setMensagens(prev => [...prev, mensagemAssistente]);

      // Salvar resposta no backend
      await fetch(`http://127.0.0.1:8002/api/conversas/${conversaAtual.id}/mensagens`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(mensagemAssistente)
      });

    } catch (error) {
      console.error('Erro ao processar mensagem:', error);
    } finally {
      setCarregando(false);
    }
  };

  const processarPergunta = async (pergunta: string) => {
    // Integrar com sua lógica existente de análise
    // Retorna: { resposta, complexidade, feedback }
    return {
      resposta: "Resposta processada pela IA...",
      complexidade: 88,
      feedback: "Sua compreensão textual está se desenvolvendo bem."
    };
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 p-4">
        <div className="flex items-center justify-between">
          <h1 className="text-xl font-semibold text-gray-800">
            {conversaAtual?.titulo || "Nova Conversa"}
          </h1>
          <button
            onClick={criarNovaConversa}
            className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600"
          >
            Nova Conversa
          </button>
        </div>
      </div>

      {/* Chat Container com Scroll */}
      <div 
        ref={chatContainerRef}
        className="flex-1 overflow-y-auto p-4 space-y-4"
        style={{ maxHeight: 'calc(100vh - 200px)' }}
      >
        {mensagens.map((mensagem, index) => (
          <div
            key={index}
            className={`flex ${mensagem.tipo === 'usuario' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                mensagem.tipo === 'usuario'
                  ? 'bg-blue-500 text-white'
                  : 'bg-white text-gray-800 shadow'
              }`}
            >
              <p className="text-sm">{mensagem.conteudo}</p>
              <p className="text-xs opacity-75 mt-1">
                {new Date(mensagem.timestamp).toLocaleTimeString()}
              </p>
              
              {/* Mostrar complexidade e feedback para mensagens do assistente */}
              {mensagem.tipo === 'assistente' && mensagem.complexidade && (
                <div className="mt-2 pt-2 border-t border-gray-200">
                  <p className="text-xs text-blue-600">
                    Complexidade: {mensagem.complexidade}%
                  </p>
                  {mensagem.feedback && (
                    <p className="text-xs text-green-600 mt-1">
                      {mensagem.feedback}
                    </p>
                  )}
                </div>
              )}
            </div>
          </div>
        ))}

        {/* Indicador de carregamento */}
        {carregando && (
          <div className="flex justify-start">
            <div className="bg-gray-200 rounded-lg px-4 py-2">
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Input de Mensagem */}
      <div className="bg-white border-t border-gray-200 p-4">
        <div className="flex space-x-4">
          <input
            type="text"
            value={novaMensagem}
            onChange={(e) => setNovaMensagem(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && !carregando && enviarMensagem()}
            placeholder="Digite sua mensagem..."
            className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            disabled={carregando}
          />
          <button
            onClick={enviarMensagem}
            disabled={carregando || !novaMensagem.trim() || !conversaAtual}
            className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed"
          >
            {carregando ? 'Enviando...' : 'Enviar'}
          </button>
        </div>
      </div>
    </div>
  );
};