param([Parameter(Mandatory=$true)][string]$ImagePath,
      [Parameter(Mandatory=$true)][string]$ExpectedSHA256)
$ErrorActionPreference = 'Stop'
$Resolved = (Resolve-Path -LiteralPath $ImagePath).Path
if (-not $Resolved.EndsWith('.img.xz')) { throw 'This is not a compressed CubeHAOS image (.img.xz).' }
if (-not ($ExpectedSHA256 -match '^[0-9A-Fa-f]{64}$')) { throw 'ExpectedSHA256 must be 64 hexadecimal characters.' }
$Actual = (Get-FileHash -LiteralPath $Resolved -Algorithm SHA256).Hash
Write-Host ('Expected: ' + $ExpectedSHA256)
Write-Host ('Actual:   ' + $Actual)
if ($Actual -ine $ExpectedSHA256) { throw 'Image SHA256 differs. DO NOT FLASH.' }
Write-Host 'SHA256 verified. This verifies file integrity, NOT compatibility or hardware boot.'
