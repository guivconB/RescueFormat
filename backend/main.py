from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from scanner import fast_scan
import os
import json

app = FastAPI(title="RescueFormat API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScanRequest(BaseModel):
    path: str = os.path.expanduser("~")
    max_depth: int = 5

@app.post("/api/scan")
def scan_directory(req: ScanRequest):
    """Rota para iniciar a varredura do disco."""
    try:
        data = fast_scan(req.path, req.max_depth)
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/export")
def export_plan(plan: dict):
    """
    Salva o arquivo de 'memória' e gera os scripts mágicos de Auto-Instalação e Auto-Backup.
    """
    try:
        # Define a pasta raiz do projeto e cria a subpasta de Exportação
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        export_dir = os.path.join(base_dir, "Arquivos_de_Backup_Gerados")
        os.makedirs(export_dir, exist_ok=True)
        
        # Arquivos vão para dentro da pasta criada
        json_path = os.path.join(export_dir, "Format_Master_Plan.json")
        winget_path = os.path.join(export_dir, "Instalar_Tudo.bat")
        backup_path = os.path.join(export_dir, "Realizar_Backup.bat")

        # Salva o Cérebro JSON
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(plan, f, indent=4, ensure_ascii=False)
            
        # Gera o Script do Winget (Instalador Automático)
        with open(winget_path, "w", encoding="utf-8") as f:
            f.write("@echo off\n")
            f.write("echo === Iniciando Auto-Instalador RescueFormat ===\n")
            if "installed_apps" in plan:
                for app in plan["installed_apps"]:
                    f.write(f'echo Instalando: {app}\n')
                    f.write(f'winget install --name "{app}" --accept-package-agreements --accept-source-agreements\n')
            f.write("echo Instalacao concluida!\npause\n")

        # Gera o Script de Auto-Backup
        with open(backup_path, "w", encoding="utf-8") as f:
            f.write("@echo off\n")
            f.write('echo === Iniciando Caminhao de Mudanca (Auto-Backup) ===\n')
            f.write('mkdir "BKP_RESCUEFORMAT" 2>nul\n')
            
            f.write('echo.\n')
            f.write('echo === Exportando Drivers do Sistema (Execute como Administrador se der erro) ===\n')
            f.write('mkdir "BKP_RESCUEFORMAT\\Meus_Drivers" 2>nul\n')
            f.write('dism /online /export-driver /destination:"%CD%\\BKP_RESCUEFORMAT\\Meus_Drivers"\n')
            f.write('echo Drivers exportados com sucesso!\n\n')

            if "gems" in plan:
                for gem in plan["gems"]:
                    path = gem["path"]
                    folder_name = os.path.basename(path.rstrip('\\'))
                    f.write(f'echo Copiando {gem["gem_id"]}...\n')
                    f.write(f'xcopy "{path}" "BKP_RESCUEFORMAT\\{folder_name}" /E /I /H /Y\n')
            f.write("echo Backup concluido! Arraste a pasta BKP_RESCUEFORMAT para o Pen Drive.\npause\n")

        return {"status": "success", "message": "Plano exportado! Scripts .bat criados com sucesso!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/load")
def load_plan():
    """
    Chamado no 'Modo Pós-Formatação'. Lê o arquivo gerado antes da formatação
    para exibir o Guia de Sobrevivência e as instruções de restauração.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(base_dir, "Arquivos_de_Backup_Gerados", "Format_Master_Plan.json")

    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return {"status": "success", "mode": "recovery", "data": data}
        except Exception as e:
            return {"status": "error", "message": f"Erro ao ler plano: {e}"}
            
    return {"status": "not_found", "mode": "scanner", "message": "Nenhum plano encontrado. Você está no Modo Pré-Formatação."}

@app.get("/")
def health_check():
    return {"status": "online", "app": "RescueFormat Motor Backend"}
