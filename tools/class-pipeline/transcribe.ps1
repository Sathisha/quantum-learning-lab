<#
.SYNOPSIS
  Transcribe a class recording (or every new recording in a folder) with Docker.

.EXAMPLE
  .\tools\class-pipeline\transcribe.ps1 "C:\workspace\quantum-learning-lab\class material\week-02\lecture.mp4"
.EXAMPLE
  .\tools\class-pipeline\transcribe.ps1 "C:\workspace\quantum-learning-lab\class material\week-02" -Notes
.EXAMPLE
  .\tools\class-pipeline\transcribe.ps1 lecture.mp4 -Cpu -- --model medium.en
#>
param(
  [Parameter(Mandatory = $true, Position = 0)][string]$Path,
  [switch]$Notes,     # also write notes.md with the model loaded in LM Studio (start its server first)
  [switch]$Cpu,       # no NVIDIA GPU, or the GPU is busy
  [switch]$Rebuild,   # rebuild the image after the pipeline code changes
  [Parameter(ValueFromRemainingArguments = $true)][string[]]$Extra   # passed straight to class_pipeline.py
)
$ErrorActionPreference = "Stop"

$item = Get-Item -LiteralPath $Path
if ($item.PSIsContainer) {
  $env:MEDIA_DIR = $item.FullName
  $target = "/data"
} else {
  $env:MEDIA_DIR = $item.DirectoryName
  $target = "/data/" + $item.Name
}

$compose = Join-Path $PSScriptRoot "docker-compose.yml"
$service = if ($Cpu) { "transcribe-cpu" } else { "transcribe" }
$pipelineArgs = @($target)
if ($Notes) { $pipelineArgs += "--notes" }
if ($Extra) { $pipelineArgs += ($Extra | Where-Object { $_ -ne "--" }) }

if ($Rebuild) { docker compose -f $compose build }
Write-Host "Processing $($item.FullName) on $(if ($Cpu) {'CPU'} else {'GPU'})..."
docker compose -f $compose run --rm $service @pipelineArgs
if ($LASTEXITCODE -ne 0 -and -not $Cpu) {
  Write-Host "`nIf that failed with a GPU or 'nvidia' error, run again with -Cpu, or see README.md (GPU setup)."
}
