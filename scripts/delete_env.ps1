# Define common locations for virtual environments
$locations = @(
    "C:\Users\$env:USERNAME\Envs",
    "C:\Users\$env:USERNAME\.virtualenvs",
    "C:\dev\2024\py-skb\app"
)

# Loop through locations and delete folders named venv or .venv
foreach ($location in $locations) {
    if (Test-Path $location) {
        Get-ChildItem -Path $location -Directory -Recurse | Where-Object {
            $_.Name -match "^(venv|\.venv)$"
        } | ForEach-Object {
            Write-Output "Deleting: $($_.FullName)"
            Remove-Item -Recurse -Force -Path $_.FullName
        }
    }
}