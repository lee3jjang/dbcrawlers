@ECHO OFF

@REM 변수 선언
set SPHINXBUILD=sphinx-build
set SOURCEDIR=source
set BUILDDIR=build

@REM 빌드
%SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR%

