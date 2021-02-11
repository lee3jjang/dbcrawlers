@ECHO OFF

@REM 변수 선언
set SPHINXBUILD=sphinx-build
set SOURCEDIR=sphinx_source
set BUILDDIR=docs

@REM docs 폴더 비우기
rmdir /s /q %BUILDDIR%

@REM 빌드
%SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR%

@REM docs/html 파일 및 폴더들을 docs로 이동
for %%I in (%BUILDDIR%/html/*) do (
	move /y %BUILDDIR%\html\%%I %BUILDDIR% >nul 2>nul
)

for /d %%I in (%BUILDDIR%/html/*) do (
	move /y %BUILDDIR%\html\%%I %BUILDDIR% >nul 2>nul
)

rmdir %BUILDDIR%\html
