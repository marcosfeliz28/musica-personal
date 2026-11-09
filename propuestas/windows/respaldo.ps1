<#
.SYNOPSIS
  Respaldo y restauración de Música personal. PROPUESTA, no activa.

.DESCRIPTION
  Respaldar:  detiene Navidrome, guarda data\ en un .zip, copia la música sin comprimir
              (robocopy /E, que nunca borra nada en el destino) y copia .env. Navidrome se
              vuelve a iniciar siempre, aunque algo falle.
  Restaurar:  detiene Navidrome, renombra data\ a data.bak-<fecha>, extrae el .zip y,
              con -ConMusica, copia la música de vuelta. No borra nada: lo anterior queda en .bak.

  Por qué no se comprime la música: Compress-Archive limita el tamaño máximo a 2 GB e ignora
  archivos ocultos (documentación de Microsoft). data\ es pequeño y sí va en .zip.

  El destino contiene .env (secreto): usa un disco tuyo y, si puedes, cifrado.

.EXAMPLE
  .\propuestas\windows\respaldo.ps1 -Accion Respaldar -Destino D:\respaldos
  .\propuestas\windows\respaldo.ps1 -Accion Restaurar -Destino D:\respaldos -ConMusica
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory)][ValidateSet('Respaldar', 'Restaurar')][string]$Accion,
    [Parameter(Mandatory)][string]$Destino,
    [string]$Repo = (Get-Location).Path,
    [switch]$ConMusica,
    [switch]$SinDocker   # solo para pruebas: no toca Docker
)
$ErrorActionPreference = 'Stop'

function Copiar-Arbol($origen, $destino) {
    if (-not (Test-Path -LiteralPath $origen)) { return }
    New-Item -ItemType Directory -Force -Path $destino | Out-Null
    if (Get-Command robocopy -ErrorAction SilentlyContinue) {
        & robocopy $origen $destino /E /R:1 /W:1 /NFL /NDL /NJH /NJS /NP | Out-Null
        if ($LASTEXITCODE -ge 8) { throw "robocopy falló con código $LASTEXITCODE" }   # 0-7 = éxito
        $global:LASTEXITCODE = 0
    } else {
        Get-ChildItem -LiteralPath $origen -Force | Copy-Item -Destination $destino -Recurse -Force
    }
}

function Docker-Navidrome($verbo) {
    if ($SinDocker) { Write-Host "[prueba] docker compose $verbo navidrome (omitido)"; return }
    Push-Location $Repo
    try { & docker compose $verbo navidrome; if ($LASTEXITCODE -ne 0) { throw "docker compose $verbo falló" } }
    finally { Pop-Location }
}

$data  = Join-Path $Repo 'data'
$local = Join-Path $Repo 'music/local'
$gratis = Join-Path $Repo 'music/gratis'
if ($Accion -eq 'Respaldar' -and -not (Test-Path -LiteralPath $data)) { throw "No encuentro $data. ¿Estás en la raíz del repo? Usa -Repo." }
New-Item -ItemType Directory -Force -Path $Destino | Out-Null

if ($Accion -eq 'Respaldar') {
    $fecha = Get-Date -Format 'yyyy-MM-dd_HHmm'
    $zip = Join-Path $Destino "data-$fecha.zip"
    Docker-Navidrome 'stop'
    try {
        Compress-Archive -LiteralPath $data -DestinationPath $zip
        Copiar-Arbol $local  (Join-Path $Destino 'music/local')
        Copiar-Arbol $gratis (Join-Path $Destino 'music/gratis')
        $env = Join-Path $Repo '.env'
        if (Test-Path -LiteralPath $env) { Copy-Item -LiteralPath $env -Destination (Join-Path $Destino ".env-$fecha") }
        $hash = (Get-FileHash -LiteralPath $zip -Algorithm SHA256).Hash
        Set-Content -LiteralPath (Join-Path $Destino "data-$fecha.sha256") -Value "$hash  data-$fecha.zip"
        Write-Host "Respaldo OK: $zip"
    }
    finally { Docker-Navidrome 'start' }
}
else {
    $zip = Get-ChildItem -LiteralPath $Destino -Filter 'data-*.zip' | Sort-Object Name | Select-Object -Last 1
    if (-not $zip) { throw "No hay data-*.zip en $Destino" }
    $esperado = Join-Path $Destino ($zip.BaseName + '.sha256')
    if (Test-Path -LiteralPath $esperado) {
        $ok = ((Get-Content -LiteralPath $esperado -Raw).Split(' ')[0].Trim()) -eq (Get-FileHash -LiteralPath $zip.FullName -Algorithm SHA256).Hash
        if (-not $ok) { throw "La suma SHA-256 de $($zip.Name) no coincide: el respaldo está dañado." }
    } else { Write-Warning "Sin archivo .sha256: no se pudo comprobar la integridad." }
    Docker-Navidrome 'stop'
    try {
        $bak = "$data.bak-" + (Get-Date -Format 'yyyy-MM-dd_HHmm')
        if (Test-Path -LiteralPath $data) { Rename-Item -LiteralPath $data -NewName (Split-Path $bak -Leaf) }
        else { $bak = '(no había data\ previa)' }
        Expand-Archive -LiteralPath $zip.FullName -DestinationPath $Repo
        if ($ConMusica) {
            Copiar-Arbol (Join-Path $Destino 'music/local')  $local
            Copiar-Arbol (Join-Path $Destino 'music/gratis') $gratis
        }
        Write-Host "Restaurado desde $($zip.Name). Lo anterior quedó en $bak"
    }
    finally { Docker-Navidrome 'start' }
}
