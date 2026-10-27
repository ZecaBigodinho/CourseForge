# Terminal de teste para capturas do módulo de Git (Fase 7). Uso no PowerShell (5.1):
#   . .\ferramentas\midia\git\terminal_git.ps1
#   $t = NovoTerminalGit "C:\Projetos\meu-primeiro-repo"   # abre uma janela do PowerShell nessa pasta
#   Digitar "git status"                                   # digita o comando na janela, tecla por tecla
#   Capturar "nome"                                        # PNG da janela em $PASTA
#   FecharTerminalGit                                       # fecha a janela e apaga a configuração de teste
# A janela usa GIT_CONFIG_GLOBAL apontando para um arquivo de teste (nome "Ana Souza", e-mail ana.souza@example.com — domínio reservado para exemplos; NUNCA use um e-mail noreply com número inventado: o número é o ID de uma conta real),
# então a configuração real do Git do computador NÃO é alterada. O prompt mostra só a pasta.
Add-Type -AssemblyName System.Drawing, System.Windows.Forms
if (-not ("TelaGit" -as [type])) {
Add-Type @"
using System; using System.Runtime.InteropServices;
public class TelaGit {
  [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool MoveWindow(IntPtr h, int x, int y, int w, int hh, bool r);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [StructLayout(LayoutKind.Sequential)] public struct RECT { public int Left, Top, Right, Bottom; }
}
"@
}
[void][TelaGit]::SetProcessDPIAware()
$PASTA = Join-Path $env:TEMP "courseforge_capturas"
New-Item -ItemType Directory -Force $PASTA | Out-Null
$CONFIG_TESTE = Join-Path $env:TEMP "courseforge_git_teste\gitconfig"

function NovoTerminalGit([string]$pasta, [int]$largura = 1100, [int]$altura = 700) {
  New-Item -ItemType Directory -Force (Split-Path $CONFIG_TESTE) | Out-Null
  Set-Content $CONFIG_TESTE "[user]`n`tname = Ana Souza`n`temail = ana.souza@example.com`n[init]`n`tdefaultBranch = main`n[core]`n`teditor = code --wait" -Encoding ascii
  New-Item -ItemType Directory -Force $pasta | Out-Null
  $setup = "`$env:GIT_CONFIG_GLOBAL='$CONFIG_TESTE'; Set-Location '$pasta'; function prompt { 'PS ' + (Get-Location).Path + '> ' }; `$host.UI.RawUI.WindowTitle='Windows PowerShell'; Clear-Host"
  $proc = Start-Process powershell -ArgumentList "-NoExit", "-NoProfile", "-Command", $setup -PassThru
  Start-Sleep 3
  $script:TerminalGit = $proc
  [void][TelaGit]::MoveWindow($proc.MainWindowHandle, 60, 40, $largura, $altura, $true)
  [void][TelaGit]::SetForegroundWindow($proc.MainWindowHandle)
  Start-Sleep 1
  $proc
}

function Digitar([string]$texto, [int]$espera = 1500) {
  $h = $script:TerminalGit.MainWindowHandle
  [void][TelaGit]::SetForegroundWindow($h); Start-Sleep -Milliseconds 300
  foreach ($ch in $texto.ToCharArray()) {
    [System.Windows.Forms.SendKeys]::SendWait(("$ch" -replace '([+^%~(){}\[\]])', '{$1}'))
    Start-Sleep -Milliseconds 20
  }
  [System.Windows.Forms.SendKeys]::SendWait("{ENTER}"); Start-Sleep -Milliseconds $espera
}

function Capturar([string]$nome) {
  $h = $script:TerminalGit.MainWindowHandle
  $r = New-Object TelaGit+RECT; [void][TelaGit]::GetWindowRect($h, [ref]$r)
  $w = $r.Right - $r.Left; $hh = $r.Bottom - $r.Top
  $bmp = New-Object System.Drawing.Bitmap $w, $hh
  $g = [System.Drawing.Graphics]::FromImage($bmp); $g.CopyFromScreen($r.Left, $r.Top, 0, 0, $bmp.Size)
  $arq = Join-Path $PASTA "$nome.png"; $bmp.Save($arq, [System.Drawing.Imaging.ImageFormat]::Png)
  $g.Dispose(); $bmp.Dispose(); "$arq ($w x $hh)"
}

function FecharTerminalGit {
  if ($script:TerminalGit) { Stop-Process -Id $script:TerminalGit.Id -ErrorAction SilentlyContinue }
  Remove-Item (Split-Path $CONFIG_TESTE) -Recurse -Force -ErrorAction SilentlyContinue
}
