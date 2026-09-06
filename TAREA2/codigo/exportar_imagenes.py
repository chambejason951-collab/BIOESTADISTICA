"""Renderiza las mismas páginas del carrusel PDF como PNG de 1920 x 1080.
Requiere pdfplumber y Pillow. No modifica el contenido ni recorta las páginas.
"""
from pathlib import Path
import json
import pdfplumber
R=Path(__file__).resolve().parents[1]
meta=json.loads((R/'linkedin/guion_carrusel.json').read_text())['paginas']
with pdfplumber.open(R/'linkedin/carrusel_tamano_muestra.pdf') as pdf:
    assert len(pdf.pages)==len(meta)==20
    for i,p in enumerate(pdf.pages):
        c=meta[i].get('caso','').lower()
        name=f"{i+1:02}_{c+'_' if c else ''}{meta[i]['tipo']}.png"
        img=p.to_image(width=1920).original.convert('RGB')
        assert img.size==(1920,1080), img.size
        img.save(R/'linkedin/imagenes'/name,optimize=True)
print('20 imágenes exportadas con el contenido exacto del PDF.')
