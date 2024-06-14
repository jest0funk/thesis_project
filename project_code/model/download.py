from huggingface_hub import snapshot_download, hf_hub_download
import os


def single_model_download(model_ref, model_repo, local_dir):
    local_dir = os.path.join(local_dir, model_ref)
    if os.path.isdir(local_dir):
        print(f'Target exists. Skipping for local dir {local_dir}')
    else:
        print(f'>>> {model_ref}')
        if type(model_repo) == list:
            for model_file in model_repo:
                hf_hub_download(repo_id=model_file[0], filename=model_file[1], subfolder=model_file[2], local_dir=local_dir)
        else:
            snapshot_download(repo_id=model_repo, local_dir=local_dir)


def model_download(model_refs, local_dir, hf_source='inbox225710'):
    if type(model_refs) == dict:
        for model_ref, model_repo in model_refs.items():
            single_model_download(model_ref, model_repo, local_dir)
    else:
        for model_ref in model_refs:
            single_model_download(model_ref, f'{hf_source}/{model_ref}', local_dir)

