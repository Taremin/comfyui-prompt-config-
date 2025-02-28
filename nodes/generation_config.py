from nodes import KSampler, EmptyLatentImage
from ..extranetwork_param import ExtraNetworksParam

TRIGGER = "config"

KSamplerInputTypes = KSampler.INPUT_TYPES()
EmptyLatentImageInputTypes = EmptyLatentImage.INPUT_TYPES()


class PromptGenerationConfig:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "width": EmptyLatentImageInputTypes["required"]["width"],
                "height": EmptyLatentImageInputTypes["required"]["height"],
                "steps": KSamplerInputTypes["required"]["steps"],
                "cfg": KSamplerInputTypes["required"]["cfg"],
                "sampler_name": KSamplerInputTypes["required"]["sampler_name"],
                "scheduler": KSamplerInputTypes["required"]["scheduler"],
                "denoise": KSamplerInputTypes["required"]["denoise"],
                "prompt": (
                    "STRING",
                    {"multiline": True, "forceInput": True},
                ),
            }
        }

    RETURN_TYPES = (
        "INT",
        "INT",
        "INT",
        "FLOAT",
        KSamplerInputTypes["required"]["sampler_name"][0],
        KSamplerInputTypes["required"]["scheduler"][0],
        "FLOAT",
        "STRING",
        "STRING",
    )
    RETURN_NAMES = (
        "width",
        "height",
        "steps",
        "cfg",
        "sampler_name",
        "scheduler",
        "denoise",
        "replaced_string",
        "original_string",
    )
    FUNCTION = "process"
    CATEGORY = "prompt-config"

    def cast(self, type: str, value: str):
        if type == "STRING":
            return str(value)
        if type == "INT":
            return int(value)
        if type == "FLOAT":
            return float(value)

        return value

    def process(self, *args, **kwargs):
        replaced_prompt, extra_networks = ExtraNetworksParam.parse(
            prompt=kwargs["prompt"]
        )
        input_types_required = self.INPUT_TYPES()["required"]

        for required_key in input_types_required.keys():
            if kwargs[required_key] is None:
                raise KeyError(f"required input[{required_key}] is None")

        if TRIGGER in extra_networks:
            configs = extra_networks[TRIGGER]

            for config in configs:
                # named
                for key, value in config.named.items():
                    if key not in input_types_required:
                        print(f"Invalid config key(not in input types): {key}")
                        continue
                    if key not in kwargs:
                        print(f"Invalid config key(not in kwargs): {key}")
                        continue
                    kwargs[key] = self.cast(input_types_required[key][0], value)

                # positional
                if len(config.positional) == 0:
                    continue

                if config.positional[0] == "swap":
                    kwargs["width"], kwargs["height"] = (
                        kwargs["height"],
                        kwargs["width"],
                    )

        return (
            kwargs["width"],
            kwargs["height"],
            kwargs["steps"],
            kwargs["cfg"],
            kwargs["sampler_name"],
            kwargs["scheduler"],
            kwargs["denoise"],
            replaced_prompt,
            kwargs["prompt"],
        )


NODE_CLASS_MAPPINGS = {"PromptGenerationConfig": PromptGenerationConfig}
NODE_DISPLAY_NAME_MAPPINGS = {"PromptGenerationConfig": "PromptGenerationConfig"}
