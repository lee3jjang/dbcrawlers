@ECHO OFF

@REM 스크립트 위치로 이동
pushd %~dp0

@REM SPHINXBUILD에 "sphinx-build" 할당
if "%SPHINXBUILD%" == "" (
    set SPHINXBUILD=sphinx-build
)
@REM SOURCEDIR, BUILDDIR 할당
set SOURCEDIR=sphinx_source
set BUILDDIR=docs

@REM %1에 아무 변수 없으면 help로 이동
if "%1" == "" goto help

%SPHINXBUILD% >NUL 2>NUL
if errorlevel 9009 (
	echo.
	echo.The 'sphinx-build' command was not found. Make sure you have Sphinx
	echo.installed, then set the SPHINXBUILD environment variable to point
	echo.to the full path of the 'sphinx-build' executable. Alternatively you
	echo.may add the Sphinx directory to PATH.
	echo.
	echo.If you don't have Sphinx installed, grab it from
	echo.http://sphinx-doc.org/
	exit /b 1
)

%SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR%
goto end

:help
%SPHINXBUILD% -M help %SOURCEDIR% %BUILDDIR%

:end
popd