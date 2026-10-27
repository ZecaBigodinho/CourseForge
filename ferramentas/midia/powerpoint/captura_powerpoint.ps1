# Funções para capturar telas do PowerPoint por automação (Fase 7). SÓ USE COM AUTORIZAÇÃO DO PROFESSOR.
# Mesma ideia de ferramentas/midia/excel/captura_excel.ps1. Uso no PowerShell (5.1):
#   . .\ferramentas\midia\powerpoint\captura_powerpoint.ps1
#   $p = NovoPowerPoint                 # abre o PowerPoint, apresentação nova, janela 1400x900 em (60,40)
#   Clicar x y / CliqueDireito x y      # coordenadas relativas ao canto da janela do PowerPoint
#   Capturar "nome"                     # PNG da janela do PowerPoint em $PASTA
#   Capturar "nome" ([Tela]::GetForegroundWindow())   # janela/diálogo em primeiro plano
#   Get-PowerPoint                      # reconecta ao PowerPoint aberto (o estado não passa entre chamadas)
# No fim: $p.ActivePresentation.Saved = -1; $p.ActivePresentation.Close(); $p.Quit()   (fecha SEM salvar)
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
if (-not ("Mouse" -as [type])) {
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Mouse {
  [DllImport("user32.dll")] public static extern bool SetCursorPos(int x, int y);
  [DllImport("user32.dll")] public static extern void mouse_event(int f, int x, int y, int d, int e);
  public static void Clique(int x, int y) { SetCursorPos(x, y); mouse_event(2,0,0,0,0); mouse_event(4,0,0,0,0); }
  public static void Direito(int x, int y) { SetCursorPos(x, y); mouse_event(8,0,0,0,0); mouse_event(16,0,0,0,0); }
}
"@
}
[void][Tela]::SetProcessDPIAware()
# Capturas vão para uma pasta temporária (fora do repositório)
$PASTA = Join-Path $env:TEMP "courseforge_capturas"
New-Item -ItemType Directory -Force $PASTA | Out-Null

function Get-PowerPoint { [Runtime.InteropServices.Marshal]::GetActiveObject("PowerPoint.Application") }
# Pela classe da janela principal (PPTFrameClass), e não pelo MainWindowHandle do processo,
# que pode apontar para uma dica de tela. Fica só com a janela visível.
if (-not ("JanelaPpt" -as [type])) {
Add-Type @"
using System; using System.Text; using System.Runtime.InteropServices;
public class JanelaPpt {
  public delegate bool CB(IntPtr h, IntPtr l);
  [DllImport("user32.dll")] static extern bool EnumWindows(CB cb, IntPtr l);
  [DllImport("user32.dll")] static extern int GetClassName(IntPtr h, StringBuilder s, int n);
  [DllImport("user32.dll")] static extern bool IsWindowVisible(IntPtr h);
  public static IntPtr Visivel() {
    IntPtr achada = IntPtr.Zero;
    EnumWindows((h, l) => {
      var s = new StringBuilder(64); GetClassName(h, s, 64);
      if (s.ToString() == "PPTFrameClass" && IsWindowVisible(h)) { achada = h; return false; }
      return true; }, IntPtr.Zero);
    return achada;
  }
}
"@
}
function HwndPpt { [JanelaPpt]::Visivel() }

function Capturar([string]$nome, [IntPtr]$janela = [IntPtr]::Zero) {
  if ($janela -eq [IntPtr]::Zero) { $janela = HwndPpt }
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

function Frente {
  $h = HwndPpt
  [void][Tela]::ShowWindow($h, 9); [void][Tela]::SetForegroundWindow($h)
  Start-Sleep -Milliseconds 600
}
function Teclas([string]$t) { Frente; [System.Windows.Forms.SendKeys]::SendWait($t); Start-Sleep -Milliseconds 900 }

# Cliques em coordenadas relativas ao canto da janela do PowerPoint
function Clicar([int]$x, [int]$y) {
  $h = HwndPpt; [void][Tela]::SetForegroundWindow($h); Start-Sleep -Milliseconds 300
  $r = New-Object Tela+RECT; [void][Tela]::GetWindowRect($h, [ref]$r)
  [Mouse]::Clique($r.Left + $x, $r.Top + $y); Start-Sleep -Milliseconds 900
  [Mouse]::SetCursorPos(5, 1075) | Out-Null  # tira o ponteiro de cima da janela
}
function CliqueDireito([int]$x, [int]$y) {
  $h = HwndPpt; [void][Tela]::SetForegroundWindow($h); Start-Sleep -Milliseconds 300
  $r = New-Object Tela+RECT; [void][Tela]::GetWindowRect($h, [ref]$r)
  [Mouse]::Direito($r.Left + $x, $r.Top + $y); Start-Sleep -Milliseconds 900
}

function NovoPowerPoint {
  $p = New-Object -ComObject PowerPoint.Application
  $p.Visible = -1  # msoTrue
  [void]$p.Presentations.Add(-1)
  Start-Sleep 2
  $p.WindowState = 1  # ppWindowNormal
  $h = [IntPtr]$p.HWND
  [void][Tela]::ShowWindow($h, 9)
  [void][Tela]::MoveWindow($h, 60, 40, 1400, 900, $true)
  [void][Tela]::SetForegroundWindow($h)
  Start-Sleep 1
  $p
}
