# FFmpeg Auto-Installer for AI Clipper
# Run this script as Administrator

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   AI Clipper - FFmpeg Installer" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as administrator
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
$isAdmin = $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "ERROR: This script must be run as Administrator!" -ForegroundColor Red
    Write-Host "Please right-click and select 'Run as Administrator'" -ForegroundColor Yellow
    pause
    exit 1
}

# Create installation directory
$installDir = "C:\ffmpeg"
$binPath = Join-Path $installDir "bin"
$ffmpegExe = Join-Path $binPath "ffmpeg.exe"

if (-not (Test-Path $ffmpegExe)) {
    Write-Host "Installing FFmpeg to $installDir..." -ForegroundColor Yellow
    Write-Host ""

    # Download FFmpeg (using a reliable mirror)
    $downloadUrl = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    $zipFile = "$env:TEMP\ffmpeg.zip"

    Write-Host "Downloading FFmpeg..." -ForegroundColor Cyan
    Write-Host "URL: $downloadUrl" -ForegroundColor Gray
    try {
        Invoke-WebRequest -Uri $downloadUrl -OutFile $zipFile -UseBasicParsing
        Write-Host "Download complete!" -ForegroundColor Green
    }
    catch {
        Write-Host "ERROR: Failed to download FFmpeg!" -ForegroundColor Red
        Write-Host $_.Exception.Message -ForegroundColor Red
        pause
        exit 1
    }

    Write-Host ""
    Write-Host "Extracting FFmpeg..." -ForegroundColor Cyan

    # Create install directory
    New-Item -ItemType Directory -Force -Path $installDir | Out-Null

    # Extract zip
    try {
        # Use PowerShell's Expand-Archive for Windows 10+
        Expand-Archive -Path $zipFile -DestinationPath $env:TEMP -Force

        # Find the extracted folder (it has a version in the name)
        $extractedFolder = Get-ChildItem $env:TEMP | Where-Object { $_.Name -like "ffmpeg-*" -and $_.PSIsContainer } | Select-Object -First 1

        if ($extractedFolder) {
            # Move contents to install directory
            Copy-Item -Path "$($extractedFolder.FullName)\*" -Destination $installDir -Recurse -Force
            Write-Host "Extraction complete!" -ForegroundColor Green

            # Cleanup
            Remove-Item $extractedFolder.FullName -Recurse -Force
        }
        else {
            Write-Host "ERROR: Could not find extracted FFmpeg folder!" -ForegroundColor Red
            pause
            exit 1
        }
    }
    catch {
        Write-Host "ERROR: Failed to extract FFmpeg!" -ForegroundColor Red
        Write-Host $_.Exception.Message -ForegroundColor Red
        pause
        exit 1
    }

    # Cleanup zip file
    Remove-Item $zipFile -Force
}
else {
    Write-Host "FFmpeg already installed at $installDir" -ForegroundColor Green
}

# Verify installation
if (Test-Path $ffmpegExe) {
    Write-Host ""
    Write-Host "FFmpeg installed successfully!" -ForegroundColor Green

    # Get version
    $version = & $ffmpegExe -version 2>&1 | Select-Object -First 1
    Write-Host "Version: $version" -ForegroundColor Gray
}
else {
    Write-Host ""
    Write-Host "ERROR: FFmpeg installation failed!" -ForegroundColor Red
    pause
    exit 1
}

# Add to PATH
Write-Host ""
Write-Host "Adding FFmpeg to system PATH..." -ForegroundColor Cyan

# Get current PATH
$pathEntries = [Environment]::GetEnvironmentVariable("Path", "Machine") -split ';'

# Check if already in PATH
if ($binPath -notin $pathEntries) {
    # Add to PATH
    $newPath = ($pathEntries + $binPath) -join ';'
    [Environment]::SetEnvironmentVariable("Path", $newPath, "Machine")
    Write-Host "FFmpeg added to system PATH!" -ForegroundColor Green
}
else {
    Write-Host "FFmpeg already in PATH" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Installation Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "NOTE: You may need to restart your terminal" -ForegroundColor Yellow
Write-Host "or log out and back in for PATH changes to take effect." -ForegroundColor Yellow
Write-Host ""
Write-Host "To verify, run: ffmpeg -version" -ForegroundColor Cyan
Write-Host ""
pause
