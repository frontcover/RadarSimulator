# Powershell script 
# Compile .ui file into .py file

$filenames = @("ui_main_screen")

foreach ($element in $filenames) {
    pyuic5 ui/xml/$element.ui -o ui/python/$element.py
    Write-Output "$element.ui -> $element.py"
}