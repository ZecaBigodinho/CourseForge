# Funções para capturar telas do CorelDRAW por automação COM. SÓ USE COM AUTORIZAÇÃO DO PROFESSOR.
# Uso no PowerShell (5.1):  . .\ferramentas\midia\coreldraw\captura_corel.ps1
#   $c = NovoCorel                      # abre o CorelDRAW por COM, visível, janela 1400x900 em (60,40)
#   $d = NovoDoc                        # documento novo (A4 retrato, mm)
#   Clicar x y / CliqueDireito x y      # coordenadas relativas ao canto da janela do CorelDRAW
#   Capturar "nome"                     # PNG só da janela do CorelDRAW em $PASTA
#   Capturar "nome" ([Tela]::GetForegroundWindow())   # diálogo em primeiro plano
#   Get-Corel                           # a instância aberta por NovoCorel (só vale na MESMA chamada do
#                                       # PowerShell: rode cada rodada inteira num único script)
# No fim: FecharSemSalvar               # fecha os documentos SEM salvar e pede para sair
#         FecharPropaganda (em OUTRA chamada do PowerShell) # fecha a propaganda da avaliação
# Observação: uma janela do CorelDRAW aberta à mão (fora da automação) não aparece para o COM;
# por isso o script sempre abre a sua própria instância.
# Dados dos exemplos: sempre fictícios (Ana Souza, (11) 90000-0000, ana.souza@example.com).
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
if (-not ("Jan" -as [type])) {
Add-Type @"
using System; using System.Text; using System.Runtime.InteropServices; using System.Collections.Generic;
public class Jan {
  public delegate bool CB(IntPtr h, IntPtr l);
  [DllImport("user32.dll")] public static extern bool EnumWindows(CB cb, IntPtr l);
  [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h, out uint p);
  [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
  [DllImport("user32.dll")] public static extern int GetWindowText(IntPtr h, StringBuilder s, int n);
  [StructLayout(LayoutKind.Sequential)] public struct R { public int Left, Top, Right, Bottom; }
  [DllImport("dwmapi.dll")] public static extern int DwmGetWindowAttribute(IntPtr h, int a, out R r, int n);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out R r);
  // Janelas visíveis do processo: "hwnd|título"
  public static List<string> Lista(uint pid) { var o = new List<string>();
    EnumWindows((h,l)=>{ uint p; GetWindowThreadProcessId(h,out p); if(p==pid && IsWindowVisible(h)){ var s=new StringBuilder(256); GetWindowText(h,s,256); o.Add(h+"|"+s); } return true; }, IntPtr.Zero); return o; }
}
"@
}
[void][Tela]::SetProcessDPIAware()

# Capturas vão para uma pasta temporária (fora do repositório)
$PASTA = Join-Path $env:TEMP "courseforge_capturas\corel"
New-Item -ItemType Directory -Force $PASTA | Out-Null

# Constantes do CorelDRAW (cdrUnit / cdrPaperOrientation)
$cdrMillimeter = 3
$cdrPortrait = 0

function Get-Corel { $global:CorelApp }

function Get-JanelaCorel {
  Get-Process CorelDRW -ErrorAction SilentlyContinue |
    Where-Object { $_.MainWindowHandle -ne 0 } |
    Sort-Object StartTime -Descending | Select-Object -First 1
}

function HwndCorel {
  $c = Get-Corel
  try { $h = [IntPtr]$c.AppWindow.Handle; if ($h -ne [IntPtr]::Zero) { return $h } } catch {}
  (Get-JanelaCorel).MainWindowHandle
}

function Frente {
  $h = HwndCorel
  [void][Tela]::ShowWindow($h, 9)
  [void][Tela]::SetForegroundWindow($h)
  Start-Sleep -Milliseconds 600
}

