[Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12

Add-Type -AssemblyName System.Web

$ProgressPreference = 'SilentlyContinue'

$game_path = ""

Write-Host "$([char]0x6b63)$([char]0x5728)$([char]0x83b7)$([char]0x53d6)$([char]0x62bd)$([char]0x5361)$([char]0x5206)$([char]0x6790)$([char]0x94fe)$([char]0x63a5)..." -ForegroundColor Green
Write-Host " "

if ($args.Length -eq 0) {
    $app_data = [Environment]::GetFolderPath('ApplicationData')
    $locallow_path = "$app_data\..\LocalLow\miHoYo\$([char]0x5d29)$([char]0x574f)$([char]0xff1a)$([char]0x661f)$([char]0x7a79)$([char]0x94c1)$([char]0x9053)\"

    $log_path = "$locallow_path\Player.log"

    if (-Not [IO.File]::Exists($log_path)) {
        Write-Host "$([char]0x627e)$([char]0x4e0d)$([char]0x5230)$([char]0x65e5)$([char]0x5fd7)$([char]0x6587)$([char]0x4ef6)"  -ForegroundColor Red
        Write-Host "$([char]0x8bf7)$([char]0x786e)$([char]0x4fdd)$([char]0x6e38)$([char]0x620f)$([char]0x5b89)$([char]0x88c5)$([char]0x8def)$([char]0x5f84)$([char]0x6ca1)$([char]0x6709)$([char]0x4e2d)$([char]0x6587)"
        return
    }

    $log_lines = Get-Content $log_path -First 11

    if ([string]::IsNullOrEmpty($log_lines)) {
        $log_path = "$locallow_path\Player-prev.log"

        if (-Not [IO.File]::Exists($log_path)) {
            Write-Host "$([char]0x627e)$([char]0x4e0d)$([char]0x5230)$([char]0x65e5)$([char]0x5fd7)$([char]0x6587)$([char]0x4ef6)"  -ForegroundColor Red
            Write-Host "$([char]0x8bf7)$([char]0x786e)$([char]0x4fdd)$([char]0x6e38)$([char]0x620f)$([char]0x5b89)$([char]0x88c5)$([char]0x8def)$([char]0x5f84)$([char]0x6ca1)$([char]0x6709)$([char]0x4e2d)$([char]0x6587)"
            return
        }

        $log_lines = Get-Content $log_path -First 11
    }

    if ([string]::IsNullOrEmpty($log_lines)) {
        Write-Host "$([char]0x627e)$([char]0x4e0d)$([char]0x5230)$([char]0x65e5)$([char]0x5fd7)$([char]0x6587)$([char]0x4ef6)"  -ForegroundColor Red
        Write-Host "$([char]0x8bf7)$([char]0x786e)$([char]0x4fdd)$([char]0x6e38)$([char]0x620f)$([char]0x5b89)$([char]0x88c5)$([char]0x8def)$([char]0x5f84)$([char]0x6ca1)$([char]0x6709)$([char]0x4e2d)$([char]0x6587)"
        return
    }

    $log_lines = $log_lines.split([Environment]::NewLine)

    for ($i = 0; $i -lt 10; $i++) {
        $log_line = $log_lines[$i]

        if ($log_line.startsWith("Loading player data from ")) {
            $game_path = $log_line.replace("Loading player data from ", "").replace("data.unity3d", "")
            break
        }
    }
} else {
    $game_path = $args[0]
}

if ([string]::IsNullOrEmpty($game_path)) {
    Write-Host "$([char]0x627e)$([char]0x4e0d)$([char]0x5230)$([char]0x65e5)$([char]0x5fd7)$([char]0x6587)$([char]0x4ef6)"  -ForegroundColor Red
    Write-Host "$([char]0x8bf7)$([char]0x786e)$([char]0x4fdd)$([char]0x6e38)$([char]0x620f)$([char]0x5b89)$([char]0x88c5)$([char]0x8def)$([char]0x5f84)$([char]0x6ca1)$([char]0x6709)$([char]0x4e2d)$([char]0x6587)"
}

$copy_path = [IO.Path]::GetTempPath() + [Guid]::NewGuid().ToString()

Copy-Item -Path "$game_path/webCaches/Cache/Cache_Data/data_2" -Destination $copy_path
$cache_data = Get-Content -Encoding UTF8 -Raw $copy_path
Remove-Item -Path $copy_path

$cache_data_split = $cache_data -split '1/0/'

for ($i = $cache_data_split.Length - 1; $i -ge 0; $i--) {
    $line = $cache_data_split[$i]

    if ($line.StartsWith('http') -and $line.Contains("getGachaLog")) {
        $url = ($line -split "\0")[0]

        $res = Invoke-WebRequest -Uri $url -ContentType "application/json" -UseBasicParsing | ConvertFrom-Json

        if ($res.retcode -eq 0) {
            $uri = [Uri]$url
            $query = [Web.HttpUtility]::ParseQueryString($uri.Query)

            $keys = $query.AllKeys
            foreach ($key in $keys) {
                if ($key -eq "authkey") { continue }
                if ($key -eq "authkey_ver") { continue }
                if ($key -eq "sign_type") { continue }
                if ($key -eq "game_biz") { continue }
                if ($key -eq "lang") { continue }

                $query.Remove($key)
            }

            $latest_url = $uri.Scheme + "://" + $uri.Host + $uri.AbsolutePath + "?" + $query.ToString()

            Write-Output $latest_url
            Set-Clipboard -Value $latest_url
            Write-Host " "
            Write-Host "$([char]0x62bd)$([char]0x5361)$([char]0x5206)$([char]0x6790)$([char]0x5730)$([char]0x5740)$([char]0x83b7)$([char]0x53d6)$([char]0x6210)$([char]0x529f)$([char]0xff0c)$([char]0x5df2)$([char]0x7ecf)$([char]0x590d)$([char]0x5236)$([char]0x5230)$([char]0x526a)$([char]0x5207)$([char]0x677f)"-ForegroundColor Green
            Write-Host "****** $([char]0x5341)$([char]0x8fde)$([char]0x5fc5)$([char]0x4e2d)$([char]0xff01)$([char]0x5c0f)$([char]0x4fdd)$([char]0x5e95)$([char]0x4e0d)$([char]0x6b6a)$([char]0xff01) ******" -ForegroundColor DarkYellow
            return;
        }
    }
}

Write-Host "$([char]0x627e)$([char]0x4e0d)$([char]0x5230)$([char]0x65e5)$([char]0x5fd7)$([char]0x6587)$([char]0x4ef6)"  -ForegroundColor Red
Write-Host "$([char]0x8bf7)$([char]0x786e)$([char]0x4fdd)$([char]0x6e38)$([char]0x620f)$([char]0x5b89)$([char]0x88c5)$([char]0x8def)$([char]0x5f84)$([char]0x6ca1)$([char]0x6709)$([char]0x4e2d)$([char]0x6587)"
        