# Manda um comando ao servidor_corel.ps1 e mostra a resposta.
# Uso: powershell -File cliente_corel.ps1 -Codigo 'Capturar "nome"' [-Espera 120]
param([Parameter(Mandatory = $true)][string]$Codigo, [int]$Espera = 120)
$FILA = Join-Path $env:TEMP "courseforge_capturas\corel\fila"
if (-not (Test-Path $FILA)) { "servidor não está rodando"; exit 1 }
$id = Get-Date -Format "yyyyMMdd_HHmmss_fff"
$cmd = Join-Path $FILA "$id.cmd.ps1"
$out = Join-Path $FILA "$id.out.txt"
$tmp = Join-Path $FILA "$id.tmp"
[IO.File]::WriteAllText($tmp, $Codigo, (New-Object Text.UTF8Encoding $true))
Move-Item $tmp $cmd
$fim = (Get-Date).AddSeconds($Espera)
while (-not (Test-Path $out)) {
  if ((Get-Date) -gt $fim) { "sem resposta em $Espera s (o comando pode ainda estar rodando)"; exit 2 }
  Start-Sleep -Milliseconds 300
}
Get-Content $out -Encoding UTF8 -Raw
Remove-Item $out -Force
