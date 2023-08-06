from processrepo.ProcessRunProfile import ProcessRunProfile


def serialize_process_run_profile(process_run_profile: ProcessRunProfile) -> dict:
    serialized = {
        'run_profile': process_run_profile.run_profile.value,
        'enabled': process_run_profile.enabled
    }
    return serialized
