$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Runtime.WindowsRuntime
[Windows.Storage.StorageFile, Windows.Storage, ContentType = WindowsRuntime] | Out-Null
[Windows.Data.Pdf.PdfDocument, Windows.Data.Pdf, ContentType = WindowsRuntime] | Out-Null
[Windows.Storage.Streams.InMemoryRandomAccessStream, Windows.Storage.Streams, ContentType = WindowsRuntime] | Out-Null
$asTask = [System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object { $_.Name -eq 'AsTask' -and $_.IsGenericMethod -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' } | Select-Object -First 1
function AwaitOp($operation, $type) {
    $task = $asTask.MakeGenericMethod($type).Invoke($null, @($operation))
    $task.Wait()
    return $task.Result
}
$file = AwaitOp ([Windows.Storage.StorageFile]::GetFileFromPathAsync('C:\Users\KCSK\Downloads\ล่าราคา_PriceHunter_สไลด์นำเสนอ_v4.pdf')) ([Windows.Storage.StorageFile])
$pdf = AwaitOp ([Windows.Data.Pdf.PdfDocument]::LoadFromFileAsync($file)) ([Windows.Data.Pdf.PdfDocument])
$out = Join-Path $PSScriptRoot 'reference-preview'
New-Item -ItemType Directory -Path $out -Force | Out-Null
$actionTask = [System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object { $_.Name -eq 'AsTask' -and -not $_.IsGenericMethod -and $_.GetParameters().Count -eq 1 } | Select-Object -First 1
for ($i=0; $i -lt $pdf.PageCount; $i++) {
    $page = $pdf.GetPage($i)
    $stream = New-Object Windows.Storage.Streams.InMemoryRandomAccessStream
    $action = $page.RenderToStreamAsync($stream)
    ($actionTask.Invoke($null, @($action))).Wait()
    $reader = [System.IO.WindowsRuntimeStreamExtensions]::AsStreamForRead($stream)
    $target = [System.IO.File]::Create((Join-Path $out ('page-{0:D2}.png' -f ($i+1))))
    $reader.CopyTo($target)
    $target.Dispose(); $reader.Dispose(); $stream.Dispose(); $page.Dispose()
}
Write-Output "Rendered $($pdf.PageCount) reference pages"
