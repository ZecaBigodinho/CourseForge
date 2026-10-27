# Captura de janelas por título (VS Code, GitHub Desktop) para o módulo de Git (Fase 7).
# SÓ USE COM AUTORIZAÇÃO DO PROFESSOR. Uso no PowerShell (5.1):
#   . .\ferramentas\midia\git\captura_janela.ps1
#   $JANELA = "Visual Studio Code"            # parte do título da janela que será usada
#   Posicionar                                # janela 1400x900 em (60,40), em primeiro plano
#   Clicar x y / CliqueDireito x y            # coordenadas relativas ao canto da janela
#   Teclas "^+g"                              # SendKeys para a janela
#   Capturar "nome"                           # PNG da janela em $PASTA
#   Capturar "nome" ([TelaJ]::GetForegroundWindow())   # diálogo em primeiro plano
Add-Type -AssemblyName System.Drawing, System.Windows.Forms
if (-not ("TelaJ" -as [type])) {
Add-Type @"
using System; using System.Text; using System.Runtime.InteropServices;
public class TelaJ {
  [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int c);
  [DllImport("user32.dll")] public static extern bool MoveWindow(IntPtr h, int x, int y, int w, int hh, bool r);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll")] public static extern bool SetCursorPos(int x, int y);
  [DllImport("user32.dll")] public static extern void mouse_event(int f, int x, int y, int d, int e);
  public delegate bool CB(IntPtr h, IntPtr l);
  [DllImport("user32.dll")] static extern bool EnumWindows(CB cb, IntPtr l);
  [DllImport("user32.dll")] static extern int GetWindowText(IntPtr h, StringBuilder s, int n);
  [DllImport("user32.dll")] static extern bool IsWindowVisible(IntPtr h);
  public static IntPtr PorTitulo(string parte) {
    IntPtr achada = IntPtr.Zero;
    EnumWindows((h, l) => {
      var s = new StringBuilder(512); GetWindowText(h, s, 512);
      if (IsWindowVisible(h) && s.ToString().Contains(parte)) { achada = h; return false; }
      return true; }, IntPtr.Zero);
    return achada;
  }
  [StructLayout(LayoutKind.Sequential)] public struct RECT { public int Left, Top, Right, Bottom; }
}
"@
}
[void][TelaJ]::SetProcessDPIAware()
$PASTA = Join-Path $env:TEMP "courseforge_capturas"
New-Item -ItemType Directory -Force $PASTA | Out-Null
if (-not $JANELA) { $JANELA = "Visual Studio Code" }

# Prefere a janela principal do processo (o VS Code tem janelas invisíveis com o mesmo título)
function Hwnd {
  $proc = Get-Process | Where-Object { $_.MainWindowTitle -like "*$JANELA*" } | Select-Object -First 1
  if ($proc) { return $proc.MainWindowHandle }
  [TelaJ]::PorTitulo($JANELA)
}
function Posicionar([int]$largura = 1400, [int]$altura = 900) {
  $h = Hwnd; [void][TelaJ]::ShowWindow($h, 9); [void][TelaJ]::MoveWindow($h, 60, 40, $largura, $altura, $true)
  [void][TelaJ]::SetForegroundWindow($h); Start-Sleep 1
}
function Frente { $h = Hwnd; [void][TelaJ]::SetForegroundWindow($h); Start-Sleep -Milliseconds 500 }
function Teclas([string]$t) { Frente; [System.Windows.Forms.SendKeys]::SendWait($t); Start-Sleep -Milliseconds 900 }
function Escrever([string]$texto) {
  Frente
  foreach ($ch in $texto.ToCharArray()) { [System.Windows.Forms.SendKeys]::SendWait(("$ch" -replace '([+^%~(){}\[\]])', '{$1}')); Start-Sleep -Milliseconds 20 }
}
function Clicar([int]$x, [int]$y) {
  $h = Hwnd; [void][TelaJ]::SetForegroundWindow($h); Start-Sleep -Milliseconds 300
  $r = New-Object TelaJ+RECT; [void][TelaJ]::GetWindowRect($h, [ref]$r)
  [void][TelaJ]::SetCursorPos($r.Left + $x, $r.Top + $y); [TelaJ]::mouse_event(2, 0, 0, 0, 0); [TelaJ]::mouse_event(4, 0, 0, 0, 0)
  Start-Sleep -Milliseconds 900; [void][TelaJ]::SetCursorPos(5, 1075)
}
function CliqueDireito([int]$x, [int]$y) {
  $h = Hwnd; [void][TelaJ]::SetForegroundWindow($h); Start-Sleep -Milliseconds 300
  $r = New-Object TelaJ+RECT; [void][TelaJ]::GetWindowRect($h, [ref]$r)
  [void][TelaJ]::SetCursorPos($r.Left + $x, $r.Top + $y); [TelaJ]::mouse_event(8, 0, 0, 0, 0); [TelaJ]::mouse_event(16, 0, 0, 0, 0)
  Start-Sleep -Milliseconds 900
}
function Capturar([string]$nome, [IntPtr]$janela = [IntPtr]::Zero) {
  if ($janela -eq [IntPtr]::Zero) { $janela = Hwnd }
  $r = New-Object TelaJ+RECT; [void][TelaJ]::GetWindowRect($janela, [ref]$r)
  $w = $r.Right - $r.Left; $hh = $r.Bottom - $r.Top
  $bmp = New-Object System.Drawing.Bitmap $w, $hh
  $g = [System.Drawing.Graphics]::FromImage($bmp); $g.CopyFromScreen($r.Left, $r.Top, 0, 0, $bmp.Size)
  $arq = Join-Path $PASTA "$nome.png"; $bmp.Save($arq, [System.Drawing.Imaging.ImageFormat]::Png)
  $g.Dispose(); $bmp.Dispose(); "$arq ($w x $hh)"
}
