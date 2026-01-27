Write-Host "==========================================" -ForegroundColor DarkGray
Write-Host " Behave + Selenium + Allure (PARALLEL RUN) " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor DarkGray

# ---------------------------------------------
# Go to project root (works in local & CI)
# ---------------------------------------------
$PROJECT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $PROJECT_DIR

Write-Host "Project directory:" (Get-Location) -ForegroundColor Gray

# ---------------------------------------------
# Activate virtual environment
# ---------------------------------------------
Write-Host "Enabling virtual environment..." -ForegroundColor Cyan
.\.venv\Scripts\Activate.ps1

# ---------------------------------------------
# Clean previous results
# ---------------------------------------------
Write-Host "Deleting old Allure results..." -ForegroundColor Cyan
Remove-Item reports\allure-results -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item reports\allure-report -Recurse -Force -ErrorAction SilentlyContinue

New-Item -ItemType Directory -Path reports\allure-results | Out-Null

# ---------------------------------------------
# Parallel execution
# ---------------------------------------------
Write-Host "Executing Features tests Behave in PARALLEL using Chrome..." -ForegroundColor Yellow

$jobs = @()

$jobs += Start-Job {
    Set-Location $using:PROJECT_DIR
    behave features/login.feature `
        -D browser=chrome `
        -f allure_behave.formatter:AllureFormatter `
        -o reports/allure-results/worker-1
}

$jobs += Start-Job {
    Set-Location $using:PROJECT_DIR
    behave features/cart.feature `
        -D browser=chrome `
        -f allure_behave.formatter:AllureFormatter `
        -o reports/allure-results/worker-2
}

$jobs += Start-Job {
    Set-Location $using:PROJECT_DIR
    behave features/checkout.feature `
        -D browser=chrome `
        -f allure_behave.formatter:AllureFormatter `
        -o reports/allure-results/worker-3
}

# ---------------------------------------------
# Wait for all jobs
# ---------------------------------------------
Write-Host "Waiting for parallel jobs to finish..." -ForegroundColor Cyan
Wait-Job $jobs
Receive-Job $jobs | Out-Host
Remove-Job $jobs

# ---------------------------------------------
# Generate Allure HTML report
# ---------------------------------------------
Write-Host "Generating Allure HTML report..." -ForegroundColor Cyan
cmd /c "allure generate reports/allure-results/* -o reports/allure-report"


# ---------------------------------------------
# Open Allure report (local only)
# ---------------------------------------------
Write-Host "Opening Allure report..." -ForegroundColor Green
cmd /c "allure open reports/allure-report"

Write-Host "==========================================" -ForegroundColor DarkGray
Write-Host " EXECUTION FINISHED SUCCESSFULLY " -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor DarkGray
