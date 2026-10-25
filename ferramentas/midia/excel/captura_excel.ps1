# Funções para capturar telas do Excel por automação (Fase 7). SÓ USE COM AUTORIZAÇÃO DO PROFESSOR.
# Mesma ideia de ferramentas/midia/word/captura_word.ps1. Uso no PowerShell (5.1):
#   . .\ferramentas\midia\excel\captura_excel.ps1
#   $x = NovoExcel                     # abre o Excel, pasta nova, janela 1400x900 em (60,40)
#   Clicar x y / CliqueDireito x y      # coordenadas relativas ao canto da janela do Excel
#   Capturar "nome" (HwndExcel)         # PNG da janela do Excel em $PASTA
#   Capturar "nome" ([Tela]::GetForegroundWindow())   # janela/diálogo em primeiro plano
#   Get-Excel                           # reconecta ao Excel aberto (o estado não passa entre chamadas)
# No fim: $x.DisplayAlerts = $false; $x.ActiveWorkbook.Close($false); $x.Quit()   (fecha SEM salvar)
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

function Get-Excel { [Runtime.InteropServices.Marshal]::GetActiveObject("Excel.Application") }
# Pela classe da janela principal (XLMAIN), e não pelo COM: com uma célula em edição o Excel
# recusa chamadas COM, e o MainWindowHandle do processo pode apontar para uma dica de tela.
# O Excel também cria uma XLMAIN invisível: fica só com a visível.
if (-not ("Janela" -as [type])) {
Add-Type @"
using System; using System.Text; using System.Runtime.InteropServices;
public class Janela {
  public delegate bool CB(IntPtr h, IntPtr l);
  [DllImport("user32.dll")] static extern bool EnumWindows(CB cb, IntPtr l);
  [DllImport("user32.dll")] static extern int GetClassName(IntPtr h, StringBuilder s, int n);
  [DllImport("user32.dll")] static extern bool IsWindowVisible(IntPtr h);
  public static IntPtr ExcelVisivel() {
    IntPtr achada = IntPtr.Zero;
    EnumWindows((h, l) => {
      var s = new StringBuilder(64); GetClassName(h, s, 64);
      if (s.ToString() == "XLMAIN" && IsWindowVisible(h)) { achada = h; return false; }
      return true; }, IntPtr.Zero);
    return achada;
  }
}
"@
}
function HwndExcel { [Janela]::ExcelVisivel() }

function Capturar([string]$nome, [IntPtr]$janela = [IntPtr]::Zero) {
  if ($janela -eq [IntPtr]::Zero) { $janela = HwndExcel }
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
  $h = HwndExcel
  [void][Tela]::ShowWindow($h, 9); [void][Tela]::SetForegroundWindow($h)
  Start-Sleep -Milliseconds 600
}
function Teclas([string]$t) { Frente; [System.Windows.Forms.SendKeys]::SendWait($t); Start-Sleep -Milliseconds 900 }

# Cliques em coordenadas relativas ao canto da janela do Excel
function Clicar([int]$x, [int]$y) {
  $h = HwndExcel; [void][Tela]::SetForegroundWindow($h); Start-Sleep -Milliseconds 300
  $r = New-Object Tela+RECT; [void][Tela]::GetWindowRect($h, [ref]$r)
  [Mouse]::Clique($r.Left + $x, $r.Top + $y); Start-Sleep -Milliseconds 900
  [Mouse]::SetCursorPos(5, 1075) | Out-Null  # tira o ponteiro de cima da janela
}
function CliqueDireito([int]$x, [int]$y) {
  $h = HwndExcel; [void][Tela]::SetForegroundWindow($h); Start-Sleep -Milliseconds 300
  $r = New-Object Tela+RECT; [void][Tela]::GetWindowRect($h, [ref]$r)
  [Mouse]::Direito($r.Left + $x, $r.Top + $y); Start-Sleep -Milliseconds 900
}

function NovoExcel {
  $x = New-Object -ComObject Excel.Application
  $x.Visible = $true
  [void]$x.Workbooks.Add()
  Start-Sleep 2
  $x.WindowState = -4143  # xlNormal
  $h = [IntPtr]$x.Hwnd
  [void][Tela]::ShowWindow($h, 9)
  [void][Tela]::MoveWindow($h, 60, 40, 1400, 900, $true)
  [void][Tela]::SetForegroundWindow($h)
  Start-Sleep 1
  $x
}
