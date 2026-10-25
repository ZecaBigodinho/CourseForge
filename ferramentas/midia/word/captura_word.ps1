# Funções para capturar telas do Word por automação (Fase 7). SÓ USE COM AUTORIZAÇÃO DO PROFESSOR.
# Uso no PowerShell (5.1):  . .\ferramentas\midia\word\captura_word.ps1
#   $w = NovoWord                      # abre o Word, documento novo, janela 1400x900 em (60,40)
#   Clicar x y / CliqueDireito x y      # coordenadas relativas ao canto da janela do Word
#   Capturar "nome" (HwndWord)          # PNG da janela do Word em $PASTA
#   Capturar "nome" ([Tela]::GetForegroundWindow())   # janela/diálogo em primeiro plano
#   Get-Word                            # reconecta ao Word aberto (o estado não passa entre chamadas)
# No fim: $w.ActiveDocument.Close(0); $w.Quit(0)   (fecha SEM salvar)
Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName System.Windows.Forms
if (-not ("Tela" -as [type])) {
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Tela {
  [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int c);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll")] public static extern bool MoveWindow(IntPtr h, int x, int y, int w, int hh, bool r);
  [StructLayout(LayoutKind.Sequential)] public struct RECT { public int Left, Top, Right, Bottom; }
}
"@
}
[void][Tela]::SetProcessDPIAware()
# Capturas vão para uma pasta temporária (fora do repositório)
$PASTA = Join-Path $env:TEMP "courseforge_capturas"
New-Item -ItemType Directory -Force $PASTA | Out-Null

function Get-Word { [Runtime.InteropServices.Marshal]::GetActiveObject("Word.Application") }

function Get-JanelaWord {
  Get-Process WINWORD -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
}

function Frente {
  $p = Get-JanelaWord
  [void][Tela]::ShowWindow($p.MainWindowHandle, 9)
  [void][Tela]::SetForegroundWindow($p.MainWindowHandle)
  Start-Sleep -Milliseconds 600
}

function Capturar([string]$nome, [IntPtr]$janela = [IntPtr]::Zero) {
  if ($janela -eq [IntPtr]::Zero) { $janela = (Get-JanelaWord).MainWindowHandle }
  $r = New-Object Tela+RECT
  [void][Tela]::GetWindowRect($janela, [ref]$r)
  $w = $r.Right - $r.Left; $h = $r.Bottom - $r.Top
  $bmp = New-Object System.Drawing.Bitmap $w, $h
  $g = [System.Drawing.Graphics]::FromImage($bmp)
  $g.CopyFromScreen($r.Left, $r.Top, 0, 0, $bmp.Size)
  $arq = Join-Path $PASTA "$nome.png"
  $bmp.Save($arq, [System.Drawing.Imaging.ImageFormat]::Png)
  $g.Dispose(); $bmp.Dispose()
  "$arq ($w x $h)"
}

function Teclas([string]$t) { Frente; [System.Windows.Forms.SendKeys]::SendWait($t); Start-Sleep -Milliseconds 900 }

if (-not ("Mouse" -as [type])) {
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Mouse {
  [DllImport("user32.dll")] public static extern bool SetCursorPos(int x, int y);
  [DllImport("user32.dll")] public static extern void mouse_event(int f, int x, int y, int d, int e);
  public static void Clique(int x, int y) { SetCursorPos(x, y); mouse_event(2,0,0,0,0); mouse_event(4,0,0,0,0); }
}
"@
}
function HwndWord { [IntPtr](Get-Word).ActiveWindow.Hwnd }
# Clique em coordenadas relativas ao canto da janela do Word
function Clicar([int]$x, [int]$y) {
  $h = HwndWord; [void][Tela]::SetForegroundWindow($h); Start-Sleep -Milliseconds 300
  $r = New-Object Tela+RECT; [void][Tela]::GetWindowRect($h, [ref]$r)
  [Mouse]::Clique($r.Left + $x, $r.Top + $y); Start-Sleep -Milliseconds 900
  [Mouse]::SetCursorPos(5, 1075) | Out-Null  # tira o ponteiro de cima da janela
}

if (-not ("Mouse2" -as [type])) {
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Mouse2 {
  [DllImport("user32.dll")] public static extern bool SetCursorPos(int x, int y);
  [DllImport("user32.dll")] public static extern void mouse_event(int f, int x, int y, int d, int e);
  public static void Direito(int x, int y) { SetCursorPos(x, y); mouse_event(8,0,0,0,0); mouse_event(16,0,0,0,0); }
}
"@
}
function CliqueDireito([int]$x, [int]$y) {
  $h = HwndWord; [void][Tela]::SetForegroundWindow($h); Start-Sleep -Milliseconds 300
  $r = New-Object Tela+RECT; [void][Tela]::GetWindowRect($h, [ref]$r)
  [Mouse2]::Direito($r.Left + $x, $r.Top + $y); Start-Sleep -Milliseconds 900
}
function NovoWord {
  $w = New-Object -ComObject Word.Application
  $w.Visible = $true
  [void]$w.Documents.Add()
  Start-Sleep 2
  $h = [IntPtr]$w.ActiveWindow.Hwnd
  $w.WindowState = 0
  [void][Tela]::ShowWindow($h, 9)
  [void][Tela]::MoveWindow($h, 60, 40, 1400, 900, $true)
  [void][Tela]::SetForegroundWindow($h)
  Start-Sleep 1
  $w
}
