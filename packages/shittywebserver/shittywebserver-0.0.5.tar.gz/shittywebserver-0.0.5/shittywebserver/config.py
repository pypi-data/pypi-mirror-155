from Configs import ConfigBase


class DEFAULT(ConfigBase):
    PORT: int = 8000
    HOST: str = "127.0.0.1"
    RANDOM_SEED: int = 33245435


class DOCKER(DEFAULT):
    HOST: str = "0.0.0.0"
