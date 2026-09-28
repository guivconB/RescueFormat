import React, { useState } from 'react';
import { HardDrive, Shield, Trash2, CheckCircle, DownloadCloud, Box, Save, RotateCcw } from 'lucide-react';
import './App.css';

function App() {
  const [scanData, setScanData] = useState(null);
  const [isScanning, setIsScanning] = useState(false);
  const [recoveryMode, setRecoveryMode] = useState(false);
  const [planSaved, setPlanSaved] = useState(false);

  const startScan = async () => {
    setIsScanning(true);
    setScanData(null);
    setRecoveryMode(false);
    try {
      const res = await fetch('http://localhost:8000/api/scan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({})
      });
      if (!res.ok) throw new Error(`Status HTTP: ${res.status}`);
      const payload = await res.json();
      
      if (payload.status === 'error') throw new Error(payload.message);
      if (!payload.data || !payload.data.junk) throw new Error('Retorno da API não possui os dados esperados.');
      
      setScanData(payload.data);
    } catch (err) {
      console.error(err);
      alert('Erro ao comunicar com o Motor Python: ' + err.message);
    }
    setIsScanning(false);
  };

  const loadSavedPlan = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/load');
      const payload = await res.json();
      
      if (payload.status === 'success' && payload.data) {
        setScanData(payload.data);
        setRecoveryMode(true);
      } else {
        alert('Nenhum "Format_Master_Plan.json" encontrado nesta pasta. Faça a varredura primeiro!');
      }
    } catch (err) {
      console.error(err);
      alert('Erro ao carregar o plano salvo.');
    }
  };

  const simulateRecovery = () => {
    if (!scanData) {
      alert('Faça o mapeamento antes para simular!');
      return;
    }
    setRecoveryMode(true);
  };

  const exportPlan = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/export', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(scanData)
      });
      if (res.ok) {
        setPlanSaved(true);
        setTimeout(() => setPlanSaved(false), 5000);
      }
    } catch (err) {
      console.error(err);
      alert('Erro ao exportar o plano.');
    }
  };

  if (isScanning) {
    return (
      <div className="container loader-container">
        <HardDrive size={64} className="spinner" />
        <h2 style={{ fontFamily: 'Space Grotesk' }}>Analisando Profundamente...</h2>
        <p style={{ color: 'var(--text-secondary)' }}>Vasculhando HD, Registro do Windows e Arquivos Ocultos.</p>
      </div>
    );
  }

  // === MODO RECUPERAÇÃO (SOBREVIVÊNCIA) ===
  if (recoveryMode && scanData) {
    return (
      <div className="container">
        <header className="header recovery">
          <h1><Shield size={48} /> Modo Sobrevivência</h1>
          <p>O Windows está formatado e novo! Recupere seus dados agora.</p>
          
          <div className="recovery-assets">
            {scanData.windows_key && scanData.windows_key !== "Não encontrada ou não autorizada" && (
              <div className="asset-box" style={{ borderColor: 'var(--accent-amber)' }}>
                <h3 style={{ color: 'var(--accent-amber)' }}>🔑 Chave do Windows</h3>
                <code>{scanData.windows_key}</code>
              </div>
            )}
            
            {scanData.wifi_passwords && scanData.wifi_passwords.length > 0 && (
              <div className="asset-box" style={{ borderColor: 'var(--accent-blue)' }}>
                <h3 style={{ color: 'var(--accent-blue)' }}>📶 Senhas de Wi-Fi</h3>
                <ul className="wifi-list">
                  {scanData.wifi_passwords.map((w, i) => (
                    <li key={i}>
                      <strong>{w.ssid}</strong>
                      <code style={{ padding: '4px 8px', fontSize: '0.9rem' }}>{w.password}</code>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
          
          <div className="top-actions">
            <button onClick={() => setRecoveryMode(false)} className="btn-secondary">
              <RotateCcw size={20}/> Voltar ao Mapeamento
            </button>
          </div>
        </header>

        <div className="dashboard" style={{ gridTemplateColumns: '1fr' }}>
          <section className="section gems" style={{ height: 'auto', minHeight: '500px' }}>
            <h2><CheckCircle color="var(--accent-emerald)" /> Guia de Sobrevivência: Restaurando Gems</h2>
            <p>O script salvou estas pastas no seu Pen Drive. Siga os passos ou use os botões de pesquisa para reinstalar tudo.</p>
            
            <div className="recovery-assets">
              {scanData.gems.map((g, i) => {
                const tutorials = {
                  'antigravity': 'Abra o Explorador de Arquivos, navegue até C:\\Users\\SeuUsuario\\.gemini\\antigravity e cole a pasta do backup por cima da existente.',
                  'android_emulator': 'Copie a pasta do Pen Drive e cole exatamente no mesmo caminho indicado abaixo. O Android Studio reconhecerá automaticamente.',
                  'vscode_roaming': 'Aperte as teclas [Win + R], digite "%appdata%" e dê Enter. Ache a pasta "Code" e substitua pelo seu backup.',
                  'vscode': 'Aperte as teclas [Win + R], digite "%userprofile%" e dê Enter. Entre na pasta ".vscode" e cole o backup lá.',
                  'chrome_sessions': 'Aperte as teclas [Win + R], digite "%localappdata%" e navegue até Google\\Chrome\\User Data\\Default. Cole a pasta Sessions.',
                  'edge_sessions': 'Aperte as teclas [Win + R], digite "%localappdata%" e navegue até Microsoft\\Edge\\User Data\\Default. Cole a pasta Sessions.',
                  'pasta_documents': 'Simplesmente abra sua nova pasta Documentos do Windows e cole tudo.',
                  'pasta_desktop': 'Simplesmente abra sua nova Área de Trabalho e cole os arquivos.',
                };
                const instruction = tutorials[g.gem_id] || 'Copie a pasta do seu backup e cole no caminho exato indicado abaixo no novo computador.';

                return (
                  <div key={i} className="asset-box" style={{ flex: '1 1 350px', display: 'flex', flexDirection: 'column' }}>
                    <h3 style={{ color: 'var(--accent-emerald)' }}>{g.gem_id.toUpperCase()}</h3>
                    
                    <div style={{ marginBottom: '16px', color: 'var(--text-secondary)' }}>
                      <strong>📚 Tutorial Offline:</strong>
                      <p style={{ marginTop: '4px', fontSize: '0.95rem' }}>{instruction}</p>
                    </div>

                    <div style={{ marginBottom: '24px' }}>
                      <strong>📍 Caminho Alvo no PC Novo:</strong> <br/>
                      <code style={{ marginTop: '8px', wordBreak: 'break-all' }}>{g.path}</code>
                    </div>
                    
                    <div className="top-actions" style={{ marginTop: 'auto', display: 'flex', gap: '8px' }}>
                      <a href={`https://www.google.com/search?q=como+restaurar+pasta+${g.gem_id}+no+windows`} target="_blank" rel="noreferrer" className="btn-secondary" style={{ flex: 1, textDecoration: 'none', padding: '10px' }}>
                        Buscar no Google
                      </a>
                      <a href={`https://www.youtube.com/results?search_query=como+fazer+backup+restaurar+${g.gem_id}`} target="_blank" rel="noreferrer" className="btn-secondary" style={{ flex: 1, textDecoration: 'none', padding: '10px', color: '#f87171', borderColor: 'rgba(248, 113, 113, 0.2)' }}>
                        Ver no YouTube
                      </a>
                    </div>
                  </div>
                );
              })}
            </div>
          </section>
        </div>
      </div>
    );
  }

  // === MODO MAPEAMENTO (PRÉ-FORMATAÇÃO) ===
  return (
    <div className="container">
      <header className="header">
        <h1>RescueFormat <Shield size={56} style={{ color: 'var(--accent-blue)' }}/></h1>
        <p>O Assistente de IA Definitivo para Backup e Formatação.</p>
        
        {scanData && scanData.disk_health && (
          <div className={`health-indicator ${scanData.disk_health.status === 'ok' ? 'ok' : 'warning'}`}>
            {scanData.disk_health.status === 'ok' ? '🩺 HD/SSD 100% Saudável (S.M.A.R.T OK)' : '⚠️ ALERTA: Disco falhando! Formatar não vai resolver lentidão.'}
          </div>
        )}

        <div className="top-actions">
          <button onClick={startScan} className="btn-primary">
            <HardDrive size={24} /> {scanData ? 'Refazer Varredura' : 'Mapear Sistema Agora'}
          </button>
          
          {!scanData && (
            <button onClick={loadSavedPlan} className="btn-secondary">
              <RotateCcw size={24} /> Carregar Plano Salvo (Pós-Formatação)
            </button>
          )}

          {scanData && !recoveryMode && (
            <button onClick={simulateRecovery} className="btn-secondary">
              <Shield size={24} /> Entrar no Modo Pós-Formatação
            </button>
          )}
        </div>
      </header>

      {scanData && (
        <main>
          <div className="dashboard">
            
            {/* Lixo */}
            <section className="section junk">
              <h2><Trash2 color="var(--accent-red)" /> Para o Lixo</h2>
              <p>Caches inúteis e pesados que você NUNCA deve fazer backup.</p>
              <ul className="file-list">
                {scanData.junk.map((j, i) => {
                  const name = j.name || j.path.split('\\').pop();
                  return (
                    <li key={i}>
                      <strong className="friendly-title">{name}</strong>
                      <span className="path-tooltip">{j.path}</span>
                      <span className="badge" style={{ color: 'var(--accent-red)', background: 'var(--accent-red-glow)' }}>Pode Apagar</span>
                    </li>
                  );
                })}
              </ul>
            </section>

            {/* Ouro */}
            <section className="section gems">
              <h2><CheckCircle color="var(--accent-emerald)" /> Ouro Puro</h2>
              <p>O robô fará backup destas pastas para o Pen Drive pra você.</p>
              <ul className="file-list">
                {scanData.gems.map((g, i) => {
                  const friendlyNames = {
                    'antigravity': 'Config. Antigravity',
                    'android_emulator': 'Máquina Virtual Android',
                    'android_sdk': 'Bibliotecas Android SDK',
                    'vscode': 'Extensões VSCode',
                    'vscode_roaming': 'Preferências VSCode',
                    'chrome_sessions': 'Sessão do Chrome (Abas)',
                    'edge_sessions': 'Sessão do Edge (Abas)',
                    'pasta_documents': 'Sua Pasta de Documentos',
                    'pasta_desktop': 'Sua Área de Trabalho',
                    'pasta_pictures': 'Sua Pasta de Imagens',
                    'pasta_videos': 'Sua Pasta de Vídeos',
                    'pasta_downloads': 'Downloads'
                  };
                  return (
                    <li key={i} className="gem-item">
                      <strong className="friendly-title-gem">{friendlyNames[g.gem_id] || g.gem_id.toUpperCase()}</strong>
                      <span className="path-tooltip">{g.path}</span>
                    </li>
                  );
                })}
              </ul>
            </section>

            {/* Pesados */}
            <section className="section web">
              <h2><DownloadCloud color="var(--accent-blue)" /> Arquivos Gigantes</h2>
              <p>Maioria são instaladores velhos. Re-baixe da internet.</p>
              <ul className="file-list">
                {scanData.large_files.slice(0, 10).map((f, i) => {
                  const name = f.path.split('\\').pop();
                  return (
                    <li key={i}>
                      <strong className="friendly-title">{name}</strong>
                      <span className="path-tooltip">{f.path}</span>
                      <span className="badge" style={{ color: 'var(--accent-blue)', background: 'var(--accent-blue-glow)' }}>
                        {(f.size / 1024 / 1024).toFixed(2)} MB
                      </span>
                    </li>
                  );
                })}
              </ul>
            </section>

            {/* Programas */}
            {scanData.installed_apps && (
              <section className="section apps">
                <h2><Box color="var(--accent-amber)" /> Programas Instalados</h2>
                <p>Serão reinstalados pelo Winget no PC formatado.</p>
                <ul className="file-list">
                  {scanData.installed_apps.map((app, i) => (
                    <li key={i}>
                      <strong className="friendly-title">{app}</strong>
                    </li>
                  ))}
                </ul>
              </section>
            )}

          </div>

          <div className="export-container">
            <button onClick={exportPlan} className="btn-success">
              <Save size={24} /> Gerar Scripts de Auto-Backup e Auto-Instalação
            </button>
            {planSaved && <p className="success-msg">Mágica feita! Arquivos .bat e .json gerados na raiz do projeto.</p>}
          </div>
        </main>
      )}
    </div>
  );
}

export default App;
