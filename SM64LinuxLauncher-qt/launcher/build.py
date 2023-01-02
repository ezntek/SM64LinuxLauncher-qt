import json

# function definitions

def parse_to_dict(custom_name: str,
                  repo: dict[str, str],
                  model_pack_folder: str,
                  texture_pack_folder: str,
                  rom_path: str,
                  region: str,
                  jobs: int,
                  additional_make_opts: str) -> dict[str, dict[str, str] | str | int | bool]:
    return {
        "repo": repo,
        "usingCustomName": False if custom_name == "" else True,
        "customName": custom_name,
        "romPath": rom_path,
        "romRegion": region,
        "jobs": jobs,
        "customTextures": False if texture_pack_folder == "" else True,
        "texturesPath": texture_pack_folder,
        "customModels": False if model_pack_folder == "" else True,
        "modelsPath": model_pack_folder,
        "additionalMakeOpts": additional_make_opts,
        "playable": False,
        "execPath": ""
    }

def parse_to_json(build_dict: dict[str, dict[str, str] | str | int | bool]) -> str:
    return json.dumps(build_dict)
