# Servidor de comandos do CorelDRAW para capturas passo a passo. SÓ USE COM AUTORIZAÇÃO DO PROFESSOR.
# Por quê: o CorelDRAW aberto por COM fecha quando o PowerShell que o abriu termina, e a instância
# não aparece para outras chamadas (GetActiveObject falha). Este processo fica vivo, segura o
# CorelDRAW e executa, um por vez, os comandos que chegam como arquivos .ps1 na pasta de comandos.
#
# Iniciar (em segundo plano):  powershell -File servidor_corel.ps1
# Mandar comandos:             powershell -File cliente_corel.ps1 -Codigo '$c = NovoCorel'
# Encerrar:                    cliente_corel.ps1 -Codigo 'Sair'   (fecha os documentos sem salvar)
# Os comandos rodam no escopo deste script: variáveis ($c, $d...) passam de um comando para o outro.
. (Join-Path $PSScriptRoot "captura_corel.ps1")

$FILA = Join-Path $PASTA "fila"
New-Item -ItemType Directory -Force $FILA | Out-Null
Get-ChildItem $FILA -File | Remove-Item -Force
$global:Continuar = $true
function Sair { if ($global:CorelApp) { FecharSemSalvar }; $global:Continuar = $false; "servidor encerrado" }

"servidor pronto em $FILA"
while ($global:Continuar) {
  $cmd = Get-ChildItem $FILA -Filter "*.cmd.ps1" | Sort-Object Name | Select-Object -First 1
  if (-not $cmd) { Start-Sleep -Milliseconds 300; continue }
  $saida = $cmd.FullName -replace '\.cmd\.ps1$', '.out.txt'
  try {
    $codigo = [IO.File]::ReadAllText($cmd.FullName, [Text.Encoding]::UTF8)
    Remove-Item $cmd.FullName -Force
    $r = . ([ScriptBlock]::Create($codigo)) 2>&1 | Out-String -Width 200
  } catch { $r = "ERRO: " + $_.Exception.Message }
  $tmp = $saida -replace '\.out\.txt$', '.res'
  [IO.File]::WriteAllText($tmp, "$r", [Text.Encoding]::UTF8)
  Move-Item $tmp $saida -Force
}