function Capturar([string]$nome, [IntPtr]$janela = [IntPtr]::Zero) {
  if ($janela -eq [IntPtr]::Zero) { $janela = HwndCorel }
  $r = New-Object Jan+R
  # Limites visíveis (sem a borda invisível do Windows 10, que mostraria a área de trabalho)
  if ([Jan]::DwmGetWindowAttribute($janela, 9, [ref]$r, 16) -ne 0) { [void][Jan]::GetWindowRect($janela, [ref]$r) }
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

# Clique em coordenadas relativas ao canto da janela do CorelDRAW
function Clicar([int]$x, [int]$y) {
  $h = HwndCorel; [void][Tela]::SetForegroundWindow($h); Start-Sleep -Milliseconds 300
  $r = New-Object Tela+RECT; [void][Tela]::GetWindowRect($h, [ref]$r)
  [Mouse]::Clique($r.Left + $x, $r.Top + $y); Start-Sleep -Milliseconds 900
  [Mouse]::SetCursorPos(5, 1075) | Out-Null  # tira o ponteiro de cima da janela
}
function CliqueDireito([int]$x, [int]$y) {
  $h = HwndCorel; [void][Tela]::SetForegroundWindow($h); Start-Sleep -Milliseconds 300
  $r = New-Object Tela+RECT; [void][Tela]::GetWindowRect($h, [ref]$r)
  [Mouse]::Direito($r.Left + $x, $r.Top + $y); Start-Sleep -Milliseconds 900
}

# Acha uma janela visível do CorelDRAW pelo começo do título (ex.: "Criar um novo documento")
function JanelaPorTitulo([string]$titulo) {
  foreach ($p in @(Get-Process CorelDRW -ErrorAction SilentlyContinue)) {
    foreach ($l in [Jan]::Lista([uint32]$p.Id)) {
      $hw, $t = $l -split '\|', 2
      if ($t -like "$titulo*") { return [IntPtr][int64]$hw }
    }
  }
  [IntPtr]::Zero
}
# Clique em coordenadas relativas a uma janela qualquer (diálogo)
function ClicarEm([IntPtr]$h, [int]$x, [int]$y) {
  [void][Tela]::SetForegroundWindow($h); Start-Sleep -Milliseconds 400
  $r = New-Object Tela+RECT; [void][Tela]::GetWindowRect($h, [ref]$r)
  [Mouse]::Clique($r.Left + $x, $r.Top + $y); Start-Sleep -Milliseconds 900
  [Mouse]::SetCursorPos(5, 1075) | Out-Null
}
# Fecha avisos que o CorelDRAW abre sozinho (relatório de falhas, propaganda da avaliação)
function FecharAvisos {
  $h = JanelaPorTitulo "Relatório de falhas"
  if ($h -ne [IntPtr]::Zero) { [void][Tela]::SetForegroundWindow($h); Start-Sleep -Milliseconds 300; [System.Windows.Forms.SendKeys]::SendWait("{ESC}"); Start-Sleep 1 }
}

function NovoCorel {
  $c = New-Object -ComObject CorelDRAW.Application
  $c.Visible = $true
  $global:CorelApp = $c
  Start-Sleep 6
  FecharAvisos
  $h = HwndCorel
  [void][Tela]::ShowWindow($h, 9)
  [void][Tela]::MoveWindow($h, 60, 40, 1400, 900, $true)
  [void][Tela]::SetForegroundWindow($h)
  Start-Sleep 1
  $c
}

function NovoDoc {
  $c = Get-Corel
  $d = $c.CreateDocument()
  $d.Unit = $cdrMillimeter
  Start-Sleep 2
  $d
}

function FecharSemSalvar {
  $c = Get-Corel
  if ($null -eq $c) { return }
  foreach ($d in @($c.Documents)) { $d.Dirty = $false; $d.Close() }
  $c.Quit()
  $global:CorelApp = $null
}

# Ao sair, a versão de avaliação mostra uma propaganda (586x700). O clique em "Fechar" só funciona
# numa chamada do PowerShell DEPOIS da que abriu o CorelDRAW: rode FecharPropaganda em separado.
# Sair por ela é uma saída normal (evita o "Relatório de falhas" na próxima abertura).
function FecharPropaganda {
  for ($i = 0; $i -lt 20; $i++) {
    $h = JanelaPorTitulo "CorelDRAW Graphics Suite"
    if ($h -ne [IntPtr]::Zero) { ClicarEm $h 530 667; Start-Sleep 3 }
    if (-not (Get-Process CorelDRW -ErrorAction SilentlyContinue)) { return "CorelDRAW encerrado" }
    Start-Sleep 1
  }
  "CorelDRAW ainda aberto"
}
