# Create Windows ICO file from PNG
Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName System.IO

# Function to convert PNG to ICO
function ConvertTo-Ico {
    param(
        [string]$PngPath,
        [string]$IcoPath
    )

    # Load PNG
    $png = [System.Drawing.Image]::FromFile($PngPath)

    # Create memory stream for ICO
    $memoryStream = New-Object System.IO.MemoryStream

    # ICO header (6 bytes)
    $writer = New-Object System.IO.BinaryWriter($memoryStream)
    $writer.Write([UInt16]0)           # Reserved
    $writer.Write([UInt16]1)           # Type: 1 = ICO
    $writer.Write([UInt16]1)           # Number of images

    # Image directory entry (16 bytes per image)
    $width = 32
    $height = 32
    $colors = 0
    $reserved = 0
    $planes = 1
    $bitCount = 32
    $bytesInRes = 40 + ($width * $height * 4)
    $imageOffset = 22

    $writer.Write([byte]$width)
    $writer.Write([byte]$height)
    $writer.Write([byte]$colors)
    $writer.Write([byte]$reserved)
    $writer.Write([UInt16]$planes)
    $writer.Write([UInt16]$bitCount)
    $writer.Write([UInt32]$bytesInRes)
    $writer.Write([UInt32]$imageOffset)

    # Write the PNG data directly
    $pngData = [System.IO.File]::ReadAllBytes($PngPath)
    $writer.Write($pngData)

    # Save to file
    $bytes = $memoryStream.ToArray()
    [System.IO.File]::WriteAllBytes($IcoPath, $bytes)

    # Cleanup
    $writer.Close()
    $memoryStream.Close()
    $png.Dispose()

    Write-Host "Created $IcoPath" -ForegroundColor Green
}

# Create ICO file
$iconDir = "D:\clipper\frontend\src-tauri\icons"
$pngFile = Join-Path $iconDir "32x32.png"
$icoFile = Join-Path $iconDir "icon.ico"

if (Test-Path $pngFile) {
    ConvertTo-Ico -PngPath $pngFile -IcoPath $icoFile
} else {
    Write-Host "PNG file not found: $pngFile" -ForegroundColor Red
}
