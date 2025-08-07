
# 🎛️ Projet Synthétiseur Virtuel en Python

## 🧭 Objectif

Créer un **synthétiseur audio virtuel** avec une interface utilisateur, permettant de :

- Générer des sons à l’aide de **deux oscillateurs**
- Appliquer une **enveloppe ADSR**
- Ajouter un **filtre passe-bas**
- Appliquer des effets : **Delay** et **Reverb**
- Contrôler le son en cliquant sur un clavier visuel ou via un **clavier MIDI**

---

## 🧱 Architecture du projet

```
synthesizer_project/
├── main.py
├── audio/
│   ├── oscillator.py
│   ├── envelope.py
│   ├── filter.py
│   ├── effects.py
│   └── mixer.py
├── interface/
│   ├── ui.py
│   └── midi_input.py
├── utils/
│   └── audio_utils.py
├── assets/
│   └── presets.json
└── requirements.txt
```

---

## 🔊 Audio : Modules et Fonctionnalités

### Oscillateurs

- 2 oscillateurs indépendants
- Types : `sine`, `square`, `sawtooth`, `triangle`, `noise`
- Paramètres : `waveform`, `frequency`, `detune`, `volume`

### Enveloppe ADSR

- Paramètres : `attack`, `decay`, `sustain`, `release`
- Appliquée à l'amplitude du signal mixé

### Filtre passe-bas

- Type : Low-pass
- Paramètres : `cutoff_frequency`, `resonance`

### Effets audio

- **Delay** :
  - `time` (en ms)
  - `feedback`
  - `mix` (dry/wet)

- **Reverb** :
  - `room_size`
  - `damping`
  - `mix` (dry/wet)

---

## 🎚️ Mixage

- Addition des signaux des 2 oscillateurs
- Application de l’enveloppe
- Application du filtre
- Application des effets
- Envoi vers la sortie audio

---

## 🎹 Interface utilisateur (UI)

- Bibliothèque : `PyQt5`, `Tkinter` ou `Streamlit`
- Composants :
  - Choix de la forme d’onde pour chaque oscillateur
  - Sliders pour tous les paramètres audio
  - Clavier virtuel (1 ou 2 octaves) ou support MIDI
  - Boutons pour sauvegarder/charger les presets

---

## 💾 Presets utilisateur

Fichier JSON de configuration, exemple :

```json
{
  "osc1": {"waveform": "saw", "detune": 5, "volume": 0.8},
  "osc2": {"waveform": "square", "detune": -5, "volume": 0.7},
  "adsr": {"attack": 0.1, "decay": 0.3, "sustain": 0.7, "release": 0.4},
  "filter": {"cutoff": 1200, "resonance": 0.8},
  "effects": {"delay": {"time": 250, "feedback": 0.4, "mix": 0.3}, "reverb": {"room_size": 0.5, "mix": 0.3}}
}
```

---

## ✅ Checklist pour Codex

### 🔧 Mise en place

- [x] Créer le projet avec l'arborescence décrite
- [x] Ajouter les dépendances dans `requirements.txt` :
  ```
  numpy
  scipy
  sounddevice
  PyQt5
  audiolazy
  mido
  python-rtmidi
  ```

### 🔊 Implémentation audio

- [x] `oscillator.py` : Génération des formes d'onde
- [x] `envelope.py` : Calcul de l’enveloppe ADSR
- [x] `filter.py` : Implémentation d’un filtre passe-bas
- [x] `effects.py` : Delay et Reverb
- [x] `mixer.py` : Chaînage du signal complet

### 🎹 Interface

- [x] `ui.py` : Interface utilisateur avec contrôle de tous les paramètres
- [x] `midi_input.py` : Support MIDI (optionnel)

### 💾 Sauvegarde/chargement

- [x] Lecture/écriture des presets depuis un fichier JSON

### 🧪 Tests

- [x] Test des oscillateurs avec signal unique
- [x] Vérification du rendu audio avec effet delay/reverb
- [x] Synchronisation entre UI et moteur audio

---

## 🧠 Prompt à donner à Codex

```python
# Prompt à envoyer à Codex pour démarrer

Tu es Codex. Voici un document de spécifications pour un projet de synthétiseur audio en Python avec interface. Il est structuré par modules, avec une architecture claire et une checklist à suivre. Lis le document `synth_description.md` dans le repo, puis commence à créer les fichiers un par un à partir de la checklist. Commence par `oscillator.py` dans le dossier `audio/`. Tu créeras ensuite `envelope.py`, `filter.py`, etc., en suivant l'ordre de la checklist.

Objectif : avoir un synthétiseur fonctionnel et testable via l'interface définie dans `ui.py`. Utilise `numpy`, `sounddevice`, `PyQt5` et `scipy`.

Travaille étape par étape et coche chaque item de la checklist une fois terminé. Si un module dépend d’un autre, génère d’abord le module parent.
```
