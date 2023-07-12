for %%f in ("teams\*") do (
    python "main.py" "%%~ff"
)