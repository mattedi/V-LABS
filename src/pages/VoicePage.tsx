// src/pages/VoicePage.tsx

/**
 * Página dedicada ao modo de voz da aplicação
 * Esta página permite aos usuários interagir com o assistente através de comandos
 * de voz, fornecendo uma interface completa para gravação, processamento e
 * reprodução de áudio para comunicação natural.
 * Funcionalidades principais:
 * - Gravação de comandos de voz em tempo real
 * - Conversão de voz para texto (Speech-to-Text)
 * - Processamento de comandos naturais
 * - Síntese de voz para respostas (Text-to-Speech)
 * - Interface visual com feedback de status
 * - Instruções claras de uso
 * Interface implementada:
 * - Botão de gravação com estados visuais
 * - Indicadores de atividade (animações pulsantes)
 * - Seção de instruções passo-a-passo
 * - Design responsivo e acessível
 * 
 * @returns {JSX.Element} Componente da página de interação por voz
 */

// Importações do React
import React from 'react';

// Importa o layout principal que fornece estrutura comum
import MainLayout from '../components/layout/MainLayout';

/**
 * Componente principal da página de interação por voz
 * 
 * Renderiza uma interface completa para comunicação por voz, incluindo
 * controles de gravação, feedback visual e instruções de uso.
 * 
 * Props do MainLayout utilizadas:
 * - showChatBar: true - Mantém a barra de chat disponível
 * - showTutorButtons: true - Exibe botões de tutoria para navegação rápida
 */
export default function VoicePage() {
  return (
    <MainLayout showChatBar={true} showTutorButtons={true}>
      
      {/* REMOVIDO: Título duplicado "Bem vindo VL Studio" */}
      {/* O título principal já é exibido pelo MainLayout */}
      
      {/* Seção do título específico da página */}
      <div className="text-center mb-8">
        {/* Título da página com cor laranja para destaque visual */}
        <h2 className="text-3xl font-bold text-orange-600 mb-6">
          Modo de Voz
        </h2>
      </div>

      {/* Interface principal de controle de voz */}
      <div className="bg-white rounded-lg shadow-lg p-8 max-w-lg mx-auto mb-6">
        <div className="text-center">
          {/* Ícone visual do microfone - elemento central da interface */}
          <div className="w-24 h-24 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <span className="text-5xl">🎤</span>
          </div>
          
          {/* Título da seção de controles */}
          <h3 className="text-xl font-semibold text-gray-800 mb-4">
            Interface de Voz
          </h3>
          
          {/* Instrução principal para o usuário */}
          <p className="text-gray-600 mb-6">
            Clique no botão abaixo para começar a conversar por voz com o assistente
          </p>
          
          {/* 
            Botão principal de gravação de voz
            TODO: Implementar funcionalidades:
            - onClick handler para iniciar/parar gravação
            - Estados visuais (gravando, processando, erro)
            - Integração com APIs de Speech-to-Text
            - Feedback sonoro de início/fim de gravação
          */}
          <button className="bg-green-500 hover:bg-green-600 text-white px-8 py-3 rounded-lg font-semibold transition-colors shadow-lg w-full mb-4">
            🎤 Iniciar Gravação de Voz
          </button>
          
          {/* 
            Indicadores visuais de atividade
            Animação pulsante que simula atividade de áudio
            TODO: Sincronizar com estado real de gravação/processamento
          */}
          <div className="flex justify-center space-x-2">
            <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
            <span className="w-2 h-2 bg-green-300 rounded-full animate-pulse delay-75"></span>
            <span className="w-2 h-2 bg-green-200 rounded-full animate-pulse delay-150"></span>
          </div>
        </div>
      </div>

      {/* Seção de instruções de uso passo-a-passo */}
      <div className="bg-blue-50 rounded-lg p-6 max-w-2xl mx-auto">
        {/* Título da seção de instruções */}
        <h4 className="text-lg font-semibold text-blue-800 mb-3 text-center">
          Como usar o Modo de Voz:
        </h4>
        
        {/* Grid responsivo com instruções numeradas */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-blue-700">
          {/* Passo 1: Ativação do microfone */}
          <div className="flex items-start space-x-3">
            <span className="flex-shrink-0 w-6 h-6 bg-blue-500 text-white rounded-full flex items-center justify-center text-sm font-bold">1</span>
            <span>Clique no botão do microfone</span>
          </div>
          
          {/* Passo 2: Entrada de voz */}
          <div className="flex items-start space-x-3">
            <span className="flex-shrink-0 w-6 h-6 bg-blue-500 text-white rounded-full flex items-center justify-center text-sm font-bold">2</span>
            <span>Fale sua pergunta claramente</span>
          </div>
          
          {/* Passo 3: Processamento */}
          <div className="flex items-start space-x-3">
            <span className="flex-shrink-0 w-6 h-6 bg-blue-500 text-white rounded-full flex items-center justify-center text-sm font-bold">3</span>
            <span>Aguarde o processamento</span>
          </div>
          
          {/* Passo 4: Resposta em áudio */}
          <div className="flex items-start space-x-3">
            <span className="flex-shrink-0 w-6 h-6 bg-blue-500 text-white rounded-full flex items-center justify-center text-sm font-bold">4</span>
            <span>Escute a resposta em áudio</span>
          </div>
        </div>
      </div>

    </MainLayout>
  );
}

// EXTENSÕES FUTURAS:
// - Implementar integração com APIs de Speech-to-Text e Text-to-Speech
// - Adicionar feedback visual e sonoro durante o processamento
// - Implementar histórico de comandos de voz
// - Adicionar suporte a múltiplos idiomas e sotaques
// - Implementar reconhecimento de comandos específicos (ex: "ajuda", "configurações")
// - Adicionar suporte a comandos personalizados e macros de voz
// - Implementar um sistema de aprendizado contínuo para melhorar a precisão
// - Adicionar suporte a comandos de voz offline (armazenamento local)
// - Implementar um sistema de feedback do usuário para melhorar a experiência
// - Adicionar suporte a integração com dispositivos IoT (ex: controle de luzes, temperatura)
// - Implementar um sistema de segurança para autenticação por voz
// - Adicionar suporte a comandos de voz contextuais (ex: "no chat", "na imagem")
// - Implementar um sistema de personalização de voz do assistente