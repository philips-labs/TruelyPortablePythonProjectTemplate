@echo OFF

:: state the python version you wish to use
set target_version=3.11.0

:: directories that are to be added to PYTHONPATH. Same level as Python
set source_dirs=source\src source\tests

:: The rest is standard.....

set STARTDIR="%~dp0"
set target_pythondir="%~dp0..\..\Python%target_version%"

IF EXIST %target_pythondir% call:create_update

IF EXIST "%~dp0\pyenv" call:pyenv_exists

git clone https://github.com/pyenv-win/pyenv-win pyenv
echo "pyenv dir created"

IF EXIST "%~dp0\pyenv" call:pyenv_exists

echo "please install git for windows from https://gitforwindows.org/"
echo "This allows the program to download the latest version of pyenv which will than get the Python Distribution"
call:END


:pyenv_exists
IF EXIST "%~dp0\pyenv\pyenv-win\versions\%target_version%" call:MOVING

echo "build %target_version%"

echo pyenv will produce pop-ups please click ok on them...sorry....
pause
::call pyenv\pyenv-win\bin\pyenv install %target_version%
call pyenv\pyenv-win\libexec\pyenv-install.vbs %target_version%

cd %STARTDIR%

IF EXIST "%~dp0\pyenv\pyenv-win\versions\%target_version%" call:MOVING
echo "Failed to get %target_version% Please look at errors to correct"
EXIT /b
:MOVING

move "%~dp0\pyenv\pyenv-win\versions\%target_version%"  %target_pythondir%


:create_update
REM Clean up unneeded directories if they exist
IF EXIST "%~dp0\pyenv" RMDIR /S /Q "%~dp0\pyenv" 

echo Creating Update

FOR %%a IN (%source_dirs%) DO (
IF NOT EXIST "%~dp0..\..\%%a" (mkdir "%~dp0..\..\%%a" )
)



%target_pythondir%\python.exe  "%~dp0\updatescriptfiles.py"

:END
CMD.EXE /k
