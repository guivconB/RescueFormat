@echo off
color 0B
echo ===================================================
echo       Iniciando o RescueFormat (Assistente)
echo ===================================================
echo.

echo [1/2] Ligando o Motor (Backend Python)...
start "RescueFormat - Motor Python" cmd /c "cd backend && python -m uvicorn main:app --reload"

echo [2/2] Ligando a Interface Visual (Frontend React)...
start "RescueFormat - Interface Web" cmd /c "cd frontend && npm run dev"

echo.
echo Tudo pronto! Os servidores estao rodando em segundo plano.
echo Abrindo o painel no seu navegador...
timeout /t 3 >nul

:: Abre o navegador padrao direto no painel
start http://localhost:5173

exit
