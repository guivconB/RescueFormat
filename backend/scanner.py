import os
import time
from pathlib import Path

# Diretórios que sabemos que são lixo (pastas pesadas que não precisam de backup)
JUNK_DIRS = {"node_modules", ".cache", "Temp", "tmp", "$RECYCLE.BIN", "System Volume Information"}

# Ouro puro: pastas de configurações cruciais (Hidden Gems)
HIDDEN_GEMS = {
    "antigravity": r".gemini\antigravity",
    "android_emulator": r".android",
    "android_sdk": r"AppData\Local\Android",
    "vscode": r".vscode",
    "vscode_roaming": r"AppData\Roaming\Code",
    "chrome_sessions": r"AppData\Local\Google\Chrome\User Data\Default\Sessions",
    "edge_sessions": r"AppData\Local\Microsoft\Edge\User Data\Default\Sessions"
}

import winreg
import subprocess

def get_windows_product_key():
    """Tenta recuperar a chave original do Windows do registro."""
    try:
        path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\SoftwareProtectionPlatform"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path) as key:
            product_key = winreg.QueryValueEx(key, "BackupProductKeyDefault")[0]
            return product_key
    except Exception:
        return "Não encontrada ou não autorizada"

def get_wifi_passwords():
    """Extrai perfis de Wi-Fi e suas senhas salvas no Windows."""
    try:
        # Executa comando para pegar nomes dos perfis, lidando com idiomas PT e EN
        meta_data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('cp1252', errors="ignore")
        profiles = [line.split(":")[1].strip() for line in meta_data.split('\n') if "Perfil de Todos os Usuários" in line or "All User Profile" in line]
        
        wifi_list = []
        for profile in profiles:
            try:
                results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear']).decode('cp1252', errors="ignore")
                password = "Sem Senha / Oculta"
                for line in results.split('\n'):
                    if "Conteúdo da Chave" in line or "Key Content" in line:
                        password = line.split(":")[1].strip()
                        break
                wifi_list.append({"ssid": profile, "password": password})
            except Exception:
                pass
        return wifi_list
    except Exception:
        return []

def check_disk_health():
    """Verifica a integridade física do disco via S.M.A.R.T"""
    try:
        output = subprocess.check_output(['wmic', 'diskdrive', 'get', 'status']).decode('utf-8', errors="ignore")
        statuses = [s.strip() for s in output.split('\n') if s.strip() and s.strip().lower() != 'status']
        if all(s.lower() == 'ok' for s in statuses):
            return {"status": "ok", "message": "Discos 100% saudáveis. Pode formatar tranquilo!"}
        else:
            return {"status": "warning", "message": "ALERTA! Possível falha de Hardware no Disco."}
    except Exception:
        return {"status": "unknown", "message": "Saúde do disco desconhecida."}

def get_installed_apps():
    """Busca aplicativos instalados lendo o registro do Windows."""
    apps = set()
    paths = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
    ]
    for hkey, path in paths:
        try:
            with winreg.OpenKey(hkey, path) as key:
                for i in range(0, winreg.QueryInfoKey(key)[0]):
                    try:
                        skey_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, skey_name) as skey:
                            name = winreg.QueryValueEx(skey, "DisplayName")[0]
                            if name and not name.startswith("Update"):
                                apps.add(name)
                    except OSError:
                        pass
        except OSError:
            pass
    return sorted(list(apps))

