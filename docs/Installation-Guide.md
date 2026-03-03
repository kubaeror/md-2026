# Installation Guide

## Requirements

- **Hearts of Iron IV** v1.17.x
- **[Millennium Dawn: A Modern Day Mod](https://steamcommunity.com/sharedfiles/filedetails/?id=2777392649)** v1.12.3 or later

### Recommended DLCs

The mod is fully playable without any DLC. However, certain technology branches unlock additional content with these DLCs:

| DLC | Content Unlocked |
|-----|-----------------|
| **No Step Back** | Tank designer, advanced armor/artillery/AA/helicopter modules |
| **By Blood Alone** | Aircraft designer, airframe and module technologies |
| **Gotterdammerung** | Missile systems — ICBMs, IRBMs, cruise missiles, SAMs |
| **La Resistance** | Intelligence agency (replaces encryption/decryption) |

Without these DLCs, the mod falls back to equivalent non-DLC technology paths automatically.

---

## Steam Workshop Installation

*(Coming soon — Workshop page is not yet published)*

---

## Manual Installation

### Step 1: Download the Mod

**Option A — Git Clone:**
```bash
cd "Documents/Paradox Interactive/Hearts of Iron IV/mod/"
git clone https://github.com/kubaeror/md-2026.git
```

**Option B — ZIP Download:**
1. Go to [https://github.com/kubaeror/md-2026](https://github.com/kubaeror/md-2026)
2. Click **Code** > **Download ZIP**
3. Extract the `md-2026` folder into your HoI4 mod directory

### Step 2: Locate Your Mod Directory

| Platform | Path |
|----------|------|
| **Windows** | `Documents\Paradox Interactive\Hearts of Iron IV\mod\` |
| **Linux** | `~/.local/share/Paradox Interactive/Hearts of Iron IV/mod/` |
| **macOS** | `~/Documents/Paradox Interactive/Hearts of Iron IV/mod/` |

### Step 3: Create the Launcher File

Create a file named `md-2026.mod` in the `mod/` directory (next to the `md-2026/` folder) with the following content:

```
path="mod/md-2026"
version="1.0.0"
tags={
	"Alternative History"
	"Technologies"
	"Balance"
	"Fixes"
	"Ideologies"
	"Military"
	"Utilities"
	"National Focuses"
	"Map"
}
name="Millennium Dawn 2026 Rework"
supported_version="1.17.*"
dependencies={
	"Millennium Dawn: A Modern Day Mod"
}
replace_path="common/bookmarks"
```

### Step 4: Enable in Launcher

1. Open the Hearts of Iron IV launcher
2. Go to **Mods** (or **Playset**)
3. Enable **Millennium Dawn: A Modern Day Mod**
4. Enable **Millennium Dawn 2026 Rework**
5. Ensure the 2026 Rework loads **after** the base Millennium Dawn mod (it should do so automatically due to the `dependencies` declaration)

### Step 5: Launch and Play

1. Start the game
2. On the start screen, you should see **two bookmarks**:
   - **Millennium Dawn** (January 1, 2000) — the original
   - **MD 2026** (January 1, 2026) — the new bookmark
3. Select the 2026 bookmark and choose your country

---

## Updating the Mod

If installed via git:
```bash
cd "Documents/Paradox Interactive/Hearts of Iron IV/mod/md-2026"
git pull
```

If installed via ZIP, re-download and replace the folder.

---

## Uninstallation

1. Remove the `md-2026/` folder from your mod directory
2. Remove the `md-2026.mod` file from the mod directory
3. The original Millennium Dawn mod is unaffected
