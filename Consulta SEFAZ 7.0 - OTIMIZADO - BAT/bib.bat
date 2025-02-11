@echo off
title Verificador e Atualizador do Python e Tkinter
echo Verificando instalação do Python...
echo.

:: Verifica se o Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python não encontrado. Instalando a versão mais recente...
    goto :instalar_python
)

:: Obtém a versão do Python instalada
for /f "delims=" %%i in ('python -c "import sys; print(sys.version.split()[0])"') do set PYTHON_VERSION=%%i

echo Versão instalada: %PYTHON_VERSION%
echo Obtendo a versão mais recente do Python...

:: Obtém a versão mais recente do site oficial do Python
curl -s https://www.python.org/downloads/ | findstr /r "Latest Python [0-9]\.[0-9]\.[0-9]" > temp.txt
for /f "tokens=3" %%a in (temp.txt) do set LATEST_PYTHON_VERSION=%%a
del temp.txt

echo Versão mais recente disponível: %LATEST_PYTHON_VERSION%

:: Compara a versão instalada com a versão mais recente
if "%PYTHON_VERSION%"=="%LATEST_PYTHON_VERSION%" (
    echo Python já está atualizado.
) else (
    echo Atualizando para a versão mais recente...
    goto :instalar_python
)

:: Verifica a presença do Tkinter
echo Verificando Tkinter...
python -c "import tkinter" 2>nul
if %errorlevel% neq 0 (
    echo Tkinter não encontrado! Instalando...
    python -m pip install tk
) else (
    echo Tkinter já está instalado.
)

echo.
echo Verificação concluída! 🚀
pause
exit /b

:instalar_python
echo Baixando Python %LATEST_PYTHON_VERSION%...
curl -o python_installer.exe https://www.python.org/ftp/python/%LATEST_PYTHON_VERSION%/python-%LATEST_PYTHON_VERSION%-amd64.exe

echo Instalando Python...
start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

echo Python instalado/atualizado com sucesso!
del python_installer.exe

:: Garante que o Python está no PATH
setx PATH "%PATH%;C:\Python%LATEST_PYTHON_VERSION%;C:\Python%LATEST_PYTHON_VERSION%\Scripts" >nul
refreshenv

goto :EOF