def fast_scan(start_path, max_depth=6):
    """
    Realiza uma varredura profunda e mapeia TODOS os programas instalados e pastas de backup.
    """
    results = {
        "junk": [],
        "gems": [],
        "large_files": [],
        "installed_apps": get_installed_apps(),
        "windows_key": get_windows_product_key(),
        "wifi_passwords": get_wifi_passwords(),
        "disk_health": check_disk_health(),
        "files_by_category": {
            "documents": [],
            "media": [],
            "code": [],
            "archives": []
        }
    }

    
    # 1. Pastas Padrão Essenciais (Sempre fazer backup)
    standard_folders = ["Documents", "Desktop", "Pictures", "Videos", "Music", "Downloads"]
    for folder in standard_folders:
        folder_path = os.path.join(start_path, folder)
        if os.path.exists(folder_path):
            results["gems"].append({"path": folder_path, "gem_id": f"pasta_{folder.lower()}"})

    # Mapa simples de categorias por extensão
    categories = {
        ".pdf": "documents", ".docx": "documents", ".txt": "documents", ".xlsx": "documents",
        ".mp4": "media", ".jpg": "media", ".png": "media", ".mp3": "media", ".mkv": "media",
        ".py": "code", ".js": "code", ".html": "code", ".jsx": "code", ".ts": "code", ".json": "code",
        ".zip": "archives", ".rar": "archives", ".7z": "archives", ".tar": "archives", ".gz": "archives"
    }

    try:
        # Usamos uma pilha (stack) em vez de recursão para melhor controle de profundidade e memória
        stack = [(start_path, 0)]
        
        while stack:
            current_path, depth = stack.pop()
            
            if depth > max_depth:
                continue
                
            try:
                with os.scandir(current_path) as it:
                    for entry in it:
                        # Ignorar atalhos de sistema para evitar loops infinitos
                        if entry.is_symlink():
                            continue
                            
                        if entry.is_dir():
                            # Verificar se é lixo (Junk)
                            if entry.name in JUNK_DIRS:
                                results["junk"].append({"path": entry.path, "type": "dir", "name": entry.name})
                                continue # Não entra na pasta de lixo
                                
                            # Verificar se é uma "Hidden Gem"
                            for gem_name, gem_path_part in HIDDEN_GEMS.items():
                                if gem_path_part.lower() in entry.path.lower():
                                    # Evita duplicação se já pegou a raiz
                                    if entry.path.lower().endswith(gem_path_part.lower()):
                                        results["gems"].append({"path": entry.path, "gem_id": gem_name})
                                        
                            stack.append((entry.path, depth + 1))
                            
                        elif entry.is_file():
                            try:
                                size = entry.stat(follow_symlinks=False).st_size
                            except OSError:
                                size = 0
                                
                            # Caçador de arquivos pesados (> 100MB)
                            if size > 100 * 1024 * 1024: 
                                results["large_files"].append({"path": entry.path, "size": size})
                                
                            # Identificar arquivos Lixo isolados (Ex: Instaladores velhos em Downloads)
                            ext = Path(entry.name).suffix.lower()
                            if ext in {".exe", ".msi"} and "Downloads" in current_path:
                                results["junk"].append({"path": entry.path, "type": "file", "size": size, "name": entry.name})
                            
                            # Categorização normal
                            if ext in categories:
                                cat = categories[ext]
                                results["files_by_category"][cat].append({"path": entry.path, "size": size})
                                
            except PermissionError:
                continue
            except OSError:
                continue
    except Exception as e:
        print(f"Erro crítico ao escanear {start_path}: {e}")
        
    # Ordenar os arquivos pesados (Top maiores primeiro)
    results["large_files"].sort(key=lambda x: x["size"], reverse=True)
    results["large_files"] = results["large_files"][:50] # Pega apenas os Top 50
        
    return results

if __name__ == "__main__":
    print("Iniciando varredura rápida na pasta de Usuário...")
    user_home = os.path.expanduser("~")
    start = time.time()
    
    # Rodando um teste local rápido (profundidade 4 para não demorar no teste)
    data = fast_scan(user_home, max_depth=4)
    
    print(f"\nVarredura finalizada em {time.time() - start:.2f} segundos!")
    print(f"Lixo encontrado: {len(data['junk'])} pastas/arquivos")
    print(f"Configurações ocultas (Gems) encontradas: {len(data['gems'])}")
    print(f"Arquivos Gigantes (>100MB): {len(data['large_files'])}")
    if data['gems']:
        print("\nGems detalhadas:")
        for gem in data['gems']:
            print(f" - {gem['gem_id']}: {gem['path']}")
