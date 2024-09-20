@echo off
setlocal enabledelayedexpansion
:: Turn off command echoing to keep the output clean and enable delayed expansion for variables

:: Prompt the user to enter the file to be parsed (e.g., arcade_list.txt)
set /p file_to_parse="Enter the name of the file to parse (e.g., arcade_list.txt): "

:: Prompt the user to enter the source directory (where the files to copy are located)
set /p source_dir="Enter the source directory (e.g., D:\Files\roms): "

:: Prompt the user to enter the destination directory (where the files should be copied to)
set /p destination_dir="Enter the destination directory (e.g., D:\Files\roms_2): "

:: Check if the destination directory exists
:: If it does not exist, create the directory
if not exist "%destination_dir%" mkdir "%destination_dir%"

:: Read each line from the user-specified file and use it to copy files from the user-specified source directory to the user-specified destination directory
for /f "tokens=* delims=" %%a in ('type "%file_to_parse%"') do (

    :: Extract the filename without the extension (%%~na gives the filename without extension)
    set "filename=%%~na"
    
    :: Copy the file from source to destination
    xcopy /hrkvy "%source_dir%\%%a" "%destination_dir%\"

    :: Check if a directory with the same name as the file (without extension) exists in the source directory
    if exist "%source_dir%\!filename!" (
        :: Copy the matching directory and all its contents to the destination directory
        xcopy /e /i /hrkvy "%source_dir%\!filename!" "%destination_dir%\!filename!\"
    )
)

:: Return to the original directory
popd

:: Pause to allow the user to see the result
pause
