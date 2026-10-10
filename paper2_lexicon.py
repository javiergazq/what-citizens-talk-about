# -*- coding: utf-8 -*-
"""Lexicons: the ORIGINAL lexicon and the FINAL lexicon, plus the detection functions.

The final lexicon was fixed before manual validation and not subsequently modified. Its
disambiguation rules were derived from a documented audit of substring over-matching in the
original lexicon (section 3 of `Paper2_analysis.ipynb`), and the final lexicon is the one
that was validated. The original lexicon is kept only for sensitivity analysis S2.

Internal names keep the historical suffixes: `*_ORIG` / version="orig" is the original
lexicon and `*_V2` / version="v2" is the final lexicon.

Disambiguation rules of the final lexicon:
  due                 -> due (full word boundary; excludes duele/dueño/duermen)
  lista               -> listas? de espera (full phrase; excludes especialista)
  cita                -> cita (initial word boundary; excludes felicitar/felicito,
                         keeps citación/citarme/citado)
  sala                -> excluded from Facilities when followed by "espera" or "de espera"
                         (that mention is captured by 'espera' in System/Management)
  información         -> requires an administrative anchor within +-3 tokens
  personal sanitario  -> removed from pat_profesionalidad (neutral phrase)
  atención recibida   -> removed from pat_gratitud (not an autonomous marker)
  pat_espera          -> rebuilt from unambiguous waiting/delay expressions; isolated
                         durations removed (dos horas, dos semanas, día siguiente,
                         toda mañana, hora media)
  auxiliar            -> unchanged (no clear semantic rule; over-represented in the
                         validation sample and its precision is reported)
"""
import re
import numpy as np

# ══════════════════════════════ ORIGINAL LEXICON ══════════════════════════════

ENT_ORIG = {
 "Médico": ["médico","médica","medico","doctor","doctora","facultativo","especialista","pediatra","cirujano"],
 "Enfermería": ["enfermero","enfermera","enfermería","auxiliar","due","enfermeros","enfermeras"],
 "Administrativos": ["administrativo","administrativa","recepción","mostrador","ventanilla","celador","secretaria","información","centralita"],
 "Sistema/Gestión": ["cita","citas","teléfono","telefono","telefónico","espera","lista","burocracia","agenda","app","salud responde","no cogen","no atienden"],
 "Instalaciones": ["sala","habitacion","habitación","limpieza","equipamiento","instalación","parking","aparcamiento","cafetería","infraestructura"],
 "Urgencias": ["urgencia","urgencias","triaje","triage","emergencia","emergencias"],
}

CON_ORIG = {
 "pat_acceso": ["cogen teléfono","cojan teléfono","nunca cogen","jamás cogen","nunca cogen teléfono","jamás cogen teléfono","llamando cogen","vergüenza cogen teléfono","salud cogen teléfono","teléfono centro salud","pedir cita","coger cita","dan cita","cita telefónica","pedir cita telefónica","contactar centro salud","llamar centro salud"],
 "pat_espera": ["sala espera","horas esperando","horas sala espera","dos horas","dos horas esperando","toda mañana","hora media","día siguiente","dos semanas","horas esperando urgencias"],
 "pat_evaluativo": ["peor centro","peor centro salud","vergüenza centro","vergüenza centro salud","vaya centro salud","cada vez peor","ganas trabajar","pocas ganas","deja desear","malas formas","pongo estrella"],
 "pat_sistema": ["sanidad pública","seguridad social","salud responde","hoja reclamaciones","falta personal"],
 "pat_gratitud": ["muchas gracias","mil gracias","muchísimas gracias","dar gracias","quiero agradecer","palabras agradecimiento","atención recibida","muchas gracias equipo","muchas gracias personal","quiero dar gracias","dar gracias equipo","dar gracias personal","quiero agradecer personal","palabras agradecimiento personal","solo palabras agradecimiento","gracias gracias gracias"],
 "pat_profesionalidad": ["buenos profesionales","grandes profesionales","gran profesional","buena atención","buen trato","trato recibido","personal sanitario","buena atención parte","buena atención personal","buen centro salud","mejor centro salud","médicos enfermeras auxiliares"],
 "pat_humanizacion": ["trato humano","calidad humana","trato tan humano","siempre atendido bien"],
}

# ═══════════════════════════════ FINAL LEXICON ════════════════════════════════

