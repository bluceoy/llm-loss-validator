from huggingface_hub import HfApi
from loguru import logger

#api = HfApi()
api = HfApi(endpoint="https://hf-mirror.com")


def download_lora_config(repo_id: str, revision: str) -> bool:
    try:
        api.hf_hub_download(
            repo_id=repo_id,
            filename="adapter_config.json",
            local_dir="lora",
            revision=revision
        )
    except Exception as e:
        if "adapter_config.json" in str(e):
            logger.info("No adapter_config.json found in the repo, assuming full model")
            return False
        else:
            raise  # Re-raise the exception if it's not related to the missing file
    return True


def download_lora_repo(repo_id: str, revision: str) -> None:
    api.snapshot_download(repo_id=repo_id, local_dir="lora", revision=revision)
