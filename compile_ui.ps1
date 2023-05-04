# Powershell script 
# Compile .ui file into .py file

$filenames = @("ui_main_screen", "login")

foreach ($element in $filenames) {
    pyuic5 ui/xml/$element.ui -o ui/python/$element.py
    Write-Output "$element.ui -> $element.py"
}

pyrcc5 ui/xml/logo.qrc -o logo_rc.py
Write-Output "Compiled resource file"