from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pinecone import Pinecone
import pinecone as pinecone_pkg
import os
from src.config import Config

router = APIRouter()
config = Config()

def _to_primitive(v):
    # samo int/float/bool/None/str
    if isinstance(v, (int, float, bool)) or v is None:
        return v
    return str(v)

@router.get("/test-pinecone")
async def test_pinecone():
    api_key = config.pinecone_api_key or os.getenv("PINECONE_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="Pinecone API key is not set.")

    # v7 klijent
    pc = Pinecone(api_key=api_key)

    index_name = (
        getattr(config, "pinecone_index_name", None)
        or os.getenv("PINECONE_INDEX")
        or "knowledge-base"
    )

    out = {
        "status": "success",
        "sdk_version": _to_primitive(getattr(pinecone_pkg, "__version__", None)),
        "index": _to_primitive(index_name),
        "indexes": [],           # samo imena
        "details": {},           # samo primitivna polja
    }

    # list indexes -> samo imena kao stringovi
    try:
        idxs = pc.list_indexes() or []
        names = []
        for it in idxs:
            if isinstance(it, dict):
                names.append(str(it.get("name", "")))
            else:
                name = getattr(it, "name", None)
                names.append(str(name if name is not None else it))
        out["indexes"] = [n for n in names if n]
    except Exception as e:
        out["indexes_error"] = str(e)

    # describe -> izvuci samo dimension/metric (ostalo kao raw string)
    try:
        desc = pc.describe_index(index_name)
        if isinstance(desc, dict):
            dim = desc.get("dimension", None)
            met = desc.get("metric", None)
            out["details"] = {
                "dimension": int(dim) if isinstance(dim, (int, str)) and str(dim).isdigit() else _to_primitive(dim),
                "metric": _to_primitive(met),
            }
        else:
            # objekt – pokušaj preko atributa; sve pretvori u primitivno
            dim = getattr(desc, "dimension", None)
            met = getattr(desc, "metric", None)
            if dim is not None or met is not None:
                out["details"] = {
                    "dimension": int(dim) if isinstance(dim, (int, str)) and str(dim).isdigit() else _to_primitive(dim),
                    "metric": _to_primitive(met),
                }
            else:
                out["details"] = {"raw": str(desc)}
    except Exception as e:
        out["details"] = {"error": str(e)}

    return JSONResponse(out)
