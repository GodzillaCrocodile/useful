@net stop spooler
@del %WINDIR%\SYSTEM32\spool\Printers\*.* /q
@net start spooler