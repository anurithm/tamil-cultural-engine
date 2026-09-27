import React, { useState, useEffect, useRef } from 'react';
import { MessageSquare, X, ShieldAlert, CheckCircle2, Sparkles, AlertTriangle } from 'lucide-react';

export default function Chatbot({ lang }) {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    if (isOpen) {
      scrollToBottom();
    }
  }, [messages, isOpen]);

  // Autonomous Preservation Simulation
  useEffect(() => {
    const sequence = async () => {
      // 1. Initial Greeting
      setMessages([
        {
          id: 1,
          type: 'ai',
          text: lang === 'ta' 
            ? "வணக்கம்! நான் AUREX’26 Cultural AI. நான் காணாமல் போன அறிவை கண்காணிக்கிறேன்." 
            : "Hello! I am the AUREX'26 Cultural AI. I continuously monitor the system for vanishing knowledge.",
          time: new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})
        }
      ]);

      // 2. Alert (Trigger after 4 seconds)
      await new Promise(resolve => setTimeout(resolve, 4000));
      setIsOpen(true); // Auto-open when critical alert happens
      setMessages(prev => [...prev, {
        id: 2,
        type: 'alert',
        icon: <AlertTriangle className="w-4 h-4 text-rose-500" />,
        text: lang === 'ta'
          ? "🚨 நெருக்கடி எச்சரிக்கை: கரகாட்டம் பாரம்பரியத்தில் அவசர இடைவெளி கண்டறியப்பட்டுள்ளது (Urgency: 92/100). மனித தலையீடு இல்லாமல் தன்னாட்சி முறையில் அறிவை பாதுகாக்கும் செயல்முறை தொடங்குகிறது..."
          : "🚨 CRITICAL ALERT: High urgency gap detected in Karagattam (Urgency: 92/100). Missing step: 'Brass pot balancing physics'. Initiating autonomous preservation without human intervention...",
        time: new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})
      }]);

      // 3. Autonomous Processing
      await new Promise(resolve => setTimeout(resolve, 3000));
      setMessages(prev => [...prev, {
        id: 3,
        type: 'ai',
        icon: <Sparkles className="w-4 h-4 text-[#064e3b]" />,
        text: lang === 'ta'
          ? "வரலாற்று தரவுகளை ஒப்பிட்டு புதிய வரைவை உருவாக்குகிறேன்..."
          : "Cross-referencing historical archives and formulating missing physical alignment data...",
        time: new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})
      }]);

      // 4. Preservation Complete
      await new Promise(resolve => setTimeout(resolve, 3000));
      setMessages(prev => [...prev, {
        id: 4,
        type: 'success',
        icon: <CheckCircle2 className="w-4 h-4 text-emerald-600" />,
        text: lang === 'ta'
          ? "✅ தன்னாட்சி பாதுகாப்பு நிறைவுற்றது! மறுகட்டமைக்கப்பட்ட அறிவு பாதுகாக்கப்பட்ட ஆவணங்களில் சேர்க்கப்பட்டுள்ளது."
          : "✅ Autonomous Preservation Complete! The reconstructed knowledge has been successfully archived to the Preserved Records database.",
        time: new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})
      }]);
    };

    sequence();
  }, [lang]);

  return (
    <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end">
      {/* Chat Window */}
      {isOpen && (
        <div className="bg-[#F8E7C9] w-80 md:w-96 rounded-2xl shadow-2xl border-2 border-[#064e3b]/20 mb-4 overflow-hidden flex flex-col transform transition-all duration-300 origin-bottom-right">
          
          {/* Header */}
          <div className="bg-[#064e3b] px-4 py-3 flex justify-between items-center text-[#F8E7C9]">
            <div className="flex items-center space-x-2">
              <ShieldAlert className="w-5 h-5 text-[#F8E7C9]" />
              <span className="font-bold font-serif-title tracking-wide">AUREX'26 AI Monitor</span>
            </div>
            <button onClick={() => setIsOpen(false)} className="hover:bg-[#022c22] p-1 rounded-full transition-colors">
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Messages Area */}
          <div className="h-80 overflow-y-auto p-4 space-y-4 bg-[#F8E7C9]/50">
            {messages.map((msg) => (
              <div key={msg.id} className={`flex flex-col ${msg.type === 'user' ? 'items-end' : 'items-start'}`}>
                <div className={`
                  max-w-[85%] rounded-xl px-4 py-2.5 text-sm shadow-sm
                  ${msg.type === 'alert' ? 'bg-rose-100 text-rose-900 border border-rose-200 font-medium' : ''}
                  ${msg.type === 'success' ? 'bg-emerald-100 text-emerald-900 border border-emerald-200 font-medium' : ''}
                  ${msg.type === 'ai' ? 'bg-white text-[#064e3b] border border-[#064e3b]/10' : ''}
                  ${msg.type === 'user' ? 'bg-[#064e3b] text-[#F8E7C9]' : ''}
                `}>
                  {(msg.icon && msg.type !== 'user') && (
                    <div className="mb-1">{msg.icon}</div>
                  )}
                  <p className="leading-relaxed">{msg.text}</p>
                </div>
                <span className="text-[10px] text-[#064e3b]/40 mt-1 px-1">{msg.time}</span>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area (Visual Only for Demo) */}
          <div className="p-3 border-t border-[#064e3b]/10 bg-white flex items-center">
            <input 
              type="text" 
              placeholder={lang === 'ta' ? 'செய்தியை உள்ளிடுக...' : 'Type a message...'}
              className="flex-1 bg-[#F8E7C9]/30 border border-[#064e3b]/20 rounded-full px-4 py-2 text-sm focus:outline-none focus:border-[#064e3b]/50 text-[#064e3b] placeholder-[#064e3b]/40"
              disabled
            />
          </div>
        </div>
      )}

      {/* Floating Button */}
      <button 
        onClick={() => setIsOpen(!isOpen)}
        className="bg-[#064e3b] text-[#F8E7C9] p-4 rounded-full shadow-2xl hover:bg-[#022c22] hover:scale-110 transition-all duration-300 border-2 border-[#F8E7C9]/20 relative"
      >
        <MessageSquare className="w-6 h-6" />
        {/* Unread badge logic (simplified) */}
        {!isOpen && messages.length > 1 && (
          <span className="absolute -top-1 -right-1 flex h-4 w-4 items-center justify-center rounded-full bg-rose-500 text-[10px] font-bold text-white border-2 border-[#064e3b]">
            !
          </span>
        )}
      </button>
    </div>
  );
}
