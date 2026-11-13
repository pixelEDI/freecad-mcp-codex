# FreeCAD MCP: Installation und erster Test

Mit [FreeCAD MCP](https://github.com/neka-nat/freecad-mcp) kann Codex Modelle direkt in FreeCAD erstellen und bearbeiten.

## 1. Installation (Arch Linux + Codex)

Voraussetzungen: FreeCAD, `uv` und Codex sind installiert.

```bash
git clone https://github.com/neka-nat/freecad-mcp.git
cd freecad-mcp
uv sync
mkdir -p ~/.local/share/FreeCAD/v1-1/Mod
cp -r addon/FreeCADMCP ~/.local/share/FreeCAD/v1-1/Mod/
codex mcp add freecad -- uv --directory "$PWD" run freecad-mcp --only-text-feedback
```

Der Add-on-Pfad gilt für die hier verwendete FreeCAD-Version 1.1.

## 2. Erster Test

1. FreeCAD neu starten und die Workbench **MCP Addon** auswählen.
2. Auf **Start RPC Server** klicken und FreeCAD geöffnet lassen.
3. Codex neu starten und mit `codex mcp list` prüfen, ob `freecad` eingetragen ist.
4. Diesen Auftrag an Codex geben:

   > Erstelle mit FreeCAD MCP ein neues Dokument und darin einen Würfel mit 20 mm Kantenlänge. Passe die Ansicht so an, dass der Würfel sichtbar ist.

Wenn der Würfel in FreeCAD erscheint, funktioniert die Verbindung.
Optional unter **FreeCAD MCP → Auto-Start Server** den automatischen Start aktivieren.

## Beispiel: XIAO ESP32-C5 Gehäuse

Ein zweiteiliges Gehäuse für die Platine **ohne angelötete Pinleisten**: 28,6 × 24 × 11 mm, mit USB-C-Aussparung, Lüftungsschlitzen und aufsteckbarem Deckel.
Als Vorlage dient dieses [STEP-Modell der Platine](https://grabcad.com/library/seeed-studio-xiao-esp32-c5-1).

Die Dateien liegen unter [codexmcptest/xiao_base/gehaeuse](codexmcptest/xiao_base/gehaeuse/):

- **XIAO_C5_Gehaeuse.FCStd**: geschlossenes Gehäuse in FreeCAD.
- **XIAO_C5_Explosionsansicht.FCStd**: Deckel angehoben, Platine sichtbar.
- **Base.stl / Deckel.stl**: für den Druck ausgerichtete Teile.
- **Base.step / Deckel.step**: zum Weiterbearbeiten.

Maße lassen sich im [build_enclosure.py](codexmcptest/xiao_base/build_enclosure.py) anpassen.

**Druck und Montage:** Als Ausgangspunkt PETG, 0,2 mm Schichthöhe und 3 Wandlinien verwenden. Bei Bedarf die USB-Öffnung lokal stützen. Platine mit USB zur Aussparung einlegen und den Deckel gleichmäßig aufdrücken. Durchführungen für Pinleisten oder Antennenkabel fehlen.

Die CAD-Prüfung ist dokumentiert in [geometrie_check.json](codexmcptest/xiao_base/gehaeuse/geometrie_check.json). Rastpassung und USB-Stecker müssen noch mit einem Probedruck geprüft werden.
