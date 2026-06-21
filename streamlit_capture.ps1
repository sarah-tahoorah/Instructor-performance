$log = 'c:\Users\SARAH\OneDrive\Instructor performance\streamlit.log'
$err = 'c:\Users\SARAH\OneDrive\Instructor performance\streamlit.err'
Get-Process -Name streamlit -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Process -FilePath 'C:\venvs\edupro_venv\Scripts\streamlit.exe' -ArgumentList "run 'c:\Users\SARAH\OneDrive\Instructor performance\streamlit_dashboard.py' --server.port 8501 --logger.level debug" -RedirectStandardOutput $log -RedirectStandardError $err -NoNewWindow
Start-Sleep -s 2
& 'C:\venvs\edupro_venv\Scripts\python.exe' 'c:\Users\SARAH\OneDrive\Instructor performance\fetch_streamlit_root.py'
Start-Sleep -s 1
Write-Output '---STDOUT---'
if (Test-Path $log) { Get-Content $log -Tail 200 -ErrorAction SilentlyContinue } else { Write-Output '(no stdout log yet)' }
Write-Output '---STDERR---'
if (Test-Path $err) { Get-Content $err -Tail 200 -ErrorAction SilentlyContinue } else { Write-Output '(no stderr log yet)' }
