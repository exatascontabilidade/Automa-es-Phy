@echo off
title Instalador do Ambiente Python e Bibliotecas
echo Instalando Python e bibliotecas necessárias...
echo.

:: Verifica se o Python já está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python não encontrado. Baixando e instalando...
    
    :: Baixa o instalador do Python (ajuste a versão conforme necessário)
    curl -o python_installer.exe https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe
    
    :: Instala o Python silenciosamente
    start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    
    echo Python instalado com sucesso!
) else (
    echo Python já está instalado.
)

:: Garante que o Python está disponível no PATH após instalação
setx PATH "%PATH%;C:\Python312;C:\Python312\Scripts" >nul

:: Aguarda que a variável de ambiente seja aplicada
echo Atualizando variáveis de ambiente...
refreshenv

:: Atualiza o PIP
echo Atualizando o pip...
python -m ensurepip
python -m pip install --upgrade pip

:: Instala bibliotecas necessárias
echo Instalando bibliotecas necessárias...
python -m pip install pandas selenium webdriver-manager datetime openpyxl

:: Finalização
echo.
echo Instalação concluída! 🚀
pause
exit
