# App Icons

This folder contains application icons for AI Clipper.

## Required Icons

- `32x32.png` - Small icon
- `128x128.png` - Medium icon
- `128x128@2x.png` - High DPI icon
- `icon.ico` - Windows icon
- `icon.icns` - macOS icon (optional for Windows build)

## How to Create Icons

### Option 1: Online Icon Generator (Recommended)

1. Visit: https://realfavicongenerator.net/
2. Upload a 512x512 PNG logo/image
3. Download the generated icons
4. Extract and copy files to this folder
5. Rename as needed:
   - `android-chrome-192x192.png` → `128x128.png`
   - `android-chrome-512x512.png` → `128x128@2x.png`
   - `favicon.ico` → `icon.ico`

### Option 2: Using ImageMagick

```powershell
# Install ImageMagick first
# Then run:
magick convert logo.png -resize 32x32 32x32.png
magick convert logo.png -resize 128x128 128x128.png
magick convert logo.png -resize 256x256 128x128@2x.png
magick convert logo.png icon.ico
```

### Option 3: Manual Creation

Use any image editor (Photoshop, GIMP, Paint.NET) to create:
- 32x32 PNG
- 128x128 PNG
- 256x256 PNG (for 2x)
- ICO file (can contain multiple sizes)

## Placeholder Icons

For testing, you can create simple placeholder icons:

```powershell
# Using PowerShell to create simple colored squares
Add-Type -AssemblyName System.Drawing

# Create 128x128 placeholder
$bmp = New-Object System.Drawing.Bitmap 128, 128
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.Clear([System.Drawing.Color]::FromArgb(139, 92, 246)) # Purple
$font = New-Object System.Drawing.Font("Arial", 20, [System.Drawing.FontStyle]::Bold)
$g.DrawString("AI", $font, [System.Drawing.Brushes]::White, 30, 40)
$bmp.Save("128x128.png")
$g.Dispose()
$bmp.Dispose()
```

## Icon Design Guidelines

- Use a simple, recognizable logo
- Ensure good contrast
- Test on dark and light backgrounds
- Keep it minimal and modern
- Consider how it looks at small sizes (32x32)

## Current Status

⚠️ **Icons need to be created before building the installer**

You can use any of the options above to create the required icons.

## Suggested Logo Ideas

1. **Play button with AI spark** - Simple play button with sparkles
2. **Clip symbol with brain** - Film clip icon with brain/purple glow
3. **Video frame with AI** - Video frame outline with "AI" inside
4. **Camera with lightning** - Camera icon with purple lightning bolt
5. **Simple "AI Clipper" text** - Clean typography-based logo

For best results, hire a designer or use tools like:
- Canva (https://www.canva.com/)
- Figma (https://www.figma.com/)
- Adobe Illustrator
- Inkscape (free)

## Once Icons Are Ready

After adding icons to this folder, run:
```powershell
cd D:\clipper\frontend
npm run tauri:build
```

The icons will be automatically included in the installer.
