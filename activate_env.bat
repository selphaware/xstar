@echo off
echo Activating XSTAR Python Environment...
color 0c
CALL xstar_env\Scripts\activate
setx PYTHONPATH i:\xstar >NUL
set PYTHONPATH=i:\xstar
echo Complete.
