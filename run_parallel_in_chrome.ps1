$PROJECT_DIR = "C:\SeleniumPythonAutomationBDD"

Write-Host "Enabling virtual environment..." -ForegroundColor Cyan
Set-Location $PROJECT_DIR
.\.venv\Scripts\Activate.ps1

Write-Host "Deleting old results..." -ForegroundColor Cyan
Remove-Item reports\allure-results -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item reports\allure-report -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path reports\allure-results | Out-Null

Write-Host "Executing Features Scenarios in PARALLEL using Chrome..." -ForegroundColor Yellow

$jobs = @()

$jobs += Start-Job -ScriptBlock {
    Set-Location "C:\SeleniumPythonAutomationBDD"
    behave features/login.feature `
      -D browser=chrome `
      -f allure_behave.formatter:AllureFormatter `
      -o reports/allure-results/worker-1
}

$jobs += Start-Job -ScriptBlock {
    Set-Location "C:\SeleniumPythonAutomationBDD"
    behave features/cart.feature `
      -D browser=chrome `
      -f allure_behave.formatter:AllureFormatter `
      -o reports/allure-results/worker-2
}

$jobs += Start-Job -ScriptBlock {
    Set-Location "C:\SeleniumPythonAutomationBDD"
    behave features/checkout.feature `
      -D browser=chrome `
      -f allure_behave.formatter:AllureFormatter `
      -o reports/allure-results/worker-3
}

# ⏳ Wait to all jopbs
Wait-Job $jobs

# Show Output Behave
Receive-Job $jobs | Out-Host

Write-Host "Generating Allure HTML report..." -ForegroundColor Cyan
cmd /c "allure generate reports/allure-results/** -o reports/allure-report"

Write-Host "Opening Allure report..." -ForegroundColor Green
cmd /c "allure open reports/allure-report"