# Entities: substring terms without over-matching risk are kept; terms with a
# disambiguation rule become explicit regex patterns. 'auxiliar' is deliberately unchanged.
ENT_V2_SUBSTR = {
 "Médico": ["médico","médica","medico","doctor","doctora","facultativo","especialista","pediatra","cirujano"],
 "Enfermería": ["enfermero","enfermera","enfermería","auxiliar","enfermeros","enfermeras"],
 "Administrativos": ["administrativo","administrativa","recepción","mostrador","ventanilla","celador","secretaria","centralita"],
 "Sistema/Gestión": ["teléfono","telefono","telefónico","espera","burocracia","agenda","app","salud responde","no cogen","no atienden"],
 "Instalaciones": ["habitacion","habitación","limpieza","equipamiento","instalación","parking","aparcamiento","cafetería","infraestructura"],
 "Urgencias": ["urgencia","urgencias","triaje","triage","emergencia","emergencias"],
}

# Additional regex patterns per entity (disambiguation rules)
ENT_V2_REGEX = {
 "Enfermería": [r"\bdue\b"],                       # due -> the DUE abbreviation only
 "Sistema/Gestión": [r"\bcita", r"\blistas? de espera\b"],  # cita without felicitar; lista only in "lista de espera"
 "Instalaciones": [r"\bsalas?\b(?!\s+(?:de\s+)?espera)"],   # sala except "sala(s) (de) espera"
}

# Administrative anchor for 'información': must occur within 3 tokens.
INFO_ANCLAS = {"mostrador","ventanilla","recepción","recepcion","admisión","admision",
               "administración","administracion","administrativo","administrativa",
               "celador","secretaria","centralita","punto","servicio","personal"}

def _info_con_contexto(texto, ventana=3):
    """True if 'información' occurs within `ventana` tokens of an administrative anchor."""
    toks = texto.split()
    pos = [i for i, t in enumerate(toks) if t == "información"]
    if not pos:
        return False
    for i in pos:
        lo, hi = max(0, i - ventana), min(len(toks), i + ventana + 1)
        if INFO_ANCLAS & set(toks[lo:hi]):
            return True
    return False

# Discourse markers (final lexicon)
CON_V2 = dict(CON_ORIG)

# pat_profesionalidad: 'personal sanitario' removed
CON_V2["pat_profesionalidad"] = [p for p in CON_ORIG["pat_profesionalidad"]
                                 if p != "personal sanitario"]
# pat_gratitud: 'atención recibida' removed
CON_V2["pat_gratitud"] = [p for p in CON_ORIG["pat_gratitud"]
                          if p != "atención recibida"]

# pat_espera rebuilt from unambiguous waiting or delay expressions. Isolated durations
# (dos horas, dos semanas, día siguiente, toda mañana, hora media), whose meaning depends
# on context, are removed.
CON_V2["pat_espera"] = [
    # explicit waiting
    "sala espera", "salas espera",
    "horas esperando", "horas espera", "hora esperando",
    "tiempo espera", "tiempos espera",
    "lista espera", "listas espera",
    "mucha espera", "larga espera", "largas esperas", "demasiada espera",
    "esperando horas", "esperando hora",
    "llevo esperando", "llevamos esperando", "llevo hora", "llevo horas",
    "sigo esperando", "seguimos esperando", "estuve esperando", "estuvimos esperando",
    "hicieron esperar", "hacen esperar", "haciendo esperar",
    "esperar horas", "esperé horas", "esperar hora",
    # delay
    "retraso", "retrasos", "retrasa", "con retraso",
    "demora", "demoras", "demorado",
    "tardan", "tardaron", "tardó", "tarda mucho",
]

# ═════════════════════════════════ DETECTION ═════════════════════════════════

def detectar_entidades(serie_texto, version="v2"):
    """Return {entity: boolean array} for a Series of cleaned text. version: "v2" (final) or "orig"."""
    out = {}
    base = ENT_V2_SUBSTR if version == "v2" else ENT_ORIG
    for ent, terms in base.items():
        m = np.zeros(len(serie_texto), dtype=bool)
        if terms:
            m |= serie_texto.str.contains("|".join(re.escape(t) for t in terms),
                                          case=False, na=False, regex=True).to_numpy()
        if version == "v2":
            for pat in ENT_V2_REGEX.get(ent, []):
                m |= serie_texto.str.contains(pat, case=False, na=False, regex=True).to_numpy()
            if ent == "Administrativos":
                m |= serie_texto.apply(_info_con_contexto).to_numpy()
        out[ent] = m
    return out

def detectar_constructos(serie_texto, version="v2"):
    """Return {marker: boolean array} by phrase matching. version: "v2" (final) or "orig"."""
    base = CON_V2 if version == "v2" else CON_ORIG
    out = {}
    for con, frases in base.items():
        pat = "|".join(re.escape(f) for f in frases)
        out[con] = serie_texto.str.contains(pat, case=False, na=False, regex=True).to_numpy()
    return out

# Stricter alternative for 'cita' (not adopted), used only to quantify its recall cost
CITA_ESTRICTA = r"\bcitas?\b"
