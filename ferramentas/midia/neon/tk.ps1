# Funções para dirigir e capturar o Sistema Escolar (Tkinter) na Fase 7.
Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName System.Windows.Forms
if (-not ("TkW" -as [type])) {
Add-Type @"
using System; using System.Text; using System.Runtime.InteropServices;
public class TkW {
  public delegate bool CB(IntPtr h, IntPtr l);
  [DllImport("user32.dll")] public static extern bool EnumWindows(CB cb, IntPtr l);
  [DllImport("user32.dll")] public static extern int GetWindowText(IntPtr h, StringBuilder s, int n);
  [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out R r);
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
  [DllImport("user32.dll")] public static extern bool SetCursorPos(int x, int y);
  [DllImport("user32.dll")] public static extern void mouse_event(int f, int x, int y, int d, int e);
  [DllImport("dwmapi.dll")] public static extern int DwmGetWindowAttribute(IntPtr h, int a, out R r, int s);
  [StructLayout(LayoutKind.Sequential)] public struct R { public int L, T, Rr, B; }
  public static IntPtr Achar(string titulo) {
    IntPtr a = IntPtr.Zero;
    EnumWindows((h, l) => { var s = new StringBuilder(256); GetWindowText(h, s, 256);
      if (s.ToString() == titulo && IsWindowVisible(h)) { a = h; return false; } return true; }, IntPtr.Zero);
    return a;
  }
}
"@
}
[void][TkW]::SetProcessDPIAware()
$PASTA = Join-Path $env:TEMP "courseforge_capturas\neon"; New-Item -ItemType Directory -Force $PASTA | Out-Null

function Janela([string]$t) { [TkW]::Achar($t) }
function Ret([IntPtr]$h) { $r = New-Object TkW+R; [void][TkW]::DwmGetWindowAttribute($h, 9, [ref]$r, 16); $r }
function Frente([IntPtr]$h) { [void][TkW]::SetForegroundWindow($h); Start-Sleep -Milliseconds 400 }
function Clicar([IntPtr]$h, [int]$x, [int]$y) {
  Frente $h; $r = Ret $h; [void][TkW]::SetCursorPos($r.L + $x, $r.T + $y)
  [TkW]::mouse_event(2,0,0,0,0); [TkW]::mouse_event(4,0,0,0,0); Start-Sleep -Milliseconds 700
  [void][TkW]::SetCursorPos(5, 1075)
}
function Teclar([string]$t) { [System.Windows.Forms.SendKeys]::SendWait($t); Start-Sleep -Milliseconds 600 }
function Capturar([string]$nome, [IntPtr]$h) {
  $r = Ret $h; $w = $r.Rr - $r.L; $a = $r.B - $r.T
  $b = New-Object System.Drawing.Bitmap $w, $a; $g = [System.Drawing.Graphics]::FromImage($b)
  $g.CopyFromScreen($r.L, $r.T, 0, 0, $b.Size); $b.Save((Join-Path $PASTA "$nome.png")); $g.Dispose(); $b.Dispose()
  "$nome ($w x $a)"
}
