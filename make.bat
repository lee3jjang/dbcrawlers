@ECHO OFF

@REM 변수 선언
set SPHINXBUILD=sphinx-build
set SOURCEDIR=sphinx_source
set BUILDDIR=docs

@REM 빌드
%SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR%

